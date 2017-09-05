# Copyright (C) 2000-2016 by the Free Software Foundation, Inc.
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

import sys
import time
import locale
import gettext
from types import StringType, UnicodeType

from Mailman import mm_cfg
from Mailman.SafeDict import SafeDict

_translation = None


def _get_ctype_charset():
    old = locale.setlocale(locale.LC_CTYPE, '')
    charset = locale.nl_langinfo(locale.CODESET)
    locale.setlocale(locale.LC_CTYPE, old)
    return charset

if not mm_cfg.DISABLE_COMMAND_LOCALE_CSET:
    _ctype_charset = _get_ctype_charset()
else:
    _ctype_charset = None



def set_language(language=None):
    global _translation
    if language is not None:
        language = [language]
    try:
        _translation = gettext.translation('mailman', mm_cfg.MESSAGES_DIR,
                                           language)
    except IOError:
        # The selected language was not installed in messages, so fall back to
        # untranslated English.
        _translation = gettext.NullTranslations()

def get_translation():
    return _translation

def set_translation(translation):
    global _translation
    _translation = translation


# Set up the global translation based on environment variables.  Mostly used
# for command line scripts.
if _translation is None:
    set_language()



def _(s, frame=1):
    if s == '':
        return s
    assert s
    # Do translation of the given string into the current language, and do
    # Ping-string interpolation into the resulting string.
    #
    # This lets you write something like:
    #
    #     now = time.ctime(time.time())
    #     print _('The current time is: %(now)s')
    #
    # and have it Just Work.  Note that the lookup order for keys in the
    # original string is 1) locals dictionary, 2) globals dictionary.
    #
    # First, get the frame of the caller
    frame = sys._getframe(frame)
    # A `safe' dictionary is used so we won't get an exception if there's a
    # missing key in the dictionary.
    dict = SafeDict(frame.f_globals.copy())
    dict.update(frame.f_locals)
    # Translating the string returns an encoded 8-bit string.  Rather than
    # turn that into a Unicode, we turn any Unicodes in the dictionary values
    # into encoded 8-bit strings.  BAW: Returning a Unicode here broke too
    # much other stuff and _() has many tentacles.  Eventually I think we want
    # to use Unicode everywhere.
    tns = _translation.gettext(s)
    charset = _translation.charset()
    if not charset:
        charset = 'us-ascii'
    for k, v in dict.items():
        if isinstance(v, UnicodeType):
            dict[k] = v.encode(charset, 'replace')
    try:
        return tns % dict
    except (ValueError, TypeError):
        # Bad interpolation format. Punt.
        return tns



def tolocale(s):
    global _ctype_charset
    if isinstance(s, UnicodeType) or _ctype_charset is None:
        return s
    source = _translation.charset ()
    if not source:
        return s
    return unicode(s, source, 'replace').encode(_ctype_charset, 'replace')

if mm_cfg.DISABLE_COMMAND_LOCALE_CSET:
    C_ = _
else:
    def C_(s):
        return tolocale(_(s, 2))

    

def ctime(date):
    # Don't make these module globals since we have to do runtime translation
    # of the strings anyway.
    daysofweek = [
        _('Mon'), _('Tue'), _('Wed'), _('Thu'),
        _('Fri'), _('Sat'), _('Sun')
        ]
    months = [
        '',
        _('Jan'), _('Feb'), _('Mar'), _('Apr'), _('May'), _('Jun'),
        _('Jul'), _('Aug'), _('Sep'), _('Oct'), _('Nov'), _('Dec')
        ]

    tzname = _('Server Local Time')
    if isinstance(date, StringType):
        try:
            year, mon, day, hh, mm, ss, wday, ydat, dst = time.strptime(date)
            if dst in (0,1):
                tzname = time.tzname[dst]
            else:
                # MAS: No exception but dst = -1 so try
                return ctime(time.mktime((year, mon, day, hh, mm, ss, wday,
                                          ydat, dst)))
        except (ValueError, AttributeError):
            try:
                wday, mon, day, hms, year = date.split()
                hh, mm, ss = hms.split(':')
                year = int(year)
                day = int(day)
                hh = int(hh)
                mm = int(mm)
                ss = int(ss)
            except ValueError:
                return date
            else:
                for i in range(0, 7):
                    wconst = (1999, 1, 1, 0, 0, 0, i, 1, 0)
                    if wday.lower() == time.strftime('%a', wconst).lower():
                        wday = i
                        break
                for i in range(1, 13):
                    mconst = (1999, i, 1, 0, 0, 0, 0, 1, 0)
                    if mon.lower() == time.strftime('%b', mconst).lower():
                        mon = i
                        break
    else:
        year, mon, day, hh, mm, ss, wday, yday, dst = time.localtime(date)
        if dst in (0,1):
            tzname = time.tzname[dst]

    wday = daysofweek[wday]
    mon = months[mon]
    return _('%(wday)s %(mon)s %(day)2i %(hh)02i:%(mm)02i:%(ss)02i '
             '%(tzname)s %(year)04i')
