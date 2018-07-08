import os
import glob
import setuptools

path = os.path.join(os.path.dirname(__file__), 'src/boggart/version.py')
with open(path, 'r') as f:
    exec(f.read())

setuptools.setup(
    name='boggart',
    version=__version__,
    description='Lightweight, extensible, language-independent mutation testing.',
    long_description='TBA',
    author='Chris Timperley',
    author_email='christimperley@gmail.com',
    url='https://github.com/squaresLab/Hulk',
    license='mit',
    python_requires='>=3.5',
    install_requires=[
        'bugzoo>=2.1.14',
        'rooibos>=0.3.0',
        'attrs>=17.2.0',
        'pyyaml',
        'requests>=2.0.0',
        'flask>=0.10',
        'Flask-API'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    include_package_data=True,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        '': ['*.yml']
    },
    py_modules=[
        splitext(basename(path))[0] for path in glob.glob('src/*.py')
    ],
    entry_points = {
        'console_scripts': [ 'boggartd = boggart.server:main' ]
    },
    test_suite = 'tests'
)
