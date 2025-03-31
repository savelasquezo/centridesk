import json
import traceback

import requests

from shared.infrastructure.get_config import GetConfig


def get_traceback():
    t = traceback.format_exc()
    return t if t.strip() != 'NoneType: None' else None


def create_jira(summary, exception):
    config = GetConfig()
    settings = config.get('settings')

    description = exception
    trace = get_traceback()
    if trace:
        description += '\n{code:Shell}' + trace + '{code}'

    if settings.env in ['local', 'dev', 'docker']:
        print(f"\n\033[0;31mSummary: {summary}\nDescription:\n{description}\n\033[0m")

    else:
        url = "https://wf4dn4vxmd.execute-api.eu-central-1.amazonaws.com/prod/create"

        payload = {
            "project": "CENTRIMAN",
            "issuetype": "Bug",
            "summary": f"[{settings.env.upper()}][{settings.project.capitalize()}] {summary}",
            "description": description,
            "labels": [
                "mantenimiento"
            ]
        }

        x_api_key = "4QBycc2jvM0X4LGcLZlf14xDtRYbwbO1Trc5y4Yi"
        headers = {
            'x-api-key': x_api_key,
            'Content-Type': "application/json"
        }

        requests.request("POST", url, data=json.dumps(payload), headers=headers)
