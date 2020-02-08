import heartandsole # an example of fitparse
def read_heartandsole(input_file):
    log.info(f'opening {input_file}')
    fit = heartandsole.FitFileReader(input_file)
    # activity = heartandsole.Activity(fit.data)
