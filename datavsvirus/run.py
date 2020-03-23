# run in ipython using "%run run.py"

from IPython import get_ipython
import os 

script_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))

ipython = get_ipython()
print(ipython)
# stuff like subprocess, call requires locations of the python binary,
# and bash may not be available on Windows. Thus, we run by ipython magic.
# (which isn't great either, because it doesn't use fresh python instances, but well...)

os.chdir(os.path.join(script_dir, 'load'))
for country in [f for f in os.listdir('./') if f.startswith('load_')]:
    print(f"Loading, running {country}")
    ipython.magic(f'run {country}')

os.chdir(os.path.join(script_dir, 'convert'))
for country in [f for f in os.listdir('./') if f.startswith('convert_')]:
    print(f"Converting, running {country}")
    ipython.magic(f'run {country}')

os.chdir(script_dir)
ipython.magic(f'run fuse.py')
