from visitors._abstract_visitor import AbstractVisitor
from util.os_util import OSName
import os
import logging
import glob


class AppVisitor(AbstractVisitor):

    def __init__(self):
        os_name = OSName.by_current_platform()
        self.__path_sign = "\\" if os_name == OSName.WINDOWS else "/"

    def visit(self, apps):
        results = {}
        for app in apps:
            try:
                app_name = app['name']
            except KeyError:
                logging.warning(f"Invalid app: cannot find app name in {app}")
                continue

            try:
                file_name = app['fileName']
            except KeyError:
                logging.warning(f"Invalid app: cannot find filename in {app}")
                continue

            try:
                app_locations = app['locations']
            except KeyError:
                logging.warning(f"Invalid app: cannot find app locations in {app}")
                continue

            for app_location in app_locations:
                logging.info(f"Searching for {app_name} in {app_location}")

                if app_location.find("*") == -1:
                    self._search_by_full_locations(app_location, app_name, file_name, results)
                else:
                    self._search_by_pattern(app_location, app_name, file_name, results)

        return results

    def _search_by_full_locations(self, app_location, app_name, file_name, results):
        try:
            files_in_location = os.listdir(app_location)
        except FileNotFoundError:
            return
        for file_in_location in files_in_location:
            if file_in_location == file_name:
                self._report(app_name, file_name, app_location, results)

    def _search_by_pattern(self, app_location, app_name, file_name, results):
        pattern = app_location
        if not pattern.endswith(self.__path_sign):
            pattern = pattern + self.__path_sign
        pattern = pattern + file_name
        locations_by_pattern = glob.glob(pattern)
        for _ in locations_by_pattern:
            self._report(app_name, file_name, app_location, results)

    def _report(self, app_name, file_name, app_location, results) -> None:
        logging.info(f"Found {app_name} ({file_name}) in {app_location}")
        if not app_location.endswith(self.__path_sign):
            app_location = app_location + self.__path_sign
        file_and_location = app_location + file_name
        if app_name in results:
            results[app_name].append(file_and_location)
        else:
            results[app_name] = [file_and_location]

