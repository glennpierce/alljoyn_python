#!/usr/bin/env python

#
# Copyright 2012 Glenn Pierce
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import sys
import os
import resource
import time
import atexit
import traceback
import logging
import signal
import grp
import errno
from pwd import getpwnam


class DaemonException(Exception):
    pass


class Daemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidfile, user=None, group=None, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

        if user == None and group == None:
            self.user = self.group = Daemon.find_unprivileged_user()
        else:
            self.user = user
            self.group = group

        logging.debug("found user, group %s:%s", self.user, self.group)
        self.uid, self.gid = self.get_uid_gid_from_names(self.user, self.group)

    @staticmethod
    def find_unprivileged_user():
        # Try to find unprivileged user
        name = None
        for search_group in ['nobody', 'www-data']:
            try:
                grp.getgrnam(search_group)
                name = search_group
                break
            except KeyError, e:
                continue
            except Exception, e:
                logging.critical(e)

        if name == None:
            logging.critical("No user specified to run as")
            sys.exit(1)

        return name

    @staticmethod
    def get_uid_gid_from_names(user, group):
        uid = -1
        if user != None:
            try:
                uid = getpwnam(user).pw_uid
            except KeyError:
                raise DaemonException("user %s does not exist" % (user,))

        gid = -1
        if group != None:
            try:
                gid = grp.getgrnam(group).gr_gid
            except KeyError:
                raise DaemonException("group %s does not exist" % (group,))

        logging.info("Found uid %s gid %s", uid, gid)

        return (uid, gid)

    def set_user_and_group(self, user, group):
        logging.info("Setting daemon to user %s, group %s", user, group)
        self.uid, self.gid = self.get_uid_gid_from_names(user, group)

    @staticmethod
    def change_process_owner(uid=None, gid=None):
        """ Change the owning UID and GID of this process.
            Sets the GID then the UID of the process (in that order, to
            avoid permission errors) to the specified `gid` and `uid`
            values. Requires appropriate OS privileges for this process.
        """
        try:
            if gid is not None:
                os.setgid(gid)
            if uid is not None:
                os.setuid(uid)
        except Exception, exc:
            raise DaemonException(u"Unable to change file creation mask (%(exc)s)" % vars())

    def prevent_core_dump(self):
        """ Prevent this process from generating a core dump.
        Sets the soft and hard limits for core dump size to zero. On
        Unix, this prevents the process from creating core dump
        altogether.
        """
        core_resource = resource.RLIMIT_CORE

        try:
            # Ensure the resource limit exists on this platform, by requesting
            # its current value
            core_limit_prev = resource.getrlimit(core_resource)
        except ValueError, exc:
            error = DaemonOSEnvironmentError(
                u"System does not support RLIMIT_CORE resource limit (%(exc)s)" % vars())
            raise error

        # Set hard and soft limits to zero, i.e. no core dump at all
        core_limit = (0, 0)
        resource.setrlimit(core_resource, core_limit)

    def sig_term_called(self, signum, frame):
        logging.info("sig_term_called: pid id %s:", os.getpid())
        try:
            self.shutdown()
        except Exception, e:
            logging.critical(e)

        pid = self.readpid()
        logging.info("sig_term_called: read pid id %s:", pid)
        if pid:
            self.delpid()

        logging.info("exiting")
        self.exited()
        sys.exit(1)

    def is_pidfile_stale(self, pidfile):
        """ Determine whether a PID file is stale.
            Return True (stale) if the contents of the PID file are
            valid but do not match the PID of a currently-running process;
            otherwise return False.
        """
        result = False

        pid = self.readpid()
        if pid is not None:
            try:
                os.kill(pid, signal.SIG_DFL)
            except OSError, exc:
                if exc.errno == errno.ESRCH:
                    # The specified PID does not exist
                    result = True

        return result

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """

        # For security reasons
        self.prevent_core_dump()

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
        os.chown(self.pidfile, self.uid, self.gid)
        signal.signal(signal.SIGTERM, self.sig_term_called)

        # drop privilege
        self.change_process_owner(self.uid, self.gid)

    def readpid(self):
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
            return pid
        except IOError:
            return None

    def delpid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        pid = self.readpid()

        if pid:
            if self.is_pidfile_stale(self.pidfile):
                self.delpid()
            else:
                message = "pidfile %s already exists and another daemon appears to be running\n"
                sys.stderr.write(message % self.pidfile)
                sys.exit(1)

        # Start the daemon
        try:
            self.daemonize()
            self.run()
        except Exception as e:
            logging.critical(e)

    def stop(self):
        # Get the pid from the pidfile
        pid = self.readpid()
        logging.info("shutdown issued pid: %s", pid)
        if pid:
            try:
                logging.info("sending sigterm %s" % (pid,))
                os.kill(pid, signal.SIGTERM)
            except Exception, e:
                print e

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        time.sleep(2)
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
        pass

    def shutdown(self):
        pass

    def exited(self):
        pass
