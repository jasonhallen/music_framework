# Handled in Csound
    # Instrument amplitude scaling factor

from random import choice, random, randrange
import elements
from engine import *


class Piece:
    """A class used to represent the entire piece of music."""

    def __init__(self, melody_voices, drum_voices, bass_voices):
        """Initialize the piece of music"""
        self.mode = None
        self._set_mode()
        self.offset = self._set_offset()
        self.max_line_length = 48
        self.measure_lengths = choice([[8,12,16,20,24,28,32]])
        self.melody_voices = melody_voices
        self.drum_voices = drum_voices
        self.bass_voices = bass_voices
        self.voice_list = self._set_voices()
        self.play_count = 0
        self.rule_engine = RuleEngine()
        self.swing_offset = random()/4

    def _set_mode(self):
        diatonic = [0.00, 0.02, 0.04, 0.05, 0.07, 0.09, 0.11]
        weights = [[(0,3),(2,2),(4,2)],[(0,3),(2,2),(4,2),(6,2)]]
        for __ in range(randrange(0,7)):
            diatonic.append(diatonic[0])
            diatonic = diatonic[1:]
        for tuple in choice(weights):
            for __ in range(tuple[1]):
                diatonic.append(diatonic[tuple[0]])
        self.mode = diatonic

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
        section_rules = []
        output = "t 0 360\n"
        section_number = 0
        while section_number < 20:
            section_length = 8*randrange(4,6)
            section_rules = []
            section_rules.append(choice([None, self._set_mode]))
            if section_rules[0]:
                section_rules[0]()

            note_rules = []
            note_rules.append(choice([None, self.evolve]))
            copier_voice = choice(self.voice_list)
            target_voice = choice(self.voice_list)

            # self.rule_list.select_section_rules()
            # output += choice(options)(section_length)
            # self.mode = self._set_mode()
            output += f";LOOP {self.voice_list.index(copier_voice)} {self.voice_list.index(target_voice)}\n\n"
            for __ in range(section_length):
                for i in range(len(self.voice_list)):
                    note = self.voice_list[i].line.note_list[self.play_count%self.voice_list[i].line_length]
                    # Fire rules in the rule_list

                    if note_rules[0]:
                        note_rules[0](note,0.7)
                    self.mimic(note, copier_voice, target_voice)
                    
                    output += note._play()
                self.play_count += 1
            section_number += 1
        return output #choice(options)(section_length)

    def evolve_constructor(self):
        pass

    def evolve(self, note, prob):
        note._evolve(prob)

    def mimic_constructor(self):
        copier_voice = choice(self.voice_list)
        target_voice = choice(self.voice_list)
        return f"mimic(note, copier_voice, target_voice)"

    def mimic(self, note, copier_voice, target_voice):
        """Turn note into target_voice note"""

        if note.voice == copier_voice:
            note.duration = target_voice.line.note_list[self.play_count%target_voice.line_length].duration
            note.amplitude = target_voice.line.note_list[self.play_count%target_voice.line_length].amplitude
            note.on_off = target_voice.line.note_list[self.play_count%target_voice.line_length].on_off
            note.frequency = target_voice.line.note_list[self.play_count%target_voice.line_length].frequency

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
        # self.play_count = 0

    def __str__(self):
        """Return string representation."""
        return f'Name:{self.name}, Csnd Inst:{self.csnd_instrument}, Register:{self.register}, Length:{self.line.line_length}'

    def __repr__(self):
        """Return string representation."""
        return self.__str__()

    #def play(self):
    #    """Play Voice's line."""
    #    output, self.play_count = self.line._play(self.csnd_instrument, self.play_count)
    #    return output


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
        self.on_off = self._set_on_off()
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
        return f"{self.voice.register} + {choice(self.piece.mode)} {self.piece.offset}"

    def _play(self):
        """Return Csound note event"""
        if self.piece.play_count%2:
            swing_offset = self.piece.swing_offset
        else:
            swing_offset = 0

        output = f"i {self.voice.csnd_instrument} [{self.piece.play_count} + {swing_offset}] {self.duration} [{self.amplitude}*{self.on_off}/8] [{self.frequency}] ;{self.piece.mode}" + "\n"
        return output

    def _evolve(self, prob):
        """Evolve note"""
        if random() <= prob:
            self.__init__(self.piece, self.voice)
