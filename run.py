import asyncio
from truck import check_log_file, check_internet_connection

async def main():
    task1 = asyncio.create_task(check_log_file())
    task2 = asyncio.create_task(check_internet_connection())
    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    asyncio.run(main())
