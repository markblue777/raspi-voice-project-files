# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Detect claps in the audio stream."""

import logging
import speech_recognition as sr
from triggers.trigger import Trigger

logger = logging.getLogger('trigger')


class SpeechTrigger(Trigger):

    """Detect claps in the audio stream."""

    def __init__(self, recorder, phrase, audioSampleRate, audioSampleSize):
        super().__init__()
        self.phrase = phrase
        self.have_phrase = True  # don't start yet
        self.prev_sample = 0
        self.audioSampleRate = audioSampleRate
        self.audioSampleSize = audioSampleSize
        recorder.add_processor(self)

    def start(self):
        self.prev_sample = 0
        self.have_phrase = False

    def add_data(self, data):
        ##need to get the supplied data to valid audio stream to be passed through phonix or some speech to text parser

        #get the recognizer
        r = sr.Recognizer()

        ##data dont need to go through microphone as it is from that already
        ##maybe convert data to a temp wav file to pass into speech rec
        ##this should convert it to an audio file to be able to pass it through sphinx
        audio = sr.AudioData(data, self.audioSampleRate, self.audioSampleSize)

        #pass through sphinx to get the text
        ##if sphinx aint any good then chop out to a different handler (maybe even google speach engine api - limits apply
        try:
            text = r.recognize_sphinx(audio)
            print("Sphinx thinks you said " + text)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

        #
        if not self.have_phrase:
            if text == self.phrase:
                logger.info("clap detected")
                self.have_phrase = True
                self.callback()

        ##prob dont need this as this is used for detecting a sharp clap sound i think
        self.prev_sample = audio[-1]
