from datetime import datetime, timedelta
import logging
from sortedcontainers import SortedList, SortedSet, SortedDict
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
import json
import pickle

key_value_pair = {}
zdata_store = {}
timeout_key = {}
value_score_map = {}
logger = logging.getLogger(__name__)

def add_key_value(key, value):
    key_value_pair[key]=[]
    key_value_pair[key].append(value)
    return

def get_value_for_key(key):
    load_data_on_start()
    try:
        return key_value_pair[key][0]
    except Exception as e:
        logger.exception('Error: '+str(e))

def set_expiry_time(key, timeout):
    timeout_key[key] = datetime.now() + timedelta(seconds=timeout)
    return

def delete_key_value():
    for key, value in timeout_key.items():
        if datetime.now() > value:
            try:
                if key in key_value_pair.keys():
                    del key_value_pair[key]
                elif key in zdata_store.keys():
                    del zdata_store[key]
                elif key in value_score_map.keys():
                    del value_score_map[key]
            except Exception as e:
                logger.exception("Error:"+str(e))
    return

def store_zdata(key, data):
    n = len(data)
    if key not in zdata_store:
        zdata_store[key] = SortedDict()
    if key not in value_score_map:
        value_score_map[key] = {}
    cnt = 0
    for i in range(0,n,2):
        if data[i+1] in value_score_map[key].keys():
            temp = value_score_map[key][data[i+1]]
            if len(zdata_store[key][temp]) > 1:
                idx = zdata_store[key][temp].index(data[i+1])
                del zdata_store[key][temp][idx]
            elif len(zdata_store[key][temp]) == 1:
                del zdata_store[key][temp]
        value_score_map[key][data[i+1]] = data[i]
        if data[i] not in zdata_store[key]:
            zdata_store[key][data[i]] = SortedList()
        if data[i+1] not in zdata_store[key][data[i]]: 
            zdata_store[key][data[i]].add(data[i+1])
        cnt = cnt + 1
    print(value_score_map)
    print(zdata_store)
    return cnt

def get_rank_for_value(key, value):
    cnt = 0
    for i, j in zdata_store[key].items():
        if value in j:
            # return int(list(zdata_store[key].keys()).index(str(i)))+j.index(value)
            return cnt + j.index(value)
        cnt = cnt + len(j)
    return 'nil'

def get_values_for_range(key, start, stop):
    target = list(zdata_store[key].values())
    print(target)
    print(len(target))
    if stop < 0:
        return target[start:stop+len(target)+1]
    elif start < 0 and stop < 0:
        print("HIII")
        return target[start+len(target)+1:stop+len(target)+1]
    else:
        return target[start:stop]


def save_data_in_disk():
    with open('key_value_pair.pkl', 'wb') as fp:
        pickle.dump(key_value_pair, fp)
    with open('zdata_store.pkl', 'wb') as fp:
        pickle.dump(zdata_store, fp)
    with open('timeout_key.pkl', 'wb') as fp:
        pickle.dump(timeout_key, fp)
    with open('value_score_map.pkl', 'wb') as fp:
        pickle.dump(value_score_map, fp)

def load_data_on_start():
    global key_value_pair, zdata_store, timeout_key, value_score_map
    with open('key_value_pair.pkl', 'rb') as fp:
        key_value_pair = pickle.load(fp)
    with open('zdata_store.pkl', 'rb') as fp:
        zdata_store = pickle.load(fp)
    with open('timeout_key.pkl', 'rb') as fp:
        timeout_key = pickle.load(fp)
    with open('value_score_map.pkl', 'rb') as fp:
        value_score_map =  pickle.load(fp)
    # scheduler.remove_job('1')


def add_jobs():
    scheduler.start()
    # job = scheduler.add_job(load_data_on_start, 'interval', seconds=1, id='1',replace_existing=False)
    load_data_on_start()
    job = scheduler.add_job(save_data_in_disk,'interval' , seconds=10, replace_existing=False)
    job = scheduler.add_job(delete_key_value, 'interval' , seconds=6, replace_existing=True)
    