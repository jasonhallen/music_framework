from random import choice, random, randrange
import elements
from rules import *


class Piece:
    """A class used to represent the entire piece of music."""

    def __init__(self, melody_voices, drum_voices, bass_voices):
        """Initialize the piece of music"""
        self.mode = Mode()
        self.offset = self._set_offset()
        self.max_line_length = 48
        self.measure_lengths = [8,12,16,20,24,28,32] #[num for num in range(8,33)]
        self.melody_voices = melody_voices
        self.drum_voices = drum_voices
        self.bass_voices = bass_voices
        self.voice_list = self._set_voices()
        self.play_count = 0
        self.rule_engine = RuleEngine(self)
        self.swing_offset = random()/4
        self.max_sections = randrange(15,25)

    def _set_offset(self):
        return choice(["-0.92","-0.91","-0.9","-0.89","+0.06","+0.05","+0.04","+0.03","+0.02","+0.01","+0"])

    def _set_voices(self):

        voice_list = []

        for __ in range(self.melody_voices):
            voice_list.append(self._construct_voice(choice(elements.melody_instruments)))

        drum_kit = choice(elements.drum_instruments)
        for __ in range(self.drum_voices):
            voice_list.append(self._construct_voice(drum_kit))

        for __ in range(self.bass_voices):
            voice_list.append(self._construct_voice(choice(elements.bass_instruments)))

        return voice_list

    def _construct_voice(self, instrument):

        name = instrument[0]
        csnd_instrument = choice(instrument[1])
        register = choice(instrument[2])
        line_length = choice(self.measure_lengths)
        return Voice(name, csnd_instrument, register, line_length, self)

    def perform(self):
        tempo = randrange(300,360)
        output = f"t 0 {tempo}\n"
        section_number = 0
        print("INSTRUMENTS")
        [print(instrument) for instrument in self.voice_list]
        print()
        section_rules = [[],[]]

        while not any(rule.function == Rule.end for rule in section_rules[0]):
            # self.rule_engine.update()
            # apply section rules
            # play through notes, apply note rules

            section_length = randrange(16,80)
            print()
            print(f"SECTION {section_number} - {section_length} beats long")
            print()
            section_rules = self.rule_engine.select_section_rules(section_number)

            print()
            print("EXECUTED")
            for rule in range(len(section_rules[0])):
                if section_rules[0][0]:
                    section_rules[0][rule].execute_rule(None)
            print()

            for __ in range(section_length):
                for i in range(len(self.voice_list)):
                    note = self.voice_list[i].line.note_list[self.play_count%self.voice_list[i].line_length]

                    # Fire rules in the rule_list
                    for __ in range(len(section_rules[1])):
                        if section_rules[1][0]:
                            section_rules[1][0].execute_rule(note)

                    output += note._play()
                self.play_count += 1

            [print(instrument) for instrument in self.voice_list]
            section_number += 1
        return output

class Mode:
    """A class to represent the mode"""

    def __init__(self):
        self.tonic = randrange(0,6)
        self.scale = [0.00, 0.02, 0.04, 0.05, 0.07, 0.09, 0.11]
        self.chord_position = 0
        self.scale_position_list = self.expand_scale()

    def __repr__(self):
        return str(self.scale_position_list)

    def expand_scale(self):
        scale_position_list = [item for item in range(len(self.scale))]
        for chord_voicing in choice([[(0,3),(2,2),(4,2)],
        [(0,2),(2,3),(4,3)],
        [(0,3),(2,2),(4,2),(6,2)],
        [(2,4),(4,6)]]):
            for __ in range(chord_voicing[1]):
                scale_position_list.append((chord_voicing[(0)]+self.tonic+self.chord_position)%len(self.scale))
        return scale_position_list

    def set_chord(self):
        chord_choices = [[1,2,2,3,3,4,4,4,4,5,6],
        [0,0,0,0,2,2,3,3,4,4,4,5,6],
        [0,1,3,3,3,3,4,4,5,5,5,6],
        [0,0,0,0,0,1,2,2,4,4,4,5,6],
        [0,0,0,0,0,1,2,2,2,2,3,3,5,5,5,6],
        [0,0,0,1,2,2,3,3,3,3,4,4,4,6],
        [0,0,1,1,1,2,2,3,3,4,4,4,5]]
        self.chord_position = choice(chord_choices[self.chord_position])
        self.scale_position_list = self.expand_scale()


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
        self.busyness = random()/2
        self.piece = piece
        self.line = Line(self, piece)
        self.rule_list = []
        self.mute = 1
        # self.play_count = 0

    def __str__(self):
        """Return string representation."""
        return f'{self.name}|{self.csnd_instrument}|Mute:{self.mute}|Busyness:{round(self.busyness,3)}'

    def __repr__(self):
        """Return string representation."""
        return self.__str__()


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
            note_list.append(self._generate_note())
        return note_list

    def _generate_note(self):
        return Note(self.piece, self.voice)

    #def _play(self, csnd_instrument, play_count):
    #    output = ""
    #    for i in range(self.voice.line_length):
    #        note = self.note_list[i]
    #        output += f"i {csnd_instrument} {play_count} {note.duration} [{note.amplitude}*{note.on_off}/8] [{note.frequency}]" + "\n"
    #        play_count += 1
    #    return output, play_count

    #def evolve(self):
    #    """Evolve Line."""
    #    prob = 0.50
    #    for i in range(self.voice.line_length):
    #        if random() <= prob:
    #            self.note_list[i] = Note(self.piece, self.voice)

class Note:
    """A class used to represent a musical note"""

    def __init__(self, piece, voice):
        """Initialize a Note object"""
        self.piece = piece
        self.voice = voice
        self.duration = choice([0.5,0.5,0.5,1,1,1,1,1,3,3,3,6])
        self.amplitude = choice([0.3,0.5,0.7,0.9])
        self.on_off = self._set_on_off()
        self.scale_position = choice(self.piece.mode.scale_position_list)
        self.frequency = self._set_frequency()

    def __str__(self):
        """Return string representation."""
        return "Note"

    def __repr__(self):
        """Return string representation."""
        return str(self.frequency)

    def _set_on_off(self):
        if random() <= self.voice.busyness:
            return 1
        else:
            return 0

    def _set_frequency(self):
        return f"{self.voice.register} + {self.piece.mode.scale[self.scale_position]} {self.piece.offset}"

    def _play(self):
        """Return Csound note event"""
        if self.piece.play_count%2:
            swing_offset = self.piece.swing_offset
        else:
            swing_offset = 0
        if self.on_off != 0 and self.voice.mute != 0:
            output = f"i {self.voice.csnd_instrument} [{self.piece.play_count} + {swing_offset}] {self.duration} [{self.amplitude}*{self.on_off}*{self.voice.mute}/8] [{self.frequency}] ;{self.piece.mode}" + "\n"
        else:
            output = ""
        return output

    def _evolve(self, prob):
        """Evolve note"""
        if random() <= prob:
            self.__init__(self.piece, self.voice)
