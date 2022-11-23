import logging
import json
import os
import time
import argparse

from typing import Final

from util.os_name import OSName
from visitors.app_visitor import AppVisitor
from visitors.browser_visitor import BrowserVisitor

CONFIG_PATH: Final = "./config"
CONFIG_EXT: Final = ".json"
CONFIG_GLOB_PATTERN: Final = f"*{CONFIG_EXT}"
REPORT_FILE_NAME: Final = "report.json"
REPORT_PREFIX: Final = "report_"
REPORTS_DIR: Final = "reports"
REPORT_SCREENSHOTS_DIR: Final = "screenshots"


class Krex:

    def __init__(self):
        self.__files_and_directories = os.listdir(CONFIG_PATH)
        self.__app_visitor = AppVisitor()
        self.__browser_visitor = BrowserVisitor(REPORT_PREFIX)
        self.__set_custom_configs()

    def start(self):
        files_and_directories = []
        if self.__custom_configs is None:
            for file_or_directory in self.__files_and_directories:
                files_and_directories.append(f"{CONFIG_PATH}/{file_or_directory}")
        else:
            files_and_directories = self.__custom_configs

        for file_or_directory in files_and_directories:
            if not file_or_directory.endswith(CONFIG_EXT):
                continue
            try:
                config = self.__read_config_file(file_or_directory)
                if config is not None:
                    results = self.__visit(config)
                    results_json = json.dumps(results, sort_keys=True, indent=4)
                    self.__report(results_json)
            except FileNotFoundError as e:
                logging.error(e)

    def __set_custom_configs(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-config', '--config')
        args = parser.parse_args()
        custom_configs_args = args.config
        if custom_configs_args:
            custom_configs_raw = custom_configs_args.split(',')
            custom_configs_filtered = []
            for custom_config in custom_configs_raw:
                if custom_config.endswith(CONFIG_EXT):
                    custom_configs_filtered.append(custom_config)
            self.__custom_configs = custom_configs_filtered
        else:
            self.__custom_configs = None

    def __read_config_file(self, file_or_directory) -> str | None:
        logging.info(f"Executing config file {file_or_directory}")
        with open(file_or_directory, "r") as file:
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
        app_results = self.__visit_apps(config)
        if app_results is not None and len(app_results) > 0:
            results.append(app_results)
        browser_results = self.__visit_browsers(config)
        if browser_results is not None and len(browser_results) > 0:
            results.append(browser_results)
        return results

    def __visit_apps(self, config) -> dict:
        try:
            apps = config['apps']
            app_results = self.__app_visitor.visit(apps)
            return app_results
        except KeyError:
            logging.debug("Skip app visits since there are none")
            pass

    def __visit_browsers(self, config) -> dict:
        try:
            browsers = config['browsers']
            browser_results = self.__browser_visitor.visit(browsers)
            return browser_results
        except KeyError:
            logging.debug("Skip browser visits since there are none")
            pass

    def __report(self, results_json) -> None:
        current_time = time.time()
        report_location = os.path.join(os.getcwd(), REPORTS_DIR, f"{REPORT_PREFIX}{current_time}")
        os.mkdir(report_location)

        time.sleep(2)

        with open(os.path.join(report_location, REPORT_FILE_NAME), "w") as fh:
            fh.write(results_json)

        cwd = os.getcwd()
        files = os.listdir(cwd)
        for file in files:
            if file.startswith(REPORT_PREFIX):
                screenshots_dir = os.path.join(report_location, REPORT_SCREENSHOTS_DIR)
                if not os.path.isdir(screenshots_dir):
                    os.mkdir(screenshots_dir)

                os.replace(os.path.join(cwd, file), os.path.join(report_location, REPORT_SCREENSHOTS_DIR, file))

        print(f"Report saved to {report_location}")


krex = Krex()
krex.start()




