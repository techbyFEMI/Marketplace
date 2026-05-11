from supabase import acreate_client as create_async_client, AClient as AsyncClient, create_client, Client
from core.config import settings

_async_client: AsyncClient = None

# Async client for FastAPI routers (Reuses connection pool)
async def get_supabase_async() -> AsyncClient:
    global _async_client
    if _async_client is None:
        _async_client = await create_async_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _async_client

# Sync client for legacy support
_sync_client: Client = None
def get_supabase_sync() -> Client:
    global _sync_client
    if _sync_client is None:
        _sync_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _sync_client

def get_supabase() -> Client:
    return get_supabase_sync()