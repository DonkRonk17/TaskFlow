# 📋 TaskFlow - Usage Examples

Comprehensive examples demonstrating all TaskFlow capabilities.

**Quick Navigation:**
- [Example 1: First Time Setup](#example-1-first-time-setup)
- [Example 2: Basic Task Workflow](#example-2-basic-task-workflow)
- [Example 3: Priority-Based Organization](#example-3-priority-based-organization)
- [Example 4: Tag-Based Filtering](#example-4-tag-based-filtering)
- [Example 5: Sprint Planning](#example-5-sprint-planning)
- [Example 6: Bug Tracking Workflow](#example-6-bug-tracking-workflow)
- [Example 7: Due Dates and Overdue Detection](#example-7-due-dates-and-overdue-detection)
- [Example 8: Task Editing and Updates](#example-8-task-editing-and-updates)
- [Example 9: Markdown Export for Team Sharing](#example-9-markdown-export-for-team-sharing)
- [Example 10: Python API Integration](#example-10-python-api-integration)
- [Example 11: Multi-Project Workflow](#example-11-multi-project-workflow)
- [Example 12: Daily Standup Report](#example-12-daily-standup-report)

---

## Example 1: First Time Setup

**Scenario:** You're starting a new project and want to use TaskFlow for task management.

**Steps:**

```bash
# Navigate to your project directory
cd ~/my-new-project

# Initialize TaskFlow
python taskflow.py init
```

**Expected Output:**

```
[OK] TaskFlow initialized!
   Task file: .taskflow.json

[TIP] Quick start:
   taskflow add "My first task"
   taskflow list
```

**What Happened:**
- Created `.taskflow.json` in your project root
- This file will store all your tasks
- You can now add tasks to this project

**Pro Tip:** Add `.taskflow.json` to your `.gitignore` for personal tasks, or commit it for team visibility.

---

## Example 2: Basic Task Workflow

**Scenario:** Complete workflow from adding a task to marking it done.

**Steps:**

```bash
# Add a new task
python taskflow.py add "Implement user login"
```

**Output:**

```
[OK] Task added: [1] Implement user login
```

```bash
# List all tasks
python taskflow.py list
```

**Output:**

```
[TASKS] TaskFlow - 1 task(s)

[ ] [~] [1] Implement user login

[STATS] Summary:
   [ ] Todo: 1
```

```bash
# Start working on it
python taskflow.py start 1
```

**Output:**

```
[>] Task started: [1] Implement user login
```

```bash
# Mark as done
python taskflow.py done 1
```

**Output:**

```
[OK] Task completed: [1] Implement user login
```

**What You Learned:**
- `add` creates a new task
- `list` shows all tasks with status icons
- `start` marks a task as "in progress"
- `done` marks a task as completed

---

## Example 3: Priority-Based Organization

**Scenario:** Add multiple tasks with different priorities and filter by priority.

**Steps:**

```bash
# Add high priority task
python taskflow.py add "Critical security fix" --priority high

# Add medium priority task (default)
python taskflow.py add "Update documentation"

# Add low priority task
python taskflow.py add "Refactor old code" --priority low

# List all tasks
python taskflow.py list
```

**Output:**

```
[TASKS] TaskFlow - 3 task(s)

[ ] [!] [1] Critical security fix
[ ] [~] [2] Update documentation
[ ] [-] [3] Refactor old code

[STATS] Summary:
   [ ] Todo: 3
```

```bash
# Filter by priority
python taskflow.py list --priority high
```

**Output:**

```
[TASKS] TaskFlow - 1 task(s)

[ ] [!] [1] Critical security fix

[STATS] Summary:
   [ ] Todo: 1
```

**Priority Icons:**
- `[!]` = High priority (urgent)
- `[~]` = Medium priority (normal)
- `[-]` = Low priority (when time permits)

---

## Example 4: Tag-Based Filtering

**Scenario:** Organize tasks with tags and filter by specific tags.

**Steps:**

```bash
# Add tasks with multiple tags
python taskflow.py add "Fix login bug" --tags bug,auth,urgent
python taskflow.py add "Add OAuth support" --tags feature,auth
python taskflow.py add "Update README" --tags docs

# List all tasks with a specific tag
python taskflow.py list --tag auth
```

**Output:**

```
[TASKS] TaskFlow - 2 task(s)

[ ] [~] [1] Fix login bug
[ ] [~] [2] Add OAuth support

[STATS] Summary:
   [ ] Todo: 2
```

```bash
# Show detailed info with tags
python taskflow.py list --tag auth --details
```

**Output:**

```
[TASKS] TaskFlow - 2 task(s)

[ ] [~] [1] Fix login bug
    Priority: medium | Status: todo
    Tags: bug, auth, urgent
    Created: 2026-01-22

[ ] [~] [2] Add OAuth support
    Priority: medium | Status: todo
    Tags: feature, auth
    Created: 2026-01-22

[STATS] Summary:
   [ ] Todo: 2
```

**Use Cases for Tags:**
- `bug`, `feature`, `enhancement`
- `sprint-1`, `sprint-2`, `backlog`
- `frontend`, `backend`, `devops`
- `urgent`, `blocked`, `review-needed`

---

## Example 5: Sprint Planning

**Scenario:** Set up tasks for a development sprint.

**Steps:**

```bash
# Create sprint tasks
python taskflow.py add "User stories for auth" --priority high --tags sprint-1,planning
python taskflow.py add "API endpoint design" --priority high --tags sprint-1,backend
python taskflow.py add "UI mockups" --priority medium --tags sprint-1,frontend
python taskflow.py add "Write integration tests" --priority medium --tags sprint-1,testing
python taskflow.py add "Deploy to staging" --priority low --tags sprint-1,devops

# View sprint tasks
python taskflow.py list --tag sprint-1
```

**Output:**

```
[TASKS] TaskFlow - 5 task(s)

[ ] [!] [1] User stories for auth
[ ] [!] [2] API endpoint design
[ ] [~] [3] UI mockups
[ ] [~] [4] Write integration tests
[ ] [-] [5] Deploy to staging

[STATS] Summary:
   [ ] Todo: 5
```

```bash
# Start sprint work
python taskflow.py start 1
python taskflow.py start 2

# Check progress
python taskflow.py stats
```

**Output:**

```
[STATS] TaskFlow Statistics

Total Tasks: 5

By Status:
  [ ] Todo: 3 (60.0%)
  [>] In Progress: 2 (40.0%)
  [#] Blocked: 0 (0.0%)
  [X] Done: 0 (0.0%)

By Priority:
  [!] High: 2 (40.0%)
  [~] Medium: 2 (40.0%)
  [-] Low: 1 (20.0%)
```

---

## Example 6: Bug Tracking Workflow

**Scenario:** Track and manage bug reports.

**Steps:**

```bash
# Add bugs with severity indicators
python taskflow.py add "Login fails on mobile" --priority high --tags bug,critical,mobile
python taskflow.py add "Slow dashboard load" --priority medium --tags bug,performance
python taskflow.py add "Typo in footer" --priority low --tags bug,ui

# List all bugs
python taskflow.py list --tag bug
```

**Output:**

```
[TASKS] TaskFlow - 3 task(s)

[ ] [!] [1] Login fails on mobile
[ ] [~] [2] Slow dashboard load
[ ] [-] [3] Typo in footer

[STATS] Summary:
   [ ] Todo: 3
```

```bash
# Start working on critical bug
python taskflow.py start 1

# Bug is blocked waiting for more info
python taskflow.py block 1
```

**Output:**

```
[#] Task blocked: [1] Login fails on mobile
```

```bash
# View blocked tasks
python taskflow.py list --status blocked
```

**Output:**

```
[TASKS] TaskFlow - 1 task(s)

[#] [!] [1] Login fails on mobile

[STATS] Summary:
   [#] Blocked: 1
```

```bash
# Unblock and complete
python taskflow.py start 1
python taskflow.py done 1
```

---

## Example 7: Due Dates and Overdue Detection

**Scenario:** Set deadlines and track overdue tasks.

**Steps:**

```bash
# Add tasks with due dates
python taskflow.py add "Submit report" --due 2026-01-25
python taskflow.py add "Past deadline" --due 2026-01-01  # Already past!
python taskflow.py add "Code review" --due 2026-01-30

# List tasks
python taskflow.py list
```

**Output:**

```
[TASKS] TaskFlow - 3 task(s)

[ ] [~] [1] Submit report
[ ] [~] [2] Past deadline [!] OVERDUE
[ ] [~] [3] Code review

[STATS] Summary:
   [ ] Todo: 3
```

```bash
# Show details including due dates
python taskflow.py list --details
```

**Output:**

```
[TASKS] TaskFlow - 3 task(s)

[ ] [~] [1] Submit report
    Priority: medium | Status: todo
    Due: 2026-01-25
    Created: 2026-01-22

[ ] [~] [2] Past deadline [!] OVERDUE
    Priority: medium | Status: todo
    Due: 2026-01-01
    Created: 2026-01-22

[ ] [~] [3] Code review
    Priority: medium | Status: todo
    Due: 2026-01-30
    Created: 2026-01-22

[STATS] Summary:
   [ ] Todo: 3
```

**Overdue Detection:**
- Tasks past their due date show `[!] OVERDUE`
- Completed tasks don't show overdue warning
- Stats command shows total overdue count

---

## Example 8: Task Editing and Updates

**Scenario:** Modify existing tasks.

**Steps:**

```bash
# Add a task
python taskflow.py add "Initial task title"

# Edit the title
python taskflow.py edit 1 --title "Updated task title"
```

**Output:**

```
[EDIT] Task updated: [1] Updated task title
```

```bash
# Change priority
python taskflow.py edit 1 --priority high
```

**Output:**

```
[EDIT] Task updated: [1] Updated task title
```

```bash
# Add tags
python taskflow.py edit 1 --tags important,urgent

# Set due date
python taskflow.py edit 1 --due 2026-02-01

# Verify changes
python taskflow.py list --details
```

**Output:**

```
[TASKS] TaskFlow - 1 task(s)

[ ] [!] [1] Updated task title
    Priority: high | Status: todo
    Tags: important, urgent
    Due: 2026-02-01
    Created: 2026-01-22

[STATS] Summary:
   [ ] Todo: 1
```

---

## Example 9: Markdown Export for Team Sharing

**Scenario:** Export tasks to a readable Markdown file for team meetings.

**Steps:**

```bash
# Create some tasks first
python taskflow.py add "API design" --priority high --tags sprint-1
python taskflow.py add "Frontend layout" --priority medium --tags sprint-1
python taskflow.py start 1
python taskflow.py done 2

# Export to Markdown
python taskflow.py export
```

**Output:**

```
[OK] Tasks exported to: TASKS.md
```

**Generated TASKS.md:**

```markdown
# 📋 TaskFlow - Project Tasks

**Generated:** 2026-01-22 14:30
**Total Tasks:** 2

---

## 🔄 In Progress (1)

### 🔴 [1] API design

- **Priority:** high
- **Status:** in_progress
- **Tags:** sprint-1
- **Created:** 2026-01-22

## ✅ Done (1)

### 🟡 [2] Frontend layout

- **Priority:** medium
- **Status:** done
- **Tags:** sprint-1
- **Created:** 2026-01-22
```

```bash
# Export with custom filename
python taskflow.py export --output SPRINT_1_TASKS.md
```

**Use Cases:**
- Share progress in team meetings
- Include in pull request descriptions
- Generate weekly status reports
- Documentation for handoffs

---

## Example 10: Python API Integration

**Scenario:** Use TaskFlow programmatically in your Python scripts.

**Code:**

```python
#!/usr/bin/env python3
"""Example: Using TaskFlow Python API"""

from taskflow import TaskFlow

# Initialize with custom file
tf = TaskFlow("my_project_tasks.json")

# Add a task
task = tf.add_task(
    title="Build feature X",
    priority="high",
    tags=["feature", "sprint-1"],
    due_date="2026-02-01"
)
print(f"Created task: [{task['id']}] {task['title']}")

# List high priority tasks
high_priority = tf.list_tasks(priority="high")
for t in high_priority:
    print(f"  - [{t['id']}] {t['title']}")

# Mark task in progress
tf.mark_in_progress(task['id'])

# Check if task is overdue
if tf.is_overdue(task):
    print(f"Task {task['id']} is overdue!")

# Mark task done
tf.mark_done(task['id'])

# Export to markdown
tf.export_markdown("PROJECT_TASKS.md")
print("Tasks exported!")
```

**Output:**

```
Created task: [1] Build feature X
  - [1] Build feature X
Tasks exported!
```

**Integration Ideas:**
- Pre-commit hooks to check for uncompleted tasks
- CI/CD scripts to update task status
- Daily automation scripts
- Team Brain agent workflows

---

## Example 11: Multi-Project Workflow

**Scenario:** Manage tasks across multiple projects.

**Steps:**

```bash
# Project A
cd ~/project-a
python taskflow.py init
python taskflow.py add "Project A task 1"
python taskflow.py list

# Output shows only Project A tasks
```

```bash
# Project B (different directory)
cd ~/project-b
python taskflow.py init
python taskflow.py add "Project B task 1"
python taskflow.py list

# Output shows only Project B tasks
```

**Key Points:**
- Each project has its own `.taskflow.json`
- Tasks are scoped to the current directory
- No cross-contamination between projects
- Perfect for monorepos or multi-service architectures

---

## Example 12: Daily Standup Report

**Scenario:** Generate a quick status report for daily standups.

**Steps:**

```bash
# Morning: Check what's in progress
python taskflow.py list --status in_progress

# Check what's blocked
python taskflow.py list --status blocked

# Check overall stats
python taskflow.py stats

# Export for sharing
python taskflow.py export --output STANDUP_$(date +%Y%m%d).md
```

**Sample Workflow:**

```bash
# Yesterday I completed:
python taskflow.py list --status done

# Today I'm working on:
python taskflow.py list --status in_progress

# Blockers:
python taskflow.py list --status blocked
```

---

## 🎯 Summary: Quick Reference

| Action | Command | Example |
|--------|---------|---------|
| Initialize | `init` | `taskflow init` |
| Add task | `add` | `taskflow add "Title" --priority high --tags a,b --due 2026-02-01` |
| List all | `list` | `taskflow list` |
| Filter by status | `list --status` | `taskflow list --status todo` |
| Filter by priority | `list --priority` | `taskflow list --priority high` |
| Filter by tag | `list --tag` | `taskflow list --tag bug` |
| Show details | `list --details` | `taskflow list --details` |
| Start task | `start` | `taskflow start 1` |
| Complete task | `done` | `taskflow done 1` |
| Block task | `block` | `taskflow block 1` |
| Edit task | `edit` | `taskflow edit 1 --title "New title"` |
| Delete task | `delete` | `taskflow delete 1` |
| Export | `export` | `taskflow export --output TASKS.md` |
| Statistics | `stats` | `taskflow stats` |

---

## 📚 Additional Resources

- **Main Documentation:** [README.md](README.md)
- **Quick Reference:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- **Integration Guide:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- **Agent Guides:** [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)

---

**Built by:** Atlas (Team Brain)  
**For:** Logan Smith / Metaphy LLC  
**Date:** January 2026
