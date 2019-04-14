""" 

Copyright [2019] [Gazorpazorp]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

- Package information

pledger: project and pledger package

This collects the pledgers of the project and checks if their corresponding payments are spent or not using the bitcoin.rpc package

"""

import bitcoin.rpc as br
import subprocess
import json


# Class output object contains pledger transaction info in order to check if transaction is spent or not
class Output():

    def __init__(self):
        self.address = ""
        self.value = 0
        self.spent = False
        self.vout = -1
        self.txid = ""

class Pledger():

    def __init__(self,txid,vout):
        # Create a connection to local Bitcoin Core node

        # Initialize pledger
        self.txid = txid
        self.vout = vout

        self.tx_output_old = self.old_tx_cmmd_line(self.txid,self.vout)
        # Find old address and value from previous transaction
        self.address_old = self.tx_output_old.address
        self.value_old = self.tx_output_old.value

        # Check if output has been spent
        self.is_spent = self.output_spent(self.tx_output_old)

    def update(self):
        # Update pledger variables
        self.tx_output_old = self.old_tx_cmmd_line(self.txid, self.vout)       # Get output from previous transaction
        self.address_old = self.tx_output_old.address                # Corresponding address
        self.value_old = self.tx_output_old.value                    # Value
        self.is_spent = self.output_spent_cmmd_line(self.tx_output_old)        # Check if output is spent

    def old_tx_cmmd_line(self,txid,vout):
        # Do exactly what old_tx function but returns output as a dictionary
        
        # Transaction raw transaction command
        cmmd_raw_tx = ["bitcoin-cli","getrawtransaction",txid]
        # Execute command
        cmmd_raw_out = subprocess.check_output(cmmd_raw_tx)
        # Decode
        cmmd_decode_tx = ["bitcoin-cli","decoderawtransaction",cmmd_raw_out[:-1].decode("utf-8")]
        # Execute command
        cmmd_out = subprocess.check_output(cmmd_decode_tx)
        # Filter out added character
        cmmd_out = cmmd_out[:-1]
        # Convert byte array 
        cmmd_out_str = cmmd_out.decode("utf-8")

        # For reading file use json.load / for reading string use json.loads

        # Open json file
        #f = open("/Users/tombax/Desktop/Hackaton/json.txt",'r')
        #cmmd_out_json = json.load(f)
        # Read string
        cmmd_out_json = json.loads(cmmd_out_str)


        # Find correct info from jsonfile
        output_blocks = cmmd_out_json["vout"]
        output = output_blocks[vout]
        scriptPubKey = output["scriptPubKey"]
        

        # Create an output object
        output_obj = Output()
        output_obj.addresses = scriptPubKey["addresses"]
        output_obj.value = float(output["value"])
        
        output_obj.vout = vout
        output_obj.txid = txid

        return output_obj


    def old_tx(self,txid,vout):
        # Get the previous transaction

        # Go to old transaction
        tx_old = blockexplorer.get_tx(txid)

        # Find the correct output
        return tx_old.outputs[vout]

    def output_spent(self,output):
        # Checks if transaction is still unconfirmed. Return true if output is already spend
        return output.spent

    def output_spent_cmmd_line(self,output):
        # Checks if transaction is still unconfirmed. Return true if output is already spend

        # Command for terminal
        cmmd = ["bitcoin-cli", "gettxout",output.txid,str(output.vout)]
        # Execute command
        cmmd_out = subprocess.check_output(cmmd)
        print(cmmd_out)
        # Command return is empty if spent
        if cmmd_out == b'' or cmmd_out == b'\n':
            output.spent = True
        else:
            output.spent = False

        return output.spent

    def get_unspent_value(self):
        # Function returns unspent value, if output is spent return 0
        if not self.output_spent(self.tx_output_old):
            return self.value_old
        else:
            return 0

class Project():

    def __init__(self,target):
        # Project pledgers
        self.pledgers = []
        # Add target
        self.target = target

    def add_pledger(self,pledger):
        # Add pledgers to project
        self.pledgers.append(pledger)

    def target_reached(self):
        # Returns true if target is reached
        if self.target < self.get_total_fund():
            return True
        else:
            return False

    def get_total_fund(self):
        # Get total amount of funded money from the pledger object list
        total = 0

        for p in self.pledgers:
            # Get the output vales that are still unspent
            total += p.get_unspent_value()

        return total 

    def get_targed(self):
        return self.target

    def update_pledgers(self):
        # Update pledgers from list
        for p in self.pledgers:
            p.update()


if __name__ == "__main__":

    # `Set target
    target = 400000

    # Create project
    project = Project(target)

    txid1 = "278778790ed2431fd67a3db55450869c88af1bac94b228fd25ee6e6d80da5c5c"
    txid2 = "8be808f480b4e7a7734f8f41c4caeae6ee86481b02868c908fe6ec0ee617b9da"
    # Define a pledger list
    pledgers = [Pledger(txid1,0), Pledger(txid2,0)]

    # Add new pledgers
    for pledger in pledgers:
        project.add_pledger(pledger)

    # Update pledgers transaction
    project.update_pledgers()

    for i,p in enumerate(pledgers):
        print([str(i) + " Value: " + str(p.value_old) + " Spent: " + str(p.is_spent)])


    print()
    print("Total fund")
    print(project.get_total_fund())






