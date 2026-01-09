"""
TaskFlow - Automated Test Script
Tests all functionality
"""

import sys
import io
import os
import json
import tempfile
from pathlib import Path

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Import TaskFlow class
sys.path.insert(0, '.')
from taskflow import TaskFlow

print("🧪 TASKFLOW FUNCTIONALITY TEST\n")
print("="*60)

# Use temp file
test_file = Path(tempfile.gettempdir()) / "test_taskflow.json"
if test_file.exists():
    test_file.unlink()

tf = TaskFlow(str(test_file))

# TEST 1: Add tasks
print("\n[TEST 1] Adding tasks...")
try:
    task1 = tf.add_task("Implement feature A", "high", ["feature", "urgent"], "2026-01-15")
    task2 = tf.add_task("Fix bug in login", "high", ["bug"])
    task3 = tf.add_task("Write documentation", "medium", ["docs"])
    task4 = tf.add_task("Refactor code", "low", ["refactor"])
    print(f"✅ PASS: Added 4 tasks (IDs: {task1['id']}, {task2['id']}, {task3['id']}, {task4['id']})")
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 2: List tasks
print("\n[TEST 2] Listing all tasks...")
try:
    tasks = tf.list_tasks()
    if len(tasks) == 4:
        print(f"✅ PASS: Found {len(tasks)} tasks")
    else:
        print(f"❌ FAIL: Expected 4 tasks, got {len(tasks)}")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 3: Filter by priority
print("\n[TEST 3] Filtering by priority...")
try:
    high_priority = tf.list_tasks(priority="high")
    if len(high_priority) == 2:
        print(f"✅ PASS: Found {len(high_priority)} high-priority tasks")
    else:
        print(f"❌ FAIL: Expected 2 high-priority tasks, got {len(high_priority)}")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 4: Filter by tag
print("\n[TEST 4] Filtering by tag...")
try:
    bug_tasks = tf.list_tasks(tag="bug")
    if len(bug_tasks) == 1 and bug_tasks[0]['title'] == "Fix bug in login":
        print(f"✅ PASS: Found bug task")
    else:
        print(f"❌ FAIL: Tag filtering not working")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 5: Mark task in progress
print("\n[TEST 5] Marking task in progress...")
try:
    if tf.mark_in_progress(1):
        task = tf.get_task(1)
        if task['status'] == 'in_progress':
            print(f"✅ PASS: Task 1 marked as in_progress")
        else:
            print(f"❌ FAIL: Status not updated")
            sys.exit(1)
    else:
        print(f"❌ FAIL: Could not update task")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 6: Mark task done
print("\n[TEST 6] Marking task done...")
try:
    if tf.mark_done(2):
        task = tf.get_task(2)
        if task['status'] == 'done':
            print(f"✅ PASS: Task 2 marked as done")
        else:
            print(f"❌ FAIL: Status not updated")
            sys.exit(1)
    else:
        print(f"❌ FAIL: Could not update task")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 7: Update task
print("\n[TEST 7] Updating task...")
try:
    if tf.update_task(3, title="Write comprehensive documentation", priority="high"):
        task = tf.get_task(3)
        if task['title'] == "Write comprehensive documentation" and task['priority'] == "high":
            print(f"✅ PASS: Task 3 updated")
        else:
            print(f"❌ FAIL: Task not updated correctly")
            sys.exit(1)
    else:
        print(f"❌ FAIL: Could not update task")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 8: Persistence (save & reload)
print("\n[TEST 8] Testing persistence...")
try:
    tf.save_tasks()
    
    # Create new instance
    tf2 = TaskFlow(str(test_file))
    tasks = tf2.list_tasks()
    if len(tasks) == 4:
        task1 = tf2.get_task(1)
        if task1['status'] == 'in_progress':
            print("✅ PASS: Tasks saved and reloaded correctly")
        else:
            print("❌ FAIL: Task status not persisted")
            sys.exit(1)
    else:
        print(f"❌ FAIL: Expected 4 tasks after reload, got {len(tasks)}")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 9: Filter by status
print("\n[TEST 9] Filtering by status...")
try:
    done_tasks = tf.list_tasks(status="done")
    if len(done_tasks) == 1:
        print(f"✅ PASS: Found {len(done_tasks)} done task")
    else:
        print(f"❌ FAIL: Expected 1 done task, got {len(done_tasks)}")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 10: Delete task
print("\n[TEST 10] Deleting task...")
try:
    if tf.delete_task(4):
        tasks = tf.list_tasks()
        if len(tasks) == 3:
            print(f"✅ PASS: Task deleted, {len(tasks)} tasks remaining")
        else:
            print(f"❌ FAIL: Expected 3 tasks after delete, got {len(tasks)}")
            sys.exit(1)
    else:
        print(f"❌ FAIL: Could not delete task")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 11: Export to Markdown
print("\n[TEST 11] Exporting to Markdown...")
try:
    export_file = Path(tempfile.gettempdir()) / "test_tasks.md"
    if tf.export_markdown(str(export_file)):
        if export_file.exists():
            content = export_file.read_text(encoding='utf-8')
            if "TaskFlow" in content and "Implement feature A" in content:
                print(f"✅ PASS: Markdown export successful")
                export_file.unlink()  # Clean up
            else:
                print(f"❌ FAIL: Export file missing expected content")
                sys.exit(1)
        else:
            print(f"❌ FAIL: Export file not created")
            sys.exit(1)
    else:
        print(f"❌ FAIL: Export returned False")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 12: Overdue detection
print("\n[TEST 12] Testing overdue detection...")
try:
    # Add task with past due date
    past_task = tf.add_task("Overdue task", "high", [], "2025-01-01")
    if tf.is_overdue(past_task):
        print(f"✅ PASS: Overdue detection working")
    else:
        print(f"❌ FAIL: Overdue task not detected")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# Clean up
if test_file.exists():
    test_file.unlink()

print("\n" + "="*60)
print("🎉 ALL 12 TESTS PASSED!")
print("="*60)
print("\n✅ TaskFlow core functionality verified!")
print("   - Task creation working")
print("   - Listing and filtering working")
print("   - Status updates working")
print("   - Task editing working")
print("   - Persistence (save/load) working")
print("   - Markdown export working")
print("   - Overdue detection working\n")
