from setuptools import setup, find_packages


with open('README.md','r',encoding="utf8") as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

# windows_req = requirements.append()
      
setup(
        name ='debuggy',
        version ='1.2.1',
        author ='Eje Daniel',
        author_email ='ejedenials@gmail.com',
        url ='https://github.com/derhnyel/deBuggy',
        description ='Stalk StackOverflow.',
        license =license,
        py_modules=['debuggy','stalkoverflow'],
        packages=find_packages(exclude=('tests', 'docs','bin','assets','.circleci')),
        long_description_content_type ="text/markdown",
        long_description = readme,
        entry_points ={
            'console_scripts': [
                'debuggy = stalkoverflow.__main__:main'
            ]
        },
        classifiers =[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        keywords ='debuggy python package stalkoverflow',
        install_requires = requirements,
        zip_safe = False,
        package_data={
        '': ['*.*'],
        'requirements': ['*.*'],
        },
        include_package_data=True,
        extras_require = {
        'win': 'windows-curses\n'
        },
        )