from global_settings import *


class Timer:
    # class to manage timers for the game
    def __init__(self, duration, repeated=False, func=None):
        self.repeated = repeated
        self.func = func
        self.duration = duration

        self.start_time = 0
        self.active = False

    def start(self):
        # start the timer
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        # stop the timer
        self.active = False
        self.start_time = 0

    def update(self):
        # update the time within the timer
        current_time = pygame.time.get_ticks()
        if self.active:
            if current_time - self.start_time >= self.duration:
                if self.func and self.start_time != 0:
                    self.func()
                self.stop()

                if self.repeated:
                    self.start()
