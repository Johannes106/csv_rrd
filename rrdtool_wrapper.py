# actions of rrdtool
# wrapper for the actions of the rrdtool
# - create a round-robin-database
# - update the rrd:
#   - with a single value
#   - with a list of values (in form of -> time:value)
# - create a graph of rrd
import sys
import rrdtool
import os.path
from os import path
from datetime import datetime


def convert_timestamp_to_date(timestamp):
    date_timestamp_obj = datetime.fromtimestamp(timestamp)
    return(date_timestamp_obj)

# get the first timestamp which have a value of numbers
# iterate over a already defined database and look for values which are not 'none'


def look_for_real_values(fetch_data, start, fetch_data_heartbeat):
    array_real_values = []
    fetch_data_timestamp = int(start)
    # print(f"fetch_data_timestamp{type(fetch_data_timestamp)}{fetch_data_timestamp}")
    for fetch_data_entry in fetch_data:
        fetch_data_content = str(fetch_data_entry[0])
        if(fetch_data_content != 'None'):
            string_real_values = f"[{fetch_data_timestamp}][{fetch_data_content}]"
            array_real_values.append(string_real_values)
        fetch_data_timestamp = fetch_data_timestamp + int(fetch_data_heartbeat)
    return array_real_values


def creator_rrd(rrdfile_name, starttime, step):
    create_status_msg = ""
    try:
        rrdtool.create(
            rrdfile_name,
            "--start", starttime,
            "--step", step,
            "DS:etoday:GAUGE:600:0:50000",
            "RRA:AVERAGE:0.5:1:600",  # 5  min
            "RRA:AVERAGE:0.5:6:700",  # 30 min
            "RRA:AVERAGE:0.5:24:775",  # 2  std
            "RRA:AVERAGE:0.5:288:797",  # 1 day
            "RRA:MIN:0.5:1:600",
            "RRA:MIN:0.5:6:700",
            "RRA:MIN:0.5:24:775",
            "RRA:MIN:0.5:288:797",
            "RRA:MAX:0.5:1:600",
            "RRA:MAX:0.5:6:700",
            "RRA:MAX:0.5:24:775",
            "RRA:MAX:0.5:288:797",
            "RRA:LAST:0.5:1:600",
            "RRA:LAST:0.5:6:700",
            "RRA:LAST:0.5:24:775",
            "RRA:LAST:0.5:288:797")
        create_status_msg = f"{rrdfile_name} was created successfully"
    except Exception as e:
        create_status_msg = f"rrd creation error: {sys.exc_info()[1]} \n{e}"
    return create_status_msg


def updater_rrd(rrdfile_name, value):
    # is the given value a list
    if(isinstance(value, list)):
        # iterate over the list
        counter = 0
        update_status_msg = ""
        for entry in value:
            try:
                rrdtool.update(rrdfile_name, entry)
                update_status_msg = f"success: {rrdfile_name} was updated successfully"
                counter = counter + 1
            except Exception as e:
                update_status_msg = f"error: rrd update error: {sys.exc_info()[1]}, \n{e}"
    else:
        try:
            rrdtool.update(rrdfile_name, value)
            update_status_msg = f"success: {rrdfile_name}: was updated successfully"
        except Exception as e:
            update_status_msg = f"error: rrd update error: {sys.exc_info()[1]} \n{e}"
    return update_status_msg


def info_rrd(rrdfile_name):
    info_content = []
    info_status_msg = ""
    # get the last value
    try:
        db_info = rrdtool.info(rrdfile_name)
        info_content = db_info
        info_status_msg = f"success: {rrdfile_name}: was read successfully"
    except Exception as e:
        info_status_msg = f"error: rrd update error: {sys.exc_info()[1]} \n{e}"
    info_msg = dict()
    info_msg['data'] = info_content
    info_msg['status'] = info_status_msg
    return info_msg


def get_first_timestamp_rrd(rrdfile_name):
    first_timestamp = []
    get_first_status_msg = ""
    # is the given file a rrd
    try:
        db_first_timestamp = rrdtool.first(rrdfile_name)
        get_first_status_msg = f"success: first timestamp of {rrdfile_name} was found"
    except Exception as e:
        get_first_status_msg = f"error: get_first_timestamp_rrd({rrdfile_name}) was not possible: {sys.exc_info()[1]} \n{e}"
    get_first_msg = dict()
    get_first_msg['first_timestamp'] = db_first_timestamp
    get_first_msg['status'] = get_first_status_msg
    return get_first_msg


def get_last_timestamp_rrd(rrdfile_name):
    last_timestamp = []
    get_last_status_msg = ""
    try:
        db_last_timestamp = rrdtool.last(rrdfile_name)
        get_last_status_msg = f"success: last timestamp of {rrdfile_name} was found"
    except Exception as e:
        get_last_status_msg = f"error: get_last_timestamp_rrd({rrdfile_name}) was not possible: {sys.exc_info()[1]} \n{e}"
    get_last_msg = dict()
    get_last_msg['last_timestamp'] = db_last_timestamp
    get_last_msg['status'] = get_last_status_msg
    return get_last_msg


def get_last_update_rrd(rrdfile_name):
    last_value = []
    get_last_update_status_msg = ""
    try:
        db_last_value = rrdtool.lastupdate(rrdfile_name)
        get_last_update_status_msg = f"success: last value of {rrdfile_name} was found"
    except Exception as e:
        get_last_update_status_msg = f"error: get_last_value_rrd({rrdfile_name}) was not possible: {sys.exc_info()[1]} \n{e}"
    get_last_value_msg = dict()
    get_last_value_msg['last_value'] = db_last_value
    get_last_value_msg['status'] = get_last_update_status_msg
    return get_last_value_msg


def fetch_rrd(rrdfile_name, cf, start, end):
    fetch_content = []
    fetch_status_msg = ""
    fetch_data = ""
    fetch_data_value = ""
    fetch_data_value_first = ""
    fetch_data_first_real_value = 0
    try:
        db_values = rrdtool.fetch(rrdfile_name,
                                  cf,
                                  '--start', start,
                                  '--end', end
                                  )
        fetch_data_heartbeat = db_values[0][2]
        fetch_data = db_values[2]
        fetch_data_first_real_value = look_for_real_values(
            fetch_data, start, fetch_data_heartbeat)[0]
        # print(f"fetch_data_first_real_value{type(fetch_data_first_real_value)}{fetch_data_first_real_value}")
        fetch_status_msg = f"success: {rrdfile_name}: was fetched successfully"
    except Exception as e:
        fetch_status_msg = f"error: rrd fetch error: {sys.exc_info()[1]} \n{e}"
        print("fetch error")
    fetch_msg = dict()
    fetch_msg['data'] = fetch_data
    fetch_msg['first_real_value'] = fetch_data_first_real_value
    fetch_msg['status'] = fetch_status_msg
    return fetch_msg


def grapher_rrd(rrd_filename, devicename, image_name, image_typ, starttime, endtime, last_time, last_update):
    last_time_date_format_de = (last_time.split(' ')[0]).replace('/', '.')
    last_time_time = last_time.split(' ')[1]
    last_time_time_point = last_time_time.replace(':', '.')
    starttime_date_string = str(convert_timestamp_to_date(int(starttime)))
    starttime_date_point = starttime_date_string.replace(':', '.')
    # print(f"grapher_rrd: starttime_date_point {type(starttime_date_point)}:{starttime_date_point}")
    string_from_to = f"From {starttime_date_point} To {last_time_date_format_de} {last_time_time_point}"
    graph_status_msg = ""
    rrd_def = f"DEF:kwh_etoday={rrd_filename}:etoday:AVERAGE"
    try:
        rrdtool.graph(image_name,
                      '--width', '740',
                      '--height', '300',
                      '--imgformat', image_typ,
                      '--start', starttime,
                      '--end', endtime,
                      '--font', "DEFAULT:7",
                      '--title', f"{devicename}: Generated Energy of {last_time_date_format_de}: {last_update}kwh",
                      '--watermark', "date",
                      '--vertical-label', "kwh",
                      '--right-axis-label', f"last update time: {last_time_time}",
                      f"{rrd_def}",
                      "LINE2:kwh_etoday#FF0000", f"COMMENT: {string_from_to}"
                      )
        graph_status_msg = f"success: {image_name} was successfully generated"
    except Exception as e:
        graph_status_msg = f"error: rrd graph error: {sys.exc_info()[1]} \nargs: {type(rrd_filename)}:{rrd_filename}, {type(devicename)}:{devicename}, {type(image_name)}:{image_name}, {type(image_typ)}:{image_typ}, {type(starttime)}:{starttime}, {type(endtime)}:{endtime}, {type(last_time)}:{last_time}, {type(last_update)}:{last_update} \n{e}"
    return graph_status_msg
