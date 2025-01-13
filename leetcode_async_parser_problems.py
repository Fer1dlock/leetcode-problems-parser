import asyncio
import os

import aiofiles
import aiohttp
import json

from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from config import headers, cookies


async def fetch_problem_data(session, problem, semaphore):
    async with semaphore:
        retry = 0
        url = f'https://leetcode.com/problems/{problem["titleSlug"]}/description/'
        print('Scraping...', problem['frontendQuestionId'], url)
        while True:
            try:
                headers['user-agent'] = UserAgent().random
                response = await session.get(url, cookies=cookies, headers=headers)

                if response.status_code == 403:
                    print(f'[ERROR] 403 Forbidden for {problem["frontendQuestionId"]} {url}. Retrying...')
                    retry += 1

                    if retry <= 3:
                        await asyncio.sleep(2)
                    else:
                        await asyncio.sleep(35)

                    continue

                text = response.text
                soup = BeautifulSoup(text, 'lxml')

                try:
                    leetcode_question = json.loads(soup.find('script', id='__NEXT_DATA__').text)['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['question']
                except:
                    print(f'[ERROR] Failed to parse problem data for {problem["frontendQuestionId"]} {url}. Retrying in 35 seconds...')
                    await asyncio.sleep(35)
                    continue

                if leetcode_question['canSeeQuestion'] is False:
                    print('[ERROR] Premium task')
                    title = leetcode_question['title']
                    title_slug = leetcode_question['titleSlug']
                    premium = True
                    testcases = None
                    code = None
                    data_schemas = []
                else:
                    title = leetcode_question['title']
                    title_slug = leetcode_question['titleSlug']
                    testcases = leetcode_question['exampleTestcaseList']
                    premium = False
                    if leetcode_question['dataSchemas']:
                        data_schemas = leetcode_question['dataSchemas']
                    else:
                        data_schemas = []
                    try:
                        code = leetcode_question['codeSnippets'][3]['code']
                    except:
                        print('[ERROR] Task without Python code')
                        code = None

                result = {
                    'id': problem['frontendQuestionId'],
                    'title': title,
                    'title_slug': title_slug,
                    'premium': premium,
                    'status': problem['status'],
                    'testcases': testcases,
                    'code': code,
                    'dataSchemas': data_schemas
                }
                print(f'{problem["frontendQuestionId"]} Problem added to result list')
                print(f"[RESULT]{json.dumps(result)}")
                return result
            except:
                print(f"[ERROR] Network error for {problem['frontendQuestionId']} {url}. Retrying in 30 seconds...")
                await asyncio.sleep(35)
                continue


async def get_problems_data(problems: list[dict]):
    semaphore = asyncio.Semaphore(100)
    async with AsyncSession() as session:
        tasks = [fetch_problem_data(session, problem, semaphore) for problem in problems]
        results = await asyncio.gather(*tasks)

    if not os.path.exists('data'):
        os.mkdir('data')
    try:
        async with aiofiles.open('data/result_list.json', 'r', encoding='utf-8') as file:
            src = json.loads(await file.read())
    except FileNotFoundError:
        print("File result_list.json not found. Creating new...")
        src = []
    except json.JSONDecodeError:
        print("File result_list.json is corrupted. Creating new...")
        src = []

    src.extend(results)

    async with aiofiles.open('data/result_list.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(sorted(src, key=lambda problem: int(problem['id'])), indent=4, ensure_ascii=False))


async def get_result_data():
    offset = 0
    problems = []
    async with aiohttp.ClientSession() as session:
        while True:
            print(f'[+] Processed {offset} questions\n-------------------------------')

            json_data = {
                'query': '\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    ',
                'variables': {
                    'categorySlug': 'all-code-essentials',
                    'skip': offset,
                    'limit': 100,
                    'filters': {},
                },
                'operationName': 'problemsetQuestionList',
            }

            async with session.post('https://leetcode.com/graphql/', json=json_data) as response:

                data = await response.json()

                if data['data']['problemsetQuestionList']['questions']:
                    problems.extend(data['data']['problemsetQuestionList']['questions'])
                else:
                    print(f'[INFO] Surface treatment of problems is complete.')
                    break

                offset += 100

    await get_problems_data(problems)
