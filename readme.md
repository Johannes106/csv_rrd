# csv2rrd

store data of a csv-file in a round robin database.

## description

csv2rrd get the data of a csv-file and create a rrd-file of the configured parameters (in rrdtool_wrapper) to store each entry of the csv in the rrd. In this case the csv is provided by sbfspot wich is installed on a rasberry pi and with the help of sbfspot the raspberry receive the data of a pv inverter every 5 minutes. To handle a huge amount of datapoints csv2rrd will use the rrdtool. With the rrdtool it's possible to create a database, to update the database and to generate a graph of the content of the rrd. For long-term observation of the measuring points rrdtool provides the right options.
For more information: (https://www.sma-america.com/) (https://github.com/SBFspot/SBFspot) (https://oss.oetiker.ch/rrdtool/)

### target

csv2rrd is written to store the data of a sma-device (PV inverter) in a database. With code adaptions csv2rrd can be used with nearly every other csv-files.

### worklive folders

- **./csv** : In this relative path of the sourcefolder all csv-files (sma.csv) will be located.
- **./rrd** : In this relative path of the sourcefolder the rrd-file (sma.rrd) will be located.
- **./rrd/graph** : In this relative path of the sourcefolder the graph (sma.png) will be located.

## requirements

rrdtool has to be installed.

- otherwise install it!:
  `pip3 install rrdtool`
- Maybe you also need some additional steps: `sudo apt-get install rrdtool python-rrdtool librrd-dev`

### input

**input as arguments**: give **one** or **several** **csv-filenames** as arguments to the csv2rrd. if no argument will be provided rrd2csv use **./csv/sma.csv** by default.

### output

output as **rrd-file** and **png-image** and **log-file**: csv2rrd will process the given input (csv) and create a related rrd and a graph. For better usability a logfile (_csv2rrd.log_) is generated too.

## code

- **csv2rrd.py**: it is the main of the _app_. Here all scripts are bundled: csv_read.py, logger-py, rrdtool_wrapper.py
- **csv_read.py**: it is responsible for the csv. Here the csv is processed:
  - **Actions**: read the csv, return the csv to the rrdtool
- **logger.py**: it is responsible for the logfile of the csv2rrd.
  - **Actions**: print the messages of error or success to the _rrd2csv.log_
- **rrdtool_wrapper.py**: it is responsible for the actions of the rrdtool.
  - **Actions**: create or update a rrd, generate a graph of a rrd

## howto

pathes:\n

- Default pathes for rrd: ./rrd/sma_garage.rrd
- Default pathes for graphes: ./rrd/graph/sma_garage\*.png

`How to call csv2rrd?`

> Call it with no paramter: _sma.csv_ will be processed

```
python3 csv2rrd.py
```

> Call it with one parameter: _sma1-Spot-20200521.csv_ will be processed

```
python3 csv2rrd.py sma1-Spot-20200521.csv
```

> Call it with an asterisk in the parameter: _sma\*\*-Spot-20200521.csv_ will be processed

```
python3 csv2rrd.py ./csv/sma*
```

> Call it with args for rrd-location and/or graph-folder and/or csv-location and/or db_name

> _Important:_ args for rrd has to be a location (relative path) and end with: .rrd

> _Important:_ args for csv has to be a location (relative path) and end with: .csv

> _Important:_ args for graph has to be only the relativ path and it will indicated by the word 'graph'

> _Important:_ args for rrd-file to has be only a word with the prefix 'sma\_'

> _Important:_ args for graph has be only the relativ path and it will indicated by the word 'graph'

| indicator for | keyword |
| ------------- | ------- |
| csv_suffix    | .csv    |
| rrd_suffix    | .rrd    |
| graph_keyword | graph   |
| sma_keyword   | sma\_   |

```bash
python3 csv2rrd.py ./csv/sma.csv ./rrd/test.rrd ./graph
```

```bash
python3 csv2rrd.py ./csv/sma.csv ./rrd/test.rrd sma_home
```

```bash
 python3 csv2rrd.py ./csv/sma.csv ./rrd/test.rrd ./rrd/graph sma_home
```

```bash
 python3 csv2rrd.py ./csv/*.csv ./rrd/test.rrd ./rrd/graph sma_home
```

```bash
 python3 /opt/cacti/scripts/csv2rrd/csv_rrd/csv2rrd.py /home/pi/smadata/2021/garage-Spot-20210416.csv /opt/cacti/rra/smagarage.rrd var/www/pv/graph sma_home
```

## Important: Before calling csv2rrd delete all files in ./rrd and ./rrd/graph
