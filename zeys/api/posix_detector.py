from zeys.api.special_keys_builder import SpecialKeysBuilder
import io
import sys
import time
import select
import termios
import tty

DELETE_CHAR='\x7f'
ENTER_CHAR='\n'
ESC_CHAR='\x1b'
TAB_CHAR='\t'

DEFAULT_SPEED = 0.03

class PosixDetector:

  def __init__(self, special_keys=None, speed=None):
    self._special_keys = special_keys
    self._speed = speed

    if(special_keys is None):
      self._special_keys = self.get_default_special_keys_builder().build()
    if(speed is None):
      self._speed = DEFAULT_SPEED

  # Map special key outputs to their input sequence of ordinal key numbers
  def get_default_special_keys_builder(self):
   
    special_keys_builder = SpecialKeysBuilder()
    special_keys_builder.add_mapping("enter", [ ord(ENTER_CHAR) ])
    special_keys_builder.add_mapping("esc", [ ord(ESC_CHAR) ])
    special_keys_builder.add_mapping("tab", [ ord(TAB_CHAR) ])
    special_keys_builder.add_mapping("delete", [ ord(DELETE_CHAR) ])
    special_keys_builder.add_mapping("arrow-up", [ 27, 91, 65 ])
    special_keys_builder.add_mapping("arrow-down", [ 27, 91, 66 ])
    special_keys_builder.add_mapping("arrow-right", [ 27, 91, 67 ])
    special_keys_builder.add_mapping("arrow-left", [ 27, 91, 68 ])

    return special_keys_builder

  def _has_data(self):
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

  # Low level capture function
  def _capture(self):
    settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
      with io.open(sys.stdin.fileno(), 'rb', buffering=0, closefd=False) as std:

        data = []
        while True:
          if(self._has_data()):
            input_obj = x=std.read(1)
            char = input_obj[0]
            data.append(int(char))
          else:
            time.sleep(self._speed)
            if(len(data) > 0):
              yield data
              data = []

    finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

  def run(self):

    capture_generator = self._capture()
    for capture_group in capture_generator:
      skip = 0
      for index in range(0, len(capture_group)):
        if(skip > 0):
          skip = skip -1
        else:
          item = capture_group[index]
          #print("ordinal: " + str(item))
          special_key, sequence_length = self._special_keys.check_special_keys(index, capture_group)
          if(special_key is not None):
            skip = sequence_length - 1
            yield special_key
          else:
            yield chr(item)
