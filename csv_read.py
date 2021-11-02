#!/usr/bin/python3
# read data of a csv-file and print specific keys with related values of the csv to the console within a loop
import re
import sys
import csv
import datetime
import time


def _convert_date_to_timestamp(date_human):
    # private functions are named by an underscore
    date_time_human_obj = datetime.datetime.strptime(
        date_human, '%d/%m/%Y %H:%M:%S')
    unix_seconds = time.mktime(date_time_human_obj.timetuple())
    return(unix_seconds)


def read_csv(csv_filename):
    csv_data_array_list_first = []
    with open(csv_filename) as csv_f:
        # in the csv-file the seperator can be a ; or ,
        seperator_chooser = ''
        seperator_semicolon = ';'
        seperator_comma = ',' 
        seperator_set_in_first_line = csv_f.readline()
        exist_in_file = seperator_set_in_first_line.find(seperator_semicolon)
        if(exist_in_file) > -1:
            seperator_chooser = seperator_semicolon
        else:
            seperator_chooser = seperator_comma
    with open(csv_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=seperator_chooser)
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
                attribut_value = ""
                # print("attribut_value: ", attribut_value)
                delimiter_comma_regex_value = '[0-9]*,[0-9]*'
                # if any element of attribut_value contains the regex(..\,[0-9]*) then replace , with .
                for element_value in row:
                    # print("element_value", element_value)
                    row_index_of_element_value = row.index(element_value)
                    if(re.search(delimiter_comma_regex_value, element_value)):
                        element_value = element_value.replace(',', '.')
                        row[row_index_of_element_value] = element_value
                attribut_value = row
                csv_data_list_line = dict(zip(attribut_key, attribut_value))
                csv_data_list_line_filtered = (
                    f"{_convert_date_to_timestamp(csv_data_list_line['dd/MM/yyyy HH:mm:ss'])}:{csv_data_list_line['EToday']}")
                # it is important if this file (csv_read.py) is used as a script for the use with cacti
                # print(f"{csv_data_list_line['DeviceName']}")
                # print(csv_data_list_line_filtered)
                csv_data_array_list.append(csv_data_list_line)
                csv_data_array_list_filtered.append(
                    csv_data_list_line_filtered)
                content_line += 1
            line_count += 1
        csv_data_array_list_values = dict()
        csv_data_array_list_values['data'] = csv_data_array_list_filtered
        csv_data_array_list_first_value = csv_data_array_list[0]['dd/MM/yyyy HH:mm:ss']
        csv_data_array_list_values['first_timestamp'] = _convert_date_to_timestamp(
            csv_data_array_list_first_value)
        csv_data_array_list_values['first_date_time'] = csv_data_array_list_first_value
        csv_data_array_list_last_date_time = csv_data_array_list[-1]['dd/MM/yyyy HH:mm:ss']
        csv_data_array_list_values['last_timestamp'] = _convert_date_to_timestamp(
            csv_data_array_list_last_date_time)
        csv_data_array_list_values['last_date_time'] = csv_data_array_list_last_date_time
        csv_data_array_list_last_update_value = csv_data_array_list[-1]['EToday']
        csv_data_array_list_values['last_update_value'] = csv_data_array_list_last_update_value
        csv_data_array_list_devicename = csv_data_array_list[0]['DeviceName']
        csv_data_array_list_values['devicename'] = csv_data_array_list_devicename

        return csv_data_array_list_values

# deprecated feature
# main(csvfile_name) is only executed if 'csv_read.py' is directly called
def main(csvfile_name):
    print(read_csv(csvfile_name))


# check if this file (csv_read.py) is directly called
# first of all execution python looks for its own variables and if the var __name__ has the value of __main__ then it is a direct call
if __name__ == '__main__':
    csvfile_name = "./csv/sma.csv"
    
    if(len(sys.argv) > 1):
        csvfile_name = str(sys.argv[1])

    main(csvfile_name)
