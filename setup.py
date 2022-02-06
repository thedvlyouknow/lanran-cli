from setuptools import setup

setup(
    name='lancer-randomizer',
    version='0.0.1',
    author = 'thedvlyouknow',
    author_email = 'thedvlyouknow@protonmail.com',
    license = 'MIT license',
    description = 'A command line tool to generate random groups of lancer componants for scavenger style play',
    url = '<github url where the tool code will remain>',
    py_modules=['lanran'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        lanran=lanran:cli
    ''',
)