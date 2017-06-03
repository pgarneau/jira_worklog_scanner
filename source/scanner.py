from __future__ import division

import getpass
import json
import requests

URL = "http://levitus.atlassian.net/rest/api/latest/"
member_dict = {
    'Philippe': {
        'username': 'admin',
        'tasks': [],
        'total_time': 0
    },
    'Axel_Karl': {
        'username': 'axel.bosco',
        'tasks': [],
        'total_time': 0
    },
    'Nicolas Roy': {
        'username': 'Nicolas.n.roy',
        'tasks': [],
        'total_time': 0
    },
    'Mathieu Brassard': {
        'username': 'Mathieu.brassard',
        'tasks': [],
        'total_time': 0
    },
    'Lisa Anthonioz': {
        'username': 'lisa.anthonioz',
        'tasks': [],
        'total_time': 0
    },
    'Jasmin-Lysaught-Nantel': {
        'username': 'jlysnan',
        'tasks': [],
        'total_time': 0
    },
    'Jean-Francois Bilodeau': {
        'username': 'jeanfrancoisbilodeau.jfb',
        'tasks': [],
        'total_time': 0
    },
    'David Gardner': {
        'username': 'dgardner23',
        'tasks': [],
        'total_time': 0
    },
    'Alex Bouchard': {
        'username': 'alex.bouchard',
        'tasks': [],
        'total_time': 0
    },
    'Adrien Mojika': {
        'username': 'adrien.mojika',
        'tasks': [],
        'total_time': 0
    }
}

def _get_issues():
    url = URL + "search"
    body = {
        "jql": "project = LevitUS",
        "startAt": 0,
        "maxResults": 100,
        "fields": [
            "summary",
            "status",
            "assignee"
        ],
        "fieldsByKeys": False
    }

    response = requests.post(url, data=body, auth=(username, password))
    return response.json()['issues']

def _get_issue_worklog(issue):
    url = URL + "issue/{}/worklog".format(issue['id'])

    response = requests.get(url, auth=(username, password))
    return response.json()['worklogs']

def _set_total_time():
    # Total time worked in hours
    for member in member_dict.keys():
        total = 0
        for task in member_dict[member]['tasks']:
            total += task['time_spent']

        member_dict[member]['total_time'] = total / 60

# ----- MAIN PROGRAM ----------------------------------------------------------
username = raw_input("Please enter your username: ")
password = getpass.getpass("Please enter your password: ")
#password = raw_input("Please enter your password: ")

issue_list = _get_issues()

for issue in issue_list:
    worklog = _get_issue_worklog(issue)

    for log in worklog:
        # Time spent is in minutes in this case
        task_body = {
            'issue': issue['key'],
            'worklog_id': log['id'],
            'time_spent': log['timeSpentSeconds']/60
        }

        for member in member_dict.keys():
            if member_dict[member]['username'] == log['author']['name']:
                member_dict[member]['tasks'].append(task_body)

_set_total_time()
print(json.dumps(member_dict, indent=1))
