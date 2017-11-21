from datetime import datetime
import logging


class Chrono(object):
    def __init__(self, is_enabled=True):
        self.is_enabled = is_enabled
        self.checkpoint = datetime.now()

    def save(self, title):
        if self.is_enabled:
            now = datetime.now()
            delta = now - self.checkpoint
            print('Chrono: %s [%dms]' % (title, round(delta.total_seconds() * 1000)))
            self.checkpoint = now
