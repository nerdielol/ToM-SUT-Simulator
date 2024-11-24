from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
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


# Simulate PLC or breaker logic here
def simulation_loop():
    while True:
        # Example: Toggle a coil or update a register
        # This is where your PLC or breaker simulation code will go
        time.sleep(1)


# Start the simulation loop in the main thread
if __name__ == '__main__':
    try:
        simulation_loop()
    except KeyboardInterrupt:
        print("Simulation stopped.")