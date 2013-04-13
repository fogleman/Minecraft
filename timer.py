# Imports, sorted alphabetically.

# Python packages
# Nothing for now...

# Third-party packages
# Nothing for now...

# Modules from this project
# Nothing for now...


class TimerTask(object):
    def __init__(self, ticks, callback, speed):
        self.ticks = self.expire = ticks
        self.callback = callback
        self.speed = speed

    def progress(self):
        return self.ticks / self.expire


# Timer used in furnace and redstone circuits
class Timer(object):
    def __init__(self):
        self.queue = [None]

    def add_task(self, ticks, callback, speed=1):
        if ticks == 0 and callback is not None:
            callback()

        task = TimerTask(ticks, callback, speed)
        for index, _task in enumerate(self.queue):
            if _task is None:
                self.queue[index] = task
                return index

        self.queue.append(task)
        return len(self.queue) - 1

    def remove_task(self, index):
        if index >= len(self.queue):
            return False

        self.queue[index] = None
        return True

    def schedule(self, interval):
        for index, _task in enumerate(self.queue):
            if _task is None:
                continue
            self.queue[index].ticks -= interval * self.queue[index].speed
            if self.queue[index].ticks <= 0:
                self.queue[index].callback()
                self.queue[index] = None

    def progress(self, index):
        if index >= len(self.queue):
            return 0

        if self.queue[index] is not None:
            return self.queue[index].progress()
        else:
            return 0
