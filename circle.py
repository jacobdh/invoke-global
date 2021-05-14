from invoke import task
import json
from os import environ


def _confirm(msg='Are you sure?'):
    if input(f'\n{msg} (y/n) ') != 'y':
        print('Aborting...')
        exit(0)


def _trigger(c, project, branch, params={}):
    url = f'https://circleci.com/api/v2/project/gh/{project}/pipeline'
    body = json.dumps({
        'branch': branch,
        'parameters': params
    })

    circle_token = environ.get('CIRCLE_TOKEN') or input('CIRCLE_TOKEN: ')
    if not circle_token:
        print('CIRCLE_TOKEN required')
        exit(1)

    print(f'Project: {project}')
    print(f'URL: {url}')
    print(f'Body: {body}')
    _confirm()

    c.run(f'curl -s -X POST '
          f'-H "circle-token: {circle_token}" '
          f'-H "Content-Type: application/json" '
          f'-d {json.dumps(body)} '
          f'{url}')
    print('---')
    print(f'See it here: https://app.circleci.com/pipelines/github/'
          f'{project}?branch={branch}')


@task
def monolith(c, branch, deploy_env=''):
    project = 'enderlabs/eventboard.io'
    params = {'deploy-env': deploy_env}
    _trigger(c, project, branch, params)


@task
def resdal(c, branch, deploy_env=''):
    project = 'enderlabs/reservations'
    params = {'deploy-env': deploy_env}
    _trigger(c, project, branch, params)
