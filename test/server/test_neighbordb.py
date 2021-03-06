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

import os
import unittest

import yaml

#pylint: disable=F0401
from ztpserver.app import enable_handler_console
from neighbordb_test_lib import NodeTest, NeighbordbTest

TEST_DIR = 'test/neighbordb'

def load_tests(loader, tests, pattern):            #pylint: disable=W0613
    suite = unittest.TestSuite()
    test_list = os.environ.get('TESTS', None)
    if not test_list:
        test_list = [f for f in os.listdir(TEST_DIR)
                 if os.path.join(TEST_DIR, f).endswith('_test')]
    else:
        test_list = test_list.split(',')

    print test_list
    for test in test_list:
        print 'Starting test %s' % test

        definition = yaml.load(open(os.path.join(TEST_DIR, test)))

        nodes = definition.get('nodes', [])
        for node in nodes:
            print 'Adding test: %s' % node['name']
            suite.addTest(NodeTest(test, node, definition['neighbordb']))

        if definition.get('configured_neighbordb', None):
            suite.addTest(NeighbordbTest(test, definition['neighbordb'], 
                                         definition['configured_neighbordb']))

    return suite

if __name__ == '__main__':
    enable_handler_console()
    unittest.main()
