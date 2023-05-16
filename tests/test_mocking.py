from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from api.main import app
from database.crud import CrudDB


@pytest.fixture
async def test_client():
    app.state.sessionmaker = AsyncMock(
        auto_spec='api.main.create_session_maker', return_value=None)
    yield AsyncClient(app=app, base_url="http://test")


class RawMock(tuple):
    def __init__(self, mock_tup: tuple) -> None:
        self.mock_tup = mock_tup

    def _asdict(self):
        return {"id": self.mock_tup[0],
                "name": self.mock_tup[1]}


@pytest.mark.asyncio
async def test_crud_all_info():
    mock_get_table_data = AsyncMock(return_value=[
        RawMock((1, 'Data 1 - Test 1')),
        RawMock((2, 'Data 2 - Test 2')),
        RawMock((3, 'Data 3 - Test 3'))
    ])

    with patch('database.crud.CrudDB.get_table_data', mock_get_table_data):
        crud_instance = CrudDB(None)
        response = await crud_instance.get_all_info()

    assert len(response) == 9
    assert response[0]['id'] == 1
    assert response[0]['name'] == 'Data 1 - Test 1'
    mock_get_table_data.assert_called()


@pytest.mark.asyncio
async def test_crud_get_id():
    mock_execute = AsyncMock(auto_spec='api.main.create_session_maker',
                             return_value=RawMock((1, 'Data 1 - Test 1')))
    crud_instance = CrudDB(mock_execute)
    response = await crud_instance.get_data_by_id(10)
    assert response == {'error': 'no such raw'}


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_all_info(anyio_backend, test_client):
    mock_get_table_data = AsyncMock(return_value=[
        RawMock((1, 'Data 1 - Test 1')),
        RawMock((2, 'Data 2 - Test 2')),
        RawMock((3, 'Data 3 - Test 3'))
    ])

    with patch('database.crud.CrudDB.get_table_data', mock_get_table_data):
        async with test_client as client:
            response = await client.get(f"/get_all/")
            assert response.status_code == 200
            assert len(response.json()['data']) == 9
            assert response.json()['data'][0]['id'] == 1
            assert response.json()['data'][0]['name'] == 'Data 1 - Test 1'
            mock_get_table_data.assert_called()


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_by_id(anyio_backend, test_client):
    mock_get_data_by_id = AsyncMock(return_value={"id": 1, "name": "TEST_1"})
    with patch('api.main.CrudDB.get_data_by_id', mock_get_data_by_id):
        async with test_client as client:
            response = await client.get(f"/get_name/{10}")
            assert response.json() == {'data': {'id': 1, 'name': 'TEST_1'}}


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_by_range(anyio_backend, test_client):
    mock_get_range = AsyncMock(return_value=[
        {"id": 1, "name": 'Data 2 - Test 2'},
        {"id": 2, "name": 'Data 1 - Test 1'},
        {"id": 3, "name": 'Data 3 - Test 3'}
    ])
    with patch('database.crud.CrudDB.get_range',  mock_get_range):
        async with test_client as client:
            response = await client.get("/get_by_range/", params={"start": 1, "end": 3})
            assert len(response.json()['data']) == 9
            assert response.json()['data'][0]['name'] == 'Data 2 - Test 2'


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_by_range_incorrect_range(anyio_backend, test_client):
    async with test_client as client:
        response_false = await client.get("/get_by_range/", params={"start": 3, "end": 1})
        assert response_false.status_code == 400
        assert response_false.text == 'Error, incorrect range'


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_by_range_not_int(anyio_backend, test_client):
    async with test_client as client:
        response_not_int = await client.get("/get_by_range/", params={"start": "some", "end": 1})
        assert response_not_int.status_code == 422
        assert response_not_int.json(
        )['detail'][0]['msg'] == "value is not a valid integer"
        response_less_1 = await client.get("/get_by_range/", params={"start": 0, "end": 1})
        assert response_less_1.status_code == 400
        assert response_less_1.text == 'Validation error, make sure the number is greater than 0 and an integer.'
