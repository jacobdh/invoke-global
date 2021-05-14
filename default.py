from invoke import task


@task
def port_ps(c, port):
    c.run(f'lsof -nP -iTCP:{port}')

@task
def port_kill(c, port):
    c.run(f"kill -9 $(sudo lsof -i tcp:${port} | awk 'FNR == 2 {{print $2}}')")
