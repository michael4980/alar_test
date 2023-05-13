from sqlalchemy import select, text

from database.models import Data1, Data2, Data3
from database.utils import UtilsTool


class CrudDB:
    """class for some CRUD operations with DB"""

    def __init__(self, session) -> None:
        self.session = session

    async def get_all_info(self) -> list:
        """get all raws from tables

        Returns:
            list: sorted data from all tables
        """
        sources = ['data_1', 'data_2', 'data_3']
        result = []
        async for table_name in UtilsTool.generator(sources):
            data = await self.get_table_data(table_name)
            result.extend(data)
        sorted_data = sorted(result, key=lambda x: x[0])
        dicted_data = [raw._asdict() for raw in sorted_data]
        return dicted_data

    async def get_table_data(self, name: str) -> list:
        """Fetch all data from the given table in the database.

            Args:
                name (str): The name of the table to fetch data from.

            Returns:
                list: A list of dictionaries containing the fetched data.
        """
        async with self.session as session:
            query = text(f'SELECT * from {name}')
            data = await session.execute(query)
            return data.fetchall()

    async def get_data_by_id(self, raw_id: int):
        """Fetch data from the database for a given ID.

        Args:
            raw_id (int): The ID of the data to fetch.

        Returns:
            dict: A dictionary containing the fetched data if the ID exists, else an error message.
        """
        check = UtilsTool.table_id_checker(raw_id)
        if check:
            async with self.session as session:
                try:
                    query = text(f'SELECT * from {check} WHERE id={raw_id}')
                    data = await session.execute(query)
                    return data.fetchall()[0]._asdict()
                except Exception as ex:
                    return {'error': 'no such raw'}
        return {'error': 'This id doesn`t exist'}

    async def get_data_from_range(self, start, end):
        """Fetch data from a range of IDs from multiple tables in the database.

            Args:
                start (int): The start of the range.
                end (int): The end of the range.

            Returns:
                list: A list of dictionaries containing the fetched data.
        """
        result = []
        async for table_name in UtilsTool.generator([Data1, Data2, Data3]):
            data = await self.get_range(start, end, table_name)
            result.extend(data)
        return sorted(result, key=lambda x: x['id'])

    async def get_range(self, start, end, table):
        """Fetch data from a range of IDs from a given table in the database.
            Args:
                start (int): The start of the range.
                end (int): The end of the range.
                table_name (str): The name of the table to fetch data from.

            Returns:
                list: A list of dictionaries containing the fetched data.
        """
        async with self.session as session:
            data = await session.execute(select(table).filter(table.id.between(start, end)))
            data = data.fetchall()
            dicted_data = [row[0].as_dict() for row in data]
            return dicted_data
