# Handled in Csound
    # Instrument amplitude scaling factor

from random import choice, random
import elements


class Piece:
    """A class used to represent the entire piece of music."""

    def __init__(self, melody_voices, drum_voices, bass_voices):
        """Initialize the piece of music"""
        self.mode = self._set_mode()
        self.offset = self._set_offset()
        self.max_line_length = 48
        self.measure_lengths = [8,12,16,20,24,28,32]
        self.melody_voices = melody_voices
        self.drum_voices = drum_voices
        self.bass_voices = bass_voices
        self.voice_list = self._set_voices()
        self.play_count = 0

    def _set_mode(self):

        return choice(elements.mode_options)

    def _set_offset(self):
        return choice(["-0.92","-0.91","-0.9","-0.89","+0.06","+0.05","+0.04","+0.03","+0.02","+0.01","+0"])

    def _set_voices(self):

        voice_list = []

        for __ in range(self.melody_voices):
            voice_list.append(self._construct_voice(elements.melody_instruments))

        inst = choice(elements.drum_instruments)
        for __ in range(self.drum_voices):
            voice_list.append(self._construct_voice(elements.drum_instruments))

        for __ in range(self.bass_voices):
            voice_list.append(self._construct_voice(elements.bass_instruments))

        return voice_list

    def _construct_voice(self, instruments):

        inst = choice(instruments)
        name = inst[0]
        csnd_instrument = choice(inst[1])
        register = choice(inst[2])
        line_length = choice(self.measure_lengths)
        return Voice(name, csnd_instrument, register, line_length, self)

    def perform(self):
        options = [self.loop, self.evolve]
        output = "t 0 360\n"
        section_number = 0
        while section_number < 5:
            self.mode = self._set_mode()
            section_length = 8*10
            output += choice(options)(section_length)
            section_number += 1
        return output #choice(options)(section_length)

    def loop(self,length):
        output = ";LOOP\n"
        for __ in range(length):
            for i in range(len(self.voice_list)):
                note = self.voice_list[i].line.note_list[self.play_count%self.voice_list[i].line_length]
                output += note._play()
            self.play_count += 1
        return output

    def evolve(self,length):
        output = ";EVOLVE\n"
        for __ in range(length):
            for i in range(len(self.voice_list)):
                note = self.voice_list[i].line.note_list[self.play_count%self.voice_list[i].line_length]
                note._evolve()
                output += note._play()
            self.play_count += 1

        #output = ";EVOLVE\nt 0 360\n"
        #for __ in range(length):
        #    for i in range(len(self.voice_list)):
        #        self.voice_list[i].line.evolve()
        #        output += self.voice_list[i].play()
        return output

class Voice:
    """A class used to represent an instrument part."""

    # Methods
        #__init__
            # Select instrument
            # Select register
            # Generate Line
        # mute
        # solo
        # change instrument
        # play in unison with another instrument

    def __init__(self, name, csnd_instrument, register, line_length, piece):
        """Initialize a Voice object"""
        self.name = name
        self.csnd_instrument = csnd_instrument
        self.register = register
        self.line_length = line_length
        self.piece = piece
        self.line = Line(self, piece)
        self.play_count = 0

    def __str__(self):
        """Return string representation."""
        return f'Name:{self.name}, Csnd Inst:{self.csnd_instrument}, Register:{self.register}, Length:{self.line.line_length}'

    def __repr__(self):
        """Return string representation."""
        return self.__str__()

    def play(self):
        """Play Voice's line."""
        output, self.play_count = self.line._play(self.csnd_instrument, self.play_count)
        return output


class Line:
    """A class used to represent a line of music notes"""
    # Methods
        # Generate Line
        # Evolve
        # Transpose
        # Reverse
        # Rewrite
        # Invert

    def __init__(self, voice, piece):
        """Initialize a Line object"""
        self.voice = voice
        self.piece = piece
        self.note_list = self._generate_note_list()

    def __str__(self):
        """Return string representation."""
        return "Note list"

    def __repr__(self):
        """Return string representation."""
        return self.note_list

    def _generate_note_list(self):
        """Generate a list of notes"""
        note_list = []
        for i in range(self.voice.line_length):
            note_list.append(Note(self.piece, self.voice))
        return note_list

    #def _play(self, csnd_instrument, play_count):
    #    output = ""
    #    for i in range(self.voice.line_length):
    #        note = self.note_list[i]
    #        output += f"i {csnd_instrument} {play_count} {note.duration} [{note.amplitude}*{note.on_off}/8] [{note.frequency}]" + "\n"
    #        play_count += 1
    #    return output, play_count

    def evolve(self):
        """Evolve Line."""
        prob = 0.50
        for i in range(self.voice.line_length):
            if random() <= prob:
                self.note_list[i] = Note(self.piece, self.voice)

class Note:
    """A class used to represent a musical note"""

    def __init__(self, piece, voice):
        """Initialize a Note object"""
        self.piece = piece
        self.voice = voice
        self.duration = choice([0.5,0.5,0.5,1,1,1,1,1,3,3,3,6])
        self.amplitude = choice([0.3,0.5,0.7,0.9])
        self.on_off = choice([0,0,0,1])
        self.frequency = self._set_frequency()

    def __str__(self):
        """Return string representation."""
        return "Note"

    def __repr__(self):
        """Return string representation."""
        return str(self.frequency)

    def _set_frequency(self):
        return f"{self.voice.register} + {choice(self.piece.mode[1])} {self.piece.offset}"

    def _play(self):
        """Return Csound note event"""
        output = f"i {self.voice.csnd_instrument} {self.piece.play_count} {self.duration} [{self.amplitude}*{self.on_off}/8] [{self.frequency}] ;{self.piece.mode[0]}" + "\n"
        return output

    def _evolve(self):
        """Evolve note"""
        """Evolve Line."""
        prob = 0.5
        if random() <= prob:
            self.__init__(self.piece, self.voice)
