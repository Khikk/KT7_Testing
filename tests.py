import pytest
import aiohttp
import aiopg
import asyncio

@pytest.mark.asyncio
async def test_resolve():
    async def my_func():
        return 52
    
    result = await my_func()
    assert result == 52

@pytest.mark.asyncio
async def test_reject():
    async def my_func():
        raise ValueError("Error")
    
    with pytest.raises(ValueError):
        await my_func()

@pytest.mark.asyncio
async def test_api_call():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jsonplaceholder.typicode.com/todos/1') as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data['userId'] == 1
            assert data['id'] == 1
            assert data['title'] == "delectus aut autem"
            assert data['completed'] == False

@pytest.mark.asyncio
async def test_db_insert():
    async with aiopg.create_pool('dbname=test user=postgres password=postgres host=localhost') as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(255))")
                await cur.execute("INSERT INTO test_table (name) VALUES ('test')")
                await cur.execute("SELECT * FROM test_table")
                result = await cur.fetchone()
                assert result[1] == 'test'

@pytest.mark.asyncio
async def test_run_in_thread():
    async def my_func():
        return 52
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, my_func)
    assert result == 52
