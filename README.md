# Python Zeys
*zeys* is library for detecting typed keys in Python.

# Zeys features
* Pure python
* No dependencies
* Windows NT and Posix support (Linux and MacOS)
* Detect individual alphanumeric keys typed
* Detect special keys typed (enter, arrow keys, etc)
* Customizable special key detections - custom configurations for alternate keyboards

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
The Detector class can be used to detect user's input keys. When the run() function is called a generator is returned. Stdin will be polled and any keys the user enters will be accessible through the generator. The keys returned will be strings. For alphanumeric characters the string representation of a character is returned. If a user types 'a', then 'a' will be output by the generator. For special keys such as the enter key or arrow keys, a text string such as "enter" or  "arrow-right". The user can provide a custom configuration for special keys - see the Special Keys section below.

# Special Keys
You can configure which text output is produced by the generator. This is done by using the `SpecialKeysBuilder` class. The `add_mapping` function can be used to map a string text output to a sequence of stdin inputs when a key is pressed. Note example below:
```
from zeys.api.special_keys_builder import SpecialKeysBuilder
from zeys.api.posix_detector import PosixDetector

special_keys_builder = SpecialKeysBuilder()
special_keys_builder.add_mapping("arrow-up", [ 27, 91, 65 ])
special_keys = special_keys_builder.build()

detector = PosixDetector(special_keys)
```
In the example above a keyboard is setup that such that when the user presses the up arrow key, the keyboard provides 3 inputs to stdin: 27, 91, and 65. Note the three numbers are keyboard specific and can vary across systems. The add_mapping call is used to translate this sequence to output the text `arrow-up` whenever the up arrow key is pressed.

For keys such as arrow keys, a single key press will generate multiple integer inputs to `stdin`. These inputs vary from OS and keyboard so the custom special key inputs may be needed to support certain keyboard or OS types. There are two detector types PosixDetector for Linux and MacOS systems and NtDetector for Windows OS.

# Philosophy
Detecting the keys a user has typed into stdin should be easy and simple to use. It should not require root or any additional python installs. Complex issues between the Python runtime and the OS should be fully masked by the library.
