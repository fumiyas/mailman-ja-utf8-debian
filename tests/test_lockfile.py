# Copyright (C) 2002-2010 by the Free Software Foundation, Inc.
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

"""Unit tests for the LockFile class.
"""

import unittest
try:
    from Mailman import __init__
except ImportError:
    import paths

from Mailman.LockFile import LockFile

LOCKFILE_NAME = '/tmp/.mm-test-lock'



class TestLockFile(unittest.TestCase):
    def test_two_lockfiles_same_proc(self):
        lf1 = LockFile(LOCKFILE_NAME)
        lf2 = LockFile(LOCKFILE_NAME)
        lf1.lock()
        self.failIf(lf2.locked())



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLockFile))
    return suite



if __name__ == '__main__':
    unittest.main(defaultTest='suite')
