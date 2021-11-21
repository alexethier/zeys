import io
import sys
import time
import msvcrt

RETURN_CHAR='\r'
#NEWLINE_CHAR='\n'
ESC_CHAR='\x1b'
TAB_CHAR='\t'

DEFAULT_SPEED = 0.03

class NtDetector:

  def __init__(self, print_group=False, special_key_map=None, speed=None):
    self._print_group = print_group
    if(special_key_map is None):
      special_key_map = self.get_default_special_key_map()
    if(speed is None):
      speed = DEFAULT_SPEED

    # Special key text -> list of ordinals to match against
    self._special_key_map = special_key_map
    # First ordinal in special key map sequence -> list of special keys in special key map that match the first ordinal
    # The list of special keys is ordered by the special key with the longest ordinal match
    self._lookup_key_map = self._get_special_key_index(special_key_map)
    self._speed = speed

  # Map special key outputs to their input sequence of ordinal key numbers
  def get_default_special_key_map(self):
    char_map = {}
    char_map["enter"] = [ ord(RETURN_CHAR) ]
    char_map["esc"] = [ ord(ESC_CHAR) ]
    char_map["tab"] = [ ord(TAB_CHAR) ]
    char_map["delete"] = [ 8 ]
    char_map["delete"] = [ 0, 83 ]
    char_map["delete"] = [ 224, 83 ]
    char_map["arrow-up"] = [ 224, 72 ]
    char_map["arrow-down"] = [ 224, 80 ]
    char_map["arrow-right"] = [ 224, 77 ]
    char_map["arrow-left"] = [ 224, 75 ]

    return char_map

  # Build an index to quickly determine if ordinal input is a possible special key
  def _get_special_key_index(self, special_key_map):

    quick_lookup = {}

    for name in special_key_map:
      ordinal = special_key_map[name][0]
      if(ordinal not in quick_lookup):
        quick_lookup[ordinal] = []
      quick_lookup[ordinal].append(name)

    def custom_sort(e):
      return len(self._special_key_map[e])

    for ordinal in quick_lookup:
      options = quick_lookup[ordinal]
      options.sort(key=custom_sort,reverse=True)

    return quick_lookup

  def _has_data(self):
    return msvcrt.kbhit()

  # Low level capture function
  def _capture(self):
    with io.open(sys.stdin.fileno(), 'rb', buffering=0, closefd=False) as std:

      data = []
      while True:
        if(self._has_data()):
          input_obj = msvcrt.getch()
          char = input_obj[0]
          data.append(char)
        else:
          time.sleep(self._speed)
          if(len(data) > 0):
            yield data
            data = []

  def _check_special_keys(self, index, capture_group):

    item = capture_group[index]

    special_keys = self._lookup_key_map.get(item, [])
    for special_key in special_keys:
      sequence = self._special_key_map[special_key]
      if(index < len(capture_group) - (len(sequence) - 1)):
        match = True
        for sequence_index in range(1, len(sequence)):
          if(capture_group[index + sequence_index] != sequence[sequence_index]):
            match = False
            break

        if(match):
          return special_key

    return None

  def run(self):

    capture_generator = self._capture()
    for capture_group in capture_generator:
      if(self._print_group):
        print("stdin input sequence: " + str(capture_group))
      skip = 0
      for index in range(0, len(capture_group)):
        if(skip > 0):
          skip = skip -1
        else:
          item = capture_group[index]
          #print("ordinal: " + str(item))
          special_key = self._check_special_keys(index, capture_group)
          if(special_key is not None):
            skip = len(self._special_key_map[special_key]) - 1
            yield special_key
          else:
            yield chr(item)
