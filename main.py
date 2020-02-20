import argparse
import logging

from garmin_fit_eda.logging_setup import setup_logging
from garmin_fit_eda.file_reader import (
    file_to_dataframe, read_fitparse
)


log = logging.getLogger(__name__)


def app(input_file, **kwargs):
    if 'dump' in kwargs and kwargs['dump'] is True:
        df = file_to_dataframe(input_file)
        print(df[['timestamp', 'position_lat', 'position_long']].head())
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

    try:
        os.mkdir(args_dict['output_folder'])
        app(**args_dict)
    except Exception as e:
        log.error(e)
        exit(-1)
