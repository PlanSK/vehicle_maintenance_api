from httpx import AsyncClient


async def test_main_page(async_conn: AsyncClient):
    response = await async_conn.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Vehicle maintenance API main page."}
