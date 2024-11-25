class MTZBreaker:
    def __init__(self):
        self.status = 'Closed'  # 'Closed' or 'Open'
        self.fault_status = 0   # 1 if faulted, 0 otherwise
        self.accessories = {}
        self.initialize_accessories()

    def initialize_accessories(self):
        # Initialize accessory states
        self.accessories['OF'] = 1  # OF (Open/Closed Contact): 1=Closed, 0=Open
        self.accessories['XF'] = 0  # XF (Fault Indication Contact): 1=Fault, 0=Normal
        # Add other accessories as needed

    def close(self):
        if self.status == 'Open':
            print("Breaker closing...")
            self.status = 'Closed'
            self.fault_status = 0
            self.accessories['OF'] = 1
            self.accessories['XF'] = 0
            # Handle accessory updates

    def open(self):
        if self.status == 'Closed':
            print("Breaker opening...")
            self.status = 'Open'
            self.accessories['OF'] = 0
            # Handle accessory updates

    def trip(self, cause):
        if self.status != 'Open':
            print(f"Breaker tripping due to {cause}...")
            self.status = 'Open'
            self.fault_status = 1
            self.accessories['OF'] = 0
            self.accessories['XF'] = 1
            # Handle accessory updates

    def reset_fault(self):
        if self.fault_status == 1:
            print("Resetting breaker fault status...")
            self.fault_status = 0
            self.accessories['XF'] = 0
            # Handle accessory updates