''' setup script '''
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ForeignTongue',
    version='0.0.1',

    description='Generates new languages',
    long_description=long_description,

    url='https://github.com/mouse-reeve/foreign-tongue',

    author='Mouse Reeve',
    author_email='mouse.reeve@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='generative language linguistics',

    packages=['foreigntongue'],
    include_package_data=True,

    install_requires=[]
)
