# Streaks URL/route fix

## Issue
- `/goals/streaks` returned 404.
- `/streaks/...` returned: `get_streak_data() got multiple values for argument 'name'`.

## What was changed
- Updated `streaks/urls.py` to mount streaks under `streaks/<str:name>/`.

## Remaining action needed (not executed in code yet)
- Fix the view import/target: currently `streaks/urls.py` routes to `views.get_streak_data`, but `get_streak_data` actually lives in `streaks/utils.py`.
- Either:
  1) add a `get_streak_data` wrapper view in `streaks/views.py` that calls `utils.get_streak_data(name)`, or
  2) import `get_streak_data` from `.utils` in `streaks/urls.py`.

## Suggested final URLs
- With proper routing, you can request:
  - `/streaks/global_streak/`

