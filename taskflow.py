#!/usr/bin/env python3
"""
TaskFlow - Smart CLI Todo & Project Manager
A lightweight, git-friendly task management system for developers.
"""

import os
import sys
import io
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# --- Config ---
TASKFILE = ".taskflow.json"
PRIORITY_COLORS = {
    "high": "[!]",
    "medium": "[~]",
    "low": "[-]"
}
STATUS_ICONS = {
    "todo": "[ ]",
    "in_progress": "[>]",
    "done": "[X]",
    "blocked": "[#]"
}

class TaskFlow:
    """CLI task manager"""
    
    def __init__(self, task_file: str = TASKFILE):
        self.task_file = Path(task_file)
        self.tasks: List[Dict] = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if self.task_file.exists():
            try:
                with open(self.task_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
            except Exception as e:
                print(f"[!] Warning: Could not load tasks: {e}")
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        data = {
            "tasks": self.tasks,
            "last_updated": datetime.now().isoformat()
        }
        try:
            with open(self.task_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[X] Error saving tasks: {e}")
    
    def add_task(self, title: str, priority: str = "medium", tags: List[str] = None, due_date: str = None):
        """Add new task"""
        task = {
            "id": self._generate_id(),
            "title": title,
            "priority": priority,
            "status": "todo",
            "tags": tags or [],
            "due_date": due_date,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def _generate_id(self) -> int:
        """Generate unique task ID"""
        if not self.tasks:
            return 1
        return max(task['id'] for task in self.tasks) + 1
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, **kwargs):
        """Update task fields"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        for key, value in kwargs.items():
            if key in task:
                task[key] = value
        
        task['updated'] = datetime.now().isoformat()
        self.save_tasks()
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def list_tasks(self, status: str = None, priority: str = None, tag: str = None) -> List[Dict]:
        """List tasks with optional filters"""
        filtered = self.tasks
        
        if status:
            filtered = [t for t in filtered if t['status'] == status]
        
        if priority:
            filtered = [t for t in filtered if t['priority'] == priority]
        
        if tag:
            filtered = [t for t in filtered if tag in t.get('tags', [])]
        
        # Sort by priority (high > medium > low) then by ID
        priority_order = {"high": 0, "medium": 1, "low": 2}
        filtered.sort(key=lambda t: (priority_order.get(t['priority'], 3), t['id']))
        
        return filtered
    
    def mark_done(self, task_id: int) -> bool:
        """Mark task as done"""
        return self.update_task(task_id, status="done")
    
    def mark_in_progress(self, task_id: int) -> bool:
        """Mark task as in progress"""
        return self.update_task(task_id, status="in_progress")
    
    def is_overdue(self, task: Dict) -> bool:
        """Check if task is overdue"""
        if not task.get('due_date'):
            return False
        
        try:
            due = datetime.fromisoformat(task['due_date'])
            return datetime.now() > due and task['status'] != 'done'
        except:
            return False
    
    def export_markdown(self, output_file: str = "TASKS.md"):
        """Export tasks to Markdown format"""
        output = ["# 📋 TaskFlow - Project Tasks\n"]
        output.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        output.append(f"**Total Tasks:** {len(self.tasks)}\n\n")
        output.append("---\n\n")
        
        # Group by status
        for status in ["in_progress", "todo", "blocked", "done"]:
            status_tasks = [t for t in self.tasks if t['status'] == status]
            if not status_tasks:
                continue
            
            status_name = status.replace('_', ' ').title()
            output.append(f"## {STATUS_ICONS[status]} {status_name} ({len(status_tasks)})\n\n")
            
            for task in status_tasks:
                priority_icon = PRIORITY_COLORS[task['priority']]
                output.append(f"### {priority_icon} [{task['id']}] {task['title']}\n\n")
                output.append(f"- **Priority:** {task['priority']}\n")
                output.append(f"- **Status:** {task['status']}\n")
                
                if task.get('tags'):
                    output.append(f"- **Tags:** {', '.join(task['tags'])}\n")
                
                if task.get('due_date'):
                    output.append(f"- **Due:** {task['due_date']}\n")
                
                output.append(f"- **Created:** {task['created'][:10]}\n")
                output.append("\n")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(''.join(output))
            return True
        except Exception as e:
            print(f"[X] Error exporting: {e}")
            return False


def print_task(task: Dict, show_details: bool = False):
    """Pretty print a task"""
    status_icon = STATUS_ICONS[task['status']]
    priority_icon = PRIORITY_COLORS[task['priority']]
    
    # Check if overdue
    overdue_marker = ""
    if task.get('due_date'):
        try:
            due = datetime.fromisoformat(task['due_date'])
            if datetime.now() > due and task['status'] != 'done':
                overdue_marker = " [!] OVERDUE"
        except:
            pass
    
    # Basic line
    print(f"{status_icon} {priority_icon} [{task['id']}] {task['title']}{overdue_marker}")
    
    if show_details:
        print(f"    Priority: {task['priority']} | Status: {task['status']}")
        if task.get('tags'):
            print(f"    Tags: {', '.join(task['tags'])}")
        if task.get('due_date'):
            print(f"    Due: {task['due_date']}")
        print(f"    Created: {task['created'][:10]}")
        print()


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="TaskFlow - Smart CLI Todo & Project Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  taskflow add "Fix login bug" --priority high --tags bug,urgent
  taskflow list                           # List all tasks
  taskflow list --status todo             # Filter by status
  taskflow done 3                         # Mark task #3 as done
  taskflow start 5                        # Mark task #5 in progress
  taskflow delete 7                       # Delete task #7
  taskflow export                         # Export to TASKS.md
  
Statuses: todo, in_progress, done, blocked
Priorities: high, medium, low
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('--priority', choices=['high', 'medium', 'low'], default='medium')
    add_parser.add_argument('--tags', help='Comma-separated tags')
    add_parser.add_argument('--due', help='Due date (YYYY-MM-DD)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', choices=['todo', 'in_progress', 'done', 'blocked'])
    list_parser.add_argument('--priority', choices=['high', 'medium', 'low'])
    list_parser.add_argument('--tag', help='Filter by tag')
    list_parser.add_argument('--details', action='store_true', help='Show detailed info')
    
    # Done command
    done_parser = subparsers.add_parser('done', help='Mark task as done')
    done_parser.add_argument('task_id', type=int, help='Task ID')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Mark task as in progress')
    start_parser.add_argument('task_id', type=int, help='Task ID')
    
    # Block command
    block_parser = subparsers.add_parser('block', help='Mark task as blocked')
    block_parser.add_argument('task_id', type=int, help='Task ID')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete task')
    delete_parser.add_argument('task_id', type=int, help='Task ID')
    
    # Edit command
    edit_parser = subparsers.add_parser('edit', help='Edit task')
    edit_parser.add_argument('task_id', type=int, help='Task ID')
    edit_parser.add_argument('--title', help='New title')
    edit_parser.add_argument('--priority', choices=['high', 'medium', 'low'])
    edit_parser.add_argument('--tags', help='Comma-separated tags')
    edit_parser.add_argument('--due', help='Due date (YYYY-MM-DD)')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export tasks to Markdown')
    export_parser.add_argument('--output', default='TASKS.md', help='Output file')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize TaskFlow in current directory')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show task statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize TaskFlow
    tf = TaskFlow()
    
    # Execute command
    if args.command == 'init':
        if Path(TASKFILE).exists():
            print("[OK] TaskFlow already initialized in this directory")
        else:
            tf.save_tasks()
            print("[OK] TaskFlow initialized!")
            print(f"   Task file: {TASKFILE}")
            print("\n[TIP] Quick start:")
            print('   taskflow add "My first task"')
            print('   taskflow list')
    
    elif args.command == 'add':
        tags = args.tags.split(',') if args.tags else []
        task = tf.add_task(args.title, args.priority, tags, args.due)
        print(f"[OK] Task added: [{task['id']}] {task['title']}")
    
    elif args.command == 'list':
        tasks = tf.list_tasks(args.status, args.priority, args.tag)
        
        if not tasks:
            print("[INFO] No tasks found")
            return
        
        # Print summary
        print(f"\n[TASKS] TaskFlow - {len(tasks)} task(s)\n")
        
        for task in tasks:
            print_task(task, args.details)
        
        # Show counts by status
        print()
        status_counts = {}
        for task in tf.tasks:
            status = task['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("[STATS] Summary:")
        for status in ["todo", "in_progress", "blocked", "done"]:
            count = status_counts.get(status, 0)
            if count > 0:
                icon = STATUS_ICONS[status]
                status_name = status.replace('_', ' ').title()
                print(f"   {icon} {status_name}: {count}")
    
    elif args.command == 'done':
        if tf.mark_done(args.task_id):
            task = tf.get_task(args.task_id)
            print(f"[OK] Task completed: [{task['id']}] {task['title']}")
        else:
            print(f"[X] Task {args.task_id} not found")
    
    elif args.command == 'start':
        if tf.mark_in_progress(args.task_id):
            task = tf.get_task(args.task_id)
            print(f"[>] Task started: [{task['id']}] {task['title']}")
        else:
            print(f"[X] Task {args.task_id} not found")
    
    elif args.command == 'block':
        if tf.update_task(args.task_id, status="blocked"):
            task = tf.get_task(args.task_id)
            print(f"[#] Task blocked: [{task['id']}] {task['title']}")
        else:
            print(f"[X] Task {args.task_id} not found")
    
    elif args.command == 'delete':
        task = tf.get_task(args.task_id)
        if task:
            if tf.delete_task(args.task_id):
                print(f"[DEL] Task deleted: [{task['id']}] {task['title']}")
        else:
            print(f"[X] Task {args.task_id} not found")
    
    elif args.command == 'edit':
        task = tf.get_task(args.task_id)
        if not task:
            print(f"❌ Task {args.task_id} not found")
            return
        
        updates = {}
        if args.title:
            updates['title'] = args.title
        if args.priority:
            updates['priority'] = args.priority
        if args.tags:
            updates['tags'] = args.tags.split(',')
        if args.due:
            updates['due_date'] = args.due
        
        if updates:
            tf.update_task(args.task_id, **updates)
            print(f"[EDIT] Task updated: [{task['id']}] {task['title']}")
        else:
            print("[!] No changes specified")
    
    elif args.command == 'export':
        if tf.export_markdown(args.output):
            print(f"[OK] Tasks exported to: {args.output}")
        else:
            print("[X] Export failed")
    
    elif args.command == 'stats':
        total = len(tf.tasks)
        if total == 0:
            print("[INFO] No tasks yet")
            return
        
        # Calculate stats
        by_status = {}
        by_priority = {}
        overdue_count = 0
        
        for task in tf.tasks:
            status = task['status']
            priority = task['priority']
            by_status[status] = by_status.get(status, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1
            if tf.is_overdue(task):
                overdue_count += 1
        
        print("\n[STATS] TaskFlow Statistics\n")
        print(f"Total Tasks: {total}")
        print()
        
        print("By Status:")
        for status in ["todo", "in_progress", "blocked", "done"]:
            count = by_status.get(status, 0)
            icon = STATUS_ICONS[status]
            pct = (count / total * 100) if total > 0 else 0
            print(f"  {icon} {status.replace('_', ' ').title()}: {count} ({pct:.1f}%)")
        
        print()
        print("By Priority:")
        for priority in ["high", "medium", "low"]:
            count = by_priority.get(priority, 0)
            icon = PRIORITY_COLORS[priority]
            pct = (count / total * 100) if total > 0 else 0
            print(f"  {icon} {priority.title()}: {count} ({pct:.1f}%)")
        
        if overdue_count > 0:
            print()
            print(f"[!] Overdue: {overdue_count}")
        
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[BYE] TaskFlow closed")
    except Exception as e:
        print(f"\n[X] Error: {e}")
        sys.exit(1)
