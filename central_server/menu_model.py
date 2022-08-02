class MenuInfo:
    def __init__(self, crossing):
        self.crossing = crossing
        self.car_speed = {
            "speed_amount": 0,
            "car_count":  0
        }
        self.red_light_infraction = 0
        self.speed_infraction = 0
        self.car_count = {
            "line1": 0,
            "line2": 0,
            "time": 0
        }
