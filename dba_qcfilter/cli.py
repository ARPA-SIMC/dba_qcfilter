import argparse
import sys
import contextlib

import dballe


def pass_qc(attrs):
    attrs_dict = {v.code: v.get() for v in attrs}

    # Data already checked and checked as invalid by QC filter
    if attrs_dict.get("B33007", 100) == 0:
        return False

    # Gross error check failed
    if attrs_dict.get("B33192", 100) == 0:
        return False

    # Manual invalidation
    if attrs_dict.get("B33196", 100) == 1:
        return False

    total_score = 0

    for bcode, threshold, lt_score, gte_score in (
        ("B33192", 10, -1, 0),
        ("B33193", 10, -1, 1),
        ("B33194", 10, -1, 1),
    ):
        if bcode in attrs_dict:
            if attrs_dict[bcode] < threshold:
                total_score = total_score + lt_score
            else:
                total_score = total_score + gte_score

    return total_score >= -1


@contextlib.contextmanager
def open_input(path=None):
    fp = open(path, "rb") if path is not None else sys.stdin.buffer
    try:
        yield fp
    finally:
        if path is not None:
            fp.close()


@contextlib.contextmanager
def open_output(path=None):
    fp = open(path, "wb") if path is not None else sys.stdout.buffer
    try:
        yield fp
    finally:
        if path is not None:
            fp.close()


def main(input_file, output_file, preserve):
    importer = dballe.Importer("BUFR")
    exporter = dballe.Exporter("BUFR")

    with importer.from_file(input_file) as fp:
        for msgs in fp:
            for msg in msgs:
                count_vars = 0
                new_msg = dballe.Message("generic")

                new_msg.set_named("year", msg.datetime.year)
                new_msg.set_named("month", msg.datetime.month)
                new_msg.set_named("day", msg.datetime.day)
                new_msg.set_named("hour", msg.datetime.hour)
                new_msg.set_named("minute", msg.datetime.minute)
                new_msg.set_named("second", msg.datetime.second)
                new_msg.set_named("rep_memo", msg.report)
                new_msg.set_named("longitude", int(msg.coords[0] * 10 ** 5))
                new_msg.set_named("latitude", int(msg.coords[1] * 10 ** 5))
                if msg.ident:
                    new_msg.set_named("ident", msg.ident)

                for data in msg.query_data({"query": "attrs"}):
                    variable = data["variable"]
                    attrs = variable.get_attrs()
                    is_ok = pass_qc(attrs)
                    v = dballe.var(
                        data["variable"].code, data["variable"].get()
                    )

                    if not is_ok:
                        if preserve:
                            v.seta(dballe.var("B33007", 0))
                        else:
                            continue

                    new_msg.set(data["level"], data["trange"], v)
                    count_vars += 1

                for data in msg.query_station_data({"query": "attrs"}):
                    variable = data["variable"]
                    attrs = variable.get_attrs()
                    v = dballe.var(
                        data["variable"].code, data["variable"].get()
                    )
                    for a in attrs:
                        v.seta(a)

                    new_msg.set(dballe.Level(), dballe.Trange(), v)

                if count_vars > 0:
                    output_file.write(exporter.to_binary(new_msg))


if __name__ == "__main__":
    from . import __version__

    parser = argparse.ArgumentParser(
        description="""Filter data using Quality Control information. Flag
        used are *B33192,*B33193,*B33194,*B33196. Station constant data are
        reported as is"""
    )
    parser.add_argument(
        "-p",
        "--preserve",
        action="store_true",
        help=(
            "preserve wrong data, remove attribute, "
            "insert B33007=0 for wrong data"
        ),
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument(
        "-i", "--input-file", metavar="FILE",
        help="input file (default: stdin)"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        metavar="FILE",
        help="output file (default: stdout)",
    )

    args = parser.parse_args()

    with open_input(args.input_file) as input_file:
        with open_output(args.output_file) as output_file:
            main(input_file, output_file, args.preserve)
