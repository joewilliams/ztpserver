#!/usr/bin/env python
# encoding: utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# Copyright (c) 2013, Arista Networks
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#   Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
#   Neither the name of the {organization} nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import os
import sys

from glob import glob
from distutils.core import setup

from ztpserver import __version__, __author__

confdir = os.environ.get('ZTPSERVER_CONFDIR', '/etc')
confdir = '/persist/sys/etc' if os.path.exists('/etc/Eos-release') else confdir

setup(
    name='ztpserver',
    version=__version__,
    description = 'ZTP Server for EOS',
    author=__author__,
    author_email='devops@aristanetworks.com',
    url='http://eos.aristanetworks.com/',
    license='BSD-3',
    packages=['ztpserver'],
    scripts=glob('bin/*'),
    data_files=[
        ('%s/ztpserver' % confdir, ['conf/ztpserver.conf']),
        ('bootstrap', glob('repos/default/bootstrap/*')),
        ('actions', glob('repos/default/actions/*')),
        ('nodes', []),
        ('definitions', []),
        ('configs', []),
        ('repos/default/images', []),
        ('repos/default/templates', []),
        ('repos/default/files', []),
        ('repos/default/extensions', []),
        ('repos/default/plugins', [])
    ]
)
