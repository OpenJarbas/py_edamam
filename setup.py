from distutils.core import setup
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name='py_edamam',
    version='0.2',
    packages=['py_edamam'],
    url='https://github.com/JarbasAl/py_edamam',
    license='MIT',
    author='jarbasAi',
    author_email='jarbasai@mailfence.com',
    description='edamam api'
)
