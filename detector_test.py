from zeys.api.detector import Detector
import sys

class Boot:

  def __init__(self):
    pass;

  def boot(self):

    sys.stdout.write("Example prompt: ")
    sys.stdout.flush()
    detector = Detector()
    stream = detector.run()
    print()
    for output in stream:
      print("DETECTED: " + str(output))
      sys.stdout.flush()

if __name__ == "__main__":
  boot = Boot()
  boot.boot()
