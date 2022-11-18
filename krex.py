import logging
import json
import os

from typing import Final

from util.os_util import OSName
from visitors._app_visitor import AppVisitor

CONFIG_PATH: Final = "./config"
CONFIG_EXT: Final = ".json"
CONFIG_GLOB_PATTERN: Final = f"*{CONFIG_EXT}"


class Krex:

    def __init__(self):
        self.__files_and_directories = os.listdir(CONFIG_PATH)
        self.__app_visitor = AppVisitor()

    def start(self):
        for file_or_directory in self.__files_and_directories:
            if not file_or_directory.endswith(CONFIG_EXT):
                continue
            config = self.__read_config_file(file_or_directory)
            if config is not None:
                results = self.__visit(config)
                results_json = json.dumps(results, sort_keys=True, indent=4)
                print(results_json)

    def __read_config_file(self, file_or_directory) -> str | None:
        logging.info(f"Executing config file {file_or_directory}")
        with open(f"{CONFIG_PATH}/{file_or_directory}", "r") as file:
            json_file = json.load(file)
            try:
                json_os = OSName.by_name(json_file['os'])
                current_os = OSName.by_current_platform()
                if json_os == current_os:
                    return json_file
            except KeyError:
                logging.warning(f"Config file {file_or_directory} is empty, skip processing")

        return None

    def __visit(self, config) -> list:
        results = []
        return self.__visit_apps(config, results)

    def __visit_apps(self, config, results) -> list:
        try:
            apps = config['apps']
            app_results = self.__app_visitor.visit(apps)
            results.append(app_results)
        except KeyError:
            logging.debug("Skip app visits since there are none")
            pass
        return results

    def __visit_browsers(self, config, results) -> list:
        try:
            browsers = config['browsers']
            browser_results = self.__app_visitor.visit(browsers)
            results.append(browser_results)
        except KeyError:
            logging.debug("Skip browser visits since there are none")
            pass
        return results


krex = Krex()
krex.start()




