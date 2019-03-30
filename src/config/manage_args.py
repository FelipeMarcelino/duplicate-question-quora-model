def manage_arguments(config_file, tokenization,input_filepath, output_filepath, interim_filepath ):
    if len(tokenization) == 0 :
        tokenization  = config_file["operations"]["tokenization"]
    if input_filepath is None:
        input_filepath = config_file["filepaths"]["input_filepath"]
    if output_filepath is  None:
        output_filepath = config_file["filepaths"]["output_filepath"]
    if interim_filepath is None:
        interim_filepath = config_file["filepaths"]["interim_filepath"]

    print(tokenization, config_file["operations"]["tokenization"])


