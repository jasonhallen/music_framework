from random import choice, randrange, random, sample
from classes import Piece
# from rules import *
import ctcsound
from datetime import datetime
import os
import PySimpleGUI as sg

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

    sg.theme('Default1')
    sg.set_options(font=("Helvetica",25))

    frame_instruments = [[sg.Text('Melody: '), sg.Spin([i for i in range(0,11)], initial_value=4, key="-MELODY-", size=(2,1))],
                        [sg.Text('Drums: '), sg.Spin([i for i in range(0,11)], initial_value=4, key="-DRUMS-", size=(2,1))],
                        [sg.Text('Bass: '), sg.Spin([i for i in range(0,11)], initial_value=1, key="-BASS-", size=(2,1))],
                        [sg.Button('Generate'), sg.Exit()]]

    frame_parameters = [[sg.Text("Min sections:"), sg.Spin([i for i in range(5,100)], initial_value=20, key="-MIN_SECTIONS-", size=(4,1))],
                        [sg.Text("Tempo: "), sg.Slider(range=(40,480), orientation="horizontal", key="-TEMPO-", size=(10,10), default_value=320)],
                        [sg.Text("Swing:"), sg.Slider(range=(0,0.4), orientation="horizontal",resolution=0.01, default_value=0, key="-SWING-", size=(10,10))]]

    frame_rules = [[sg.Text("Rules")]]

    image_play = './images/play.png'

    frame_playback = [[sg.Button('Play', button_color=("white", "white"), image_filename='./images/play.gif', image_subsample=1, border_width=0),
                      sg.Button('Pause', button_color=("white", "white"), image_filename='./images/pause.gif', image_subsample=1, border_width=0),
                      sg.Button('Stop', button_color=("white", "white"), image_filename='./images/stop.gif', image_subsample=1, border_width=0),
                      sg.Button('Rewind', button_color=("white", "white"), image_filename='./images/rewind_2.gif', image_subsample=1, border_width=0),
                      sg.Button('Save', button_color=("white", "white"), image_filename='./images/save_2.gif', image_subsample=1, border_width=0),
                      sg.Button('Trash', button_color=("white", "white"), image_filename='./images/trash.gif', image_subsample=1, border_width=0),
                      sg.Text("0.00.00", key="-TIMER-")]] #, sg.Button('Rec'), sg.Button('StopRec')]]

    col_left = [[sg.Text('GENERATOR')],
              [sg.Frame("Instruments", frame_instruments)],
              [sg.Frame('Parameters', frame_parameters)],
              [sg.Frame("Rules", frame_rules)]]

    col_right = [[sg.Text("OVERVIEW")],
                [sg.MLine(key='-OVERVIEW-'+sg.WRITE_ONLY_KEY, size=(70,12), font=("Helvetica",12), default_text="NO CSD LOADED", do_not_clear=False)],
                [sg.Text("CSD")],
                [sg.MLine(key='-CSD_VIEWER-'+sg.WRITE_ONLY_KEY, size=(70,15), font=("Helvetica",12), default_text="NO CSD LOADED", do_not_clear=False)],
                [sg.Frame("Playback", frame_playback)]]

    layout = [[sg.Column(col_left), sg.Column(col_right)]]


    window = sg.Window('Music Generator', layout)
    cs = ctcsound.Csound()
    # while True:                             # The Event Loop
    #     event, values = window.read()
    #     if event == sg.WIN_CLOSED or event == 'Exit':
    #         break
    #     if event == 'Run':
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # Piece takes # melody, # rhythm, # bass
        # piece = Piece(melody_voices=4, drum_voices=3, bass_voices=0)
        if event == "Generate":
            csd = generate_score(values, cs)
            window['-CSD_VIEWER-'+sg.WRITE_ONLY_KEY](csd)
            window['-CSD_VIEWER-'+sg.WRITE_ONLY_KEY].set_vscroll_position(0)
            pt = ctcsound.CsoundPerformanceThread(cs.csound())
        if event == "Play":
            pt.play()
        if event == "Pause":
            pt.pause()
        if event == "Stop":
            pt.stop()
            pt.join()
            cs.reset()
        if event == "Rec":
            pt.record("test.wav",44100, 2)
        if event == "StopRec":
            pt.stopRecord()

        #window['-TIMER-'].update()

    window.close()


def generate_score(values, cs):
    piece = Piece(melody_voices=values["-MELODY-"], drum_voices=values["-DRUMS-"], bass_voices=values["-BASS-"], tempo=values["-TEMPO-"], swing=values["-SWING-"])
    score = piece.perform()
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
    # pt = ctcsound.CsoundPerformanceThread(cs.csound())
    ret = cs.compileCsdText(csd)
    if ret == ctcsound.CSOUND_SUCCESS:
        cs.start()
    return csd

def other():

    title_chars=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","1","2","3","4","5","6","7","8","9"]
    title = ""

    for i in range(7):
        title += choice(title_chars)
    date = datetime.today().strftime('%Y_%m_%d')
    if not os.path.exists(f"output/{date}"):
        os.makedirs(f"output/{date}")
    path = f"output/{date}/"
    filename = f"{date}_{title}.csd"
    print(filename)

    # if not os.path.exists("output/class"):
    #     os.makedirs("output/class")
    # path = "output/class"
    # filename = f"{title}.csd"

    with open(f"{path}/{filename}", "w") as f:
        f.write(csd)
    f.close()

    return cs

def generate_class():

    class_names = ("jason", "james", "aishee", "aldo", "ben", "cat", "edward", "eric", "henry", "jack d.", "jack r.", "john", "junyi", "kaeden", "kate", "peter", "piper", "rebecca", "rie", "sam", "vic", "yasmeen", "yemi")

    for i in range(len(class_names)):
        title = class_names[i]
        main(title)

main()
# generate_class()
