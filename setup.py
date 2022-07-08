from setuptools import find_packages, setup
from proksee import __version__

dependencies = ['click']


setup(
    name='proksee',
    version=__version__,
    url='https://github.com/proksee-project/proksee-cmd.git',
    license='Apache License, Version 2.0',
    description='Proksee Cmd Line Tools',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    package_data = { 'proksee' : ['config/config.json']},
    install_requires=dependencies,
    entry_points='''
        [console_scripts]
        proksee=proksee.cli:cli
    ''',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
    ]
)
