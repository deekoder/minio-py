# -*- coding: utf-8 -*-
# Minio Python Library for Amazon S3 Compatible Cloud Storage, (C) 2015 Minio, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from unittest import TestCase
from nose.tools import raises

from minio import minio
from minio.error import ResponseError, InvalidBucketError

from .minio_mocks import MockResponse, MockConnection
from .helpers import generate_error

__author__ = 'minio'

class RemoveBucket(TestCase):
    @raises(TypeError)
    def test_bucket_is_string(self):
        client = minio.Minio('http://localhost:9000')
        client.remove_bucket(1234)

    @raises(InvalidBucketError)
    def test_bucket_is_not_empty_string(self):
        client = minio.Minio('http://localhost:9000')
        client.remove_bucket('  \t \n  ')

    @raises(InvalidBucketError)
    def test_remove_bucket_invalid_name(self):
        client = minio.Minio('http://localhost:9000')
        client.remove_bucket('1234')

    @mock.patch('urllib3.PoolManager')
    def test_remove_bucket_works(self, mock_connection):
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(MockResponse('DELETE', 'http://localhost:9000/hello/', {}, 204))
        client = minio.Minio('http://localhost:9000')
        client.remove_bucket('hello')
