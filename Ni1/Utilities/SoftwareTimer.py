class SoftwareTimer:
    timeCounters = []
    flags = []
    tick = 100

    def __init__(self):
        return

    def setTimer(self, number, duration):
        while len(self.timeCounters) <= number:
            self.timeCounters.append(0)
            self.flags.append(0)
        self.timeCounters[number] = duration / self.tick
        self.flags[number] = 0
        # print("lenght ST: " + str(len(self.timeCounters)))

    def timerRun(self):
        for i in range(len(self.timeCounters)):
            if self.timeCounters[i] > 0:
                self.timeCounters[i] -= 1
                if self.timeCounters[i] <= 0:
                    self.flags[i] = 1
    
    def isExpire(self, number):
        if self.flags[number] == 1:
            # self.flags[number] = 0
            return True
        else : 
            return False