from distutils.core import setup, Command

import os
import re


class BuildManual(Command):
    description = "Manual build command"    
    user_options = [
        ('rsb-inventory-dir=',None,'Directory for RSB objects.inv file'),
        ('rsbag-inventory-dir=',None,'Directory for RSBAG objects.inv file'),
        ('rst-inventory-dir=',None,'Directory for RST objects.inv file')
        ]

    def initialize_options(self):
        self.rsb_inventory_dir = None
        self.rsbag_inventory_dir = None
        self.rst_inventory_dir = None

    def _finalize_option(self,name,value):
        if value is not None:
            self.modules += name + ':'
            os.environ[name] = value
    
    def finalize_options(self):
        self.modules=''
        
        self._finalize_option('rsb',self.rsb_inventory_dir)
        self._finalize_option('rsbag',self.rsbag_inventory_dir)
        self._finalize_option('rst',self.rst_inventory_dir)
        os.environ['sphinx_external_modules']  = self.modules
        
    def run(self):
        os.system("sphinx-build -b html manual manual/build")
    


setup(
    name='oncilla-sim-project-wizard',
    version='0.1dev',
    packages=['oncilla_sim'],
    license='Lesser General Public License version 3',
    long_description=open('README.rst').read(),
    scripts = ['oncilla-sim-wizard'],
    cmdclass = {
        'build_manual' : BuildManual
        }
)

