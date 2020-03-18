import unittest
import io

import dballe
import dba_qcfilter.cli


class TestDbaQcfilterCli(unittest.TestCase):
    def test_not_preserve(self):
        with open("tests/001.bufr", "rb") as fpin:
            with io.BytesIO() as fpout:
                dba_qcfilter.cli.do_qc(fpin, fpout, False)

                fpout.seek(0)
                importer = dballe.Importer("BUFR")
                with importer.from_file(fpout) as fp:
                    count = 0
                    for msgs in fp:
                        for msg in msgs:
                            for data in msg.query_data():
                                attrs = data["variable"].get_attrs()
                                # Attributes are removed after QC
                                self.assertEqual(len(attrs), 0)

                            count += 1

                # There's only one valid BUFR
                self.assertEqual(count, 1)

    def test_preserve(self):
        with open("tests/001.bufr", "rb") as fpin:
            with io.BytesIO() as fpout:
                dba_qcfilter.cli.do_qc(fpin, fpout, True)

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
                                    # If B33007 is set, it must be the only one
                                    self.assertEqual(len(attrs.keys()), 1)
                                    # If B33007 is set, its value must be 0
                                    self.assertEqual(attrs["B33007"], 0)
                                    invalid_count += 1
                                else:
                                    # If B33007 is not set, then the attributes
                                    # list must be empty
                                    self.assertEqual(len(attrs.keys()), 0)
                                    valid_count += 1

                            count += 1

                # All BUFR messages must be in the output file
                self.assertEqual(count, 3)
                # Two bufr messages are invalid
                self.assertEqual(invalid_count, 2)
                # There's only one valid BUFR
                self.assertEqual(valid_count, 1)


if __name__ == '__main__':
    unittest.main()
