import asyncio
from bot.helper.database import db

class TaskManager:
    def __init__(self):
        self.active_tasks = {} # user_id -> list of task_ids
        self.task_info = {} # task_id -> {status, progress, type}
        self.lock = asyncio.Lock()

    async def can_add_task(self, user_id):
        # We can implement per-user limits here if needed
        # For now, we check global concurrency in the main logic or here
        # But user asked for "Owner can set it in owner settings command how it shoulkd process"
        # So we likely need a global check.
        
        limit = await db.get_concurrency_limit()
        current_total_tasks = sum(len(tasks) for tasks in self.active_tasks.values())
        
        if current_total_tasks >= limit:
            return False
        return True

    async def add_task(self, user_id, task_id, task_type="Download"):
        async with self.lock:
            if user_id not in self.active_tasks:
                self.active_tasks[user_id] = []
            self.active_tasks[user_id].append(task_id)
            self.task_info[task_id] = {
                "status": "Starting...",
                "progress": 0,
                "type": task_type,
                "user_id": user_id
            }

    async def remove_task(self, task_id):
        async with self.lock:
            if task_id in self.task_info:
                user_id = self.task_info[task_id]["user_id"]
                if user_id in self.active_tasks:
                    if task_id in self.active_tasks[user_id]:
                        self.active_tasks[user_id].remove(task_id)
                    if not self.active_tasks[user_id]:
                        del self.active_tasks[user_id]
                del self.task_info[task_id]

    async def update_progress(self, task_id, progress, status):
        if task_id in self.task_info:
            self.task_info[task_id]["progress"] = progress
            self.task_info[task_id]["status"] = status

    def get_user_tasks(self, user_id):
        return self.active_tasks.get(user_id, [])

    def get_all_tasks(self):
        return self.task_info

task_manager = TaskManager()
