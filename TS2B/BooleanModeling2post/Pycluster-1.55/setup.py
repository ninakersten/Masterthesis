#!/usr/bin/env python

from distutils.core import setup, Extension, Command
import sys
import os.path
import shutil
import sys

shutil.copyfile(os.path.join('python','MANIFEST.python'),'MANIFEST')

extra_link_args = []
if sys.platform != 'darwin':
    extra_link_args = ['-s']


extension = Extension("Pycluster._cluster",
                      ["src/cluster.c", "python/clustermodule.c"],
                      include_dirs=['src'],
                      extra_link_args=extra_link_args
                      )

class test_Pycluster(Command):
    "Run all of the tests for the package."

    user_options = []

    def initialize_options(self):
        shutil.copyfile(os.path.join('python','test','test_Cluster.py'),
                        'test_Cluster.py')

    def finalize_options(self):
        pass

    def run(self):
        import unittest
        import test_Cluster
        test_Cluster.TestCluster.module = 'Pycluster'
        suite = unittest.TestLoader().loadTestsFromModule(test_Cluster)
        runner = unittest.TextTestRunner(sys.stdout, verbosity = 2)
        runner.run(suite)


setup(name="Pycluster",
      version="1.55",
      description="The C Clustering Library",
      author="Michiel de Hoon",
      author_email="michiel.dehoon 'AT' riken.jp",
      url="http://bonsai.hgc.jp/~mdehoon/software/software.html",
      license="Python License",
      package_dir = {'Pycluster':'python'},
      packages = ['Pycluster'],
      ext_modules=[extension],
      cmdclass={"test" : test_Pycluster},
      )
