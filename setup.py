from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='tele2task_executor',
    packages=['tele2task_executor'],
    version='1.0.1',
    license='MIT',
    description='Python tele2 task executor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ilichev Andrey',
    author_email='ilichev.andrey.y@gmail.com',
    url='https://github.com/ilichev-andrey/tele2task_executor.git',
    keywords=['tele2'],
    install_requires=[
        'ddt',
        'tele2client'
        'aiohttp',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9'
    ],
)
