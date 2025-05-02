class Button:
    def __init__(self):
        self.last_state = False  # předchozí hodnota (True=stisknuto)
        self.current_state = False  # aktuální hodnota
        self.just_pressed = False
        self.just_released = False

    def update(self, raw_value: bool):
        """raw_value = co vrátí hardware (True=stisknuto)"""
        self.just_pressed = False
        self.just_released = False

        if raw_value != self.current_state:
            # Stav se změnil → edge detection
            if raw_value:  # False → True
                self.just_pressed = True
            else:  # True → False
                self.just_released = True

        self.last_state = self.current_state
        self.current_state = raw_value

    def is_pressed(self):
        return self.current_state

    def was_just_pressed(self):
        return self.just_pressed

    def was_just_released(self):
        return self.just_released
