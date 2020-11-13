from random import choice
from classes import *
import ctcsound

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

def main():

    # Piece takes # melody, # rhythm, # bass

    piece = Piece(melody_voices=4, drum_voices=3, bass_voices=1)
    output = piece.perform()

    print(output)

    #csnd_ochrestra = open("orchestra.orc","r")
    #csd = csnd_ochrestra.read()

    with open("orchestra.orc","r") as csnd_orchestra:
        csd = ""
        for line in csnd_orchestra:
            csd += line

    cs = ctcsound.Csound()
    csd = csd + output + '''

    s
    i 1 0 1 0 0 0
    i -1000 2 0

    </CsScore>
    </CsoundSynthesizer>
    '''

    ret = cs.compileCsdText(csd)
    if ret == ctcsound.CSOUND_SUCCESS:
        cs.start()
        cs.perform()
        cs.reset()

main()
