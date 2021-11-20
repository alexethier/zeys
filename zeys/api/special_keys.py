class SpecialKeys:

  def __init__(self, special_keys_map, special_keys_lookup):
    self._special_keys_map = special_keys_map
    self._special_keys_lookup = special_keys_lookup

  def check_special_keys(self, index, capture_group):

    item = capture_group[index]

    special_keys_tuples = self._special_keys_lookup.get(item, [])
    for special_key_text, special_key_index in special_keys_tuples:
      sequence = self._special_keys_map[special_key_text][special_key_index]
      if(index < len(capture_group) - (len(sequence) - 1)):
        match = True
        for sequence_index in range(1, len(sequence)):
          if(capture_group[index + sequence_index] != sequence[sequence_index]):
            match = False
            break

        if(match):
          return special_key_text, len(sequence)

    return None, None
