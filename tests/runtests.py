import unittest
import io

import dballe
import dba_qcfilter.cli


class TestDbaQcfilterCli(unittest.TestCase):
    def test_not_preserve(self):
        with open("tests/001.bufr", "rb") as fpin:
            with io.BytesIO() as fpout:
                dba_qcfilter.cli.main(fpin, fpout, False)

                fpout.seek(0)
                importer = dballe.Importer("BUFR")
                with importer.from_file(fpout) as fp:
                    count = 0
                    for msgs in fp:
                        for msg in msgs:
                            count += 1

                self.assertEqual(count, 1)

    def test_preserve(self):
        with open("tests/001.bufr", "rb") as fpin:
            with io.BytesIO() as fpout:
                dba_qcfilter.cli.main(fpin, fpout, True)

                fpout.seek(0)
                importer = dballe.Importer("BUFR")
                with importer.from_file(fpout) as fp:
                    count = 0
                    invalid_count = 0
                    valid_count = 0
                    for msgs in fp:
                        for msg in msgs:
                            for data in msg.query_data():
                                attrs = {
                                    a.code: a.get()
                                    for a in data["variable"].get_attrs()
                                }
                                if "B33007" in attrs:
                                    self.assertEqual(len(attrs.keys()), 1)
                                    self.assertEqual(attrs["B33007"], 0)
                                    invalid_count += 1
                                else:
                                    self.assertEqual(len(attrs.keys()), 0)
                                    valid_count += 1

                            count += 1

                self.assertEqual(count, 3)
                self.assertEqual(invalid_count, 2)
                self.assertEqual(valid_count, 1)


if __name__ == '__main__':
    unittest.main()
