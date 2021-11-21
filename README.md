# Python Zeys
*zeys* is library for detecting typed keys in Python.

# Zeys features
* Pure python
* No dependencies
* Windows NT and Posix support (Linux and MacOS)
* Detect individual alphanumeric keys typed
* Detect special keys typed (enter, arrow keys, etc)
* Customizable output when special keys are typed.

# Installation
```
pip install zeys
```

# Getting Started
The most simple example of the library would look like this:
```
from zeys.api.detector import Detector
import sys

if __name__ == "__main__":
    print("Type some keys!")
    detector = Detector()
    detections_generator = detector.run()
    print()
    for key_typed in detections_generator:
      print(f'You typed: {key_typed}')
```
# Usage
The Detector class can be used to detect user's input keys. When the run() function is called a generator is returned. Stdin will be polled and any keys the user enters will be accessible through the generator. The keys returned will be Python strings. For alphanumeric characters the string representation of a character is returned. For example, if a user types 'a', then 'a' will be output by the generator. For special keys such as the enter key or arrow keys, a text string such as "enter" or  "arrow-right" will be output. The user can change which text strings are outputted for special keys by providing custom configurations. See the Special Keys section below for more details.

# Special Keys
You can configure which text is output when typing an enter key, arrow key, or other special key. This is done by using the `SpecialKeysBuilder` class. The `add_mapping` function can be used to map a string text output to a sequence of stdin inputs when a key is pressed. Note the example below:
```
from zeys.api.special_keys_builder import SpecialKeysBuilder
from zeys.api.posix_detector import PosixDetector

special_keys_builder = SpecialKeysBuilder()
special_keys_builder.add_mapping("arrow-up", [ 27, 91, 65 ])
special_keys = special_keys_builder.build()

detector = PosixDetector(special_keys)
```
In the example above a keyboard is setup on a Linux OS. When the user types the up arrow key, the keyboard provides 3 inputs to stdin: 27, 91, and 65. Note that the three numbers are keyboard specific and can vary across systems. In this example the `add_mapping` call is used to translate this sequence to output the text `arrow-up` whenever the up arrow key is typed.

To determine the numerical sequences outputted by a key press you can create a detector with the `print_group` option set to true like so: `detector = Detector(print_group=True)`. On any key press, the sequence of numbers outputted on each key typed will be printed to the terminal. These outputs can be used to configure custom special key values.

Some special keys will not trigger any output. These include `shift`, `caps lock`, and possibly others.

# Philosophy
Detecting the keys a user has typed into stdin should be easy and simple to use. It should not require root or any additional python installs. Complex issues between the Python runtime and the OS should be fully masked by the library.
