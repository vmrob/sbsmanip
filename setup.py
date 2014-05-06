try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'SEGarbageCollect is a set of utilities designed to help '
                   'clean a Space Engineers savefile for performance reasons',
    'author': 'Victor Robertson',
    'url': 'https://github.com/vmrob/SEGarbageCollect',
    'download_url': 'https://github.com/vmrob/SEGarbageCollect/tarball/master',
    'author_email': 'victor.robertson.iv@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['SEGarbageCollect'],
    'scripts': [
        'bin/count_objects.py',
        'bin/plot_sector.py',
        'bin/remove_debris.py',
        'bin/remove_objects.py',
        'bin/remove_ship.py',
        'bin/scale_world.py'
    ],
    'name': 'SEGarbageCollect'
}

setup(**config)
