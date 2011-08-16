from setuptools import setup

setup(
    name='python-zohodocs',
    version='0.0.1',
    description='',
    author='Matt Robenolt',
    author_email='matt@ydekproductions.com',
    packages=[
        'zohodocs',
    ],
    package_dir={
        'zohodocs': 'zohodocs',
    },
    license='MIT',
    url='https://github.com/mattrobenolt/python-zohofiles',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires='pycurl',
)
