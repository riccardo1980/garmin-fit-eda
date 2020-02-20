import argparse
import logging
import os
import pandas as pd
import fitparse
from garmin_fit_eda.logging_setup import setup_logging
from garmin_fit_eda.file_reader import messages_to_dataframe

log = logging.getLogger(__name__)


def app(input_file, output_folder, dump_units=False):
    try:
        fitfile = fitparse.FitFile(input_file)
    except Exception as e:
        log.error(e)
        raise

    msg_types = set([message.name for message in fitfile.get_messages()])

    for msg_type in set(msg_types):
        df = messages_to_dataframe(
            fitfile.get_messages(msg_type),
            dump_units=False
        )
        df.to_html(os.path.join(output_folder, msg_type+'.html'))


if __name__ == "__main__":
    setup_logging()
    log.debug("Starting")

    parser = argparse.ArgumentParser(description='read fit file')
    parser.add_argument('input_file', metavar='file', type=str, nargs=1,
                        help='input fit file')

    parser.add_argument('--output_folder', type=str,
                        help='output folder')

    parser.add_argument('--dump_units', action='store_true')

    args = parser.parse_args()
    args_dict = vars(args)
    args_dict['input_file'] = args_dict['input_file'][0]

    if args_dict['output_folder'] is None:
        args_dict['output_folder'] = os.path.split(args_dict['input_file'])[1]

    log.info(args_dict)
    try:
        os.mkdir(args_dict['output_folder'])
        app(**args_dict)
    except Exception as e:
        log.error(e)
        exit(-1)
