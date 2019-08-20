import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='sisa',  
     version='0.105',
     license='MIT',
     scripts=['sisa_cli'],
     author="Andres Vazquez",
     author_email="andres@data99.com.ar",
     description="SISA APIs tools",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/cluster311/sisa",
     packages=setuptools.find_packages(),
     classifiers=[
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
         'Intended Audience :: Developers', 
     ],
 )
