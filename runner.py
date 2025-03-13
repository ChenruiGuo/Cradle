import argparse
import importlib

from cradle.config import Config
from cradle.gameio import GameManager
from cradle.log import Logger
from cradle.monitor import set_verbose

config = Config()
logger = Logger()


def main(args):

    # Choose shared or specific runner
    if config.env_shared_runner is not None and len(config.env_shared_runner) > 0:
        runner_key = config.env_shared_runner.lower()
    else:
        runner_key = config.env_short_name.lower()

    # Load the runner module
    runner_module = importlib.import_module(f'cradle.runner.{runner_key}_runner')
    entry = getattr(runner_module, 'entry')

    # Run the entry
    entry(args)


def get_args_parser():

    parser = argparse.ArgumentParser("Cradle Agent Runner")
    parser.add_argument("--llmProviderConfig", type=str, default="./conf/openai_config.json", help="The path to the LLM provider config file")
    parser.add_argument("--embedProviderConfig", type=str, default="./conf/openai_config.json", help="The path to the embedding model provider config file")
    parser.add_argument("--envConfig", type=str, default="./conf/env_config_outlook.json", help="The path to the environment config file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode (Cradle logs will show on Cradle Monitor)")
    return parser


if __name__ == '__main__':
    parser = get_args_parser()
    args = parser.parse_args()
    set_verbose(args.verbose)
    config.load_env_config(args.envConfig)
    config.set_fixed_seed()

    main(args)
