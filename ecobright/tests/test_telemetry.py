
import unittest
from unittest.mock import MagicMock, patch
import frappe
from ecobright.driver import read_inverter_data
from ecobright.telemetry_worker import process_telemetry

class TestTelemetry(unittest.TestCase):
    
    def test_read_inverter_data_success(self):
        """Test driver parsing logic with valid data."""
        # Mock Modbus Connection
        mock_modbus = MagicMock()
        # [Temp, Voltage, SOC, Grid, Power, Current]
        # Registers: 586 (Temp), 587 (Volts), 588 (SOC), 589 (Grid-unused), 590 (Power), 591 (Current)
        # Temp: 1250 -> (1250 - 1000)/10 = 25.0 C
        # Volts: 5200 -> 52.00 V
        # SOC: 85 -> 85%
        # Power: 1500 -> 1500 W
        # Current: 2500 -> 25.00 A
        mock_modbus.read_holding_registers.return_value = [1250, 5200, 85, 0, 1500, 2500]

        data = read_inverter_data(mock_modbus)
        
        self.assertIsNotNone(data)
        self.assertEqual(data['soc'], 85)
        self.assertEqual(data['power_w'], 1500)
        self.assertEqual(data['voltage'], 52.00)
        self.assertEqual(data['current'], 25.00)
        self.assertEqual(data['temp'], 25.0)

    def test_read_inverter_data_failure(self):
        """Test driver handles exceptions gracefully."""
        mock_modbus = MagicMock()
        mock_modbus.read_holding_registers.side_effect = Exception("Connection Timeout")

        data = read_inverter_data(mock_modbus)
        self.assertIsNone(data)

    @patch('ecobright.telemetry_worker.frappe')
    @patch('ecobright.telemetry_worker.read_inverter_data')
    def test_process_telemetry_flow(self, mock_read, mock_frappe):
        """Test the worker loop orchestration."""
        
        # Setup Mocks
        mock_read.return_value = {
            "soc": 90, 
            "power_w": 2000,
            "voltage": 53.5,
            "current": 40.0,
            "temp": 30.0
        }
        
        # Mock Cache and Realtime
        mock_cache = MagicMock()
        mock_frappe.cache.return_value = mock_cache
        mock_frappe.utils.now.return_value = "2023-10-01 12:00:00"

        # initial state
        last_log = 1000 
        # Current time > last_log + 300 to trigger history log
        with patch('time.time', return_value=1500): 
            new_last_log = process_telemetry("INV-001", MagicMock(), last_log)

        # 1. Verify Redis Update
        mock_cache.set_value.assert_called_with(
            "live_data::INV-001", 
            {
                "soc": 90, "power_w": 2000, "voltage": 53.5, 
                "current": 40.0, "temp": 30.0, 
                "timestamp": "2023-10-01 12:00:00",
                "inverter": "INV-001"
            }
        )

        # 2. Verify Socket.io Push
        mock_frappe.publish_realtime.assert_called()
        call_args = mock_frappe.publish_realtime.call_args[1]
        self.assertEqual(call_args['event'], 'inverter_update')
        self.assertEqual(call_args['room'], 'inverter_room_INV-001')

        # 3. Verify Historical Log Creation
        mock_frappe.get_doc.assert_called()
        self.assertEqual(mock_frappe.get_doc.call_args[0][0]['doctype'], 'Telemetry Log')
        
        # 4. Verify Log Time Updated
        self.assertEqual(new_last_log, 1500)
