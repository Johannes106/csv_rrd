#!/usr/bin/python3
# read data of a csv-file and print specific keys with related values of the csv to the console within a loop
import re
import sys
import csv
import datetime
import time

# private functions are named by an underscore
def _convert_date_to_timestamp(date_human):
    date_time_human_obj = datetime.datetime.strptime(date_human, '%d/%m/%Y %H:%M:%S')
    unix_seconds = time.mktime(date_time_human_obj.timetuple())
    return(unix_seconds)

def read_csv(csv_filename):
    csv_data_array_list_first = []
    with open(csv_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        headline_line = 4
        content_line = 0
        attribut_value = ""
        attribut_key = []
        csv_data_array_list = []
        csv_data_array_list_filtered = []

        for row in csv_reader:
            if line_count == headline_line:
                attribut_key = row
                attribut_amount = len(attribut_key)
            elif line_count > headline_line:
                attribut_value = row
                csv_data_list_line = dict(zip(attribut_key, attribut_value))
                csv_data_list_line_filtered = (f"{_convert_date_to_timestamp(csv_data_list_line['dd/MM/yyyy HH:mm:ss'])}:{csv_data_list_line['EToday']}")
                # it is important if this file (csv_read.py) is used as a script for the use with cacti
                # print(f"{csv_data_list_line['DeviceName']}")
                print(csv_data_list_line_filtered)
                csv_data_array_list.append(csv_data_list_line)
                csv_data_array_list_filtered.append(csv_data_list_line_filtered)
                content_line += 1
            line_count += 1
        csv_data_array_list_values = dict()
        csv_data_array_list_values['data'] = csv_data_array_list_filtered
        csv_data_array_list_first_value = csv_data_array_list[0]['dd/MM/yyyy HH:mm:ss']
        csv_data_array_list_values['first_timestamp'] = _convert_date_to_timestamp(csv_data_array_list_first_value)
        csv_data_array_list_values['first_date_time'] = csv_data_array_list_first_value
        csv_data_array_list_last_date_time = csv_data_array_list[-1]['dd/MM/yyyy HH:mm:ss']
        csv_data_array_list_values['last_timestamp'] = _convert_date_to_timestamp(csv_data_array_list_last_date_time)
        csv_data_array_list_values['last_date_time'] = csv_data_array_list_last_date_time
        csv_data_array_list_last_update_value = csv_data_array_list[-1]['EToday']
        csv_data_array_list_values['last_update_value'] = csv_data_array_list_last_update_value
        csv_data_array_list_devicename = csv_data_array_list[0]['DeviceName']
        csv_data_array_list_values['devicename'] = csv_data_array_list_devicename

        return csv_data_array_list_values

# main(csvfile_name) is only executed if 'csv_read.py' is directly called
def main(csvfile_name):
    read_csv(csvfile_name)

# check if this file (csv_read.py) is directly called
# first of all execution python looks for its own variables and if the var __name__ has the value of __main__ then it is a direct call
if __name__ == '__main__':
    csvfile_name = "./csv/sma.csv"
    # Look if there are two args (first arg is always the filename.py on an direct call) then set the filename to the second arg
    # if(len(sys.argv) > 1):
    #     csvfile_name = sys.argv[1]
    #     print("set csvfile_name to: ", csvfile_name)

    if(len(sys.argv) > 1):
        csvfile_name = str(sys.argv[1])

    main(csvfile_name)
