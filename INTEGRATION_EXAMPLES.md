# TaskFlow - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

TaskFlow is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: TaskFlow + AgentHealth](#pattern-1-taskflow--agenthealth)
2. [Pattern 2: TaskFlow + SynapseLink](#pattern-2-taskflow--synapselink)
3. [Pattern 3: TaskFlow + SessionReplay](#pattern-3-taskflow--sessionreplay)
4. [Pattern 4: TaskFlow + TokenTracker](#pattern-4-taskflow--tokentracker)
5. [Pattern 5: TaskFlow + ContextCompressor](#pattern-5-taskflow--contextcompressor)
6. [Pattern 6: TaskFlow + MemoryBridge](#pattern-6-taskflow--memorybridge)
7. [Pattern 7: TaskFlow + ConfigManager](#pattern-7-taskflow--configmanager)
8. [Pattern 8: TaskFlow + DevSnapshot](#pattern-8-taskflow--devsnapshot)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: TaskFlow + AgentHealth

**Use Case:** Correlate task completion with agent health metrics

**Why:** Track how task work affects agent performance and health

**Code:**

```python
#!/usr/bin/env python3
"""Integration: TaskFlow + AgentHealth"""

from agenthealth import AgentHealth
from taskflow import TaskFlow

# Initialize both tools
health = AgentHealth()
tf = TaskFlow("agent_tasks.json")

def work_on_task(agent_name: str, task_id: int):
    """Work on a task with health monitoring."""
    
    # Start health session
    session_id = health.start_session(agent_name)
    
    # Get and start task
    task = tf.get_task(task_id)
    if not task:
        print(f"[X] Task {task_id} not found")
        return
    
    tf.mark_in_progress(task_id)
    print(f"[>] Started: {task['title']}")
    
    try:
        # Simulate work with health heartbeats
        health.heartbeat(agent_name, status="working")
        
        # ... do actual work here ...
        
        # Complete task
        tf.mark_done(task_id)
        print(f"[OK] Completed: {task['title']}")
        
        # Log success to health
        health.end_session(agent_name, session_id=session_id, status="success")
        
    except Exception as e:
        # Log failure
        tf.update_task(task_id, status="blocked")
        health.log_error(agent_name, str(e))
        health.end_session(agent_name, session_id=session_id, status="failed")
        raise

# Example usage
work_on_task("ATLAS", 1)
```

**Result:** Correlated health and task data for analysis

---

## Pattern 2: TaskFlow + SynapseLink

**Use Case:** Notify Team Brain when tasks complete

**Why:** Keep team informed of task progress automatically

**Code:**

```python
#!/usr/bin/env python3
"""Integration: TaskFlow + SynapseLink"""

from synapselink import quick_send
from taskflow import TaskFlow

tf = TaskFlow()

def complete_task_with_notification(task_id: int, notify_to: str = "TEAM"):
    """Complete a task and notify the team."""
    
    task = tf.get_task(task_id)
    if not task:
        print(f"[X] Task {task_id} not found")
        return
    
    # Complete the task
    tf.mark_done(task_id)
    
    # Build notification message
    tags = ", ".join(task.get('tags', [])) or "None"
    
    # Send notification
    quick_send(
        notify_to,
        f"Task Complete: {task['title']}",
        f"Task [{task['id']}] has been completed!\n\n"
        f"Title: {task['title']}\n"
        f"Priority: {task['priority']}\n"
        f"Tags: {tags}\n\n"
        f"Completed by: ATLAS",
        priority="NORMAL"
    )
    
    print(f"[OK] Task {task_id} completed and team notified")

# Example: Complete task and notify Forge
complete_task_with_notification(5, "FORGE,TEAM")
```

**Result:** Team stays informed without manual status updates

---

## Pattern 3: TaskFlow + SessionReplay

**Use Case:** Record task operations for debugging

**Why:** Replay task workflows when issues occur

**Code:**

```python
#!/usr/bin/env python3
"""Integration: TaskFlow + SessionReplay"""

from sessionreplay import SessionReplay
from taskflow import TaskFlow

replay = SessionReplay()
tf = TaskFlow()

def tracked_task_workflow(agent_name: str):
    """Execute a task workflow with full session recording."""
    
    # Start recording
    session_id = replay.start_session(agent_name, task="TaskFlow operations")
    
    try:
        # Log: Add new task
        replay.log_event(session_id, "task_add", {"title": "New feature"})
        task = tf.add_task("New feature", priority="high", tags=["feature"])
        replay.log_event(session_id, "task_created", {"id": task['id']})
        
        # Log: Start task
        replay.log_event(session_id, "task_start", {"id": task['id']})
        tf.mark_in_progress(task['id'])
        
        # Simulate work
        replay.log_event(session_id, "working", {"duration": "5 minutes"})
        
        # Log: Complete task
        replay.log_event(session_id, "task_complete", {"id": task['id']})
        tf.mark_done(task['id'])
        
        # End session
        replay.end_session(session_id, status="COMPLETED")
        print(f"[OK] Workflow complete, session: {session_id}")
        
    except Exception as e:
        replay.log_error(session_id, str(e))
        replay.end_session(session_id, status="FAILED")
        raise

# Example
tracked_task_workflow("ATLAS")
```

**Result:** Full session replay available for debugging task issues

---

## Pattern 4: TaskFlow + TokenTracker

**Use Case:** Track task work alongside API token usage

**Why:** Correlate costs with specific tasks

**Code:**

```python
#!/usr/bin/env python3
"""Integration: TaskFlow + TokenTracker"""

from tokentracker import TokenTracker
from taskflow import TaskFlow

tracker = TokenTracker()
tf = TaskFlow()

def work_with_cost_tracking(agent_name: str, task_id: int, 
                            input_tokens: int, output_tokens: int):
    """Complete a task while tracking associated token costs."""
    
    task = tf.get_task(task_id)
    if not task:
        print(f"[X] Task {task_id} not found")
        return
    
    # Start task
    tf.mark_in_progress(task_id)
    
    # ... do work that uses tokens ...
    
    # Complete task
    tf.mark_done(task_id)
    
    # Log token usage with task context
    tracker.add_entry(
        agent=agent_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        task_id=str(task_id),
        notes=f"Task: {task['title']}"
    )
    
    # Calculate cost (example rate)
    cost = tracker.calculate_cost(input_tokens, output_tokens)
    print(f"[OK] Task {task_id} complete, cost: ${cost:.4f}")

# Example
work_with_cost_tracking("ATLAS", 1, input_tokens=500, output_tokens=1500)
```

**Result:** Task completion tied to cost tracking

---

## Pattern 5: TaskFlow + ContextCompressor

**Use Case:** Compress task exports for efficient sharing

**Why:** Reduce token usage when sharing task lists

**Code:**

```python
#!/usr/bin/env python3
"""Integration: TaskFlow + ContextCompressor"""

from contextcompressor import ContextCompressor
from taskflow import TaskFlow

compressor = ContextCompressor()
tf = TaskFlow()

def get_compressed_task_summary(query: str = "status"):
    """Get a compressed summary of tasks."""
    
    tasks = tf.list_tasks()
    
    # Build full task text
    task_lines = []
    for t in tasks:
        status_icon = {"todo": "[ ]", "in_progress": "[>]", 
                       "done": "[X]", "blocked": "[#]"}.get(t['status'], "[ ]")
        tags = ", ".join(t.get('tags', [])) or "none"
        task_lines.append(
            f"{status_icon} [{t['id']}] {t['title']} "
            f"(Priority: {t['priority']}, Tags: {tags})"
        )
    
    full_text = "\n".join(task_lines)
    
    # Compress
    result = compressor.compress_text(full_text, query=query)
    
    print(f"Original: {len(full_text)} chars")
    print(f"Compressed: {len(result.compressed_text)} chars")
    print(f"Savings: {result.compression_ratio:.1%}")
    
    return result.compressed_text

# Example
summary = get_compressed_task_summary("high priority tasks")
print(f"\nCompressed Summary:\n{summary}")
```

**Result:** 50-90% reduction in task list size for sharing

---

## Pattern 6: TaskFlow + MemoryBridge

**Use Case:** Persist task history to memory core

**Why:** Maintain long-term task completion records

**Code:**

```python
#!/usr/bin/env python3
"""Integration: TaskFlow + MemoryBridge"""

from memorybridge import MemoryBridge
from taskflow import TaskFlow
from datetime import datetime

memory = MemoryBridge()
tf = TaskFlow()

def complete_task_with_history(task_id: int, agent_name: str):
    """Complete a task and log to persistent memory."""
    
    task = tf.get_task(task_id)
    if not task:
        print(f"[X] Task {task_id} not found")
        return
    
    # Complete task
    tf.mark_done(task_id)
    
    # Load history from memory
    history = memory.get("taskflow_completion_history", default=[])
    
    # Add completion record
    history.append({
        "task_id": task['id'],
        "title": task['title'],
        "priority": task['priority'],
        "tags": task.get('tags', []),
        "completed_at": datetime.now().isoformat(),
        "completed_by": agent_name
    })
    
    # Keep last 100 completions
    history = history[-100:]
    
    # Save to memory
    memory.set("taskflow_completion_history", history)
    memory.sync()
    
    print(f"[OK] Task {task_id} completed and logged to memory")
    print(f"     Total completions: {len(history)}")

# Example
complete_task_with_history(3, "ATLAS")
```

**Result:** Persistent completion history across sessions

---

## Pattern 7: TaskFlow + ConfigManager

**Use Case:** Centralize TaskFlow configuration

**Why:** Share settings across agents and sessions

**Code:**

```python
#!/usr/bin/env python3
"""Integration: TaskFlow + ConfigManager"""

from configmanager import ConfigManager
from taskflow import TaskFlow

config = ConfigManager()

def get_configured_taskflow():
    """Get TaskFlow instance with centralized config."""
    
    # Load or create default config
    tf_config = config.get("taskflow", {
        "default_file": ".taskflow.json",
        "default_priority": "medium",
        "auto_export": False,
        "export_file": "TASKS.md"
    })
    
    # Create TaskFlow with configured file
    tf = TaskFlow(tf_config["default_file"])
    
    return tf, tf_config

def add_task_with_defaults(title: str, **kwargs):
    """Add task using configured defaults."""
    
    tf, tf_config = get_configured_taskflow()
    
    # Apply default priority if not specified
    if 'priority' not in kwargs:
        kwargs['priority'] = tf_config["default_priority"]
    
    # Add task
    task = tf.add_task(title, **kwargs)
    
    # Auto-export if configured
    if tf_config.get("auto_export"):
        tf.export_markdown(tf_config["export_file"])
        print(f"[OK] Auto-exported to {tf_config['export_file']}")
    
    return task

# Example
task = add_task_with_defaults("New feature implementation", tags=["feature"])
print(f"[OK] Created task [{task['id']}] with priority: {task['priority']}")
```

**Result:** Consistent task management across all agents

---

## Pattern 8: TaskFlow + DevSnapshot

**Use Case:** Capture environment state when completing tasks

**Why:** Record what state the system was in when task completed

**Code:**

```python
#!/usr/bin/env python3
"""Integration: TaskFlow + DevSnapshot"""

from devsnapshot import DevSnapshot
from taskflow import TaskFlow

snapshot = DevSnapshot()
tf = TaskFlow()

def complete_task_with_snapshot(task_id: int):
    """Complete a task and capture development state."""
    
    task = tf.get_task(task_id)
    if not task:
        print(f"[X] Task {task_id} not found")
        return
    
    # Complete the task
    tf.mark_done(task_id)
    
    # Capture snapshot
    snap = snapshot.capture(f"Task complete: {task['title']}")
    
    print(f"[OK] Task {task_id} completed")
    print(f"     Snapshot: {snap['id']}")
    print(f"     Git branch: {snap.get('git', {}).get('branch', 'N/A')}")
    print(f"     Files changed: {len(snap.get('git', {}).get('modified_files', []))}")

# Example
complete_task_with_snapshot(1)
```

**Result:** Task completion tied to specific development state

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete workflow using multiple tools

**Why:** Demonstrate real production scenario

**Code:**

```python
#!/usr/bin/env python3
"""Integration: Multi-Tool Workflow"""

from taskflow import TaskFlow
from synapselink import quick_send
from agenthealth import AgentHealth

# Initialize tools
tf = TaskFlow()
health = AgentHealth()

def full_task_workflow(agent_name: str, task_id: int):
    """Execute a complete task workflow with multiple tool integration."""
    
    # Start health session
    session_id = health.start_session(agent_name)
    
    # Get task
    task = tf.get_task(task_id)
    if not task:
        health.log_error(agent_name, f"Task {task_id} not found")
        health.end_session(agent_name, session_id=session_id, status="failed")
        return False
    
    print(f"[>] Starting: {task['title']}")
    
    try:
        # Start task
        tf.mark_in_progress(task_id)
        health.heartbeat(agent_name, status="working")
        
        # Simulate work
        # ... actual work would happen here ...
        
        # Complete task
        tf.mark_done(task_id)
        health.heartbeat(agent_name, status="idle")
        
        # Notify team
        quick_send(
            "TEAM",
            f"Task Complete: [{task['id']}] {task['title']}",
            f"Completed by: {agent_name}\n"
            f"Priority: {task['priority']}\n"
            f"Status: Done",
            priority="NORMAL"
        )
        
        # End health session
        health.end_session(agent_name, session_id=session_id, status="success")
        
        print(f"[OK] Workflow complete for task {task_id}")
        return True
        
    except Exception as e:
        # Handle failure
        tf.update_task(task_id, status="blocked")
        health.log_error(agent_name, str(e))
        health.end_session(agent_name, session_id=session_id, status="failed")
        
        # Alert team
        quick_send(
            "FORGE,LOGAN",
            f"Task Failed: [{task['id']}] {task['title']}",
            f"Agent: {agent_name}\nError: {str(e)}",
            priority="HIGH"
        )
        
        return False

# Example
success = full_task_workflow("ATLAS", 1)
```

**Result:** Fully instrumented, coordinated workflow

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade agent operation

**Code:**

```python
#!/usr/bin/env python3
"""Integration: Full Team Brain Stack"""

from taskflow import TaskFlow
from synapselink import quick_send
from agenthealth import AgentHealth
from tokentracker import TokenTracker
from memorybridge import MemoryBridge
from configmanager import ConfigManager
from datetime import datetime

class TeamBrainTaskRunner:
    """Full Team Brain integration for task execution."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        
        # Load config
        self.config = ConfigManager()
        tf_config = self.config.get("taskflow", {
            "default_file": ".taskflow.json"
        })
        
        # Initialize tools
        self.tf = TaskFlow(tf_config.get("default_file", ".taskflow.json"))
        self.health = AgentHealth()
        self.tracker = TokenTracker()
        self.memory = MemoryBridge()
    
    def run_task(self, task_id: int, estimated_tokens: int = 0):
        """Run a task with full Team Brain integration."""
        
        # Start health tracking
        session_id = self.health.start_session(self.agent_name)
        start_time = datetime.now()
        
        # Get task
        task = self.tf.get_task(task_id)
        if not task:
            self._handle_not_found(task_id, session_id)
            return False
        
        try:
            # Start task
            self.tf.mark_in_progress(task_id)
            self.health.heartbeat(self.agent_name, status="working")
            
            # === DO ACTUAL WORK HERE ===
            # ... work ...
            # ============================
            
            # Complete task
            self.tf.mark_done(task_id)
            
            # Track tokens if estimated
            if estimated_tokens > 0:
                self.tracker.add_entry(
                    agent=self.agent_name,
                    input_tokens=estimated_tokens // 2,
                    output_tokens=estimated_tokens // 2,
                    task_id=str(task_id),
                    notes=task['title']
                )
            
            # Log to memory
            self._log_completion(task, start_time)
            
            # Notify team
            quick_send(
                "TEAM",
                f"[OK] Task Complete: {task['title']}",
                f"Agent: {self.agent_name}\nTask ID: {task_id}",
                priority="NORMAL"
            )
            
            # End health session
            self.health.end_session(
                self.agent_name, 
                session_id=session_id, 
                status="success"
            )
            
            return True
            
        except Exception as e:
            self._handle_failure(task, session_id, e)
            return False
    
    def _log_completion(self, task, start_time):
        """Log completion to memory."""
        history = self.memory.get("task_history", default=[])
        history.append({
            "task_id": task['id'],
            "title": task['title'],
            "completed": datetime.now().isoformat(),
            "duration": str(datetime.now() - start_time),
            "agent": self.agent_name
        })
        self.memory.set("task_history", history[-100:])
        self.memory.sync()
    
    def _handle_not_found(self, task_id, session_id):
        """Handle task not found."""
        self.health.log_error(self.agent_name, f"Task {task_id} not found")
        self.health.end_session(
            self.agent_name, 
            session_id=session_id, 
            status="failed"
        )
        print(f"[X] Task {task_id} not found")
    
    def _handle_failure(self, task, session_id, error):
        """Handle task failure."""
        self.tf.update_task(task['id'], status="blocked")
        self.health.log_error(self.agent_name, str(error))
        self.health.end_session(
            self.agent_name, 
            session_id=session_id, 
            status="failed"
        )
        quick_send(
            "FORGE,LOGAN",
            f"[X] Task Failed: {task['title']}",
            f"Agent: {self.agent_name}\nError: {str(error)}",
            priority="HIGH"
        )
        print(f"[X] Task {task['id']} failed: {error}")

# Example usage
if __name__ == "__main__":
    runner = TeamBrainTaskRunner("ATLAS")
    runner.run_task(1, estimated_tokens=1000)
```

**Result:** Enterprise-grade task execution with full observability

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

### Week 1 (Essential)

| Integration | Priority | Benefit |
|-------------|----------|---------|
| AgentHealth | HIGH | Monitor task work impact |
| SynapseLink | HIGH | Team notifications |
| TokenTracker | MEDIUM | Cost tracking |

### Week 2 (Productivity)

| Integration | Priority | Benefit |
|-------------|----------|---------|
| MemoryBridge | MEDIUM | Persistent history |
| ConfigManager | MEDIUM | Centralized settings |
| SessionReplay | MEDIUM | Debugging |

### Week 3 (Advanced)

| Integration | Priority | Benefit |
|-------------|----------|---------|
| DevSnapshot | LOW | State correlation |
| ContextCompressor | LOW | Token optimization |
| Full Stack | LOW | Production setup |

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

### Import Errors

```python
# Ensure AutoProjects is in Python path
import sys
from pathlib import Path

# Add AutoProjects to path
autoProjects = Path.home() / "OneDrive" / "Documents" / "AutoProjects"
sys.path.insert(0, str(autoProjects))

# Now import tools
from TaskFlow.taskflow import TaskFlow
from SynapseLink.synapselink import quick_send
```

### Module Not Found

```bash
# Verify tool exists
ls C:\Users\logan\OneDrive\Documents\AutoProjects\TaskFlow\

# Check Python can import
python -c "from taskflow import TaskFlow; print('[OK]')"
```

### Configuration Issues

```python
# Reset to defaults
from configmanager import ConfigManager
config = ConfigManager()
config.set("taskflow", {
    "default_file": ".taskflow.json",
    "default_priority": "medium"
})
config.save()
```

---

## 📚 ADDITIONAL RESOURCES

- **TaskFlow README:** [README.md](README.md)
- **Full Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Integration Plan:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- **Agent Guides:** [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- **GitHub:** https://github.com/DonkRonk17/TaskFlow

---

**Last Updated:** January 2026  
**Maintained By:** Atlas (Team Brain)  
**For:** Logan Smith / Metaphy LLC
