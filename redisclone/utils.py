from datetime import datetime, timedelta
import logging
from sortedcontainers import SortedList, SortedSet, SortedDict
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
import json


key_value_pair = {}
zdata_store = {}
timeout_key = {}
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
            except Exception as e:
                logger.exception("Error:"+str(e))
    return

def store_zdata(key, data):
    n = len(data)
    if key not in zdata_store:
        zdata_store[key] = SortedDict()
    cnt = 0
    for i in range(0,n,2):
        if data[i] not in zdata_store[key]:
            zdata_store[key][data[i]] = SortedSet()
        if data[i+1] not in zdata_store[key][data[i]]: 
            zdata_store[key][data[i]].add(data[i+1])
        cnt = cnt + 1
    print(zdata_store)
    return cnt

def get_rank_for_value(key, value):
    for i, j in zdata_store[key].items():
        if value in j:
            return i
    return 'nil'

def get_values_for_range(key, start, stop):
    target = list(zdata_store[key].values())
    print(target)
    if stop <0:
        return target[start:stop+len(target)+1]
    else:
        return target[start:stop]


def save_data_in_disk():
    with open('key_value_pair.json', 'w') as fp:
        json.dump(key_value_pair, fp)
    with open('zdata_store.json', 'w') as fp:
        json.dump(zdata_store, fp)
    with open('timeout_key.json', 'w') as fp:
        json.dump(timeout_key, fp, default=str)

def load_data_on_start():
    global key_value_pair, zdata_store, timeout_key
    with open('key_value_pair.json', 'r') as fp:
        key_value_pair = json.load(fp)
    with open('./zdata_store.json', 'r') as fp:
        zdata_store = json.load(fp)
    with open('./timeout_key.json', 'r') as fp:
        timeout_key = json.load(fp)
    scheduler.remove_job('1')


def add_jobs():
    scheduler.start()
    job = scheduler.add_job(load_data_on_start, 'interval', seconds=1, id='1', max_instances=1,replace_existing=True)
    job = scheduler.add_job(save_data_in_disk,'interval' , seconds=10, replace_existing=False)
    job = scheduler.add_job(delete_key_value, 'interval' , seconds=6, replace_existing=True)