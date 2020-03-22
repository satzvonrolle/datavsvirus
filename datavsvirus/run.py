from IPython import get_ipython
import os 

script_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))

ipython = get_ipython()

# stuff like subprocess, call requires locations of the python binary,
# and bash may not be available on Windows. Thus, we run by ipython magic.
# (which isn't great either, because it doesn't use fresh python instances, but well...)

# os.chdir(os.path.join(script_dir, 'load'))
# for country in os.listdir('./'):
#     print(f"Loading, running {country}")
#     ipython.magic(f'run {country}')

os.chdir(os.path.join(script_dir, 'convert'))
for country in os.listdir('./'):
    if 'deprecated' in country:
        continue
    print(f"Converting, running {country}")
    ipython.magic(f'run {country}')

os.chdir(script_dir)
ipython.magic(f'run fuse.py')
