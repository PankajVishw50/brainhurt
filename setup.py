from setuptools import setup, find_packages

with open('./README.md', 'r') as readme:
    long_description = readme.read()


setup(
    name='brainhurt',

    author='Pankaj Vishwakarma',
    author_email='vishw.dev.1000@gmail.com',
    
    version='0.1.0',
    description='This is an Interpreter and debugger for the programming language `BrainFuck` written in `Python`',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/PankajVishw50/brainhurt',

    package_dir={'': 'src'},
    packages=find_packages(where='src'),

    install_requires=[],

    keywords='pankaj, pankaj vishw, brainfuck, brainhurt, brainfuck compiler, brainfuck interpreter, brainfuck debugger, debugger, interpretter, compiler',
    python_requires='>=3.7',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Natural Language :: English',
        
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',

        'Operating System :: OS Independent',    

        'License :: OSI Approved :: MIT License',

        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Compilers',
    ],

)
