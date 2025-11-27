import motor.motor_asyncio
from bot.config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.config_col = self.db.config

    def new_user(self, id):
        return dict(
            _id=id,
            thumbnail=None,
            blacklist_words=[]
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return True if user else False

    async def get_user(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user

    async def set_thumbnail(self, id, thumbnail_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'thumbnail': thumbnail_id}})

    async def get_thumbnail(self, id):
        user = await self.get_user(id)
        return user.get('thumbnail', None)

    async def set_blacklist(self, id, words):
        await self.col.update_one({'_id': int(id)}, {'$set': {'blacklist_words': words}})

    async def get_blacklist(self, id):
        user = await self.get_user(id)
        return user.get('blacklist_words', [])
    
    # Global Config Methods
    async def get_concurrency_limit(self):
        config = await self.config_col.find_one({'_id': 'main_config'})
        if config:
            return config.get('max_concurrent_tasks', Config.MAX_CONCURRENT_TASKS)
        return Config.MAX_CONCURRENT_TASKS

    async def set_concurrency_limit(self, limit):
        await self.config_col.update_one(
            {'_id': 'main_config'}, 
            {'$set': {'max_concurrent_tasks': int(limit)}}, 
            upsert=True
        )

db = Database(Config.MONGO_DB_URI, "BotDB")
