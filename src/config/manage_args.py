def manage_arguments(config_file, tokenization):
    if config_file["operations"]["tokenization"] is None:
        config_file["operations"]["tokenization"] = tokenization
