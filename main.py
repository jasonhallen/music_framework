from random import choice, randrange, random, sample
from classes import Piece
# from rules import *
import ctcsound
from datetime import datetime
import os

# TASKS
    # Alignment at start, center, or end of section
    # Evolve to line
    # Copy another instrument line but shift the beat
    # Evolving transitions from one line to another versus abrupt transitions
    # Add sections of rests in between lines for more space
    # Arpeggios
    # 3/4 time, cross rhythms

# CODING TIPS FROM JAMES
    # A method should be no longer than 10 lines. If it's longer, break it up into multuiple methods
    # If you're copying and pasting a chunk of code, DON'T.  Turn it into a method.
    # Pass objects into another object.
        # Voice(piece)
        # __init__(piece):
            # self.mode = piece.mode

def main(title=None):

    # Piece takes # melody, # rhythm, # bass
    piece = Piece(melody_voices=4, drum_voices=3, bass_voices=1)
    score = piece.perform()

    print(score)

    with open("orchestra.orc","r") as csnd_orchestra:
        csd = ""
        for line in csnd_orchestra:
            csd += line

    csd = csd + score + '''

    s
    i 1 0 1 0 0 0
    i -1000 2 0

    </CsScore>
    </CsoundSynthesizer>
    '''
    # cs = ctcsound.Csound()
    # ret = cs.compileCsdText(csd)
    # if ret == ctcsound.CSOUND_SUCCESS:
    #     cs.start()
    #     cs.perform()
    #     cs.reset()
    #
    # title_chars=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","1","2","3","4","5","6","7","8","9"]
    # title = ""
    #
    # for i in range(7):
    #     title += choice(title_chars)
    # date = datetime.today().strftime('%Y_%m_%d')
    # if not os.path.exists(f"output/{date}"):
    #     os.makedirs(f"output/{date}")
    # path = f"output/{date}/"
    # filename = f"{date}_{title}.csd"
    # print(filename)

    if not os.path.exists("output/class"):
        os.makedirs("output/class")
    path = "output/class"
    filename = f"{title}.csd"

    with open(f"{path}/{filename}", "w") as f:
        f.write(csd)
    f.close()

def generate_class():

    class_names = ("jason", "james", "aishee", "aldo", "ben", "cat", "edward", "eric", "henry", "jack d.", "jack r.", "john", "junyi", "kaeden", "kate", "peter", "piper", "rebecca", "rie", "sam", "vic", "yasmeen", "yemi")

    for i in range(len(class_names)):
        title = class_names[i]
        main(title)

#main()
generate_class()
