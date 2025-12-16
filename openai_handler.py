import os

# Simple memory storage (in-memory)
user_tasks = {}

def analyze_intent(user_id, user_message):
    """Process incoming messages and manage tasks"""
   message = user_message.lower().strip()
    
    # Create user task list if doesn't exist
    if user_id not in user_tasks:
        user_tasks[user_id] = []
    
    # Add task command
    if message.startswith(('add ', 'create ', 'new ')):
        task_text = user_message[len(message.split()[0]):].strip()
        user_tasks[user_id].append(task_text)
        return f"✅ Added: {task_text}"
    
    # List tasks command
    elif any(word in message for word in ['list', 'show', 'tasks', 'todo']):
        if not user_tasks[user_id]:
            return "You have no tasks yet! Send 'add [task]' to create one."
        tasks_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(user_tasks[user_id])])
        return f"📝 Your tasks:\n{tasks_list}"
    
    # Help command
    elif 'help' in message:
        return ("🤖 WhatsApp Todo Bot\n\n"
                "Commands:\n"
                "• add [task] - Add a new task\n"
                "• list - Show all tasks\n"
                "• help - Show this help")
    
    # Default response
    else:
        return "Hi! I'm your todo bot. Send 'help' to see what I can do!"
