#!/usr/bin/env python 
#
# Copyright (c) 2014, Arista Networks, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#  - Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#  - Neither the name of Arista Networks nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#pylint: disable=R0904

import os
import os.path
import unittest

from client_test_lib import debug    #pylint: disable=W0611
from client_test_lib import STARTUP_CONFIG
from client_test_lib import Bootstrap, ActionFailureTest
from client_test_lib import file_log, get_action, random_string
from client_test_lib import startup_config_action

class FailureTest(ActionFailureTest):

    def test_missing_url(self):
        self.basic_test('add_config', 1)

    def test_url_failure(self):
        self.basic_test('add_config', 2,
                        attributes={'add_config-url' : 
                                    random_string()})


class SuccessTest(unittest.TestCase):

    def test_success(self):
        bootstrap = Bootstrap(ztps_default_config=True)
        config = random_string()
        url = 'http://%s/%s' % (bootstrap.server, config)
        bootstrap.ztps.set_definition_response(
            actions=[{'name' : 'test_action'}],
            attributes={'add_config-url' : url})
        bootstrap.ztps.set_action_response('test_action',
                                           get_action('add_config'))
        contents = random_string()
        bootstrap.ztps.set_file_response(config, contents)
        bootstrap.start_test()

        try:
            self.failUnless(os.path.isfile(STARTUP_CONFIG))
            self.failUnless(contents.split() == file_log(STARTUP_CONFIG))
            self.failUnless(bootstrap.success())
        except AssertionError:
            raise
        finally:
            bootstrap.end_test()

    def test_append(self):
        bootstrap = Bootstrap(ztps_default_config=True)
        config = random_string()
        url = 'http://%s/%s' % (bootstrap.server, config)
        bootstrap.ztps.set_definition_response(
            actions=[{'name' : 'startup_config_action'},
                     {'name' : 'test_action'}],
            attributes={'add_config-url' : url})
        bootstrap.ztps.set_action_response('test_action',
                                           get_action('add_config'))

        startup_config_text = random_string()
        bootstrap.ztps.set_action_response(
            'startup_config_action',
            startup_config_action(lines=[startup_config_text]))
        contents = random_string()
        bootstrap.ztps.set_file_response(config, contents)
        bootstrap.start_test()

        try:
            self.failUnless(os.path.isfile(STARTUP_CONFIG))
            log = file_log(STARTUP_CONFIG)
            self.failUnless(contents in log)
            self.failUnless(startup_config_text in log)
            self.failUnless(bootstrap.success())
        except AssertionError:
            raise
        finally:
            bootstrap.end_test()

    def test_multi_lines(self):
        bootstrap = Bootstrap(ztps_default_config=True)
        config = random_string()
        url = 'http://%s/%s' % (bootstrap.server, config)
        bootstrap.ztps.set_definition_response(
            actions=[{'name' : 'startup_config_action'},
                     {'name' : 'test_action'}],
            attributes={'add_config-url' : url})
        bootstrap.ztps.set_action_response('test_action',
                                           get_action('add_config'))

        startup_config_lines = [random_string(), random_string(),
                                random_string(), random_string()]
        bootstrap.ztps.set_action_response(
            'startup_config_action',
            startup_config_action(lines=startup_config_lines))
        contents = '\n'.join([random_string(), random_string(),
                              random_string(), random_string(),
                              random_string(), random_string()])
        bootstrap.ztps.set_file_response(config, contents)
        bootstrap.start_test()

        try:
            self.failUnless(os.path.isfile(STARTUP_CONFIG))
            log = file_log(STARTUP_CONFIG)
            all_lines = startup_config_lines + contents.split()
            for line in all_lines:
                self.failUnless(line in log)
            self.failUnless(bootstrap.success())
        except AssertionError:
            raise
        finally:
            bootstrap.end_test()


if __name__ == '__main__':
    unittest.main()
