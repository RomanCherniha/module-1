import aiosqlite

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.pool = None

    async def connect(self):
        self.pool = await aiosqlite.connect(self.db_name)
        await self.create_moves_table()  # Create moves table on connection

    async def create_moves_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS moves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                position_from TEXT NOT NULL,
                position_to TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        async with self.pool.execute(create_table_query) as cursor:
            await cursor.fetchall()  # Execute the create table query

    async def insert_move(self, player, position_from, position_to):
        insert_query = """
            INSERT INTO moves (player, position_from, position_to)
            VALUES (?, ?, ?);
        """
        async with self.pool.execute(insert_query, (player, str(position_from), str(position_to))) as cursor:
            await self.pool.commit()  # Commit the transaction

    async def close(self):
        if self.pool:
            await self.pool.close()
