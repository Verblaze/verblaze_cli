from setuptools import setup, find_packages

setup(
    name='verblaze',
    version='0.0.4',
    author="3K",
    author_email="support@verblaze.com",
    packages=find_packages(),
    install_requires=[
        "click",
        "termcolor",
    ],
    description='Auto-Localization Generation Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Verblaze/verblaze_cli',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'verblaze=verblaze.cli:main',
        ],
    },
)