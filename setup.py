from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='poshmarkfilter',
    version='0.0.2',
    description='Use AI to create custom filters on Poshmark',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/samuel-poon/poshmarkfilter-py',
    python_requires='>=3.11',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'openai'
    ],
    packages=['poshmarkfilter']
)