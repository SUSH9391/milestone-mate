import logging
from datetime import datetime, timedelta
from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialAccount

logger = logging.getLogger(__name__)

def get_google_calendar_service(user):
    """
    Returns a Google Calendar service object for the given user.
    """
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        social_token = SocialToken.objects.get(account=social_account)
        
        credentials = Credentials(
            token=social_token.token,
            refresh_token=social_token.token_secret, # allauth stores refresh token in token_secret
            token_uri='https://oauth2.googleapis.com/token',
            client_id=settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
            client_secret=settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret']
        )
        
        # Check if token needs refresh
        if credentials.expired and credentials.refresh_token:
            from google.auth.transport.requests import Request
            credentials.refresh(Request())
            # Update the token in the database
            social_token.token = credentials.token
            social_token.save()
        
        return build('calendar', 'v3', credentials=credentials)
    except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist) as e:
        logger.error(f"Google account not connected for user {user}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error building Google Calendar service for user {user}: {e}")
        return None

def sync_goal_to_google_calendar(goal):
    """
    Creates or updates a Google Calendar event for a given goal.
    """
    if not goal.user:
        return

    service = get_google_calendar_service(goal.user)
    if not service:
        return

    # Prepare event data
    start_time = datetime.combine(goal.target_date, datetime.min.time())
    end_time = start_time + timedelta(hours=1)
    
    event_body = {
        'summary': f"Goal: {goal.name}",
        'description': goal.description or f"Milestone Mate goal: {goal.name}",
        'start': {
            'dateTime': start_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'reminders': {
            'useDefault': True,
        },
    }

    try:
        if goal.google_calendar_event_id:
            # Update existing event
            service.events().update(
                calendarId='primary',
                eventId=goal.google_calendar_event_id,
                body=event_body
            ).execute()
        else:
            # Create new event
            event = service.events().insert(
                calendarId='primary',
                body=event_body
            ).execute()
            
            # Save the event ID to the goal
            goal.google_calendar_event_id = event['id']
            # Use update_fields to avoid re-triggering signals if we were using signals
            # but since we'll call this from signals, we must be careful.
            # Actually, the signal will call this.
            from .models import Goal
            Goal.objects.filter(id=goal.id).update(google_calendar_event_id=event['id'])
            
    except Exception as e:
        logger.error(f"Failed to sync goal {goal.id} to Google Calendar: {e}")

def delete_google_calendar_event(goal):
    """
    Deletes the Google Calendar event associated with a goal.
    """
    if not goal.user or not goal.google_calendar_event_id:
        return

    service = get_google_calendar_service(goal.user)
    if not service:
        return

    try:
        service.events().delete(
            calendarId='primary',
            eventId=goal.google_calendar_event_id
        ).execute()
    except Exception as e:
        logger.error(f"Failed to delete Google Calendar event for goal {goal.id}: {e}")
