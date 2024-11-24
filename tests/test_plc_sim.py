import pytest
import threading
import time
from pymodbus.client import ModbusTcpClient
from src.sut_simulator.plc_sim import context, run_modbus_server


# Fixture to start and stop the Modbus server
@pytest.fixture(scope="module")
def modbus_server():
    # Start the Modbus server in a separate thread
    server_thread = threading.Thread(target=run_modbus_server)
    server_thread.daemon = True
    server_thread.start()
    # Wait a moment to ensure the server is up
    time.sleep(1)
    yield
    # Teardown: Nothing to do because the server runs in a daemon thread


# Fixture to reset the server context before each test
@pytest.fixture(autouse=True)
def reset_server_context():
    # Reset coils
    context[0x00].setValues(1, 0, [0] * 100)
    # Reset discrete inputs
    context[0x00].setValues(2, 0, [0] * 100)
    # Reset holding registers
    context[0x00].setValues(3, 0, [0] * 100)
    # Reset input registers
    context[0x00].setValues(4, 0, [0] * 100)


# Test reading and writing coils
def test_coils(modbus_server):
    client = ModbusTcpClient("127.0.0.1", port=5020)
    assert client.connect()

    # Write single coil
    write_coil = client.write_coil(0, True)
    assert not write_coil.isError()

    # Read back the coil
    result = client.read_coils(0, 1)
    assert not result.isError()
    assert result.bits[0] == True

    # Write multiple coils
    write_coils = client.write_coils(1, [True, False, True])
    assert not write_coils.isError()

    # Read back the coils
    result = client.read_coils(1, count=3)
    assert not result.isError()
    assert result.bits[:3] == [True, False, True]

    client.close()


# Test reading and writing holding registers
def test_holding_registers(modbus_server):
    client = ModbusTcpClient("localhost", port=5020)
    assert client.connect()

    # Write single register
    write_register = client.write_register(0, 12345)
    assert not write_register.isError()

    # Read back the register
    result = client.read_holding_registers(0, 1)
    assert not result.isError()
    assert result.registers[0] == 12345

    # Write multiple registers
    write_registers = client.write_registers(1, [100, 200, 300])
    assert not write_registers.isError()

    # Read back the registers
    result = client.read_holding_registers(1, 3)
    assert not result.isError()
    assert result.registers == [100, 200, 300]

    client.close()


# Test reading discrete inputs
def test_discrete_inputs(modbus_server):
    client = ModbusTcpClient("localhost", port=5020)
    assert client.connect()

    # Manually set discrete inputs in the server's context for testing
    context[0x00].setValues(2, 0, [True, False, True, True, False])

    # Read back the discrete inputs
    result = client.read_discrete_inputs(0, 5)
    assert not result.isError()
    assert result.bits[:5] == [True, False, True, True, False]

    client.close()


# Test reading input registers
def test_input_registers(modbus_server):
    client = ModbusTcpClient("localhost", port=5020)
    assert client.connect()

    # Manually set input registers in the server's context for testing
    context[0x00].setValues(4, 0, [10, 20, 30, 40, 50])

    # Read back the input registers
    result = client.read_input_registers(0, 5)
    assert not result.isError()
    assert result.registers == [10, 20, 30, 40, 50]

    client.close()


# Test invalid address access
def test_invalid_address(modbus_server):
    client = ModbusTcpClient("localhost", port=5020)
    assert client.connect()

    # Attempt to read from an invalid coil address
    result = client.read_coils(9999, 1)
    assert result.isError()

    client.close()


# Test concurrent client connections
def test_concurrent_clients(modbus_server):
    def client_task():
        client = ModbusTcpClient("localhost", port=5020)
        assert client.connect()
        result = client.read_coils(0, 1)
        assert not result.isError()
        client.close()

    threads = [threading.Thread(target=client_task) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
