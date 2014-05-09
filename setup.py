try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'sbsmanip is a set of utilities designed to help '
                   'clean a Space Engineers savefile for performance reasons',
    'author': 'Victor Robertson',
    'license': 'MIT License',
    'url': 'https://github.com/vmrob/sbsmanip',
    'download_url': 'https://github.com/vmrob/sbsmanip/tarball/master',
    'author_email': 'victor.robertson.iv@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['sbsmanip', 'segc'],
    'scripts': [
        'bin/segc.py'
    ],
    'name': 'sbsmanip'
}

setup(**config)
