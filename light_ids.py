#!/usr/bin/python3
import aiohttp
import asyncio
import ssl
from hue_data import ip_address, user_id

async def _init_ids():
  ssl_context = ssl.create_default_context()
  ssl_context.check_hostname = False
  ssl_context.verify_mode = ssl.CERT_NONE
  
  connector = aiohttp.TCPConnector(ssl=ssl_context)
  async with aiohttp.ClientSession(connector=connector) as session:
    async with session.get(f"https://{ip_address}/clip/v2/resource/light", headers={"hue-application-key": user_id}) as response:
      data = await response.json()
      return {light["metadata"]["name"]: light["id"] for light in data["data"]}

def _get_ids():
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  try:
    return loop.run_until_complete(_init_ids())
  finally:
    loop.close()

_cached_ids = _get_ids()

def reload_cache():
  global _cached_ids
  _cached_ids = _get_ids()

def get_name(id):
  for name, light_id in _cached_ids.items():
    if light_id == id:
      return name
  return None

def get_id(name):
  return _cached_ids.get(name) 