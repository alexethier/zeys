import sys
from zeys.api.detector import Detector

class Runner:

  def __init__(self):
    pass;

  def run(self):

    detector = Detector()
    stream = detector.run()
    for output in stream:
      print(str(output))
      sys.stdout.flush()

def main():
  runner = Runner()
  runner.run()
