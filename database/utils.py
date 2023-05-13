"""Utils for db"""


class UtilsTool:
    """basic utils class"""
    @classmethod
    def table_id_checker(cls, table_id: int) -> str | None:
        """
        Args:
            table_id (int): id of raw in table

        Returns:
            str | None: table name or none
        """
        name = None
        if table_id in range(1, 11) or table_id in range(31, 41):
            name = 'data_1'
        elif table_id in range(11, 21) or table_id in range(41, 51):
            name = 'data_2'
        elif table_id in range(21, 31) or table_id in range(51, 61):
            name = 'data_3'
        return name

    @classmethod
    async def generator(cls, names: list):
        """ returns names for async loop"""
        for name in names:
            yield name
