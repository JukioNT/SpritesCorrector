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

#Getting the sprite size

sprite_size = int(input("What is the sprite size?(If it is 16x16, then type 16)\n>"))
print(f"Selected({sprite_size}x{sprite_size})")

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

    #Choosing when start the cutting

    lines_count = width*height*3

    with open(selected_file, 'r')as image:
        lines = image.readlines()

    image_lines = len(lines)

    start_line = image_lines - lines_count + 1

    sprite = 0

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

        sprite = z
        
    bar.finish()



#Resizing the images


corrected_sprite_size = sprite_size + 2
print('a')

#Create the corrected images
content = f'''P3
# Created by JukioNT's UnitySpriteCorrector v1.0.0 https://github.com/JukioNT
{corrected_sprite_size} {corrected_sprite_size}
255
'''

if answers['answer'] == 'Yes':
    maior_numero = None
    for arquivo in os.listdir('./'):
        if arquivo.endswith('.ppm') and arquivo[:-4].isdigit():
            numero_arquivo = int(arquivo.split('.')[0])
            if maior_numero is None or numero_arquivo > maior_numero:
                maior_numero = numero_arquivo
    z = maior_numero+1


bar = IncrementalBar('Resizing...', max=z)

for y in range(z):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Resizing')
    print(f'{y+1}/{z}({round((y+1)*100/z, 2)}%)')
    bar.next()

    #Read the cutted images
    with open(f'{y}.ppm', 'r') as image:
        lines = image.readlines()


    with open(f'{y}C.ppm', 'w') as corrected:
        corrected.write(content)

    corrected_sprite_pixels = corrected_sprite_size * corrected_sprite_size
    row_lines = sprite_size * 3
    start_line = 4
    corners = []
    first_line = 5+3*sprite_size
    for i in range(corrected_sprite_size):
        corners.append(sprite_size*i*3+5)
        corners.append(sprite_size*i*3+2)
    first = True

    with open(f'{y}C.ppm', 'a') as pixel:
        while start_line < sprite_size*sprite_size*3+3:

            if(start_line == first_line-1 and first):
                start_line = 4
                first = False

            for i in range(3):
                pixel.write(lines[start_line+i])
            
            if start_line+1 in corners:
                for i in range(3):
                    pixel.write(lines[start_line+i])
            
            start_line += 3

        start_line = (sprite_size * sprite_size - sprite_size) * 3 + 5
        first = True

        for i in range(sprite_size):
            for i in range(3):
                pixel.write(lines[start_line-1+i])
            
            if first:
                first = False
                for i in range(3):
                    pixel.write(lines[start_line-1+i])

            start_line += 3
        
        start_line -= 3
        for i in range(3):
            pixel.write(lines[start_line-1+i])

bar.finish()


#Merging the resized sprites


os.system('cls' if os.name == 'nt' else 'clear')
content = f'''P3
# Created by JukioNT's UnitySpriteCorrector v1.0.0 https://github.com/JukioNT
{corrected_sprite_size} {corrected_sprite_size*z}
255
'''

with open(f'00hzwGXppHe.ppm', 'w') as file:
    file.write(content)

bar = IncrementalBar('Merging...', max=z)

with open(f'00hzwGXppHe.ppm', 'a') as file:
    for i in range(z):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Merging')
        print(f'{i+1}/{z}({round((i+1)*100/z, 2)}%)')
        bar.next()

        with open(f'{i}C.ppm', 'r') as image:
            lines = image.readlines()

        x = 4
        while True:
            try:
                file.write(lines[x])
                x+=1
            except:
                os.remove(f'./{i}.ppm')
                os.remove(f'./{i}C.ppm')
                break

bar.finish()
