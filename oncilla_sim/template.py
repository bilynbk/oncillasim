# Oncilla Simulation Wizard
import os
import re
import sys
import string
import shutil
import filecmp
import ConfigParser

from git import *

class WebotsTemplate:
    REPO_LIST_FILE = ".oncilla-sim-wizard.list"
    REPO_MAKE_FILE = ".oncilla-sim-wizard.make"

    VERBOSE = True
    ONLINE = True
    TEMPLATE_PATH = None
    TMP_PATH = None
    SYNC_IGNORE = False
    SYNC_OVERWRITE = False
    CONFIG = None

    def __init__(self, path, verbose=True, online=True):
        self.VERBOSE = verbose
        self.ONLINE = online
        self.TEMPLATE_PATH = path

        self.CONFIG = ConfigParser.RawConfigParser()
        self.CONFIG.read(['wizard.cfg',
                     '/usr/local/share/oncilla-sim/wizard.cfg',
                     '/usr/share/oncilla-sim/wizard.cfg'])

    def isEmpty(self):
        if os.path.exists(self.TEMPLATE_PATH):
            return False
        else:
            return True
    def prepare(self):
        if self.VERBOSE:
            print 'Updating project template at', self.TEMPLATE_PATH
        if not os.path.exists(self.TEMPLATE_PATH):
            os.makedirs(self.TEMPLATE_PATH)

        # Loop through config sections and update
        for repo in self.CONFIG.sections():
            path = os.path.join(self.TEMPLATE_PATH, repo)
            remote = self.CONFIG.get(repo, 'remote')
            branch = self.CONFIG.get(repo, 'branch')

            if not os.path.exists(path):
                if self.VERBOSE:
                    print '* Cloning project template from', repo, '...'
                os.makedirs(path)
                g = Git(path)
                g.execute(['git', 'clone', remote, path])
            else:
                if self.VERBOSE:
                    print '* Updating project template from', repo, '...'
                g = Git(path)
            g.execute(['git', 'fetch', '--all'])
            g.execute(['git', 'fetch', '--tags'])
            g.checkout(branch)

    def updateSkeleton(self, target):
        if self.VERBOSE:
            print '* Creating Project Skeleton'

        for repo in self.CONFIG.sections():
            path = os.path.join(self.TEMPLATE_PATH, repo)
            self.syncRepo(repo, path, target)

    def syncRepo(self, name, src, dest):

        # Read repo list file
        repofile = os.path.join(src, self.REPO_LIST_FILE)
        if not os.path.exists(repofile):
            exit("Template syncRepo: Can`t find repo list file for '"
                 + name
                 + "'. Did you change wizard.cfg? Otherwise please report this issue.")

        for srcfile, destfile in self.operationsForRepository(repofile):
            self.syncFile(os.path.join(src, srcfile),
                          os.path.join(dest, destfile))

    """
    Compiles the physics plugin and examples 
    """
    def compilePluginsAndExamples(self, target):
        # Loop through config sections and update
        for repo in self.CONFIG.sections():
            path = os.path.join(self.TEMPLATE_PATH, repo)
            makefile = os.path.join(path, self.REPO_MAKE_FILE)
            if not os.path.exists(makefile):
                exit("Can`t find makefile for '"
                     + name
                     + "'. Did you change wizard.cfg? Otherwise please report this issue.")

            # Copy makefile and execute
            shutil.copyfile(makefile, os.path.join(target, "Makefile"))
            os.chdir(target)
            success = os.system("make")
            if success > 0:
                exit ("Error: Compilation of '" + repo + "' failed!")

        print "Plugin and examples updated and compiled."

    def operationsForRepository(self, repofile):
        file = open(repofile)
        while 1:
            line = file.readline()
            if not line:
                break
            if line[0] == "#":
                continue
            m = re.search('(([^\s]+)\s*([^\s]*))', line)
            src = m.group(2)
            dest = m.group(3)
            if not dest:
                dest = src
            yield src, dest

    # If file doesn't exist, copy it
    # If file is the same, ignore it
    # If file is different, ask for solution
    # TODO Maintain database to check if difference is just a legal file update
    def syncFile(self, srcfile, destfile):
        destdir = os.path.dirname(destfile)
        if not os.path.exists(destdir):
            os.makedirs(destdir)

        if not os.path.exists(destfile):
            shutil.copyfile(srcfile, destfile)
            if self.VERBOSE:
                print '** Copied', srcfile, ' to ', destfile
        else:
            # File exists, compare
            if filecmp.cmp(srcfile, destfile):
                # Files are the same, ignore
                return
            else:
                # Files not the same, handle that
                if self.SYNC_IGNORE:
                    return
                elif self.SYNC_OVERWRITE:
                    shutil.copyfile(destfile, destfile + '.backup') # Backup
                    shutil.copyfile(srcfile, destfile) # Overwrite file
                    if self.VERBOSE:
                        print '** Copied', srcfile, ' to ', destfile
                else:
                    if self.askForOverwriting(destfile):
                        shutil.copyfile(srcfile, destfile) # Overwrite file
                        if self.VERBOSE:
                            print '** Copied', srcfile, ' to ', destfile
                    else:
                        return

    def askForOverwriting(self, filename):
        question = "Local file '" + filename + "' differs from template file," + \
                   " should we overwrite it?\n" + \
                   "[y] yes - [o] overwrite all - [n] ignore - [i] ignore all\n"
        prompt = '[y/o/N/i]'

        valid = {"y":True, "o":True, "n":False, "i":False}

        while True:
            sys.stdout.write(str(question) + prompt)
            choice = raw_input().lower()

            if choice == 'i':
                self.SYNC_IGNORE = True
            elif choice == 'o':
                self.SYNC_OVERWRITE = True

            if choice == '' or choice == 'n' or choice == 'i':
                return False
            elif choice == 'y' or choice == 'o':
                return True
            else:
                sys.stdout.write("Please respond with one of [y/o/N/i]")
