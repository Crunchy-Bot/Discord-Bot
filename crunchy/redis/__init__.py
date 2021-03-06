import asyncio
import typing as t

import aioredis


class RedisManager:
    """
    This manages all the redis systems to make is easy to dynamically create
    cache stores without having to manually make a new attr every time.
    """
    def __init__(self, collections: t.List[str]):
        self._pools: t.Dict[str, aioredis.ConnectionsPool] = {}
        self._collections = collections

    async def setup(self):
        """
        Sets up all the pools by awaiting the connection with `i` being the number of the pool,
        changing the order of the stores will affect the pool.
        :return:
        """
        for i, coll in enumerate(self._collections, start=1):
            print(f"[ REDIS ][ STATUS ] Creating pool {coll}")
            self._pools[coll] = await aioredis.create_redis_pool(f"redis://127.0.0.1:6379/{i}")

    async def shutdown(self):
        for name, pool in self._pools.items():
            print(f"[ REDIS ][ STATUS ] Shutting down pool {name}...")
            pool.close()
            await pool.wait_closed()

    def __getattr__(self, item):
        return self._pools.get(item)



