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
    download_url='https://github.com/vmrob/sbsmanip/archive/0.1.1.tar.gz',
    author_email='victor.robertson.iv@gmail.com',
    version='0.2.0',
    install_requires=['nose'],
    packages=['segc', 'sbsmanip'],
    entry_points={
        'console_scripts': [
            'segc = segc.app:main'
        ]
    },
    name='sbsmanip'
)
