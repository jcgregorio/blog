#!/usr/bin/python2.4
import time
import datetime
import re

notimezone = re.compile('(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(\.\d*)?Z')
timezone = re.compile('(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(\.\d*)?(\+|-)(\d\d):(\d\d)')

def iso_to_datetime(s):
    """
    Converts an ISO conformant string into a datetime object.
    """
    m = notimezone.match(s)
    parts = []
    if m:
        parts = [int(x) for x in m.groups()[0:6]]
        if m.groups()[6]:
            parts.append(int(float(m.groups()[6])*1000000))
    else:
        mtz = timezone.match(s)
        if mtz:
            parts = [int(x) for x in mtz.groups()[0:6]]
            if mtz.groups()[6]:
                parts.append(int(float(mtz.groups()[6])*1000000))
            else:
                parts.append(0)
            tzoffset = int(mtz.groups()[8]) * 60 + int(mtz.groups()[9])
            if mtz.groups()[7] == '-':
                tzoffset = - tzoffset 

            class TZ(datetime.tzinfo):
                def utcoffset(self, dt): 
                    return datetime.timedelta(minutes=tzoffset)
            parts.append(TZ())
    return apply(datetime.datetime, parts)
 
class LTZ(datetime.tzinfo):
    def utcoffset(self, dt): 
        return datetime.timedelta(seconds=time.timezone)

def local_to_datetime(seconds):
    """
    Converts a time, represented in seconds from the Epoch, into
    a date time object, complete with timezone information.
    """
    localtime = list(time.localtime(seconds)[0:6])
    localtime.append(0)
    localtime.append(LTZ())
    return apply(datetime.datetime, localtime)

if __name__ == "__main__":
    import unittest

    class TestGeneric(unittest.TestCase):
        def test_iso_to_local(self):
            a = "2003-12-13T18:30:02Z"
            b = "2003-12-13T18:30:02.25Z"
            c = "2003-12-13T18:30:02+01:00"
            d = "2003-12-13T18:30:02.25+01:00"
            e = "2003-12-13T18:30:02.25-05:01"
            self.assertEqual(iso_to_datetime(a).isoformat('T'), a[0:-1])
            self.assertEqual(iso_to_datetime(b).isoformat('T'), "2003-12-13T18:30:02.250000")
            self.assertEqual(iso_to_datetime(c).isoformat('T'), c)
            self.assertEqual(iso_to_datetime(d).isoformat('T'), "2003-12-13T18:30:02.250000+01:00")
            self.assertEqual(iso_to_datetime(e).isoformat('T'), "2003-12-13T18:30:02.250000-05:01")
 
        def test_local_to_iso(self):
            a = "2003-12-13T18:30:02Z"
            l1 = local_to_datetime(1124133584)
            l2 = local_to_datetime(1124133585)
            self.assertEqual("2005-08-15T15:19:44+05:00", l1.isoformat('T'))
            self.assert_(l1 < l2)
            self.assert_(l1 <= l1)
            self.assertFalse(l1 < l1)


    
    unittest.main()
