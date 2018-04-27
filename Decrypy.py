# NOTE: IMPORTS
# ---------------------------------
from PIL import Image
import numpy as np
import cv2
import math
import wave
import struct
import sys
from colorama import init
init(strip=not sys.stdout.isatty())
from termcolor import cprint, colored
from pyfiglet import figlet_format
# ---------------------------------


# NOTE: CONVERTER FUNCTIONS
# ---------------------------------
def from_code_to_image(path, code):
    size = int(len(code)/3)
    rows = int(math.sqrt(size)) + 1
    cols = int(size/rows) + 1
    counter = 0
    image_array = np.zeros((rows, cols, 3))
    for i in range(0, cols):
        for j in range(0, rows):
            for x in range(0, 3):
                # HACK: Try/catch to avoid index out of bounds
                try:
                    image_array[i][j][x] = ord(code[counter])
                    counter += 1
                except:
                    None # NOTE: Just ignore
    a = np.asarray(image_array)
    a = a.astype('uint8')
    image = Image.fromarray(a)
    image.save(path)

def from_image_to_code(path):
    image_array = cv2.imread(path)
    code = ''
    for i in range(0, len(image_array)):
        for j in range(0, len(image_array[i])):
            for x in range(2, -1, -1):
                if image_array[i][j][x] != 0:
                    code += chr(image_array[i][j][x])
    return code

def from_code_to_audio(path, code):
    wave_file = wave.open(path, 'w')
    wave_file.setnchannels(2)
    wave_file.setsampwidth(2)
    wave_file.setframerate(48000)
    wave_file.setnframes(34816)
    wave_file.setcomptype(comptype='NONE', compname='not compressed')
    chunks = b''
    for char in code:
        chunks += struct.pack('i', ord(char))
    wave_file.writeframes(chunks)
    wave_file.close()

def from_audio_to_code(path):
    wave_file = wave.open(path)
    buffer = 1
    code = ''
    chunk = wave_file.readframes(buffer)
    while len(chunk) is not 0:
        code += chr(struct.unpack('i', chunk)[0])
        chunk = wave_file.readframes(buffer)
    wave_file.close()
    return code
# ---------------------------------

# NOTE: HELPER FUNCTIONS
# ---------------------------------
def write_image(path, image_path):
    with open(path) as file:
        from_code_to_image(image_path, file.read())
        file.close()

def write_text_from_image(path, image_path):
    with open(path, 'w') as file:
        file.write(from_image_to_code(image_path))
        file.flush()
        file.close()

def write_text_from_audio(path, audio_path):
    with open(path, 'w') as file:
        file.write(from_audio_to_code(audio_path))
        file.flush()
        file.close()

def write_audio(path, audio_path):
    with open(path) as file:
        from_code_to_audio(audio_path, file.read())
        file.close()
# ---------------------------------


# NOTE: MAIN THREAD
# ---------------------------------
if __name__ == '__main__':
    if len(sys.argv) is 1:
        cprint(figlet_format('Decrypy',), 'yellow', attrs=['blink', 'bold'])
        print('\n')
        print(colored('\t Options : \n', 'yellow', attrs=['blink', 'blink']))
        print(colored('\t -e -> Encrypt an input text or a file (Operation)\n', 'yellow', attrs=['blink', 'blink']))
        print(colored('\t -d -> Decrypt an image or an audio file to text (Operation)\n', 'yellow', attrs=['blink', 'blink']))
        print(colored('\t \n\n', 'yellow', attrs=['blink', 'blink']))
        print(colored('\t -img -> Encrypt/decrypt from or to an image (Type)\n', 'yellow', attrs=['blink', 'blink']))
        print(colored('\t -aud -> Encrypt/decrypt from or to an audio (Type)\n', 'yellow', attrs=['blink', 'blink']))
        print(colored('\t \n\n', 'yellow', attrs=['blink', 'blink']))
        print(colored('\t -e -img path\\to\\image path\\to\\text\\file (Example)\n', 'yellow', attrs=['blink', 'blink']))
        print(colored('\t -d -aud path\\to\\aud path\\to\\text\\file (Example)\n', 'yellow', attrs=['blink', 'blink']))
    elif len(sys.argv) is not 5:
        cprint(figlet_format('Decrypy',), 'yellow', attrs=['blink', 'bold'])
        print(colored('Created by Borjan Gjorovski', 'yellow', attrs=['blink', 'blink']))
        print('\n')
        print(colored('Incorrect system arguments count!', 'red', attrs=['blink', 'blink']))
    elif len(sys.argv) is 5:
        operation = sys.argv[1]
        type = sys.argv[2]
        source = sys.argv[3]
        destination = sys.argv[4]

        if operation == '-e':
            if  type == '-img':
                write_image(destination, source)
            elif type == '-aud':
                write_audio(destination, source)
        elif operation == '-d':
            if  type == '-img':
                write_text_from_image(destination, source)
            elif type == '-aud':
                write_text_from_audio(destination, source)

        print('\n')
        print(colored('Done!', 'green', attrs=['blink', 'blink']))
# ---------------------------------
