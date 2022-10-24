from setuptools import setup

setup(
    name='TORC',
    version='0.1.0',
    description='The TORC dna circuit design and analysis tool',
    url='https://github.com/faulknerrainford/TORC',
    author='Penn Faulkner Rainford',
    author_email='penn.rainford@york.ac.uk',
    license='GLP v3',
    packages=['TORC'],
    install_requires=['numpy',
                      'sphinx',
                      'matplotlib',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
    ],
)