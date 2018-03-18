# multiget

Python 3 app to download file chunks in serial or parallel from url and save to disk

The app uses `time`, `math`, `threading`, `argparse` and `urllib` packages from the python 3 standard library

To run in the command line:

* `python multiget.py <your.url.com/data>`

Optional arguments:

* `-n`  integer:  number of chunks - default 4
* `-s`  float: chunk size in MiB rounded down to nearest byte - default 1
* `-o`  string: output file size - default data.jar
* `-p`  optional flag to download in parallel


Python version 3.6.4

Developed on windows, tested on linux
