import sys
from zeys.api.arrow_selection_prompt import ArrowSelectionPrompt

class Runner:

  def __init__(self):
    pass;

  def run(self):

    detector = Detector()
    stream = detector.run()
    print()
    for output in stream:
      print(str(output))
      sys.stdout.flush()

def main():
  runner = Runner()
  runner.run()
