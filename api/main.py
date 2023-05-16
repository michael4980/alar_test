import fastapi
from fastapi import Response
import sqlalchemy

from api.models.request_models import ValidModel
from database.crud import CrudDB
from database.session import create_sessionmaker

app = fastapi.FastAPI()


async def get_session() -> sqlalchemy.ext.asyncio.AsyncSession:
    """
    Returns:
        returns an instance of AsyncSession from the create_sessionmaker function.
    """
    return await create_sessionmaker()


@app.on_event("startup")
async def startup() -> None:
    """function is executed on startup of the application and creates 
    an instance of the AsyncSession which is stored in the application's state.
    """
    app.state.sessionmaker = await get_session()


@app.get('/get_all/')
async def get_all_data() -> dict:
    """This function returns all the information from the database."""
    start_session = CrudDB(session=app.state.sessionmaker())
    result = await start_session.get_all_info()
    return {'data': result}


@app.get('/get_name/{id}')
async def get_info(id: int) -> dict:
    """This function returns information from the database for a given id."""
    start_session = CrudDB(session=app.state.sessionmaker())
    result = await start_session.get_data_by_id(id)
    if 'error' in result:
        return Response('Existing error', status_code=404)
    return {'data': result}


@app.get('/get_by_range/')
async def get_info_by_range(start: int, end: int) -> dict:
    """This function returns information from the database for a given range 
    of start and end. If the start is greater than or equal to end, 
    an error response is returned.

    Args:
        request (ValidModel):

    Returns:
        dict : result data 
    """
    start_session = CrudDB(session=app.state.sessionmaker())
    try:
        params = ValidModel(start=start, end=end)
    except Exception as ex:
        return Response('Validation error, make sure the number is greater than 0 and an integer.', status_code=400)
    if params.start >= params.end:
        return Response('Error, incorrect range', status_code=400)
    result = await start_session.get_data_from_range(params.start, params.end)
    return {'data': result}
