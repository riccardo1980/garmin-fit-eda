import fitdecode # no examples

def read_fitdecode(input_file):
    log.info(f'opening {input_file}')
    with fitdecode.FitReader(input_file) as fit:
        for frame in fit:
            # The yielded frame object is of one of the following types:
            # * fitdecode.FitHeader
            # * fitdecode.FitDefinitionMessage
            # * fitdecode.FitDataMessage
            # * fitdecode.FitCRC

            if isinstance(frame, fitdecode.FitDataMessage):
                # Here, frame is a FitDataMessage object.
                # A FitDataMessage object contains decoded values that
                # are directly usable in your script logic.
                log.info(frame.name)