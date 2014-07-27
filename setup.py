import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
from mymodule.version import get_version

long_description="""
mymodule {} is totally awesome.

{}
""".format(get_version('short'), open('README.md', 'r').read())

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]
    def initialize_options(self):
        super().initialize_options()
        self.pytest_args = None
    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='mymodule',
    version=get_version('short'),
    description='Write a short description of your module',
    long_description=long_description,
    author='Your Name',
    author_email='you@example.com',
    packages=find_packages(),
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': ['mymodule_cli = mymodule.main:main',]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Aproved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
    ]
)
