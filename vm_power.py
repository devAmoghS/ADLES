#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

"""Power operations for Virtual Machines in vSphere.

Usage:
    vm_power.py [options]
    vm_power.py --version
    vm_power.py (-h | --help)

Options:
    -h, --help          Prints this page
    --version           Prints current version
    --no-color          Do not color termianl output
    -v, --verbose       Emit debugging logs to terminal
    -f, --file FILE     Name of JSON file with server connection information

"""

import logging

from docopt import docopt

from adles.utils import prompt_y_n_question, user_input, script_setup
from adles.vsphere.vm_utils import change_vm_state
from adles.vsphere.vsphere_utils import is_vm
from adles.vsphere.folder_utils import traverse_path

__version__ = "0.3.2"
args = docopt(__doc__, version=__version__, help=True)
server = script_setup('vm_power.log', args, (__file__, __version__))

operation = input("Enter the power operation you wish to perform [on | off | reset | suspend]: ")
attempt_guest = prompt_y_n_question("Use guest operations if available? ")

# TODO: prefixes
# TODO: nesting
if prompt_y_n_question("Multiple VMs? "):
    folder, folder_name = user_input("Name of or path to the folder with VMs: ", "folder",
                                     lambda x: traverse_path(server.get_folder(), x)
                                     if '/' in x else server.get_folder(x))
    vms = [x for x in folder.childEntity if is_vm(x)]
    if prompt_y_n_question("Found %d VMs in folder '%s'. Continue? " % (len(vms), folder_name)):
        for vm in vms:
            change_vm_state(vm, operation, attempt_guest)

else:
    vm, vm_name = user_input("Name of or path to the VM: ", "VM",
                             lambda x: traverse_path(server.get_folder(), x) if '/' in x else server.get_vm(x))
    logging.info("Changing power state of '%s' to '%s'", vm_name, operation)
    change_vm_state(vm, operation, attempt_guest)
