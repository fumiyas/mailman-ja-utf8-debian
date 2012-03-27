# Copyright (C) 2001,2002 by the Free Software Foundation, Inc.
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

"""Calculate the list owner recipients (includes moderators).
"""



def process(mlist, msg, msgdata):
    # The recipients are the owner and the moderator
    msgdata['recips'] = mlist.owner + mlist.moderator
    # Don't decorate these messages with the header/footers
    msgdata['nodecorate'] = 1
    msgdata['personalize'] = 0
