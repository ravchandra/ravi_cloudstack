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
#Import Local Modules
from marvin.cloudstackTestCase import cloudstackTestCase
from marvin.cloudstackAPI import (recoverVirtualMachine,
                                  destroyVirtualMachine,
                                  attachIso,
                                  detachIso)
from marvin.lib.utils import (cleanup_resources,
                              validateList)
from marvin.lib.base import (Account,
                             ServiceOffering,
                             VirtualMachine,
                             Host,
                             Iso,
                             Router,
                             Configurations)
from marvin.lib.common import (get_domain,
                                get_zone,
                                get_template)
from marvin.codes import FAILED, PASS
from nose.plugins.attrib import attr
#Import System modules
import time

_multiprocess_shared_ = True
class TestVMLifeCycle(cloudstackTestCase):

    @classmethod
    def setUpClass(cls):
        testClient = super(TestVMLifeCycle, cls).getClsTestClient()
        cls.apiclient = testClient.getApiClient()
        cls.services = testClient.getParsedTestDataConfig()
        cls.hypervisor = testClient.getHypervisorInfo()

        # Get Zone, Domain and templates
        domain = get_domain(cls.apiclient)
        cls.zone = get_zone(cls.apiclient, cls.testClient.getZoneForTests())
        cls.services['mode'] = cls.zone.networktype

        #if local storage is enabled, alter the offerings to use localstorage
        #this step is needed for devcloud
        if cls.zone.localstorageenabled == True:
            cls.services["service_offerings"]["tiny"]["storagetype"] = 'local'
            cls.services["service_offerings"]["small"]["storagetype"] = 'local'
            cls.services["service_offerings"]["medium"]["storagetype"] = 'local'

        template = get_template(
                            cls.apiclient,
                            cls.zone.id,
                            cls.services["ostype"]
                            )
        if template == FAILED:
            assert False, "get_template() failed to return template with description %s" % cls.services["ostype"]

        # Set Zones and disk offerings
        cls.services["small"]["zoneid"] = cls.zone.id
        cls.services["small"]["template"] = template.id

        # cls.services["big"]["zoneid"] = cls.zone.id
        # cls.services["big"]["template"] = template.id

        #cls.services["iso1"]["zoneid"] = cls.zone.id

        # # Create VMs, NAT Rules etc
        cls.account = Account.create(
                            cls.apiclient,
                            cls.services["account"],
                            domainid=domain.id
                            )
        cls.so_list = ServiceOffering.list(cls.apiclient)

        # cls.small_offering = ServiceOffering.create(
        #                             cls.apiclient,
        #                             cls.services["service_offerings"]["small"]
        #                            )

        # cls.medium_offering = ServiceOffering.create(
        #                             cls.apiclient,
        #                             cls.services["service_offerings"]["medium"]
        #                             )

        # cls.ravi_offering = ServiceOffering.create(
        #     cls.apiclient,
        #     cls.services["service_offerings"]["ravismall"]
        # )

        # #create small and large virtual machines
        # cls.small_virtual_machine = VirtualMachine.create(
        #                                 cls.apiclient,
        #                                 cls.services["small"],
        #                                 accountid=cls.account.name,
        #                                 domainid=cls.account.domainid,
        #                                 serviceofferingid=cls.small_offering.id,
        #                                 mode=cls.services["mode"]
        #                                 )
        # cls.medium_virtual_machine = VirtualMachine.create(
        #                                cls.apiclient,
        #                                cls.services["small"],
        #                                accountid=cls.account.name,
        #                                domainid=cls.account.domainid,
        #                                serviceofferingid=cls.medium_offering.id,
        #                                mode=cls.services["mode"]
        #                             )
        # cls.virtual_machine = VirtualMachine.create(
        #                                 cls.apiclient,
        #                                 cls.services["small"],
        #                                 accountid=cls.account.name,
        #                                 domainid=cls.account.domainid,
        #                                 serviceofferingid=cls.small_offering.id,
        #                                 mode=cls.services["mode"]
        #                                 )
        #
        cls.ravi_virtual_machine = VirtualMachine.create(
                                        cls.apiclient,
                                        cls.services["small"],
                                        accountid=cls.account.name,
                                        domainid=cls.account.domainid,
                                        serviceofferingid=cls.so_list[0].id,
                                        mode=cls.services["mode"]
                                        )

        #cls.ravi_virtual_machine = VirtualMachine.list(cls.apiclient,id='d15ae53c-924f-4db6-a2b5-8b98731b0d96')[0]
        cls._cleanup = [
                        cls.account
                        ]

    @classmethod
    def tearDownClass(cls):
        cls.apiclient = super(TestVMLifeCycle, cls).getClsTestClient().getApiClient()
        try:
            cleanup_resources(cls.apiclient, cls._cleanup)
            #pass
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return

    def setUp(self):
        self.apiclient = self.testClient.getApiClient()
        self.dbclient = self.testClient.getDbConnection()
        self.cleanup = []

    def tearDown(self):
        try:
            #Clean up, terminate the created ISOs
            cleanup_resources(self.apiclient, self.cleanup)
            #pass
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return

    @attr(tags = ["devcloud", "advanced", "advancedns", "smoke", "basic", "sg"], required_hardware="false")
    def test_02_start_vm(self):
        """Test Start Virtual Machine
        """
        # Validate the following
        # 1. listVM command should return this VM.State
        #    of this VM should be Running".

        # self.debug("Starting VM - ID: %s" % self.virtual_machine.id)
        # self.small_virtual_machine.start(self.apiclient)
        #
        # list_vm_response = VirtualMachine.list(
        #                                     self.apiclient,
        #                                     id=self.small_virtual_machine.id
        #                                     )
        # self.assertEqual(
        #                     isinstance(list_vm_response, list),
        #                     True,
        #                     "Check list response returns a valid list"
        #                 )
        #
        # self.assertNotEqual(
        #                     len(list_vm_response),
        #                     0,
        #                     "Check VM avaliable in List Virtual Machines"
        #                 )
        #
        # self.debug(
        #         "Verify listVirtualMachines response for virtual machine: %s" \
        #         % self.small_virtual_machine.id
        #         )
        # self.assertEqual(
        #                     list_vm_response[0].state,
        #                     "Running",
        #                     "Check virtual machine is in running state"
        #                 )




        self.debug("Starting VM - ID: %s" % self.ravi_virtual_machine.id)
        self.ravi_virtual_machine.start(self.apiclient)

        list_vm_response = VirtualMachine.list(
                                            self.apiclient,
                                            id=self.ravi_virtual_machine.id
                                            )
        self.assertEqual(
                            isinstance(list_vm_response, list),
                            True,
                            "Check list response returns a valid list"
                        )

        self.assertNotEqual(
                            len(list_vm_response),
                            0,
                            "Check VM avaliable in List Virtual Machines"
                        )

        self.debug(
                "Verify listVirtualMachines response for virtual machine: %s" \
                % self.ravi_virtual_machine.id
                )
        self.assertEqual(
                            list_vm_response[0].state,
                            "Running",
                            "Check virtual machine is in running state"
                        )
        return