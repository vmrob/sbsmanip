try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description='sbsmanip is a set of utilities designed to help '
                'clean a Space Engineers savefile for performance reasons',
    author='Victor Robertson',
    license='MIT License',
    url='https://github.com/vmrob/sbsmanip',
    author_email='victor.robertson.iv@gmail.com',
    version='0.3.0',
    install_requires=['nose'],
    packages=['segc', 'sbsmanip'],
    entry_points={
        'console_scripts': [
            'segc = segc.app:main'
        ]
    },
    name='sbsmanip'
)
