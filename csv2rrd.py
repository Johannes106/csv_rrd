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


#ug: update, graph -> method to update rrd and generate graph
#cug: create, update, graph -> method to create rrd and update rrd and generate graph
def ug_or_cug(rrd_filename, rrd_heartbeat, csv_file_entity, rrdtool_filename, l):
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
            # job_status = grapher_rrd(rrd_filename, csv_devicename, image_filename, "PNG", csv_first_timestamp, csv_last_timestamp, csv_last_date_time, csv_last_update_value)
            # l.i(job_status)

def start_cug_dependent_of_csv(rrd_filename, rrd_heartbeat, csv_devicename, image_filename, rrdtool_filename, l):
    csv_exists = True
    csv_file = "./csv/sma1.csv"
    csv_filename = set_and_get_csv_filename(csv_file)
    l.i(f"Read CSV: {csv_filename}")
    # if there are several csv-files found because there are several arguments by a wildcard (*) on the script-command by commandline
    if(type(csv_filename) == list):
        csv_file_list = iterate_over_csvs_and_store_it_to_list(csv_filename)
        l.i(f"process {len(csv_file_list)} csvfiles")
        counter = 0
        #iterate over all found csv files
        for csv_file_entity in csv_file_list:
            counter += 1
            ug_or_cug(rrd_filename, rrd_heartbeat, csv_file_entity, rrdtool_filename, l)
    # if only one csv is found because there is only one argument on the script-command by commandline
    else:
        job_status = f"There are no given args on the commandline so use {csv_filename} (by default)"
        l.i(job_status)
        csv_file_entity = read_csv(csv_filename)
        ug_or_cug(rrd_filename, rrd_heartbeat, csv_file_entity, rrdtool_filename, l)

def inspect_rrd(rrd_filename):
    #use functions of rrdtool_wrapper.py
    # it is used to get the timestamp and value of the first entry with not empty content
    print("rrd_filename:", rrd_filename)
    fetched_data = fetch_rrd(rrd_filename, "AVERAGE", '1589806500', '1589986215')
    return fetched_data


#generate a graph with the data of a given (external) rrd-file
def generate_graph_by_rrd(rrd_filename, devicename, image_filename, logger):
    # job status = "Generate Graph with the input of a rrd ({rrd_filename})"
    # first_timestamp = str(get_first_timestamp_rrd(rrd_filename)['first_timestamp'])
    first_timestamp = inspect_rrd(rrd_filename)['first_real_value']
    last_timestamp = str(get_last_timestamp_rrd(rrd_filename)['last_timestamp'])
    last_value = get_last_update_rrd(rrd_filename)
    last_value_date_human = str(last_value['last_value']['date'])
    last_value_valuepair = last_value['last_value']['ds']
    image_filename_rrd = f"{image_filename}_{last_timestamp}_by_rrd.png"
    # key = last_value_rrd_valuepair.items()
    last_value_valuepair_ds = str(list(last_value_valuepair.keys())[0])
    last_value_valuepair_value = str(last_value_valuepair[last_value_valuepair_ds])
    print("last_value_rrd_valuepair_ds", last_value_valuepair_ds)
    print("last_value_valuepair_value", last_value_valuepair_value)
    print(f"first_timestamp:{first_timestamp}")
    print(f"last_timestamp:{last_timestamp}")
    print(f"last_value:{last_value_date_human}")
    print(f"last_value_pair:{last_value_valuepair}")
    print(f"first_timestamp:{type(first_timestamp)}")
    print(f"last_timestamp:{type(last_timestamp)}")
    print(f"last_value:{type(last_value_date_human)}")
    job_status = grapher_rrd(rrd_filename, devicename, image_filename_rrd, "PNG", '1589947213', last_timestamp, last_value_date_human, last_value_valuepair_value)
    print(job_status)
    logger.i(job_status)

def main_():
    # in this section all basic variables are set
    # set a var as a string for logging purpose
    # for logging purposes
    l = Logger("csv2rrd.log")
    job_status = "---------CSV2RRD---------"
    l.i(job_status)
    # check if there is an existing csv-file
    csv_exists = None
    # default path for csv is set
    rrdtool_filename = "sma_garage"
    # comented pathes are the default locations for pathes of cacti on ubuntu
    rrd_filename = f"./rrd/{rrdtool_filename}.rrd" #f"/opt/cacti/rra/{rrdtool_filename}.rrd"#
    rrd_heartbeat = "300"
    csv_devicename = "rrd"
    image_filename = f"./rrd/graph/{rrdtool_filename}"#f"/opt/cacti/graphes/{rrdtool_filename}"#

    # if there no args existing the function will return false: otherwise it will return a list of filenames
    # set filename: differentiate between 0 args or 1 arg or 1 arg with regex
    # if the path of csv_file exist set this path as default otherwise do not use read_csv
    #if(file_exists(csv_file)!=None):
    start_cug_dependent_of_csv(rrd_filename, rrd_heartbeat, csv_devicename, image_filename, rrdtool_filename, l)
    #generate_graph_by_rrd(rrd_filename, csv_devicename, image_filename, l)

main_()
