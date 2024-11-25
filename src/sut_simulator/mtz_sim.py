class MTZBreaker:
    def __init__(self):
        self.status = 'Open'  # 'Closed' or 'Open'
        self.fault_status = 0   # 1 if faulted, 0 otherwise
        self.accessories = {}
        self.initialize_accessories()

    def initialize_accessories(self):
        # Initialize accessory states
        self.accessories['OF'] = 0  # OF (Open/Closed Contact): 1=Closed, 0=Open
        self.accessories['XF'] = 0  # XF (Fault Indication Contact): 1=Fault, 0=Normal
        self.accessories['SD'] = 0  # SD (Trip Indication Contact): 1=Tripped, 0=Normal
        self.accessories['SDE'] = 0  # SDE (Fault-trip Indication Contact): 1=Fault Trip, 0=Normal
        self.accessories['MX'] = 0  # MX (Shunt Trip Release): 1=Activated, 0=Inactive
        self.accessories['MN'] = 0  # MN (Undervoltage Release): 1=Voltage OK, 0=Undervoltage
        self.accessories['MCH'] = 0  # MCH (Motor Mechanism): 1=Ready, 0=Not Ready

    def charge_mch(self):
        """
        Recharge MCH (Motor Mechanism) based on an input signal.
        Update the status register to reflect readiness.
        """
        print("Recharging MCH (Motor Mechanism)...")
        self.accessories['MCH'] = 1  # MCH is charged

    def discharge_mch(self):
        """
        Discharge MCH (Motor Mechanism) and update the status register.
        """
        print("Discharging MCH (Motor Mechanism)...")
        self.accessories['MCH'] = 0  # MCH is not charged

    def close(self):
        if self.status == 'Open' and self.accessories['MCH']:
            print("Breaker closing...")
            self.status = 'Closed'
            self.fault_status = 0
            self.update_accessories_on_close()
        else:
            print("Breaker cannot close. Either already closed or MCH not ready.")

    def open(self):
        if self.status == 'Closed':
            print("Breaker opening...")
            self.status = 'Open'
            self.update_accessories_on_open()
        else:
            print("Breaker is already open.")

    def trip(self, cause):
        if self.status != 'Open':
            print(f"Breaker tripping due to {cause}...")
            self.status = 'Open'
            self.fault_status = 1
            self.update_accessories_on_trip(cause)
        else:
            print("Breaker is already open.")

    def reset_fault(self):
        if self.fault_status == 1:
            print("Resetting breaker fault status...")
            self.fault_status = 0
            self.accessories['XF'] = 0
            self.accessories['SD'] = 0
            self.accessories['SDE'] = 0
            # Additional reset actions if necessary
        else:
            print("No fault to reset.")

    def update_accessories_on_close(self):
        self.accessories['OF'] = 1
        self.accessories['XF'] = 0
        self.accessories['SD'] = 0
        self.accessories['SDE'] = 0
        # Update other accessories if needed

    def update_accessories_on_open(self):
        self.accessories['OF'] = 0
        # SD and SDE remain unchanged unless tripped
        # Update other accessories if needed

    def update_accessories_on_trip(self, cause):
        self.accessories['OF'] = 0
        self.accessories['XF'] = 1  # Fault indication
        self.accessories['SD'] = 1  # Trip indication
        if cause == 'Fault':
            self.accessories['SDE'] = 1  # Fault-trip indication
        # Update other accessories if needed

    def activate_mx(self):
        print("Activating MX (Shunt Trip Release)...")
        self.accessories['MX'] = 1
        self.trip('Remote Trip')
        self.accessories['MX'] = 0

    def check_mn(self, voltage):
        if voltage < 0.8:  # Assuming 0.8 is the undervoltage threshold
            print("MN (Undervoltage Release) detected undervoltage.")
            self.accessories['MN'] = 0
            self.trip('Undervoltage')
        else:
            self.accessories['MN'] = 1