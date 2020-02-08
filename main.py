import typing
import logging
from logging_setup import setup_logging
import fitparse
import argparse
from typing import Tuple, Dict

import pytz
from datetime import datetime
from global_params import fit_timezone

import pandas as pd

# from fitdecode_test import read_fitdecode
# from heartdecode_test import read_heartdecode

log = logging.getLogger(__name__)


def file_to_dataframe(input_file):
    log.info(f'opening {input_file}')
    fitfile = fitparse.FitFile(input_file)
    records = list(fitfile.get_messages('record'))

    rows_list = []
    for record in records:
        values, units = record_dump(record)

        merged = {**values, **units}
        rows_list.append(merged)

        # for k, v in values.items():
        #     print(f'{k}: {v}')
        # print('\n')

    return pd.DataFrame(rows_list)


def record_dump(record) -> Tuple[Dict, Dict]:
    """
    Go through all the data entries in this record

    TODO: move timestamp at the beginning
    """
    # get values
    record_values = {
        data.name: data.value for data in record
    }
    record_units = {
        data.name+'_units': data.units for data in record
    }

    return record_values, record_units


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


def app(input_file, **kwargs):
    if 'dump' in kwargs and kwargs['dump'] is True:
        df = file_to_dataframe(input_file)
        print(df.head()['timestamp'])
    else:
        read_fitparse(input_file)


if __name__ == "__main__":
    setup_logging()
    log.debug("Starting")

    parser = argparse.ArgumentParser(description='read fit file')
    parser.add_argument('input_file', metavar='file', type=str, nargs=1,
                        help='input fit file')

    parser.add_argument("--dump", help="dump complete file",
                        action="store_true")

    args = parser.parse_args()
    args_dict = vars(args)
    args_dict['input_file'] = args_dict['input_file'][0]
    app(**vars(args))
