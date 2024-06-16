from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='game',
    version='1.0.0',
    author='Kacper Kawecki',
    description='a platformer game with a level creator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Kaweciak/ProjektJS',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['Levels/*.json', 'Levels/*.png'],
    },
    install_requires=[
        'pygame',
        'pygame_gui',
    ],
    entry_points={
        'console_scripts': [
            'game=main_menu:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
