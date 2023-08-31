import logging

logger = logging.getLogger(__name__)
from ibpt.elog import Elog
from ibpt.epics import get_pv

logbook = Elog("Injection Optimization")


def upload_to_elog(routine, data, fileName):
    # Puts relevant routine information into dictionary
    logbook_attributes = {}
    logbook_attributes["Fill Number"] = get_pv("A:SR:OperationStatus:01:FillNumber")
    logbook_attributes["Environment"] = routine["env"]
    logbook_attributes["Start Time"] = data["timestamp_raw"][0]
    logbook_attributes["End Time"] = data["timestamp_raw"][-1]
    logbook_attributes["Actuators"] = str(routine["config"]["variables"])
    logbook_attributes["Objective"] = str(routine["config"]["objectives"])
    logbook_attributes["Optimizer"] = routine["algo"]

    array = [f"{fileName}.png", f"{fileName}.xml"]

    logbook.post(
        f"Automatic Badger optimization: {routine['name']}",
        attributes=logbook_attributes,
        attachments=array,
    )
