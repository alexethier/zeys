from zeys.api.special_keys import SpecialKeys

class SpecialKeysBuilder:

  def __init__(self):
    self._special_keys_map = {}

  def add_mapping(self, text, sequence):
    if(text not in self._special_keys_map):
      self._special_keys_map[text] = []

    self._special_keys_map[text].append(sequence)

  # Build an index to quickly determine if ordinal input is a possible special key
  def _generate_special_keys_lookup(self, special_key_map):

    # Map ordinal -> [ ( special_key_text, index ) ]
    # Given an input key number return a list of tuples of special key text and the index of the sequence in the char map
    quick_lookup = {}

    for name in special_key_map:
      sequence_list = special_key_map[name]
      for sequence_index in range(0,len(sequence_list)):

        sequence = sequence_list[sequence_index]
        first_ordinal = sequence[0]

        if(first_ordinal not in quick_lookup):
          quick_lookup[first_ordinal] = []
        quick_lookup[first_ordinal].append((name, sequence_index))

    def custom_sort(e):
      return len(self._special_keys_map[e[0]][e[1]])

    for ordinal in quick_lookup:
      options = quick_lookup[ordinal]
      options.sort(key=custom_sort,reverse=True)

    return quick_lookup

  def build(self):
    special_keys_lookup = self._generate_special_keys_lookup(self._special_keys_map)
    return SpecialKeys(self._special_keys_map, special_keys_lookup)
