# setup.py
from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read README for long description
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='healthcare-ops-agent',
    version='0.1.0',
    description='Healthcare Operations Management Agent using LangGraph',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/healthcare-ops-agent',
    packages=find_packages(exclude=['tests*']),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
    include_package_data=True,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.23.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.1.0',
        ],
        'docs': [
            'mkdocs>=1.5.0',
            'mkdocs-material>=9.5.0',
        ],
    }
)
