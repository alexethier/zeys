DELETE_CHAR='\x7f'
RETURN_CHAR='\r'
#NEWLINE_CHAR='\n'
ESC_CHAR='\x1b'
TAB_CHAR='\t'

SPEED = 0.03

class NtDetector:

  def __init__(self):
    import io
    import sys
    import time
    import msvcrt

  def _has_data(self):
    return msvcrt.kbhit()

  # Low level capture function
  def _capture(self):
    with io.open(sys.stdin.fileno(), 'rb', buffering=0, closefd=False) as std:

      data = []
      while True:
        if(self._has_data()):
          #input_obj = x=std.read(1)
          input_obj = msvcrt.getch()
          #print("ae: " + str(input_obj))
          char = input_obj[0]
          data.append(char)
        else:
          time.sleep(SPEED)
          if(len(data) > 0):
            yield data
            data = []

  def run(self):

    capture_generator = self._capture()
    for capture_group in capture_generator:
      skip = 0
      for index in range(0, len(capture_group)):
        if(skip > 0):
          skip = skip -1
        else:
          item = capture_group[index]

          if(int(item) == 27 and index < len(capture_group) - 2):
            item2 = capture_group[index + 1]
            item3 = capture_group[index + 2]
            if(item2 == 91):
              if(item3 == 67):
                skip = 2
                yield "arrow-right"
              elif(item3 == 65):
                skip = 2
                yield "arrow-up"
              elif(item3 == 68):
                skip = 2
                yield "arrow-left"
              elif(item3 == 66):
                skip = 2
                yield "arrow-down"
          elif (chr(item) == RETURN_CHAR):
            yield "enter"
          elif chr(item) == ESC_CHAR:
            yield "ESC"
          elif chr(item) == DELETE_CHAR:
            yield "delete"
          elif chr(item) == TAB_CHAR:
            yield "tab"
          else:
            #print("item #: " + str(item))
            yield chr(item)
            #char = chr(item)
            #if char in string.printable:
            #  yield char
            #else:
            #  skip = len(capture_group) - index
