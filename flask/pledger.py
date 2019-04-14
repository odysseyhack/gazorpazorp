from blockchain import blockexplorer


class Pledger():

    def __init__(self,txid,vout):
        # Initialize pledger
        self.txid = txid
        self.vout = vout

        self.tx_output_old = self.old_tx(self.txid,self.vout)
        # Find old address and value from previous transaction
        self.address_old = self.tx_output_old.address
        self.value_old = self.tx_output_old.value

        # Check if output has been spent
        self.is_spent = self.output_spent(self.tx_output_old)

    def update(self):
        # Update pledger variables
        self.tx_output_old = self.old_tx(self.txid, self.vout)       # Get output from previous transaction
        self.address_old = self.tx_output_old.address                # Corresponding address
        self.value_old = self.tx_output_old.value                    # Value
        self.is_spent = self.output_spent(self.tx_output_old)        # Check if output is spent


    def old_tx(self,txid,vout):
        # Get the previous transaction

        # Go to old transaction
        tx_old = blockexplorer.get_tx(txid)

        # Find the correct output
        return tx_old.outputs[vout]

    def output_spent(self,output):
        # Checks if transaction is still unconfirmed. Return true if output is already spend
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

    def get_targer(self):
        return self.target

    def update_pledgers(self):
        # Update pledgers from list
        for p in self.pledgers:
            p.update()


if __name__ == "__main__":

    # Create project with target and pledgers
    # `Set target
    target = 400000

    # Create project
    project = Project(target)


    # Define a pledger list and add this to project (for a real project the number of pledgers increases gradually)
    txid1 = "7957a35fe64f80d234d76d83a2a8f1a0d8149a41d81de548f0a65a8a999f6f18"
    txid2 = "68410a3d6cf9c571a5dd119c11fb9b4f45adb63df1418e290e1cadab398b8fcf"
    txid3 = "e0f96f26464687b670489fac550c0f5e7c534a92be495d270ea3df8afd24c79a"
    txid4 = "a70d387ef559f138ca10e95a8e56f2bcb7f59ffa2b9e0c374210427159021aff" 
    pledgers = [Pledger(txid1,0), Pledger(txid2,0), Pledger(txid3,0),Pledger(txid4,0)]
    for pledger in pledgers:
        project.add_pledger(pledger)


    print(project.get_total_fund())
    print(project.target_reached())

    # Call this function to update output checks
    project.update_pledgers()


    #for i,p in enumerate(pledgers):
    #    print([str(i) + " Value: " + str(p.value_old) + " Spent: " + str(p.is_spent)])

    #print()
    #print("Total fund")
    #print(total_funded(pledgers))






