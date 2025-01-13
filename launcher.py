import asyncio
import sys

from leetcode_async_parser_problems import get_result_data
from creation_python_files import create_python_files


async def main():
    await get_result_data()
    create_python_files()


if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
