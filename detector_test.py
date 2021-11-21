from zeys.api.detector import Detector
import sys

class Boot:

  def __init__(self):
    pass;

  def boot(self):

    print_group = False
    if("-v" in sys.argv):
      print_group = True

    sys.stdout.write("Test Keyboad Detection: ")
    sys.stdout.flush()
    detector = Detector(print_group=print_group)
    stream = detector.run()
    print()
    for output in stream:
      print("DETECTED: " + str(output))
      sys.stdout.flush()

if __name__ == "__main__":
  boot = Boot()
  boot.boot()
