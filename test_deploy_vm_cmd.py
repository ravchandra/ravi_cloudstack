# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
""" BVT tests for Virtual Machine Life Cycle
"""
# Import Local Modules
from marvin.cloudstackTestCase import cloudstackTestCase
from marvin.cloudstackAPI import deployVirtualMachine
from marvin.lib.utils import cleanup_resources
from marvin.lib.base import VirtualMachine

class TestDeployVMCmd(cloudstackTestCase):

    @classmethod
    def setUpClass(cls):
        testClient = super(TestDeployVMCmd, cls).getClsTestClient()
        cls.apiclient = testClient.getApiClient()
        cls._cleanup = []
        pass


    @classmethod
    def tearDownClass(cls):
        cls.apiclient = super(TestDeployVMCmd, cls).getClsTestClient().getApiClient()
        try:
            cleanup_resources(cls.apiclient, cls._cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return
        pass

    def setUp(self):
        self.apiclient = self.testClient.getApiClient()
        self.dbclient = self.testClient.getDbConnection()
        self.cleanup = []
        pass

    def tearDown(self):
        try:
            #Clean up, terminate the created ISOs
            cleanup_resources(self.apiclient, self.cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return
        pass

    def test_01_deploy_vm(self):
        """ test deploy vm """
        cmd = deployVirtualMachine.deployVirtualMachineCmd()
        cmd.hypervisor = "XenServer"
        cmd.serviceofferingid = "fad19d53-022c-497b-96c8-9a9d4403fb72"
        cmd.zoneid = "d822e40b-1e4d-4a13-987f-77ac5c1ac2f3"
        cmd.displayname = "CentOsVM"
        cmd.templateid = "46feed6e-7e66-11e6-ae93-08002755476e"
        cmd.networkids = "87343e7b-4f63-466f-8339-9efa1251693b"

        virtual_machine = self.apiclient.deployVirtualMachine(cmd)
        self.assertEquals(virtual_machine.state, "Running")

        return