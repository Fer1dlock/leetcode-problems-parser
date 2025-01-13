import json
import os
import re


def extract_function_name(code: str) -> str:
    match = re.search(r"def\s+(\w+)\(", code)
    if match:
        return match.group(1)


def extract_function_args(code: str) -> list[str]:
    match = re.search(r'def\s+\w+\((.*?)\)', code)
    if match:
        args = [arg.strip().split(':')[0].strip() for arg in match.group(1).split(',')]
        return args


def create_python_files():
    with open('data/result_list.json', 'r', encoding='utf-8') as file:
        problems = json.load(file)

    for problem in problems:
        code = problem['code']

        reasons = {
            'ListNode': '# Reason: ListNode is present in the code.',
            'TreeNode': '# Reason: TreeNode is present in the code.',
            'Node': '# Reason: Node is present in the code.',
            'API': '# Reason: API is present in the code.'
        }

        if (problem['premium'] is True) or (problem['code'] is None):
            continue

        if not os.path.exists('problems'):
            os.mkdir('problems')
        with open(f'problems/{problem["id"]}. {problem["title"].replace("?", "").replace("/", "")}.py', 'w', encoding='utf-8') as file:

            if any((key in code for key in reasons)):
                file.write('#  This task is not supported in IDE.\n')
                for key, value in reasons.items():
                    if key in code:
                        file.write(value + '\n')
                        break
                file.write(f'#  Link to Leetcode: https://leetcode.com/problems/{problem["title_slug"]}/description/\n\n')
                continue

            file.write(f'#  Link to Leetcode: https://leetcode.com/problems/{problem["title_slug"]}/description/\n\n')

            if '__init__' in problem['code']:
                file.write(problem['code'])
            else:
                if 'List' in problem['code']:
                    file.write('from typing import List\n\n\n')

                code_lines = problem['code'].split('\n')
                modified_code_lines = []

                if code_lines[-1] == '        ':
                    code_lines.pop()
                    code_lines.append('    ')

                if code_lines[-1] != '    ':
                    code_lines.append('    ')

                for i, line in enumerate(code_lines):
                    if line.startswith('class Solution:'):
                        continue
                    elif '"""' in line:
                        line = line[4:]
                    elif 'self, ' in line:
                        line = line.replace('self, ', '')
                        if not len(modified_code_lines) > i + 1 and code_lines[i - 1].startswith('class'):
                            line = line[4:]
                    elif 'import pandas as pd' in line:
                        line += '\n'
                    modified_code_lines.append(line)

                file.write('\n'.join(modified_code_lines))
                file.write('pass\n\n')
            file.write('\ndef main():\n')

            function_name = extract_function_name(problem['code'])

            if '__init__' in problem['code']:
                file.write('    pass')

            elif 'import pandas as pd' in problem['code']:
                for data_schema in problem['dataSchemas']:
                    data_schema_lines = data_schema.split('\n')
                    for line in data_schema_lines:
                        if function_name in line:
                            line = line.replace(function_name, function_name.upper())
                        file.write(f"    {line}\n")

                if len(extract_function_args(problem['code'])) > 1:
                    function_args = ', '.join(extract_function_args(problem['code']))
                else:
                    function_args = ''.join(extract_function_args(problem['code']))

                if function_name in function_args:
                    function_args = function_args.replace(function_name, function_name.upper())

                file.write(f"    print({function_name}({function_args}))\n")
            else:
                for testcase in problem['testcases']:
                    input_args = [f"{arg}".replace(',', ', ') for arg in testcase.split("\n")]

                    file.write(f"    print({function_name}({', '.join(input_args)}))\n")

            file.write("\n\nif __name__ == '__main__':\n    main()\n")
        print(f'File {problem["id"]}. {problem["title"]}.py successfully created.')
