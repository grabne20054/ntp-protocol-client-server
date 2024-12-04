from time import localtime, strftime

class NTPPacket:

    def __init__(self) -> None:
        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        self.t4 = 0

        self.leap_indicator = 0
        self.stratum = 0

        self.poll = 0
        self.precision = 0
        self.root_delay = 0
        self.root_dispersion = 0

    def get_local_time(self):
        return strftime(" %H:%M:%S", localtime())
    
    def calculate_offset(self):
        return ((self.t2 - self.t1) + (self.t3 - self.t4)) / 2
    
    def calculate_delay(self):
        return (self.t2 - self.t1) - (self.t3 - self.t4)
    
    def synchronize(self):
        return self.t4 + self.calculate_offset()
        

    def set_t1(self, t1: int) -> None:
        self.t1 = t1
    
    def set_t2(self, t2: int) -> None:
        self.t2 = t2

    def set_t3(self, t3: int) -> None:
        self.t3 = t3
    
    def set_t4(self, t4: int) -> None:
        self.t4 = t4

    
    def __str__(self) -> str:
        return f"t1: {self.t1}, t2: {self.t2}, t3: {self.t3}, t4: {self.t4}, leap_indicator: {self.leap_indicator}, stratum: {self.stratum}, poll: {self.poll}, precision: {self.precision}, root_delay: {self.root_delay}, root_dispersion: {self.root_dispersion}"
    

a = NTPPacket()
print(a.get_local_time())