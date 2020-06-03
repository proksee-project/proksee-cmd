from setuptools import find_packages, setup

dependencies = ['click']


setup(
    name='proksee',
    version="0.1",
    url='https://github.com/proksee-project/proksee-cmd.git',
    license='Apache License, Version 2.0',
    description='Proksee Cmd Line Tools',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
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