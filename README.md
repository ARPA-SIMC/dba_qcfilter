# dba_qcfilter

[![Build Status](https://badges.herokuapp.com/travis/ARPA-SIMC/dba_qcfilter?branch=master&env=DOCKER_IMAGE=centos:7&label=centos7)](https://travis-ci.org/ARPA-SIMC/dba_qcfilter)
[![Build Status](https://badges.herokuapp.com/travis/ARPA-SIMC/dba_qcfilter?branch=master&env=DOCKER_IMAGE=centos:8&label=centos8)](https://travis-ci.org/ARPA-SIMC/dba_qcfilter)
[![Build Status](https://badges.herokuapp.com/travis/ARPA-SIMC/dba_qcfilter?branch=master&env=DOCKER_IMAGE=fedora:31&label=fedora31)](https://travis-ci.org/ARPA-SIMC/dba_qcfilter)
[![Build Status](https://badges.herokuapp.com/travis/ARPA-SIMC/dba_qcfilter?branch=master&env=DOCKER_IMAGE=fedora:rawhide&label=fedorarawhide)](https://travis-ci.org/ARPA-SIMC/dba_qcfilter)

[![Build Status](https://copr.fedorainfracloud.org/coprs/simc/stable/package/dba_qcfilter/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/simc/stable/package/dba_qcfilter/)

## Introduction

Quality control filter for generic BUFR.

This utility reads any kind of BUFR interpreted by [wreport][1] and discards
the invalid data.

The quality control relies on this algorithm:

```
score = 0

if attribute B33192 < 10 then score = score - 1
if attribute B33193 < 10 then score = score - 1 else score = score + 1
if attribute B33194 < 10 then score = score - 1 else score = score + 1

if score < -1 then B33007 = 0
```

## Usage

```
usage: dba_qcfilter [-h] [-p] [--version] [-i FILE] [-o FILE]

Filter data using Quality Control information. Flag used are
*B33192,*B33193,*B33194,*B33196. Station constant data are reported as is

optional arguments:
  -h, --help            show this help message and exit
  -p, --preserve        preserve wrong data, remove attribute, insert B33007=0
                        for wrong data
  --version             show program's version number and exit
  -i FILE, --input-file FILE
                        input file (default: stdin)
  -o FILE, --output-file FILE
                        output file (default: stdout)
```

## License

dba_qcfilter is Free Software, licensed under the GNU General Public License
version 2 or later.



[1]: https://github.com/arpa-simc/wreport
[2]: https://github.com/arpa-simc/dballe
