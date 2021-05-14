from invoke import task
import json


JSON_ENV = {'AWS_DEFAULT_OUTPUT': 'json', 'AWS_PAGER': ''}
YAML_ENV = {'AWS_DEFAULT_OUTPUT': 'yaml', 'AWS_PAGER': ''}


def _confirm(msg='Are you sure?'):
    if input(f'\n{msg} (y/n) ') != 'y':
        print('Aborting...')
        exit(0)


def _get(c, name, decrypt=False, profile=None):
    r = c.run(
        f'aws ssm get-parameter --name "{name}" '
        f'{"--with-decryption" if decrypt else ""} '
        f'{f"--profile {profile}" if profile else ""}',
        env=JSON_ENV, hide=True)
    if not r.ok:
        raise RuntimeError(r.stderr)

    return json.loads(r.stdout)['Parameter']


@task
def get(c, name, decrypt=False, profile=None):
    p = _get(c, name, decrypt=decrypt, profile=profile)
    print(f'{p["Name"]} ({p["Type"]}) = {p["Value"]}')


def _get_by_path(c, path, decrypt=False, profile=None):
    r = c.run(
        f'aws ssm get-parameters-by-path --path "{path}" --recursive '
        f'{"--with-decryption" if decrypt else ""} '
        f'{f"--profile {profile}" if profile else ""}',
        env=JSON_ENV, hide=True)
    if not r.ok:
        raise RuntimeError(r.stderr)

    return json.loads(r.stdout)['Parameters']


@task
def get_all(c, path, values=False, decrypt=False, profile=None):
    params = _get_by_path(c, path, decrypt=decrypt, profile=profile)
    if not params:
        print('No params found')
        exit(0)
    for p in params:
        print(f'{p["Name"]} ({p["Type"]})' +
              (f' = {p["Value"]}' if values or decrypt else ''))


@task
def copy(c, src, dest, overwrite=False, src_profile=None, dest_profile=None):
    param = _get(c, src, decrypt=True, profile=src_profile)
    dest_profile = dest_profile or src_profile or None
    src_prefix = f'{src_profile}:' if src_profile else ''
    dest_prefix = f'{dest_profile}:' if dest_profile else ''
    print(f"Will copy: {src_prefix}{param['Name']} -> "
          f"{dest_prefix}{dest} ({param['Type']})")
    print(f'Overwrite existing value: {overwrite}')

    _confirm()

    print(f'\nput-parameter: {dest}')
    c.run(f'aws ssm put-parameter --name "{dest}" '
          f'--type "{param["Type"]}" --value "{param["Value"]}" '
          f'{"--overwrite" if overwrite else "--no-overwrite"} '
          f'{f"--profile {dest_profile}" if dest_profile else ""}',
          env=YAML_ENV)


@task
def copy_all(c, path, search, replace, overwrite=False,
             src_profile=None, dest_profile=None):
    params = _get_by_path(c, path, decrypt=True, profile=src_profile)
    dest_profile = dest_profile or src_profile or None
    src_prefix = f'{src_profile}:' if src_profile else ''
    dest_prefix = f'{dest_profile}:' if dest_profile else ''
    new_params = []

    print(f'Search and replace: "{search}" -> "{replace}"')
    print(f'Overwrite existing values: {overwrite}')

    for p in params:
        new = {'Name': p['Name'].replace(search, replace),
               'Type': p['Type'], 'Value': p['Value']}
        new_params.append(new)
        print(f"Will copy: {src_prefix}{p['Name']} -> "
              f"{dest_prefix}{new['Name']} ({new['Type']})")

    _confirm()

    for n in new_params:
        print(f'\nput-parameter: {n["Name"]}')
        c.run(f'aws ssm put-parameter --name "{n["Name"]}" '
              f'--type "{n["Type"]}" --value "{n["Value"]}" '
              f'{"--overwrite" if overwrite else "--no-overwrite"} '
              f'{f"--profile {dest_profile}" if dest_profile else ""}',
              env=YAML_ENV)


@task
def delete_all(c, path):
    params = _get_by_path(c, path)
    delete_names = []

    for p in params:
        delete_names.append(p['Name'])
        print(f"Will delete: {p['Name']} ({p['Type']})")

    _confirm()

    for name in delete_names:
        print(f'delete-parameter: {name}')
        c.run(f'aws ssm delete-parameter --name "{name}"', env=YAML_ENV)
