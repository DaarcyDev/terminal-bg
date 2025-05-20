from setuptools import setup, find_packages

setup(
    name='terminal-bg',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygobject',
    ],
    entry_points={
        'console_scripts': [
            'terminal-bg=terminal_bg.main:main',
        ],
    },
)
