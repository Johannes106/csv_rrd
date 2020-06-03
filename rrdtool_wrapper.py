# actions of rrdtool
# wrapper for the actions of the rrdtool
# - create a round-robin-database
# - update the rrd:
#   - with an single value
#   - with a list of values (in form of -> time:value)
# - create a graph of rrd
import sys
import rrdtool
import os.path
from os import path

def creator_rrd(rrdfile_name, starttime, step):
    create_status_msg = ""
    try:
        rrdtool.create(
            rrdfile_name,
            "--start", starttime,
            "--step", step,
            # "DS:etoday:GAUGE:600:0:50000",
            # "RRA:AVERAGE:0.5:1:200",
            # "RRA:AVERAGE:0.5:200:7",
            # "RRA:AVERAGE:0.5:1400:4",
            # "RRA:AVERAGE:0.5:5200:12",
            # "RRA:AVERAGE:0.5:62400:10")
            "DS:etoday:GAUGE:600:0:50000",
            "RRA:AVERAGE:0.5:1:600",
            "RRA:AVERAGE:0.5:6:700",
            "RRA:AVERAGE:0.5:24:775",
            "RRA:AVERAGE:0.5:288:797",
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
    except:
        create_status_msg = f"rrd creation error: {sys.exc_info()[1]}"
    return create_status_msg

def updater_rrd(rrdfile_name, value):
    #is the given value a list
    if(isinstance(value, list)):
        #iterate over the list
        counter = 0
        update_status_msg = ""
        for entry in value:
            try:
                rrdtool.update(rrdfile_name, entry)
                update_status_msg = f"success: {rrdfile_name} was updated successfully"
                counter = counter + 1
            except:
                update_status_msg = f"error: rrd update error: {sys.exc_info()[1]}"
                # raise
    else:
        try:
            rrdtool.update(rrdfile_name, values)
            update_status_msg = f"success: {rrdfile_name}: was updated successfully"
        except:
            update_status_msg = f"error: rrd update error: {sys.exc_info()[1]}"
    return update_status_msg

def info_rrd(rrdfile_name):
    info_content = []
    info_status_msg = ""
    #is the given file a rrd
    try:
        db_info = rrdtool.info(rrdfile_name)
        info_content = db_info
        # print(db_info)
        info_status_msg = f"success: {rrdfile_name}: was read successfully"
    except:
        info_status_msg = f"error: rrd update error: {sys.exc_info()[1]}"
    info_msg = dict()
    info_msg['data'] = info_content
    info_msg['status'] = info_status_msg
    return info_msg

def fetch_rrd(rrdfile_name):
    fetch_content = []
    fetch_status_msg = ""
    #is the given file a rrd
    try:
        db_values = rrdtool.fetch(rrdfile_name, "AVERAGE")
        # start, end, step = result[0]
        # ds = result[1]
        # rows = result[2]
        fetch_times = db_values[0]
        fetch_status_msg = f"success: {rrdfile_name}: was fetched successfully"
    except:
        fetch_status_msg = f"error: rrd fetch error: {sys.exc_info()[1]}"
        print("fetch error")
    fetch_msg = dict()
    fetch_msg['times'] = fetch_times
    fetch_msg['status'] = fetch_status_msg
    return fetch_msg


def grapher_rrd(rrd_filename, devicename, image_name, image_typ, starttime, endtime, last_time, last_update):
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
                      '--title', f"{devicename}: Generated Energy of {(last_time.split(' ')[0]).replace('/', '.')}: {last_update}kwh",
                      '--watermark', "date",
                      '--vertical-label', "kwh",
                      '--right-axis-label', f"last update time: {last_time.split(' ')[1]}",
                      f"{rrd_def}",
                      "LINE2:kwh_etoday#FF0000",
                      'COMMENT:"From 2020/05/25 20\:17\:07 To 2020/05/26 20\:12\:07\c"')
        graph_status_msg = f"success: {image_name} was successfully generated"
    except:
        graph_status_msg = f"error: rrd graph error: {sys.exc_info()[1]}"
    return graph_status_msg
