<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/3044c665-1fb7-4b41-a745-7e64bce3ada1" />

# 📋 TaskFlow - Smart CLI Todo & Project Manager

**Simple. Fast. Git-friendly.**

A lightweight task management system that lives in your project directory. Perfect for developers who want todo lists without leaving the terminal.

---

## 🎯 Why TaskFlow?

**Problem:** Most task managers are either:
- 🐌 Heavy GUI applications (Trello, Asana, Jira)
- ☁️ Cloud-based (requires account, internet, privacy concerns)
- 💰 Expensive subscriptions
- 🔀 Not integrated with development workflow

**Solution:** TaskFlow gives you:
- ✅ **CLI-first** - Fast, keyboard-driven workflow
- ✅ **Per-project** - Tasks live in `.taskflow.json` in project root
- ✅ **Git-friendly** - JSON format, easy to track and merge
- ✅ **Zero dependencies** - Pure Python, no external packages
- ✅ **Cross-platform** - Works on Windows, macOS, Linux
- ✅ **Markdown export** - Share tasks in TASKS.md
- ✅ **Priority & tags** - Organize however you want
- ✅ **Lightweight** - < 500 lines of code

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download
cd TaskFlow

# Make executable (Unix/Linux/Mac)
chmod +x taskflow.py

# Run directly
python taskflow.py init
```

### First Time Setup

```bash
# Navigate to your project
cd ~/my-project

# Initialize TaskFlow
python path/to/taskflow.py init

# ✅ TaskFlow initialized!
#    Task file: .taskflow.json
```

---

## 📖 Usage Guide

### Add Tasks

```bash
# Simple add
python taskflow.py add "Implement user authentication"

# With priority
python taskflow.py add "Fix critical bug" --priority high

# With tags
python taskflow.py add "Write tests" --tags testing,important

# With due date
python taskflow.py add "Deploy v2.0" --due 2026-01-15

# Everything
python taskflow.py add "Refactor database" --priority medium --tags backend,refactor --due 2026-01-20
```

### List Tasks

```bash
# List all tasks
python taskflow.py list

# Output:
# 📋 TaskFlow - 5 task(s)
#
# 🔄 🔴 [1] Fix critical bug
# ⬜ 🟡 [2] Implement user authentication
# ⬜ 🟡 [3] Refactor database
# ⬜ 🟢 [4] Write tests
# ✅ 🟡 [5] Deploy v2.0

# Filter by status
python taskflow.py list --status todo
python taskflow.py list --status in_progress
python taskflow.py list --status done

# Filter by priority
python taskflow.py list --priority high

# Filter by tag
python taskflow.py list --tag urgent

# Show details
python taskflow.py list --details
```

### Update Task Status

```bash
# Mark as in progress
python taskflow.py start 1
# 🔄 Task started: [1] Fix critical bug

# Mark as done
python taskflow.py done 1
# ✅ Task completed: [1] Fix critical bug

# Mark as blocked
python taskflow.py block 3
# 🚫 Task blocked: [3] Refactor database
```

### Edit Tasks

```bash
# Change title
python taskflow.py edit 2 --title "Implement OAuth authentication"

# Change priority
python taskflow.py edit 2 --priority high

# Update tags
python taskflow.py edit 2 --tags auth,security,urgent

# Update due date
python taskflow.py edit 2 --due 2026-01-12

# Multiple updates
python taskflow.py edit 2 --title "New title" --priority high --tags new,tags
```

### Delete Tasks

```bash
# Delete task
python taskflow.py delete 4
# 🗑️  Task deleted: [4] Write tests
```

### Export to Markdown

```bash
# Export all tasks
python taskflow.py export

# Custom output file
python taskflow.py export --output TODO.md

# Creates formatted TASKS.md with all tasks organized by status
```

### View Statistics

```bash
# Show task stats
python taskflow.py stats

# Output:
# 📊 TaskFlow Statistics
#
# Total Tasks: 10
#
# By Status:
#   ⬜ Todo: 5 (50.0%)
#   🔄 In Progress: 2 (20.0%)
#   🚫 Blocked: 1 (10.0%)
#   ✅ Done: 2 (20.0%)
#
# By Priority:
#   🔴 High: 3 (30.0%)
#   🟡 Medium: 5 (50.0%)
#   🟢 Low: 2 (20.0%)
```

---

## 💡 Examples

### Example 1: Starting a New Project

```bash
# Initialize TaskFlow
$ cd ~/new-project
$ python taskflow.py init
✅ TaskFlow initialized!

# Add initial tasks
$ python taskflow.py add "Setup project structure" --priority high
$ python taskflow.py add "Write README" --priority medium
$ python taskflow.py add "Configure CI/CD" --priority low --tags devops

# View all tasks
$ python taskflow.py list

📋 TaskFlow - 3 task(s)

⬜ 🔴 [1] Setup project structure
⬜ 🟡 [2] Write README
⬜ 🟢 [3] Configure CI/CD

📊 Summary:
   ⬜ Todo: 3

# Start working
$ python taskflow.py start 1
🔄 Task started: [1] Setup project structure
```

### Example 2: Bug Tracking

```bash
# Add bugs with tags
$ python taskflow.py add "Login fails on mobile" --priority high --tags bug,mobile,urgent
$ python taskflow.py add "Memory leak in dashboard" --priority high --tags bug,performance
$ python taskflow.py add "Typo in footer" --priority low --tags bug,ui

# List all bugs
$ python taskflow.py list --tag bug

# Mark bug fixed
$ python taskflow.py done 1
```

### Example 3: Sprint Planning

```bash
# Add sprint tasks
$ python taskflow.py add "User stories for auth" --priority high --tags sprint-1,planning
$ python taskflow.py add "API endpoint design" --priority high --tags sprint-1,backend
$ python taskflow.py add "UI mockups" --priority medium --tags sprint-1,frontend

# View sprint tasks
$ python taskflow.py list --tag sprint-1

# Export for team
$ python taskflow.py export --output SPRINT_1.md
```

### Example 4: Daily Workflow

```bash
# Morning: Check what's in progress
$ python taskflow.py list --status in_progress

# Start new task
$ python taskflow.py start 5

# Complete a task
$ python taskflow.py done 3

# Add new urgent task
$ python taskflow.py add "Hotfix: API rate limiting" --priority high --tags hotfix,urgent

# Evening: Check stats
$ python taskflow.py stats
```

---

## 🔧 Advanced Usage

### Git Integration

TaskFlow stores tasks in `.taskflow.json` - a Git-friendly JSON file.

```bash
# Track tasks in Git
git add .taskflow.json
git commit -m "Update project tasks"

# Share with team
git push

# Team members pull and see your tasks
git pull
python taskflow.py list
```

**Pro tip:** Add `.taskflow.json` to `.gitignore` if you want personal-only tasks, or commit it for team visibility.

### Alias Setup

Make TaskFlow even faster:

```bash
# Bash/Zsh (~/.bashrc or ~/.zshrc)
alias tf='python /path/to/taskflow.py'

# Now use:
tf add "Quick task"
tf list
tf done 3
```

```powershell
# PowerShell ($PROFILE)
function tf { python C:\path\to\taskflow.py $args }

# Now use:
tf add "Quick task"
tf list
tf done 3
```

### Multiple Projects

Each project gets its own `.taskflow.json`:

```bash
# Project A
cd ~/project-a
python taskflow.py list  # Shows Project A tasks

# Project B
cd ~/project-b
python taskflow.py list  # Shows Project B tasks
```

### Export Workflow

```bash
# Export tasks every Friday
python taskflow.py export --output WEEKLY_TASKS.md

# Commit to Git
git add WEEKLY_TASKS.md
git commit -m "Weekly task update"
```

---

## 📊 Task File Format

TaskFlow stores tasks in `.taskflow.json`:

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Implement feature X",
      "priority": "high",
      "status": "in_progress",
      "tags": ["feature", "urgent"],
      "due_date": "2026-01-15",
      "created": "2026-01-09T08:00:00",
      "updated": "2026-01-09T10:30:00"
    }
  ],
  "last_updated": "2026-01-09T10:30:00"
}
```

**Fields:**
- `id` - Unique task identifier (auto-generated)
- `title` - Task description
- `priority` - `high`, `medium`, or `low`
- `status` - `todo`, `in_progress`, `done`, or `blocked`
- `tags` - Array of strings for categorization
- `due_date` - ISO format date (optional)
- `created` - ISO timestamp
- `updated` - ISO timestamp

---

## 🎨 Icons & Colors

TaskFlow uses visual indicators for quick scanning:

**Status Icons:**
- ⬜ `todo` - Not started
- 🔄 `in_progress` - Currently working
- ✅ `done` - Completed
- 🚫 `blocked` - Waiting on something

**Priority Colors:**
- 🔴 `high` - Urgent, do first
- 🟡 `medium` - Normal priority
- 🟢 `low` - Do when time permits

**Special Indicators:**
- ⚠️ - Task is overdue

---

## 📋 Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize TaskFlow in current directory | `taskflow init` |
| `add` | Add new task | `taskflow add "Task title" --priority high` |
| `list` | List all tasks | `taskflow list --status todo` |
| `start` | Mark task as in progress | `taskflow start 3` |
| `done` | Mark task as done | `taskflow done 5` |
| `block` | Mark task as blocked | `taskflow block 2` |
| `edit` | Edit task properties | `taskflow edit 4 --priority high` |
| `delete` | Delete task | `taskflow delete 7` |
| `export` | Export to Markdown | `taskflow export --output TASKS.md` |
| `stats` | Show task statistics | `taskflow stats` |

---

## 🔍 Use Cases

### For Developers
- Track bugs and features per project
- Sprint planning and management
- Daily task lists synced with Git
- Personal TODO alongside codebase

### For Teams
- Commit `.taskflow.json` for shared visibility
- Export to Markdown for status updates
- Tag-based organization (sprints, epics)
- Lightweight alternative to Jira

### For Students
- Track assignments per course
- Organize study tasks by priority
- Export for study group sharing
- Due date reminders

### For Freelancers
- Per-client task tracking
- Priority management across projects
- Quick status updates for clients
- No subscription costs

---

## ❓ FAQ

### Q: How is this different from other todo apps?
**A:**
- ✅ **CLI-first** - No GUI overhead, keyboard-driven
- ✅ **Per-project** - Tasks live with your code
- ✅ **Git-friendly** - JSON format, easy to track
- ✅ **Zero cost** - No subscriptions, no accounts
- ✅ **Lightweight** - One Python file, no dependencies

### Q: Can I use this with a team?
**A:** Yes! Commit `.taskflow.json` to Git and your team sees the same tasks. Each person can run `taskflow list` to see current status.

### Q: What about conflicts when multiple people edit?
**A:** Git handles JSON merges well. For heavy concurrent editing, consider using GitHub Issues or a dedicated tool instead.

### Q: Can I have personal tasks AND shared tasks?
**A:** Yes! Keep `.taskflow.json` in `.gitignore` for personal tasks, or create a second file (`.taskflow.personal.json`) and run TaskFlow with a custom path.

### Q: Does this work without Git?
**A:** Absolutely! TaskFlow doesn't require Git. It just stores tasks in a local JSON file. Git integration is optional.

### Q: Can I import from other todo apps?
**A:** Not built-in yet, but the JSON format is simple. You could write a script to import from CSV, Trello export, etc.

### Q: Is there a GUI version?
**A:** No. TaskFlow is CLI-only by design. For GUI, consider tools like Todoist, Trello, or Things.

### Q: How do I back up my tasks?
**A:** The `.taskflow.json` file is your backup. Copy it, commit to Git, or sync with cloud storage (Dropbox, OneDrive, etc.).

---

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/e79a6f58-e00b-416a-a153-3813725bcfc5" />


## 🤝 Contributing

Found a bug? Have a feature idea? Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE file for details.

**TL;DR:** Free to use, modify, and distribute. No warranty provided.

---

## 🙏 Credits

Created by **Randell Logan Smith and Team Brain** at [Metaphy LLC](https://metaphysicsandcomputing.com)

Part of the HMSS (Heavenly Morning Star System) ecosystem.

---

**Technology:**
- Python 3.6+
- JSON for storage
- argparse for CLI
- Zero external dependencies

---

## 🚀 Quick Reference

```bash
# Initialize
taskflow init

# Add task
taskflow add "Task title" [--priority high|medium|low] [--tags tag1,tag2] [--due YYYY-MM-DD]

# List tasks
taskflow list [--status todo|in_progress|done|blocked] [--priority high|medium|low] [--tag TAG] [--details]

# Update status
taskflow start ID      # Mark as in progress
taskflow done ID       # Mark as done
taskflow block ID      # Mark as blocked

# Edit task
taskflow edit ID [--title "New title"] [--priority high|medium|low] [--tags tag1,tag2] [--due YYYY-MM-DD]

# Delete task
taskflow delete ID

# Export & stats
taskflow export [--output FILENAME]
taskflow stats
```

---

**📋 Stay organized. Stay productive. Stay in the terminal.**
