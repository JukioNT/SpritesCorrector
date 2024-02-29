import os
import fnmatch
from PIL import Image
import os
from progress.bar import IncrementalBar
import inquirer

questions = [
  inquirer.List('answer',
                message="Already did the first part?",
                choices=['Yes', 'No'],
            ),
]

answers = inquirer.prompt(questions)
if answers['answer'] == 'No':
    #Selecting the file

    directory = '.'
    file_type = '*.ppm'

    files = [file for file in os.listdir(directory) if fnmatch.fnmatch(file, file_type)]

    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    selection = int(input('Select a file: ')) -1

    selected_file = files[selection]
    print(f"Selected: {selected_file}")

    #Getting width and height of the image

    image = Image.open(selected_file)
    width, height = image.size

    print(f'Width: {width} \nHeight: {height}')

    #Getting the sprite size

    sprite_size = int(input("What is the sprite size?(If it is 16x16, then type 16)\n>"))
    print(f"Selected({sprite_size}x{sprite_size})")

    #Choosing when start the cutting

    lines_count = width*height*3

    with open(selected_file, 'r')as image:
        lines = image.readlines()

    image_lines = len(lines)

    start_line = image_lines - lines_count + 1

    print(f'Start on line {start_line}')

    #Cutting the images

    content = f'''P3
    # Created by JukioNT's UnitySpriteCorrector v1.0.0 https://github.com/JukioNT
    {sprite_size} {sprite_size}
    255
    '''

    sprite_pixels = sprite_size * sprite_size
    sprites_count = int((width * height) / (sprite_pixels))
    print(f"Sprites Quantity: {sprites_count}")

    sprite_lines = sprite_pixels * 3
    sprite_line_quantity = width / sprite_size
    sprite_jump = sprite_size * sprite_line_quantity * 3
    row_jump = sprite_lines * sprite_line_quantity

    z = 0
    bar = IncrementalBar('Cutting...', max=sprites_count)
    counter = 0
    row_mul = 1

    while z < sprites_count:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Cutting')
        print(f'{z+1}/{sprites_count}({round(((z+1)*100)/sprites_count, 2)}%)')
        bar.next()

        with open(f'{z}.ppm', 'w') as cutted:
            cutted.write(content)

        for y in range(sprite_size):
            row=start_line + sprite_jump * y
            for i in range(sprite_size * 3):
                with open(f'{z}.ppm', 'a') as file:
                    file.write(str(lines[int(row+i-1)]))
        z+=1
        start_line += (sprite_size * 3)
        counter+=1
        if counter == sprite_line_quantity:
            counter = 0
            start_line = (image_lines - lines_count + 1) + row_jump * row_mul
            row_mul += 1
        
    bar.finish()

with open('2.ppm', 'r') as file:
    lines = file.readlines()

lines[2] = '18 18\n'

with open('2.ppm', 'w') as file:
    lines = file.writelines(lines)


