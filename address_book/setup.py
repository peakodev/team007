from setuptools import setup, find_namespace_packages

setup(
    name='address_book',
    version='0.0.1',
    entry_points={
        'console_scripts': []
    },
    description='Address book',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/peakodev/team007/tree/main/address_book',
    author='Team007',
    author_email='peakodev@gmail.com',
    packages=find_namespace_packages(),
    install_requires=[],
)