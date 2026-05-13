- [ ] Fix list_goals.html: subgoal delete should target /subgoal/delete/<subgoal_id>/ and open modal per subgoal
- [ ] Update list_goals.html JS: add openSubgoalDeleteModal and set deleteForm.action accordingly; avoid duplicate modal markup / duplicate ids
- [ ] Run server and verify:
  - Deleting a subgoal deletes only that subgoal
  - CSRF works and no JS errors

