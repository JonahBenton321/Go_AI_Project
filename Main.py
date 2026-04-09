from pathlib import Path



import numpy as np
import sente
from sente import sgf, rules

director_path = Path(r'C:\Users\Jonah Benton\Downloads\9k\9k')
total_length = 0
tracker = 0
for file_path in director_path.iterdir():
    tracker+=1
    try:
        game = sgf.load(str(file_path), ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
        sequence = game.get_default_sequence()
        total_length+=len(sequence)
    except Exception:
        continue
    if tracker % 1000==0:
        print(f'game {tracker}, total moves {total_length}')
print(total_length)
