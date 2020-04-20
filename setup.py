import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='sisa',
     version='0.918',
     license='MIT',
     entry_points={
        'console_scripts': [
            'sisa_puco=sisa.puco_cli:main'
            ],
        },
     author="Andres Vazquez",
     author_email="andres@data99.com.ar",
     description="SISA APIs tools",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/cluster311/sisa",
     install_requires=[
        'requests>2',
        'oss_ar>=0.130'
     ],
     # package_dir={'': 'src'},
     packages=setuptools.find_packages(),
     classifiers=[
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
         'Intended Audience :: Developers', 
     ],
     python_requires='>=3.6',
 )
