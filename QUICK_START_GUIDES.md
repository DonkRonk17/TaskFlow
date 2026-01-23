# TaskFlow - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)
- [Logan (Human Operator)](#-logan-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Use TaskFlow for sprint planning and agent task assignment

### Step 1: Installation Check

```bash
# Verify TaskFlow is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\TaskFlow
python taskflow.py --help

# Expected: Shows help with all commands
```

### Step 2: Initialize Team Brain Tasks

```bash
# Create a shared task file for Team Brain
python taskflow.py init

# Output:
# [OK] TaskFlow initialized!
#    Task file: .taskflow.json
```

### Step 3: Create Sprint Tasks

```python
# Forge Python workflow
from taskflow import TaskFlow

tf = TaskFlow("team_brain_sprint.json")

# Assign tasks to agents
tf.add_task(
    "Build TerminalRewind tool",
    priority="high",
    tags=["sprint-1", "atlas", "tool"]
)

tf.add_task(
    "Fix BCH mobile auth",
    priority="high",
    tags=["sprint-1", "porter", "bug"]
)

tf.add_task(
    "Review Atlas's PathBridge",
    priority="medium",
    tags=["sprint-1", "forge", "review"]
)
```

### Step 4: Track Sprint Progress

```bash
# View all sprint-1 tasks
python taskflow.py list --tag sprint-1

# Check what Atlas is assigned
python taskflow.py list --tag atlas

# Generate sprint report
python taskflow.py export --output SPRINT_1_REPORT.md
```

### Step 5: Review and Complete

```bash
# Mark review complete
python taskflow.py done 3

# Check overall stats
python taskflow.py stats
```

### Forge Best Practices

1. **Use agent name tags** - `atlas`, `clio`, `nexus`, `bolt`, `forge`
2. **Use sprint tags** - `sprint-1`, `sprint-2`, etc.
3. **Export weekly** - Share progress with team
4. **Set due dates** - Keep sprints on track

### Next Steps for Forge

1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Full BCH integration roadmap
2. Try [EXAMPLES.md](EXAMPLES.md) - Example 5 (Sprint Planning)
3. Set up sprint tracking for Team Brain

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Track tool builds and quality gates with TaskFlow

### Step 1: Installation Check

```bash
# Verify TaskFlow is available
python -c "from taskflow import TaskFlow; print('[OK] TaskFlow ready')"
```

### Step 2: Initialize Per-Tool Tracking

```bash
# In each tool directory
cd C:\Users\logan\OneDrive\Documents\AutoProjects\NewTool
python ../TaskFlow/taskflow.py init
```

### Step 3: Create Build Phase Tasks

```python
from taskflow import TaskFlow

# Track Holy Grail phases
tf = TaskFlow()

phases = [
    ("Phase 1: Planning", "high"),
    ("Phase 2: Core Development", "high"),
    ("Phase 3: Documentation", "medium"),
    ("Phase 4: Examples & Guides", "medium"),
    ("Phase 5: Testing", "high"),
    ("Phase 6: Branding", "low"),
    ("Phase 7: Integration Docs", "medium"),
    ("Phase 8: Quality Audit", "high"),
    ("Phase 9: Deployment", "medium"),
]

for title, priority in phases:
    tf.add_task(title, priority=priority, tags=["build-phase"])
```

### Step 4: Track Build Progress

```bash
# Start Phase 1
python taskflow.py start 1

# Complete Phase 1
python taskflow.py done 1

# Check progress
python taskflow.py stats
```

### Step 5: Quality Gate Checklist

```bash
# Add quality gate tasks
python taskflow.py add "Tests passing (100%)" --priority high --tags quality-gate
python taskflow.py add "README 400+ lines" --priority high --tags quality-gate
python taskflow.py add "Phase 7 docs complete" --priority high --tags quality-gate
python taskflow.py add "No emojis in code" --priority medium --tags quality-gate

# Track completion
python taskflow.py list --tag quality-gate
```

### Atlas Best Practices

1. **Initialize per-tool** - Each tool gets its own `.taskflow.json`
2. **Tag build phases** - Easy filtering with `--tag build-phase`
3. **Quality gate tracking** - Never skip Phase 7!
4. **Export on completion** - `BUILD_COMPLETE.md` for records

### Next Steps for Atlas

1. Add TaskFlow tracking to next tool build
2. Integrate with Holy Grail automation
3. Create quality gate template tasks

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** CLI task management on Linux systems

### Step 1: Linux Installation

```bash
# Clone TaskFlow
git clone https://github.com/DonkRonk17/TaskFlow.git ~/tools/TaskFlow

# Verify
python3 ~/tools/TaskFlow/taskflow.py --version
```

### Step 2: Set Up Alias

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'alias tf="python3 ~/tools/TaskFlow/taskflow.py"' >> ~/.bashrc
source ~/.bashrc

# Now use:
tf --help
```

### Step 3: Basic Linux Workflow

```bash
# Initialize in automation directory
cd ~/automation
tf init

# Add Linux tasks
tf add "Update ABL services" --priority high --tags automation,abl
tf add "Check system logs" --priority medium --tags maintenance
tf add "Backup configuration" --priority low --tags backup

# List tasks
tf list
```

### Step 4: Daily Operations

```bash
# Morning check
tf list --status todo --priority high

# Start work
tf start 1

# Complete task
tf done 1

# Weekly export
tf export --output ~/reports/tasks_$(date +%Y%m%d).md
```

### Step 5: Cron Integration (Optional)

```bash
# Add to crontab for daily export
crontab -e

# Add line:
# 0 18 * * * python3 ~/tools/TaskFlow/taskflow.py export --output ~/reports/daily_tasks.md
```

### Platform Considerations

- **Paths:** Use Linux paths (`~/`, not `C:\`)
- **Encoding:** UTF-8 default (no issues)
- **Alias:** `tf` is convenient
- **Shell scripts:** TaskFlow works in bash scripts

### Next Steps for Clio

1. Set up alias in shell profile
2. Create automation task list
3. Integrate with ABL/ABIOS workflows

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Cross-platform task management

### Step 1: Platform Detection

```python
import platform
from taskflow import TaskFlow

# Works on Windows, Linux, macOS
print(f"Platform: {platform.system()}")

tf = TaskFlow()
print("[OK] TaskFlow initialized")
```

### Step 2: Cross-Platform Task File

```python
from pathlib import Path
from taskflow import TaskFlow

# Use cross-platform path for shared tasks
if platform.system() == "Windows":
    task_file = Path.home() / "OneDrive" / "tasks.json"
else:
    task_file = Path.home() / "Dropbox" / "tasks.json"

tf = TaskFlow(str(task_file))
```

### Step 3: Platform-Tagged Tasks

```python
from taskflow import TaskFlow
import platform

tf = TaskFlow("crossplatform_tasks.json")

# Tag tasks by platform
current_platform = platform.system().lower()

tf.add_task(
    f"Test on {current_platform}",
    priority="medium",
    tags=["testing", current_platform]
)

# Filter by current platform
my_tasks = tf.list_tasks(tag=current_platform)
for task in my_tasks:
    print(f"  [{task['id']}] {task['title']}")
```

### Step 4: Platform Compatibility Testing

```bash
# Windows
python taskflow.py list --tag windows

# Linux
python3 taskflow.py list --tag linux

# macOS
python3 taskflow.py list --tag macos
```

### Cross-Platform Notes

- **File paths:** Use `pathlib.Path` for portability
- **Line endings:** JSON handles this automatically
- **Encoding:** UTF-8 everywhere (no emojis in output)
- **Cloud sync:** OneDrive/Dropbox for cross-machine sync

### Next Steps for Nexus

1. Set up cloud-synced task file
2. Test on all three platforms
3. Create platform-specific task lists

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Cost-free task execution and tracking

### Step 1: Verify Free Access

```bash
# TaskFlow has zero dependencies!
# No API keys required

python taskflow.py --version
# Output: TaskFlow ready
```

### Step 2: Batch Task Processing

```bash
# List assigned tasks
python taskflow.py list --tag bolt

# Process tasks in sequence (no API costs)
python taskflow.py start 1
# ... do work ...
python taskflow.py done 1

python taskflow.py start 2
# ... do work ...
python taskflow.py done 2
```

### Step 3: Bulk Operations Script

```bash
#!/bin/bash
# bolt_batch.sh - Process multiple tasks

TASK_IDS="1 2 3 4 5"

for id in $TASK_IDS; do
    echo "Processing task $id..."
    python taskflow.py start $id
    
    # ... do the actual work here ...
    
    python taskflow.py done $id
    echo "Task $id complete"
done

# Report
python taskflow.py stats
python taskflow.py export --output batch_complete.md
```

### Step 4: Task Pickup Workflow

```bash
# Check for assigned tasks
python taskflow.py list --tag bolt --status todo

# Pick up first available
python taskflow.py start 1

# Complete and report
python taskflow.py done 1
python taskflow.py export --output BOLT_COMPLETE.md
```

### Cost Considerations

- **Zero dependencies** - No pip install needed
- **No API calls** - Runs entirely locally
- **Batch friendly** - Process many tasks sequentially
- **Perfect for Cline** - Fast, reliable, cost-free

### Next Steps for Bolt

1. Set up batch processing scripts
2. Integrate with Cline workflows
3. Track completion for reporting

---

## 👤 LOGAN QUICK START

**Role:** Human Operator / Project Owner  
**Time:** 5 minutes  
**Goal:** Personal task management and team oversight

### Step 1: Quick Setup

```bash
# Navigate to any project
cd C:\Users\logan\OneDrive\Documents\Projects\MyProject

# Initialize
python C:\Users\logan\OneDrive\Documents\AutoProjects\TaskFlow\taskflow.py init
```

### Step 2: PowerShell Alias

```powershell
# Add to $PROFILE
function tf { python C:\Users\logan\OneDrive\Documents\AutoProjects\TaskFlow\taskflow.py $args }

# Now use:
tf add "My task"
tf list
```

### Step 3: Daily Workflow

```powershell
# Morning: Check priorities
tf list --priority high

# Add new task
tf add "Review Atlas's tool builds" --priority high --tags review

# Start work
tf start 1

# Mark done
tf done 1
```

### Step 4: Team Brain Oversight

```powershell
# Check agent tasks
tf list --tag atlas
tf list --tag forge
tf list --tag clio

# Overall progress
tf stats

# Weekly report
tf export --output WEEKLY_REPORT.md
```

### Step 5: Git Integration

```powershell
# Track tasks in Git (for team visibility)
git add .taskflow.json
git commit -m "Update project tasks"

# Or keep personal
# Add to .gitignore: .taskflow.json
```

### Logan's Workflow Tips

1. **Per-project tasks** - Each project has its own `.taskflow.json`
2. **Quick alias** - `tf` saves typing
3. **Weekly exports** - Share with team as needed
4. **Priority high** - Focus on what matters

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/TaskFlow/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message Atlas for tool issues

---

**Last Updated:** January 2026  
**Maintained By:** Atlas (Team Brain)  
**For:** Logan Smith / Metaphy LLC
