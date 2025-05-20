
LOW_VOLTAGE = 3.0
HIGH_VOLTAGE = 4.2

class Battery:
    def __init__(self):
        raise NotImplementedError("I am an abstract class and cannot be instantiated directly.")

    def getVoltage_V(self) -> float:
        raise NotImplementedError("I am an abstract class and cannot be instantiated directly.")

    def getCurrent_mA(self) -> float:
        raise NotImplementedError("I am an abstract class and cannot be instantiated directly.")

    def getPower_W(self) -> float:
        return abs(self.getVoltage_V() * self.getCurrent_mA() / 1000.0)
    
    def getRemainingPercent(self) -> float:
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