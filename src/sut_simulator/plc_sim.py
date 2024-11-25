from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from mtz_sim import MTZBreaker
from threading import Thread
import time

# Create a Modbus data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0] * 100),  # Discrete Inputs (Read-only bits)
    co=ModbusSequentialDataBlock(0, [0] * 100),  # Coils (Read/Write bits)
    hr=ModbusSequentialDataBlock(0, [0] * 100),  # Holding Registers (Read/Write words)
    ir=ModbusSequentialDataBlock(0, [0] * 100)   # Input Registers (Read-only words)
)
context = ModbusServerContext(slaves=store, single=True)


# Function to start the Modbus server
def run_modbus_server():
    StartTcpServer(context=context, address=("127.0.0.1", 5020))


# Start the Modbus server in a separate thread
server_thread = Thread(target=run_modbus_server)
server_thread.daemon = True
server_thread.start()


class SimulatedPLC:
    def __init__(self, context, breaker):
        self.context: ModbusServerContext = context
        self.breaker: MTZBreaker = breaker

    def run(self):
        while True:
            self.process_modbus_requests()
            self.update_modbus_data()
            time.sleep(0.1)  # Adjust the cycle time as needed

    def process_modbus_requests(self):
        # Read commands from the automated tester
        # For example, read coils or holding registers
        # Let's assume:
        # Coil 0: Close Breaker Command
        # Coil 1: Open Breaker Command
        # Coil 2: Trip Breaker Command

        coils = self.context[0x00].getValues(1, 0, count=10)  # Function code 1 (Coils)

        # Process Close Command
        if coils[0]:
            self.breaker.close()
            self.context[0x00].setValues(1, 0, [0])  # Reset the coil after processing

        # Process Open Command
        if coils[1]:
            self.breaker.open()
            self.context[0x00].setValues(1, 1, [0])  # Reset the coil after processing

        # Process Trip Command
        if coils[2]:
            self.breaker.trip('Remote Trip')
            self.context[0x00].setValues(1, 2, [0])  # Reset the coil after processing

        if coils[3]:
            self.breaker.charge_mch()
            self.context[0x00].setValues(1, 3, [0])

        # Process additional commands as needed

    def update_modbus_data(self):
        # Update Modbus registers and coils to reflect breaker status
        # Let's assume:
        # Discrete Input 0: Breaker Status (1=Closed, 0=Open)
        # Discrete Input 1: Fault Indication (1=Fault, 0=Normal)

        breaker_status = 1 if self.breaker.status == 'Closed' else 0
        self.context[0x00].setValues(2, 0, [breaker_status])  # Function code 2 (Discrete Inputs)
        
        fault_indication = self.breaker.fault_status
        self.context[0x00].setValues(2, 1, [fault_indication])

        # I want to loop over the accessories dictionary and update the coils accordingly
        for key, value in self.breaker.accessories.items():
            self.context[0x00].setValues(1, key, [value])


if __name__ == '__main__':
    # Instantiate the breaker simulation
    breaker = MTZBreaker()

    # Instantiate the PLC simulation with the breaker and Modbus context
    plc_simulation = SimulatedPLC(context, breaker)

    # Run the PLC simulation in a separate thread
    plc_thread = Thread(target=plc_simulation.run)
    plc_thread.daemon = True
    plc_thread.start()

    # Start the Modbus TCP server (already running in server_thread)
    # The main thread can now handle other tasks or simply wait
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation stopped.")