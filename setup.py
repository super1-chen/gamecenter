#!/usr/bin/python
import setuptools

from gamecenter import version
from gamecenter.contrib import setup


setuptools.setup(
    name='gamecenter',
    version=version.__version__,
    description='',
    author='tccc123',
    author_email='tccc123@163.com',
    packages=setuptools.find_packages(exclude=['bin']),
    include_package_data=True,
    cmdclass=setup.get_cmdclass(),
    install_requires=setup.parse_requirements(),
    dependency_links=setup.parse_dependency_links(),
    classifiers=[
        'Development Status :: 1 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Environment :: No Input/Output (Daemon)',
    ],
    entry_points={
        'console_scripts': [
            'game-api = gamecenter.cmd.api:main',
            'game-manage = gamecenter.cmd.manage:main',
            'game-worker = gamecenter.cmd.worker:main',
        ]
    },
    py_modules=[],
)
