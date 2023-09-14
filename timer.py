from global_settings import *


# Class to manage timers for the game
class Timer:
    def __init__(self, duration, repeated=False, func=None):
        # Constructor, parameters duration, repeated and func
        self.repeated = repeated
        self.func = func
        self.duration = duration

        self.start_time = 0
        self.started = False

    def start(self):
        # start the timer
        self.started = True
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        # stop the timer
        self.started = False
        self.start_time = 0

    def update(self):
        # update the time within the timer to check duration
        current_time = pygame.time.get_ticks()
        if self.started:
            if current_time - self.start_time >= self.duration:
                if self.func and self.start_time != 0:
                    # call to function if one is present in parameter
                    self.func()
                self.stop()
                # run timer again if repeated
                if self.repeated:
                    self.start()
