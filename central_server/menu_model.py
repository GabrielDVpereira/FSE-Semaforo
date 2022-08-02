from datetime import datetime

class MenuInfo:
    def __init__(self, crossing):
        self.start_time = datetime.now()
        self.crossing = crossing
        self.car_speed = {
            "speed_amount": 0,
            "car_count":  0
        }
        self.red_light_infraction = 0
        self.speed_infraction = 0
        self.car_count = {
            "line1": 0,
            "line2": 0
        }
    
    def __str__(self):
        return "Crossing {}".format(self.crossing)
    
    def get_traffic_flow(self, line_str):
        line = self.car_count[line_str]
        now = datetime.now()

        time_diff = (now - self.start_time).total_seconds() / 60 # Difference in minutes
        return line / time_diff

    def get_average_speed(self):
        speed_amount = self.car_speed['speed_amount']
        car_count = self.car_speed['car_count']
        return  '0' if car_count == 0 else str(speed_amount / car_count)

    def get_red_light_infraction(self):
        return str(self.red_light_infraction)
    
    def get_speed_infraction(self):
        return str(self.speed_infraction)
