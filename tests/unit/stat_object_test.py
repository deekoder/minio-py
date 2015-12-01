# -*- coding: utf-8 -*-
# Minio Python Library for Amazon S3 Compatible Cloud Storage, (C) 2015 Minio, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import mock

from nose.tools import raises
from unittest import TestCase

from minio import minio
from minio.error import ResponseError, InvalidBucketError

from .minio_mocks import MockResponse, MockConnection
from .helpers import generate_error

__author__ = 'minio'

class StatObject(TestCase):
    @raises(TypeError)
    def test_object_is_string(self):
        client = minio.Minio('http://localhost:9000')
        client.stat_object('hello', 1234)

    @raises(ValueError)
    def test_object_is_not_empty_string(self):
        client = minio.Minio('http://localhost:9000')
        client.stat_object('hello', '  \t \n  ')

    @raises(InvalidBucketError)
    def test_stat_object_invalid_name(self):
        client = minio.Minio('http://localhost:9000')
        client.stat_object('1234', 'world')

    @mock.patch('urllib3.PoolManager')
    def test_stat_object_works(self, mock_connection):
        mock_headers = {
            'content-type': 'application/octet-stream',
            'last-modified': 'Fri, 26 Jun 2015 19:05:37 GMT',
            'content-length': 11,
            'etag': '5eb63bbbe01eeed093cb22bb8f5acdc3'
        }
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(MockResponse('HEAD', 'http://localhost:9000/hello/world', {}, 200,
                                                  response_headers=mock_headers))
        client = minio.Minio('http://localhost:9000')
        client.stat_object('hello', 'world')
