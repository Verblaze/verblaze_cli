from setuptools import setup, find_packages

setup(
    name='verblaze',
    version='0.0.1',
    author="3K",
    author_email="support@verblaze.com",
    packages=find_packages(),
    install_requires=[
        "click",
        "termcolor",
    ],
    description='Auto-Localization Generation Tool',
    entry_points={
        'console_scripts': [
            'verblaze=verblaze.cli:main',
        ],
    },
)