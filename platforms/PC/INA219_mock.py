import time
import random

LOW_VOLTAGE = 3.0
HIGH_VOLTAGE = 4.2
CAPACITY = 1000 # mAh

class INA219:
    def __init__(self, i2c_bus=1, addr=0x40, rated_capacity: int=CAPACITY):
        self.addr = addr
        self.time = time.time()
        self.battery_capacity_mAh = rated_capacity
        self.voltage_V = self.__generate_voltage()
        self.current_mA = self.__generate_current()

    def read(self,address):
        pass

    def write(self,address,data):
        pass

    def getShuntVoltage_mV(self) -> float:
        return 0.0

    def getBusVoltage_V(self):
        return self.voltage_V

    def getCurrent_mA(self):
        return -self.current_mA 

    def getPower_W(self):
        return abs(self.getBusVoltage_V() * self.getCurrent_mA() / 1000.0)
    
    def __generate_current(self):
        # 150mA to 300mA
        return random.randint(150, 300)
    
    def __generate_voltage(self):
        return round(random.uniform(LOW_VOLTAGE, HIGH_VOLTAGE), 3)
    
    def __simulate_discharge(self):
        """
        Simulate the discharge of the battery by decreasing the voltage and current values.
        Elapsed time is used to calculate the rate of discharge.
        current * d_time 
        """
        d_time = time.time() - self.time
        self.time = time.time()

        # time in hours
        d_time = d_time / 3600.0

        # Calculate the amount of current consumed in mAh
        consumed_current_mAh = self.current_mA * d_time
        # Calculate the new battery voltage based on the consumed current
        self.voltage_V -= (consumed_current_mAh / self.battery_capacity_mAh) * (HIGH_VOLTAGE - LOW_VOLTAGE)
        # Ensure the voltage does not go below LOW_VOLTAGE
        if self.voltage_V < LOW_VOLTAGE:
            self.voltage_V = LOW_VOLTAGE
    
    def getRemainingPercent(self):
        """
        Returns the remaining battery percentage based on the bus voltage. \n
        The voltage range is defined between LOW_VOLTAGE (3) and HIGH_VOLTAGE (4.2). \n
        The percentage is calculated as:

        ((bus_voltage - LOW_VOLTAGE) / (HIGH_VOLTAGE - LOW_VOLTAGE)) * 100
        """
        self.__simulate_discharge()
        return 100.0 * (self.getBusVoltage_V() - LOW_VOLTAGE) / (HIGH_VOLTAGE - LOW_VOLTAGE)
    
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