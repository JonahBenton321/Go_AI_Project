from pathlib import Path

director_path = Path(r'C:\Users\Jonah Benton\Downloads\8k2\8d')
x =0
for file_path in director_path.iterdir():
    x+=1
    if x % 1000 == 0:
        print(x)

    with open(file_path, 'r') as file:
        contents = file.read()

    fixed_contents = contents.replace('TC', 'C')

    with open(file_path, 'w') as file:
        file.write(fixed_contents)
