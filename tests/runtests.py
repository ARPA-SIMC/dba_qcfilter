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
                    msgs = list([m[0] for m in fp])
                    self.assertEqual(len(msgs), 1, "There should be only one valid message")
                    msg = msgs[0]
                    cur = msg.query_data()
                    data = next(cur)
                    attrs = data["variable"].get_attrs()
                    self.assertEqual(len(attrs), 1, "The message should have only one attribute")
                    self.assertEqual(attrs[0].code, "B33036", "The only attribute should be var B33036")
                    self.assertEqual(attrs[0].get(), 100, "The only attribute should be 100")


    def test_preserve(self):
        with open("tests/001.bufr", "rb") as fpin:
            with io.BytesIO() as fpout:
                dba_qcfilter.cli.do_qc(fpin, fpout, True)

                fpout.seek(0)
                importer = dballe.Importer("BUFR")
                with importer.from_file(fpout) as fp:
                    msgs = list([m[0] for m in fp])
                    self.assertEqual(len(msgs), 3, "There should be 3 messages")
                    data = next(msgs[0].query_data())
                    attrs = {a.code: a.get() for a in data["variable"].get_attrs()}
                    self.assertEqual(attrs, {"B33007": 0, "B33036": 100}, "The first message should have these attributes")
                    data = next(msgs[1].query_data())
                    attrs = {a.code: a.get() for a in data["variable"].get_attrs()}
                    self.assertEqual(attrs, {"B33007": 0}, "The first message should have these attributes")
                    data = next(msgs[2].query_data())
                    attrs = {a.code: a.get() for a in data["variable"].get_attrs()}
                    self.assertEqual(attrs, {"B33036": 100}, "The first message should have these attributes")


if __name__ == '__main__':
    unittest.main()
