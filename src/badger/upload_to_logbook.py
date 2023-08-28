import os
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
from .settings import read_value
from .archive import BADGER_ARCHIVE_ROOT
from ibpt.elog import Elog
from ibpt.epics import get_pv
from .logbook import screenshot
logbook = Elog('Injection Optimization')


# Check badger logbook root
BADGER_LOGBOOK_ROOT = read_value('BADGER_LOGBOOK_ROOT')
if BADGER_LOGBOOK_ROOT is None:
    raise Exception('Please set the BADGER_LOGBOOK_ROOT env var!')
elif not os.path.exists(BADGER_LOGBOOK_ROOT):
    os.makedirs(BADGER_LOGBOOK_ROOT)
    logger.info(
        f'Badger logbook root {BADGER_LOGBOOK_ROOT} created')


def upload_to_elog(routine, data, widget=None):
    from xml.etree import ElementTree

    obj_names = [next(iter(d))
        for d in routine['config']['objectives']]


    data_path = BADGER_ARCHIVE_ROOT
    obj_name = obj_names[0]
    obj_start = data[obj_name][0]
    obj_end = data[obj_name][-1]

    # Puts relevant routine information into dictionary 
    hashmap = {}
    hashmap["Fill Number"] = get_pv("A:SR:OperationStatus:01:FillNumber")
    hashmap["Environment"] = routine['env']
    hashmap["Start Time"] = data['timestamp_raw'][0]
    hashmap["End Time"] = data['timestamp_raw'][-1]
    hashmap["Actuators"] = str(routine['config']['variables'])
    hashmap["Objective"] = str(routine['config']['objectives'])
    hashmap["Optimizer"] = routine['algo']


    # Generates screenshot from xml data
    curr_time = datetime.now()
    if os.name == 'nt':
        timestr = curr_time.strftime('%Y-%m-%dT%H%M%S')
    else:
        timestr = curr_time.strftime('%Y-%m-%dT%H:%M:%S')
    log_entry = ElementTree.Element(None)
    metainfo = ElementTree.SubElement(log_entry, 'metainfo')
    metainfo.text = timestr + '-00.xml'
    BADGER_LOGBOOK_ROOT = read_value('BADGER_LOGBOOK_ROOT')
    fileName = os.path.join(BADGER_LOGBOOK_ROOT, metainfo.text)
    fileName = fileName.rstrip('.xml')
    screenshot(widget, f'{fileName}.png')

    array = [f'{fileName}.png', f'{fileName}.xml']

    logbook.post(
        f"Automatic Badger optimization: {routine['name']}", 
        attributes = hashmap, 
        attachments = array
    )