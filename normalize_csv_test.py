
from normalize_csv import FIELDNAMES, norm_timestamp, norm_name, norm_duration, norm_zipcode, normalize_csv
import io
import unittest


class TestNormalizeCSV(unittest.TestCase):
    def test_norm_timestamp(self):
        self.assertEqual(norm_timestamp('3/9/19 1:00:00 PM'),
                         '2019-03-09T16:00:00-05:00')
        self.assertEqual(norm_timestamp('2/29/16 1:00:00 PM'),
                         '2016-02-29T16:00:00-05:00')

    def test_norm_zipcode(self):
        self.assertEqual(norm_zipcode(''), '00000')
        self.assertEqual(norm_zipcode('1'), '00001')
        self.assertEqual(norm_zipcode('94301'), '94301')

    def test_norm_name(self):
        self.assertEqual(norm_name('Ana'), 'ANA')
        self.assertEqual(norm_name('María 🌟'), 'MARÍA 🌟')

    def test_norm_duration(self):
        self.assertEqual(norm_duration('20:10:10.10'), 72610.01)

    def test_normalize_csv(self):
        header_row = ",".join(FIELDNAMES) + "\r\n"
        good_csv = io.StringIO(
            header_row +
            "4/1/11 11:00:00 AM,\"Address, CA\",11,Alice,1:00:00.0,1:32:33.123,trash,notes\r\n")
        out = io.StringIO()
        normalize_csv(good_csv, out=out)
        self.assertEqual(out.getvalue(),
                         header_row + '2011-04-01T14:00:00-04:00,"Address, CA",00011,ALICE,3600.0,5553.123,9153.123,notes\r\n')

        # Handles gracefully malformed rows
        bad_csv = io.StringIO(
            header_row +
            "4/1/11 11:00:00 AM,\"Address, CA\",11,Alice,invalidduration,1:32:33.123,trash,notes\r\n")
        try:
            out = io.StringIO()
            normalize_csv(bad_csv, out=out)
            # We shouldn't have output anything other than the header row
            self.assertEqual(out.getvalue(), header_row)
        except Exception as e:
            self.fail("Normalize threw exception on bad input: {}".format(e))


if __name__ == '__main__':
    unittest.main()
