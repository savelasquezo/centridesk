import csv
import json
import re
from argparse import ArgumentParser
from os import path as os_path
from sys import path as sys_path

from urllib3 import PoolManager

sys_path.append(f"{os_path.dirname(os_path.abspath(__file__))}/..")

from shared.infrastructure.get_config import GetConfig


def make_request(http, token, url, method, data=None):
    header = {
        'Content-Type': 'application/json',
        'Authentication': f'Bearer {token}'
    }

    body = json.dumps(data).encode('utf-8') if data else None

    response = http.request(method, url, body=body, headers=header)

    if response.status != 200:
        raise Exception(f"Error in Centribot Request: \nURL: {url} \nMethod: {method} \nData: {data}"
                        f"\nStatus: {response.status} \nError: {response.data}")

    return json.loads(response.data.decode('utf-8'))


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="File location")
    parser.add_argument("-a", "--account_id", required=True, help="Account Id")
    parser.add_argument("-ag", "--agent_id", required=True, help="Agent Id")
    parser.add_argument("-t", "--token", required=True, help="Static access token")
    args = parser.parse_args()

    http = PoolManager()
    config = GetConfig().get('platform.centridesk')

    file = args.file
    account_id = args.account_id
    agent_id = args.agent_id
    token = args.token

    try:
        with open(file, encoding='utf-8') as csvf:

            csvReader = csv.DictReader(csvf, delimiter=';')
            line = 1

            for row in csvReader:
                try:
                    customer_data = json.dumps(row)
                    data = {
                        'name': f"{row['first_name']} {row['last_name']}".strip(),
                        'phone': f"+34{row['phone'].strip()}",
                        'company': row['company'].strip(),
                        'agent_id': agent_id
                    }

                    # Basic checks
                    error_reason = ''
                    if not data['name']:
                        error_reason = f'No first name and last name given at row {line}'
                    if not re.search("^\\+34\\d{9}$", data['phone']):
                        error_reason = f'No phone given or it is invalid at row {line}'

                    if error_reason:
                        print(error_reason)
                    else:
                        response = make_request(http, token, f'{config.url}/api/v1/accounts/{account_id}/customers',
                                                'POST', data)
                        print(response)

                        if response.status != 200:
                            print(f'Something went wrong with line´s {line} registry in server')

                except Exception as ex:
                    print(f'Something went wrong with line´s {line} registry in server')

                line = line + 1

    except Exception as ex:
        print('ERROR:', ex)
