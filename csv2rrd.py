#!/usr/bin/python3
# main of csv2rrd
# to respect the privacy of var (such as private) i have to use 'from ...'
import sys
import re
from os import path
from csv_read import *
from rrdtool_wrapper import *
from logger import Logger

def read_args_of_commandline():
    # if there are serveral filename found (by asterisk)
    filenames = sys.argv
    if(len(filenames) == 2):
        filenames.pop(0)
        filename = filenames
        return filename
    elif(len(filenames) > 2):
        filenames.pop(0)
        return filenames
    return None

# check if there args on the commandline otherwise set filename to the given arg of function
def set_and_get_csv_filename(filename):
    csv_filename = filename
    value_of_commandline = read_args_of_commandline()
    # print("set_and_get_csv_filename: read_args_of_commandline:", value_of_commandline)
    if(value_of_commandline == None):
        print("There are no given args on the commandline")
        return csv_filename
    else:
        #it returns a list
        print("set CSV by call")
        csv_filename = value_of_commandline
        return csv_filename

def file_exists(filename):
    if (path.exists(filename)):
        return True

def iterate_over_csvs_and_store_it_to_list(csv_filename):
    csv_files = []
    #read each csv-file
    for csv_name in csv_filename:
        print("Csvfile:", csv_name)
        if(file_exists(csv_name)):
            csv = read_csv(csv_name)
            csv_files.append(csv)
        else:
            print(csv_name, "does not exist")
    #sort list csv_files by key of 'first_timestamp'
    #lambda: create an anonymous function to define the key (here: it is like a getter)
    sorted_csv_files = sorted(csv_files, key = lambda csv_key: csv_key['first_timestamp'])
    return sorted_csv_files


def main():
    # in this section all basic variables are set
    # set a var as a string for logging purpose
    job_status = "---------CSV2RRD---------"
    # for logging purposes
    l = Logger("csv2rrd.log")
    csv_file = "./csv/sma.csv"
    # if there no args existing the function will return false: otherwise it will return a list of filenames
    # set filename: differentiate between 0 args or 1 arg or 1 arg with regex
    csv_filename = set_and_get_csv_filename(csv_file)
    l.i(job_status)
    l.i(f"Read CSV: {csv_filename}")
    rrdtool_filename = "sma_garage"
    rrd_filename = f"./rrd/{rrdtool_filename}.rrd"
    rrd_heartbeat = "300"

    #method to create rrd and update rrd and generate graph
    #method to update rrd and generate graph
    def ug_or_cug(rrd_filename, rrd_heartbeat, csv_file_entity):
        # in this section all variables for the csv-file are set
        # differentiate if filename is one value or more then one
        #first_timestamp is a float and we need an integer so parse to an int and as an update arg we need a string
        #-1 because update should be one second after the rrd is created
        csv_devicename = csv_file_entity['devicename']
        csv_first_timestamp = str(int(csv_file_entity['first_timestamp']-1))
        csv_last_timestamp = str(int(csv_file_entity['last_timestamp']))
        csv_last_date_time = csv_file_entity['last_date_time']
        csv_last_update_value = csv_file_entity['last_update_value']
        csv_data = csv_file_entity['data']
        image_filename = f"./rrd/graph/{rrdtool_filename}_{csv_first_timestamp}.png"

        if(file_exists(rrd_filename)):
            job_status = updater_rrd(rrd_filename, csv_data)
            l.i(job_status)
            # if there already exists a image with this name: do not overwrite the image
            if(file_exists(image_filename)):
                job_status = f"error: create graph: {image_filename} already exists so do not create it"
                l.i(job_status)
            else:
                job_status = grapher_rrd(rrd_filename, csv_devicename, image_filename, "PNG", csv_first_timestamp, csv_last_timestamp, csv_last_date_time, csv_last_update_value)
                l.i(job_status)
        else:
                job_status = creator_rrd(rrd_filename, csv_first_timestamp, rrd_heartbeat)
                l.i(job_status)
                job_status = updater_rrd(rrd_filename, csv_data)
                l.i(job_status)
                job_status = grapher_rrd(rrd_filename, csv_devicename, image_filename, "PNG", csv_first_timestamp, csv_last_timestamp, csv_last_date_time, csv_last_update_value)
                l.i(job_status)

    # if there are several csv-files found because there are several arguments by a wildcard (*) on the script-command by commandline
    if(type(csv_filename) == list):
        csv_file_list = iterate_over_csvs_and_store_it_to_list(csv_filename)
        l.i(f"process {len(csv_file_list)} csvfiles")
        counter = 0
        #iterate over all found csv files
        for csv_file_entity in csv_file_list:
            counter += 1
            ug_or_cug(rrd_filename, rrd_heartbeat, csv_file_entity)
    # if only one csv is found because there is only one argument on the script-command by commandline
    else:
        job_status = f"There are no given args on the commandline so use {csv_filename} (by default)"
        l.i(job_status)
        csv_file_entity = read_csv(csv_filename)
        ug_or_cug(rrd_filename, rrd_heartbeat, csv_file_entity)

main()
