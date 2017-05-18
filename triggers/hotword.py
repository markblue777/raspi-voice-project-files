from triggers.trigger import Trigger
import threading
from google.assistant.library import Assistant
from google.assistant.library.event import EventType


class HotwordTrigger(Trigger):
    def __init__(self, credentials):
        self.callback = None
        self.credentials = credentials

    def set_callback(self, callback):
        self.callback = callback

    def start(self):
        threading.Thread(target=self.run_assistant).start()

    def run_assistant(self):
        with Assistant(self.credentials) as assistant:
            for event in assistant.start():
                if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
                    break
        self.callback()