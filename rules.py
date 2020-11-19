from random import choice, randrange, random, sample

class RuleEngine():
    """Determines which rules to apply to piece"""

    def __init__(self, piece):
        self.rule_list = []
        self.piece = piece

    def select_section_rules(self, section_number):
        """Return a list of Rules to apply to a section of Notes"""

        self.rule_list = [[],[]]
        rule = 0
        print("RULE TESTING")
        while rule != None:
            rule = choice([Rule.evolve_constructor(self.rule_list),
            Rule.mimic_constructor(self.piece, self.rule_list),
            Rule.chordchange_constructor(self.piece, self.rule_list, section_number),
            Rule.mute_constructor(self.piece, self.rule_list),
            Rule.unmute_constructor(self.piece, self.rule_list),
            Rule.unmuteall_constructor(self.piece, self.rule_list),
            Rule.morebusy_constructor(self.piece, self.rule_list),
            Rule.lessbusy_constructor(self.piece, self.rule_list),
            Rule.resetbusy_constructor(self.piece, self.rule_list),
            Rule.end_constructor(self.piece, self.rule_list, section_number),
            None]) #Rule.transpose_constructor(self.piece)
            if rule != None:
                print(f"{rule} - {rule.preconditions} - {rule.arguments}")
                if rule.preconditions:
                    self.rule_list[rule.level].append(rule)
        self.rule_list[1].sort(key=lambda x: x.precedence)
        # print()
        # print("EXECUTED")
        # for i in range(len(self.rule_list)):
        #     for j in range(len(self.rule_list[i])):
        #         print(f"{str(self.rule_list[i][j])}, {self.rule_list[i][j].arguments}")
        # print()
        return self.rule_list


class Rule():
    """Create a rule to be applied to piece"""
    # RULES
        # EVOLVE TO
        # EVOLVE TO ALL (UNISON)
        # MIMIC ALL
        # CHANGE LINE LENGTH

    # MOVEMENTS
        # GET MORE BUSY / GET LESS BUSY
        # FEWER VOICES / MORE VOICES
        # SHORTEN LINES / LENGTHEN LINES
        # SLOW DOWN / SPEED UP

    def __init__(self, function, args, preconditions, precedence, level):
        self.function = function # function name
        self.arguments = args # tuple with arguments
        self.preconditions = preconditions
        self.precedence = precedence
        self.level = level
        #self.prob = 1
        #self.execution_count = 0

    def __str__(self):
        """Return string representation"""
        return self.function.__name__ #+ str(self.arguments)

    def __repr__(self):
        """Return string representation."""
        return self.__str__()

    @classmethod
    def chordchange_constructor(cls, piece, rule_list, section_number):
        function = cls.chordchange
        args = (piece,)
        level = 0
        precedence = 0
        preconditions = (not any(rule.function == cls.chordchange for rule in rule_list[level])) and section_number != 0
        return cls(function, args, preconditions, precedence, level)

    def chordchange(self, note, args):
        piece = args[0]
        old_chord_position = piece.mode.chord_position
        while old_chord_position == piece.mode.chord_position:
            piece.mode.set_chord()
        transpose_interval = piece.mode.chord_position - old_chord_position
        print(f"CHORD CHANGE: Old: {old_chord_position}|New: {piece.mode.chord_position}|Change: {transpose_interval}")
        for voice in piece.voice_list:
            for note in voice.line.note_list:
                Rule.transpose(self,note,(voice,transpose_interval))

    @classmethod
    def evolve_constructor(cls, rule_list):
        function = cls.evolve
        args = (randrange(7,11)/10,)
        level = 1
        precedence = 0
        preconditions = not any(rule.function == cls.evolve for rule in rule_list[level])
        return cls(function, args, preconditions, precedence, level)

    def evolve(self, note, args):
        note._evolve(args[0])

    @classmethod
    def mimic_constructor(cls, piece, rule_list):
        function = cls.mimic
        args = (sample(piece.voice_list,randrange(2,len(piece.voice_list)+1)),choice([0,randrange(0,5)]))
        level = 1
        precedence = 1
        preconditions = not any((rule.function == cls.mimic) for rule in rule_list[level]) #args[0] != args[1]
        return cls(function, args, preconditions, precedence, level)

    def mimic(self, note, args):
        """Turn note into target_voice note"""
        if note.voice in args[0][1:]:
            target_voice = args[0][0]
            offset = args[1]
            target_position = note.piece.play_count%target_voice.line_length - offset%target_voice.line_length
            note.duration = target_voice.line.note_list[target_position].duration
            note.amplitude = target_voice.line.note_list[target_position].amplitude
            note.on_off = target_voice.line.note_list[target_position].on_off
            note.frequency = target_voice.line.note_list[target_position].frequency

            Rule.transpose(self,note,(note.voice,choice([0,2,4])))

    @classmethod
    def transpose_constructor(cls, piece):
        function = cls.transpose
        args = (choice(piece.voice_list),choice([0,2,4]))
        level = 1
        precedence = 2
        preconditions = True
        return cls(function, args, preconditions, precedence, level)

    def transpose(self, note, args):
        """Transpose a note frequency"""
        if note.voice == args[0]:
            voice = args[0]
            transpose_interval = args[1]
            note.scale_position = (note.scale_position + transpose_interval)%len(note.piece.mode.scale)
            note.frequency = note._set_frequency()

    @classmethod
    def mute_constructor(cls, piece, rule_list):
        function = cls.mute
        args = (choice(piece.voice_list),)
        level = 0
        precedence = 3
        preconditions = (not any((rule.function == cls.mute or rule.function == cls.unmute) and rule.arguments[0] == args[0] for rule in rule_list[level])) and args[0].mute == 1
        return cls(function, args, preconditions, precedence, level)

    def mute(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_mute_value = voice.mute
        voice.mute = 0
        print(f"MUTE {voice}: old mute = {old_mute_value}, new mute = {voice.mute}")

    @classmethod
    def unmute_constructor(cls, piece, rule_list):
        function = cls.unmute
        args = (choice(piece.voice_list),)
        level = 0
        precedence = 3
        preconditions = (not any((rule.function == cls.mute or rule.function == cls.unmute) and rule.arguments[0] == args[0] for rule in rule_list[level])) and args[0].mute == 0
        return cls(function, args, preconditions, precedence, level)

    def unmute(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_mute_value = voice.mute
        voice.mute = 1
        print(f"UNMUTE {voice}: old mute = {old_mute_value}, new mute = {voice.mute}")

    @classmethod
    def unmuteall_constructor(cls, piece, rule_list):
        function = cls.unmuteall
        args = (piece.voice_list,)
        level = 0
        precedence = 3
        preconditions = (len([voice for voice in piece.voice_list if voice.mute == 1]) <= 4)
        return cls(function, args, preconditions, precedence, level)

    def unmuteall(self, note, args):
        """Transpose a note frequency"""
        voice_list = args[0]
        for voice in voice_list:
            voice.mute = 1
        print(f"UNMUTEALL")


    @classmethod
    def resetbusy_constructor(cls, piece, rule_list):
        function = cls.resetbusy
        args = (choice(piece.voice_list),)
        precedence = 3
        level = 0
        preconditions = not any((rule.function == cls.morebusy or rule.function == cls.lessbusy or rule.function == cls.resetbusy) and rule.arguments[0] == args[0] for rule in rule_list[level])
        return cls(function, args, preconditions, precedence, level)

    def resetbusy(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_busy_value = voice.busyness
        voice.busyness = random()/2
        print(f"RESETBUSY {voice}: old = {old_busy_value}, new = {voice.busyness}")


    @classmethod
    def morebusy_constructor(cls, piece, rule_list):
        function = cls.morebusy
        args = (choice(piece.voice_list),)
        precedence = 3
        level = 0
        preconditions = (not any((rule.function == cls.morebusy or rule.function == cls.lessbusy) and rule.arguments[0] == args[0] for rule in rule_list[level])) and args[0].busyness < 1
        return cls(function, args, preconditions, precedence, level)

    def morebusy(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_busy_value = voice.busyness
        voice.busyness = voice.busyness*1.2
        print(f"MOREBUSY {voice}: old = {old_busy_value}, new = {voice.busyness}")

    @classmethod
    def lessbusy_constructor(cls, piece, rule_list):
        function = cls.lessbusy
        args = (choice(piece.voice_list),)
        level = 0
        precedence = 3
        preconditions = (not any((rule.function == cls.morebusy or rule.function == cls.lessbusy) and rule.arguments[0] == args[0] for rule in rule_list[level])) and args[0].busyness > 0.01
        return cls(function, args, preconditions, precedence, level)

    def lessbusy(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_busy_value = voice.busyness
        voice.busyness = voice.busyness/1.2
        print(f"LESSBUSY {voice}: old = {old_busy_value}, new = {voice.busyness}")

    @classmethod
    def end_constructor(cls, piece, rule_list, section_number):
        function = cls.end
        args = (None,)
        level = 0
        precedence = 3
        preconditions = piece.mode.chord_position == 0 and section_number >= piece.max_sections
        return cls(function, args, preconditions, precedence, level)

    def end(self, note, args):
        """Transpose a note frequency"""
        pass

    def execute_rule(self, note):
        #self.execution_count += 1
        self.function(self, note, self.arguments)
