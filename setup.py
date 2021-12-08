from setuptools import setup, find_packages


# with open('README.rst') as f:
#     readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

  

# setup(
#     name='debuggy',
#     version='0.1.0',
#     description='   ####',
#     long_description=readme,
#     author='Eje Daniel',
#     author_email='ejedenials@gmail.com',
#     url='https://github.com/derhnyel/deBuggy',
#     license=license,
#     packages=find_packages(exclude=('tests', 'docs'))
# )

with open('requirements.txt') as f:
    requirements = f.readlines()  
  
long_description = 'A project for Automatically searching Google and displaying results in your terminal when a compiler error is gotten.\n Made by @Derhnyel'
  
setup(
        name ='debuggy',
        version ='0.0.0',
        author ='Eje Daniel',
        author_email ='ejedenials@gmail.com',
        url ='https://github.com/derhnyel/deBuggy',
        description ='StalkOverflow.',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        py_modules=['debuggy','stalkoverflow'],
        packages = find_packages(),
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