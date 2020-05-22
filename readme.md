# csv2rrd
store data of a csv-file in a round robin database.
## description
csv2rrd get the data of a csv-file and create a rrd-file of the configured parameters (in rrdtool_wrapper) to store each entry of the csv in the rrd. In this case the csv is provided by sbfspot wich is installed on a rasberry pi and with the help of sbfspot the raspberry receive the data of a pv inverter every 5 minutes. To handle a huge amount of datapoints csv2rrd will use the rrdtool. With the rrdtool it's possible to create a database, to update the database and to generate a graph of the content of the rrd. For long-term observation of the measuring points rrdtool provides the right options.
For more information: (https://www.sma-america.com/) (https://github.com/SBFspot/SBFspot) (https://oss.oetiker.ch/rrdtool/)
### target
csv2rrd is written to store the data of a sma-device (PV inverter) in a database. With code adaptions csv2rrd can be used with nearly every other csv-files.
### worklive folders
./csv : In this relative path of the sourcefolder all csv-files (sma.csv) will be located.
./rrd : In this relative path of the sourcefolder the rrd-file (sma.rrd) will be located.
./rrd/graph : In this relative path of the sourcefolder the graph (sma.png) will be located.
### input
input as arguments: give one or several csv-filenames as arguments to the csv2rrd. if no argument will be provided rrd2csv use *./csv/sma.csv* by default.
### output
output as rrd-file and png-image and log-file: csv2rrd will process the given input (csv) and create a related rrd and a graph. For better usability a logfile (*csv2rrd.log*) is generated too.

## code
***csv2rrd.py***: it is the main of the *app*. Here all scripts are bundled: csv_read.py, logger-py, rrdtool_wrapper.py
***csv_read.py***: it is responsible for the csv. Here the csv is processed: **Actions**: read the csv, return the csv to the rrdtool
***logger.py***: it is responsible for the logfile of the csv2rrd. **Actions**: print the messages of error or success to the *rrd2csv.log*
***rrdtool_wrapper.py***: it is responsible for the actions of the rrdtool. **Actions**: create or update a rrd, generate a graph of a rrd

## howto
`How to call csv2rrd?`
>Call it with no paramter: *sma.csv* will be processed
```
python3 csv2rrd.py
```

>Call it with one paramter: *sma1-Spot-20200521.csv* will be processed
```
python3 csv2rrd.py sma1-Spot-20200521.csv
```

>Call it with an asterisk in the paramter: *sma**-Spot-20200521.csv* will be processed
```
python3 csv2rrd.py ./csv/sma*
```

Important: Before calling csv2rrd delete all files in ./rrd and ./rrd/graph
