import logging
import fitparse
import pandas as pd
import pytz
from typing import Tuple, Dict, Iterator, Union

from garmin_fit_eda.logging_setup import setup_logging
from garmin_fit_eda.global_params import fit_timezone

log = logging.getLogger(__name__)


def file_to_dataframe(input_file: str) -> pd.DataFrame:
    """
    Record message to Pandas DataFrame

    :param input_file: str
    :return: Pandas DataFrame
    """
    log.info(f'opening {input_file}')
    fitfile = fitparse.FitFile(input_file)

    return messages_to_dataframe(fitfile.get_messages('record'))


def messages_to_dataframe(msg_list: Union[Tuple, Iterator],
                          dump_units=False) -> pd.DataFrame:
    rows_list = []
    for msg in msg_list:
        values = message_dump(msg, dump_units)

        rows_list.append(values)
    df = pd.DataFrame(rows_list)
    df = df.reindex(sorted(df.columns), axis=1)
    return df


def message_dump(msg, dump_units=False) -> Dict:
    """
    Go through all the data entries in this record

    """
    # get values
    data_values = {
        data.name: data.value for data in msg
        if data.value is not None
    }

    if dump_units:
        data_units = {
            data.name+'_units': data.units for data in msg
            if data.units is not None
            and data.value is not None
        }
    else:
        data_units = {}

    return {**data_values, **data_units}


def read_fitparse(input_file):
    log.info(f'opening {input_file}')
    fitfile = fitparse.FitFile(input_file)
    records = list(fitfile.get_messages('record'))

    local_tz = pytz.timezone('Europe/Rome')
    fmt = "%Y-%m-%d %H:%M:%S"

    for record in records:
        # all timestamps are in UTC
        timestamp = fit_timezone.localize(record.get('timestamp').value)
        local_timestamp = timestamp.astimezone(local_tz)
        speed_mt_sec = record.get('enhanced_speed').value
        if speed_mt_sec == 0.0:
            speed_min_km = 0.0
        else:
            speed_min_km = 1000.0/60.0 * 1.0 / speed_mt_sec

        #  speed_units = record.get('enhanced_speed').units
        print(f'[{local_timestamp.strftime(fmt)}] {speed_min_km}')
