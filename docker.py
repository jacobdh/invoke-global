from invoke import task


@task(aliases=['rm'])
def remove(c, force=False):
    c.run(f'docker rm {"-f" if force else ""} $(docker ps -aq)')

# @task
# def dcfile(c, file=None):
#     if file is not None:
#         c.run(f'export COMPOSE_FILE="{file}"', shell='zsh')
#
#     c.run('echo "COMPOSE_FILE=$COMPOSE_FILE"', shell='zsh')
