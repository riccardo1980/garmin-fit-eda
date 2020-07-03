import argparse
import logging
import os
import pandas as pd
import fitparse
from garmin_fit_eda.logging_setup import setup_logging
from garmin_fit_eda.file_reader import messages_to_dataframe

log = logging.getLogger(__name__)


def fit_to_html(input_file,
                output_folder,
                dump_units=False):
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

    parser = argparse.ArgumentParser(description='Dump fit file to html')
    parser.add_argument('input_file', metavar='file', type=str, nargs='+',
                        help='input fit file')

    parser.add_argument('--dump_units', action='store_true')

    parser.add_argument('--output_folder', default='./')

    args = parser.parse_args()
    args_dict = vars(args)

    try:
        for input_file in args_dict['input_file']:

            output_folder = os.path.join(
                args_dict['output_folder'], os.path.split(input_file)[1])
            os.makedirs(output_folder)

            log.info('dumping {} in {}'.format(input_file, output_folder))

            fit_to_html(input_file, output_folder,
                        dump_units=args_dict['dump_units'])
    except Exception as e:
        log.error(e, exc_info=True)
        exit(-1)
