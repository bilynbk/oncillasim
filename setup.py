from distutils.core import setup, Command
from distutils.filelist import findall

import os,re,errno



class BuildManual(Command):
    description = "Manual build command"    
    user_options = [
        ('rsb-inventory-dir=',None,'Directory for RSB objects.inv file'),
        ('rsbag-inventory-dir=',None,'Directory for RSBAG objects.inv file'),
        ('rst-inventory-dir=',None,'Directory for RST objects.inv file'),
        ('cca-inventory-dir=',None,'Directory for CCA objects.inv file'),
        ('liboncilla-inventory-dir=',None,'Directory for liboncilla objects.inv file'),
        ('ccaoncilla-inventory-dir=',None,'Directory for CCA-oncilla objects.inv file')
        ]

    def initialize_options(self):
        self.rsb_inventory_dir = None
        self.rsbag_inventory_dir = None
        self.rst_inventory_dir = None
        self.cca_inventory_dir = None
        self.liboncilla_inventory_dir = None
        self.ccaoncilla_inventory_dir = None

    def _finalize_option(self,name,value):
        if value is not None:
            self.modules += name + ':'
            os.environ[name] = value
    
    def finalize_options(self):
        self.modules=''
        
        self._finalize_option('rsb',self.rsb_inventory_dir)
        self._finalize_option('rsbag',self.rsbag_inventory_dir)
        self._finalize_option('rst',self.rst_inventory_dir)
        self._finalize_option('cca',self.cca_inventory_dir)
        self._finalize_option('liboncilla',self.liboncilla_inventory_dir)
        self._finalize_option('ccaoncilla',self.ccaoncilla_inventory_dir)
        os.environ['sphinx_external_modules']  = self.modules
        
    def run(self):
        os.system("sphinx-build -b html manual build/manual")
    

try:
    os.makedirs('build/manual')
except OSError, e:
    if e.errno != errno.EEXIST:
        raise

setup(
    name='oncilla-sim-project-wizard',
    version='0.1.0rc4',
    packages=['oncilla_sim'],
    license='Lesser General Public License version 3',
    long_description=open('README.rst').read(),
    scripts = ['oncilla-sim-wizard'],
    cmdclass = {
        'build_manual' : BuildManual
        },
    data_files=[('share/doc/oncilla-sim/manual',findall('build/manual/')),
                ('share/oncilla-sim',['wizard.cfg'])]
)

