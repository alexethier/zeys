from os import system, name

class Detector:

  def __init__(self):

    self._detector = None
    if name == 'nt':
      from zeys.api.nt_detector import NtDetector
      self._detector = NtDetector()
    else:
      from zeys.api.posix_detector import PosixDetector
      self._detector = PosixDetector()

  def run(self):
    return self._detector.run()
    #generator = self._detector.run()
    #for item in generator:
    #  yield item