from setuptools import setup, find_packages

with open('README.md') as f:
     readme = f.read()

with open('LICENSE') as f:
     license = f.read()

with open('requirements.txt') as f:
    requirements = f.readlines()  
   
setup(
        name ='debuggy',
        version ='0.1.0',
        author ='Eje Daniel',
        author_email ='ejedenials@gmail.com',
        url ='https://github.com/derhnyel/deBuggy',
        description ='Stalk StackOverflow.',
        license =license,
        py_modules=['debuggy','stalkoverflow'],
        packages=find_packages(exclude=('tests', 'docs','bin','assets')),
        entry_points ={
            'console_scripts': [
                'debuggy = stalkoverflow.__main__:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='debuggy python package stalkoverflow',
        install_requires = requirements,
        zip_safe = False)