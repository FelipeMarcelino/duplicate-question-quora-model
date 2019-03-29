# -*- coding: utf-8 -*-
import logging
import os
import sys
from pathlib import Path

import click
import yaml
from dotenv import find_dotenv, load_dotenv

from dataset import Data

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "config"))

from manage_args import manage_arguments  # isort:skip


def CommandWithConfigFile(config_filepath_param_name):
    class CustomCommandClass(click.Command):
        def invoke(self, ctx):
            config_filepath = ctx.params[config_filepath_param_name]
            if config_filepath is not None:
                with open(config_filepath) as f:
                    config_data = yaml.safe_load(f)
                    for param, value in ctx.params.items():
                        if value is None and param in config_data:
                            ctx.params[param] = config_data[param]
                            break
                        for section in config_data:
                            if value is None and param in config_data[section]:
                                ctx.params[param] = config_data[section][param]

            return super(CustomCommandClass, self).invoke(ctx)

    return CustomCommandClass


@click.command(cls=CommandWithConfigFile("config_filepath"))
@click.option("--input_filepath","--if", type=click.Path(), default=None)
@click.option("--output_filepath","--of", type=click.Path(), default=None)
@click.option("--interim_filepath","--if",type=click.Path(), default=None)
@click.option("--config_filepath","--cf", type=click.Path(), default="./src/config/default.yaml")
@click.option("--tokenization","--to", multiple=True, default=None)
def main(input_filepath, output_filepath, interim_filepath, config_filepath, tokenization):
    """
    Turns raw data locate in .../raw into processed data locate in .../processed

    Keyword arguments:
    input_filepath -- filepath of raw/input data
    output_filepath -- filepath to put processed data
    interim_filepath -- filepath to interim/intermediary file
    config_filepath -- filepath to config_file used to set options executions
    tokenization -- columns to apply operation tokenization
    """
    logger = logging.getLogger(__name__)
    if interim_filepath is not None:
        logger.info("Making final data set from interim data: {0}".format(str(interim_filepath)))
    else:
        logger.info("Making final data set from raw data: {}".format(str(input_filepath)))
    logger.info("Processed file will be save in: {0}".format(str(output_filepath)))

    with open(config_filepath, "r") as stream:
        try:
            config_data = yaml.safe_load(stream)
            print(config_data)
        except yaml.YAMLError as exc:
            print(exc)

    # Manage arguments passed by user with config file yaml
    manage_arguments(config_data, tokenization)
    print(config_data)

    data = Data(input_filepath, output_filepath, config_data["operations"])


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    # pylint: disable=no-value-for-parameter
    main()
