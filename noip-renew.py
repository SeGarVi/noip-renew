#!/usr/bin/env python3
# Copyright 2017 loblab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import sys
import os
import re


class Robot:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0"
    LOGIN_URL = "https://www.noip.com/login"
    HOST_URL = "https://my.noip.com/#!/dynamic-dns"

    def __init__(self, username, password, debug=0):
        self.debug = debug
        self.username = username
        self.password = password
        self.browser = self.init_browser()

    @staticmethod
    def init_browser():
        options = webdriver.ChromeOptions()
        # added for Raspbian Buster 4.0+ versions. Check https://www.raspberrypi.org/forums/viewtopic.php?t=258019
        options.add_argument("disable-features=VizDisplayCompositor")
        options.add_argument("headless")
        # options.add_argument("privileged")
        # options.add_argument("disable-gpu")
        options.add_argument("no-sandbox")  # need when run in docker
        options.add_argument("window-size=1200x800")
        options.add_argument("user-agent=%s" % Robot.USER_AGENT)
        if 'https_proxy' in os.environ:
            options.add_argument("proxy-server=" + os.environ['https_proxy'])
        browser = webdriver.Chrome(options=options)
        browser.set_page_load_timeout(60)
        return browser

    def log_msg(self, msg, level=None):
        time_string_formatter = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        if level is None:
            level = self.debug
        if level > 0:
            print("%s [%s] - %s" % (time_string_formatter, self.username, msg))

    def login(self):
        self.log_msg("Open %s..." % Robot.LOGIN_URL)
        self.browser.get(Robot.LOGIN_URL)
        if self.debug > 1:
            self.browser.save_screenshot("debug1.png")

        self.log_msg("Login...")
        ele_usr = self.browser.find_element_by_name("username")
        ele_pwd = self.browser.find_element_by_name("password")
        ele_usr.send_keys(self.username)
        ele_pwd.send_keys(self.password)
        # self.browser.find_element_by_name("login").click()
        form = self.browser.find_element_by_id("clogs")
        form.submit()
        if self.debug > 1:
            time.sleep(1)
            self.browser.save_screenshot("debug2.png")

    def update_hosts(self):
        count = 0

        self.open_hosts_page()
        time.sleep(1)
        iteration = 1

        hosts = self.get_hosts()
        for host in hosts:
            host_link = self.get_host_link(host, iteration)
            host_name = host_link.text
            expiration_days = self.get_host_expiration_days(host, iteration)

            self.log_msg(host_name + " expires in " + str(expiration_days) + " days")
            if expiration_days < 7:
                self.update_host(host_link, host_name)
                count += 1
            iteration += 1
        self.browser.save_screenshot("result.png")
        self.log_msg("Confirmed hosts: %d" % count, 2)
        return True

    def open_hosts_page(self):
        self.log_msg("Open %s..." % Robot.HOST_URL)
        try:
            self.browser.get(Robot.HOST_URL)
        except TimeoutException as e:
            self.browser.save_screenshot("timeout.png")
            self.log_msg("Timeout. Try to ignore")

    def update_host(self, host_link, host_name):
        self.log_msg("Updating " + host_name)
        host_link.click()
        time.sleep(3)
        self.browser.save_screenshot("modal_" + host_name + "_1.png")
        self.browser.find_elements_by_xpath("//button[contains(div,'Update Hostname')]")[0].click()
        time.sleep(3)
        self.browser.save_screenshot("modal" + host_name + "_2.png")

    @staticmethod
    def get_host_expiration_days(host, iteration):
        host_remaining_days = host.find_element_by_xpath(".//a[@class='no-link-style']").text
        regex_match = re.search("\d+", host_remaining_days)
        if regex_match is None:
            raise Exception("Expiration days label does not match the expected pattern in iteration " + iteration)
        expiration_days = int(regex_match.group(0))
        return expiration_days

    @staticmethod
    def get_host_link(host, iteration):
        return host.find_element_by_xpath(".//a[@class='text-info cursor-pointer']")

    def get_hosts(self):
        host_tds = self.browser.find_elements_by_xpath("//td[@data-title='Host']")
        if len(host_tds) == 0:
            raise Exception("No hosts or hos tds not found")
        return host_tds

    def run(self):
        rc = 0
        self.log_msg("Debug level: %d" % self.debug)
        try:
            self.login()
            if not self.update_hosts():
                rc = 3
        except Exception as e:
            self.log_msg(str(e), 2)
            self.browser.save_screenshot("exception.png")
            rc = 2
        finally:
            self.browser.quit()
        return rc


def main(argv=None):
    username, password, debug = get_args_values(argv)
    return (Robot(username, password, debug)).run()


def get_args_values(argv):
    if argv is None:
        argv = sys.argv
    if len(argv) < 3:
        print("Usage: %s <username> <password> <num-hosts> [<debug-level>]" % argv[0])
        sys.exit(1)

    username = argv[1]
    password = argv[2]
    debug = 1
    if len(argv) > 3:
        debug = int(argv[3])
    return username, password, debug


if __name__ == "__main__":
    sys.exit(main())
