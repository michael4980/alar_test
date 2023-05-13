import pytest


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_all_raws(anyio_backend, test_app):
    async with test_app as client:
        response = await client.get("/get_all/")
        assert response.status_code == 200, response.text
        assert response.json()['data'][0]['name'] == "Test data 1"
        assert len(response.json()['data']) == 3


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_id_by_name(anyio_backend, test_app):
    async with test_app as client:
        response = await client.get(f"/get_name/{1}")
        assert response.status_code == 200
        assert response.json()['data']['name'] == "Test data 1"


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_by_range(anyio_backend, test_app):
    async with test_app as client:
        response = await client.get("/get_by_range/", params={"start": 10, "end": 1})
        assert response.status_code == 422


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_id_false(anyio_backend, test_app):
    async with test_app as client:
        response = await client.get(f"/get_name/{2}")
        assert response.status_code == 404
        assert response.text == 'Existing error'

