from pathlib import Path
"""
The SGF file we have in out data set somtimes are in an outdated format
This code update the files to a modern format compatible with sente
"""
director_path = Path(r'C:\Users\data_location')
x = 0
for file_path in director_path.iterdir():
    x+=1
    if x % 1000 == 0: # Print progress updates
        print(f'Fixed {x} files')

    with open(file_path, 'r') as file:
        contents = file.read()

    fixed_contents = contents.replace('TC', 'C')

    with open(file_path, 'w') as file:
        file.write(fixed_contents)
