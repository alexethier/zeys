import os
from setuptools import setup

found_packages = []
found_package_dirs = {}
project_name = "zeys"
for root, dirs, files in os.walk("." + os.path.sep + project_name, topdown=True, followlinks=False):
  for name in files:
    if(name=="__init__.py"):
      package_key = root[2:]
      #print("Found package: " + package_key)
      found_packages.append(package_key)
      found_package_dirs[package_key] = "." + os.path.sep + package_key

#print(found_packages)
#print(found_package_dirs)

setup(
  name=project_name,
  version='0.0.1',
  description='Simple Python Prompt',
  url='https://github.com/alexethier/zeys',
  author='Alex Ethier',
  author_email='aethier@gmail.com',
  license='MIT',
  packages=found_packages,
  package_dir=found_package_dirs,
  install_requires=[""],
  classifiers=[
      'Development Status :: 1 - Planning',
      'License :: OSI Approved :: BSD License',  
      'Operating System :: POSIX :: Linux',        
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
  ],
  entry_points={
      'console_scripts': [
          'zeys=zeys.run.runner:main',
      ],
  },
)
