from redis import asyncio as aioredis
import json


class CacheManager:
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.redis_client = None

    async def connect(self):
        # Connect to redis
        self.redis_client = await aioredis.from_url(self.redis_url)

    async def get_conversation_config(self, conversation_id):
        # Get project configuration from redis
        if not self.redis_client:
            await self.connect()
        project_config = await self.redis_client.get(conversation_id)
        if project_config:
            return json.loads(project_config)
        else:
            return None

    async def save_conversation_config(self, conversation_id, project_config, timeout=3600):
        # Save project configuration to redis with timeout by default 1 hour(3600 seconds)
        if not self.redis_client:
            await self.connect()
        project_config_json = json.dumps(project_config)
        await self.redis_client.set(conversation_id, project_config_json, ex=timeout)

    async def flush_conversation_cache(self, conversation_id):
        # Flush project cache
        if not self.redis_client:
            await self.connect()
        await self.redis_client.delete(conversation_id)
