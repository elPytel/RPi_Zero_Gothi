import INA219
from platforms.template.battery import *

LOW_VOLTAGE = 3.0
HIGH_VOLTAGE = 4.2

class RPi_battery(Battery):
    def __init__(self):
        addr=0x43
        self.ina219 = INA219(addr=addr)

    def getVoltage_V(self):
        """
        Returns the bus voltage in volts.
        """
        # Read the bus voltage from the INA219
        bus_voltage = self.ina219.getBusVoltage_V()
        return bus_voltage

    def getCurrent_mA(self):
        """
        Returns the current in milliamps.
        """
        # Read the current from the INA219
        current = self.ina219.getCurrent_mA()
        return current

    def getPower_W(self):
        """
        Returns the power in watts.
        """
        # Read the power from the INA219
        power = self.ina219.getPower_W()
        return power
    
    def getRemainingPercent(self):
        """
        Returns the remaining battery percentage based on the bus voltage. \n
        The voltage range is defined between LOW_VOLTAGE (3) and HIGH_VOLTAGE (4.2). \n
        The percentage is calculated as:

        ((bus_voltage - LOW_VOLTAGE) / (HIGH_VOLTAGE - LOW_VOLTAGE)) * 100
        """
        return 100.0 * (self.getVoltage_V() - LOW_VOLTAGE) / (HIGH_VOLTAGE - LOW_VOLTAGE)
    
    def getRemainingTime(self) -> int:
        """
        Returns the remaining time in seconds based on the current and power values.
        The time is calculated as:
        (remaining_capacity / current) * 3600
        """
        # Get the current in mA
        current = self.getCurrent_mA()
        
        # Calculate the remaining capacity in mAh
        remaining_capacity = self.getRemainingPercent() * self.battery_capacity_mAh / 100
        
        # Calculate the remaining time in seconds
        if current > 0: # charging
            remaining_time = (100-remaining_capacity / current) * 3600
            return int(remaining_time)
        else: # discharging
            remaining_time = abs(remaining_capacity / current) * 3600
            return int(remaining_time)