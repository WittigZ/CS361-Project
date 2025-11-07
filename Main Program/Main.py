import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, data_file='tasks.json'):
        self.data_file = data_file
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data
                print("Your tasks have been loaded successfully.")
            except Exception as e:
                print(f"Could not load tasks: {e}. Starting with empty list.")
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def display_main_menu(self):
        """Show main menu"""
        print("\n" + "="*50)
        print(" WELCOME TO TASK MANAGER ")
        print("="*50)
        print("The simplest way to organize your tasks.")
        print("\nMAIN MENU:")
        print("(V)iew My Tasks")
        print("(A)dd a New Task") 
        print("(Q)uit")
        print("\nTip: Start by adding a task with 'A'.")
        print("-"*50)
    
    def add_new_task(self):
        """Add a new task"""
        print("\n" + "="*50)
        print("ADD A NEW TASK")
        print("="*50)
        print("Creating a task helps you remember and track")
        print("your progress. All you need is a title!")
        print("-"*50)
        
        while True:
            title = input("\nEnter Task Title: ").strip()
            if title:
                break
            print("Title is required. Please enter a task title.")
        
        due_date = input("Due Date (YYYY-MM-DD) [Optional - press Enter to skip]: ").strip()
        if due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Using no due date.")
                due_date = ""
        
        priority_input = input("Priority (1-High, 2-Medium, 3-Low) [2]: ").strip()
        priority_map = {'1': 'High', '2': 'Medium', '3': 'Low'}
        priority = priority_map.get(priority_input, 'Medium')
        
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'due_date': due_date,
            'priority': priority,
            'completed': False
        }
        
        self.tasks.append(task)
        
        if self.save_tasks():
            print(f"\nTask '{title}' has been added successfully!")
            print("Press any key to continue...")
            input()
        else:
            print("Failed to save task.")
    
    def view_tasks(self):
        """View and manage tasks - User Story: View Task List"""
        current_sort = 'N' 
        current_filter = 'N' 
    
        while True:
            print("\n" + "="*50)
            print("MY TASKS")
            print("="*50)
        
            print(f"SORT: (D)ue Date  (P)riority  (T)itle")
            print(f"FILTER: (N)o Filter  (I)ncomplete  (C)ompleted")
            print("-"*50)
        
            if not self.tasks:
                print("No tasks found. Add some tasks to get started!")
                print("-"*50)
                print("ACTIONS: (A)dd Task  (B)ack to Main Menu")
                choice = input("\nEnter your choice: ").strip().upper()
                if choice == 'A':
                    self.add_new_task()
                    continue
                elif choice == 'B':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    continue
        
            filtered_tasks = []
            for task in self.tasks:
                if current_filter == 'N':  
                    filtered_tasks.append(task)
                elif current_filter == 'I' and not task['completed']: 
                    filtered_tasks.append(task)
                elif current_filter == 'C' and task['completed']: 
                    filtered_tasks.append(task)
        
            if current_sort == 'D':  
                filtered_tasks.sort(key=lambda x: (x['due_date'] or '9999-99-99'))
            elif current_sort == 'P':  
                priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
                filtered_tasks.sort(key=lambda x: priority_order[x['priority']])
            elif current_sort == 'T': 
                filtered_tasks.sort(key=lambda x: x['title'].lower())
        
          
            print(f"{'#':<2} {'Status':<6} {'Task':<20} {'Due Date':<12} {'Priority':<8}")
            print("-"*50)
        
            for i, task in enumerate(filtered_tasks, 1):
                status = "✓" if task['completed'] else " "
                due_date = task['due_date'] if task['due_date'] else "No date"
                print(f"{i:<2} [{status}]   {task['title'][:18]:<18} {due_date:<12} {task['priority']:<8}")
        
            print("-"*50)
            print(f"Showing {len(filtered_tasks)} task(s)")
        

            print("ACTIONS: (A)dd Task  (1-{})Toggle Complete  (E)dit  (B)ack".format(len(filtered_tasks)))
            choice = input("\nEnter a command, task number: ").strip().upper()
        
            if choice == 'A':
                self.add_new_task()
            elif choice == 'B':
                break
            elif choice == 'E':
                self.edit_task()
            elif choice in ['D', 'P', 'T']: 
                current_sort = choice
                print(f"Now sorting by: {'Due Date' if choice == 'D' else 'Priority' if choice == 'P' else 'Title' if choice == 'T' else 'None'}")
            elif choice in ['N', 'I', 'C']:
                current_filter = choice
                print(f"Now showing: {'All Tasks' if choice == 'N' else 'Incomplete only' if choice == 'I' else 'Completed only'}")
            elif choice.isdigit():
                task_num = int(choice)
                if 1 <= task_num <= len(filtered_tasks):
                    filtered_task = filtered_tasks[task_num - 1]
                    for idx, main_task in enumerate(self.tasks):
                        if main_task['id'] == filtered_task['id']:
                            self.toggle_task_complete(idx + 1)
                            break
                else:
                    print("Invalid task number.")
            else:
                print("Invalid choice. Please try again.")
    
    def toggle_task_complete(self, task_num):
        """Toggle task completion"""
        task = self.tasks[task_num - 1]
        task['completed'] = not task['completed']
        status = "completed" if task['completed'] else "incomplete"

        if self.save_tasks():
            print(f"\nMarked '{task['title']}' as {status}!")
            print("You can toggle this again to change back.")
            print("Press any key to continue...")
            input()
        else:
            print("Failed to save changes.")
    
    def edit_task(self):
        """Edit a task"""
        if not self.tasks:
            print("No tasks to edit.")
            return
        
        print("\nEnter the task number to edit:")
        try:
            task_num = int(input("Task number: "))
            if not (1 <= task_num <= len(self.tasks)):
                print("Invalid task number.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return
        
        task = self.tasks[task_num - 1]
        
        while True:
            print("\n" + "="*50)
            print("EDIT A TASK")
            print("="*50)
            print(f"You are editing: '{task['title']}'")
            print("Changes are saved immediately.")
            print("-"*50)
            
            print(f"1. Title: {task['title']}")
            print(f"2. Due Date: {task['due_date'] or 'Not set'}")
            print(f"3. Priority: {task['priority']}")
            print(f"4. Completed: {'Yes' if task['completed'] else 'No'}")
            print("-"*50)
            print("(R)evert All Changes  (B)ack to Task List")
            
            choice = input("\nEnter the number to change, or a command: ").strip().upper()
            
            if choice == '1':
                new_title = input("Enter new title: ").strip()
                if new_title:
                    task['title'] = new_title
                    print("Title updated.")
                else:
                    print("Title cannot be empty.")
            elif choice == '2':
                new_date = input("Enter new due date (YYYY-MM-DD) or empty to remove: ").strip()
                if new_date:
                    try:
                        datetime.strptime(new_date, '%Y-%m-%d')
                        task['due_date'] = new_date
                        print("Due date updated.")
                    except ValueError:
                        print("Invalid date format.")
                else:
                    task['due_date'] = ""
                    print("Due date removed.")
            elif choice == '3':
                new_prio = input("Enter new priority (1-High, 2-Medium, 3-Low): ").strip()
                priority_map = {'1': 'High', '2': 'Medium', '3': 'Low'}
                if new_prio in priority_map:
                    task['priority'] = priority_map[new_prio]
                    print("Priority updated.")
                else:
                    print("Invalid priority.")
            elif choice == '4':
                task['completed'] = not task['completed']
                status = "completed" if task['completed'] else "incomplete"
                print(f"Marked as {status}.")
            elif choice == 'R':
                self.load_tasks()
                print("All changes reverted.")
                break
            elif choice == 'B':
                break
            else:
                print("❌ Invalid choice.")
            
            self.save_tasks()
    
    def run(self):
        """Main program loop"""
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice: ").strip().upper()
            
            if choice == 'V':
                self.view_tasks()
            elif choice == 'A':
                self.add_new_task()
            elif choice == 'Q':
                print("Thank you for using Task Manager!")
                print("Your tasks have been saved automatically")
                break
            else:
                print("Invalid choice. Please try V, A, or Q.")

if __name__ == "__main__":
    app = TaskManager()
    app.run()