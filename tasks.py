from os import path
from glob import glob

from invoke import Collection, task
import default


ns = Collection()

# Add default tasks to root collection.
for k, v in default.__dict__.items():
    if not k.startswith('_') and hasattr(v, 'times_called'):
        ns.add_task(v)

# Add other modules in this dir as sub-collections.
for f in glob(f'{path.dirname(__file__)}/*.py'):
    mod = f.split('/')[-1][:-3]
    if mod not in ('tasks', 'default'):
        exec(f'import {mod}')
        ns.add_collection(eval(mod))
