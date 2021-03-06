from os import system, name

class Detector:

  def __init__(self, print_group=False, detector = None):

    self._detector = detector

    if(self._detector is None):
      try:
        from zeys.api.nt_detector import NtDetector
        self._detector = NtDetector(print_group=print_group)
        return
      except ModuleNotFoundError:
        pass

    if(self._detector is None):
      try:
        from zeys.api.posix_detector import PosixDetector
        self._detector = PosixDetector(print_group=print_group)
        return
      except ModuleNotFoundError:
        pass

    if(self._detector is None):
      raise Exception("OS is missing required modules: 'termios' for posix systems or 'msvcrt' for nt systems.")

  def run(self):
    return self._detector.run()
