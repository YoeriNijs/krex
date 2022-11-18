import pyautogui

from visitors._abstract_visitor import AbstractVisitor

import webbrowser
import logging
import time

class BrowserVisitor(AbstractVisitor):

    def __init__(self, report_prefix):
        self.__report_prefix = report_prefix
    def visit(self, browsers):
        results = {}
        for browser in browsers:
            try:
                browser_name = browser['name']
            except KeyError:
                logging.warning(f"Invalid browser: name property is missing in {browser}")
                continue

            try:
                urls = browser['urls']
            except KeyError:
                logging.warning(f"Invalid browser: urls property is missing {browser}")
                continue

            for url in urls:
                try:
                    link = url['link']
                except KeyError:
                    logging.warning(f"Invalid browser: link property is missing {browser}")
                    continue

                try:
                    name = url['name']
                except KeyError:
                    logging.warning(f"Invalid browser: name property is missing {browser}")
                    continue

                opened = webbrowser.get(browser_name).open_new(link)
                if opened:
                    try:
                        delay_in_ms = int(url['delay_in_ms'])
                    except [KeyError, TypeError]:
                        logging.warning(f"Skip delay since no valid delay value is provided in {browser}")
                        delay_in_ms = 0

                    time.sleep(delay_in_ms / 1000)

                    screenshot = pyautogui.screenshot()

                    screenshot_name = f"{self.__report_prefix}{browser_name}_{name}.png"
                    screenshot.save(screenshot_name)


                result = {
                    "link": link,
                    "opened": opened
                }
                if browser_name in results:
                    results[browser_name].append(result)
                else:
                    results[browser_name] = [result]

        return results
