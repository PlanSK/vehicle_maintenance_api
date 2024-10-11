import os
from httpx import AsyncClient


async def test_main_page(async_conn: AsyncClient):
    response = await async_conn.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Vehicle maintenance API main page."}

def test_load_env_vars_pytest_env():
    assert os.environ["DB_FILENAME"] == "testdb.sqlite3"
