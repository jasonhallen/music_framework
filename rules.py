from random import choice, randrange, random, sample
# from classes import Note

class RuleEngine():
    """Determines which rules to apply to piece"""

    def __init__(self, piece):
        self.rule_list = [[],[]]
        self.piece = piece
        self.section_number = 0
        self.section_length = 0
        self.section_play_count = 0

    def update_rules(self):
        # for all rules in rule_list check the note_span and execution_count
        for level in self.rule_list:
            remove_list = []
            for rule in level:
                if self.section_play_count == rule.note_span:
                    remove_list.append(rule)
            for item in remove_list:
                level.remove(item)

        if self.section_play_count == self.section_length:
            self.section_play_count = 0
            self.section_length = randrange(8,64)
            print()
            print(f"SECTION {self.section_number} - {self.section_length} beats long")
            print(self.rule_list)
            print()
            self.select_rules()
            self.section_number += 1

        self.section_play_count += 1
        # remove any expired rules
            # if any note_span == exectution_count delete
        # generate any new rules

    def select_rules(self):
        """Return a list of Rules to apply to a section of Notes"""
        #
        #self.rule_list = [[],[]]
        # rule = 0
        print("RULE TESTING")
        rule_number = randrange(0,5)
        print(f"Rule Number: {rule_number}")
        while (len(self.rule_list[0]) + len(self.rule_list[1])) != rule_number:
        #while rule != None:
            rule = choice([Rule.evolve_constructor(self),
            Rule.mimic_constructor(self),
            Rule.chordchange_constructor(self),
            Rule.mute_constructor(self),
            Rule.unmute_constructor(self),
            Rule.unmuteall_constructor(self),
            Rule.morebusy_constructor(self),
            Rule.lessbusy_constructor(self),
            Rule.resetbusy_constructor(self),
            Rule.growline_constructor(self),
            Rule.shrinkline_constructor(self),
            Rule.end_constructor(self),
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
        # return self.rule_list


class Rule():
    """Create a rule to be applied to piece"""
    # RULES
        # EVOLVE TO
        # EVOLVE TO ALL (UNISON)
        # CHANGE LINE LENGTH

    # MOVEMENTS
        # GET MORE BUSY / GET LESS BUSY
        # FEWER VOICES / MORE VOICES
        # SHORTEN LINES / LENGTHEN LINES
        # SLOW DOWN / SPEED UP

    def __init__(self, rule_engine, function, args, preconditions, precedence, level):
        self.rule_engine = rule_engine
        self.function = function # function name
        self.arguments = args # tuple with arguments
        self.preconditions = preconditions
        self.precedence = precedence
        self.level = level
        self.note_span = rule_engine.section_length #note_span
        self.execution_count = 0
        #self.prob = 1

    def __str__(self):
        """Return string representation"""
        return self.function.__name__ #+ str(self.arguments)

    def __repr__(self):
        """Return string representation."""
        return self.__str__()

    @classmethod
    def chordchange_constructor(cls, rule_engine):
        function = cls.chordchange
        args = (rule_engine.piece,)
        level = 0
        precedence = 0
        preconditions = (not any(rule.function == cls.chordchange for rule in rule_engine.rule_list[level])) and rule_engine.section_number != 0
        return cls(rule_engine, function, args, preconditions, precedence, level)

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
    def evolve_constructor(cls, rule_engine):
        function = cls.evolve
        args = (sample(rule_engine.piece.voice_list,randrange(1,len(rule_engine.piece.voice_list)+1)), randrange(7,11)/10)
        level = 1
        precedence = 0
        preconditions = not any(rule.function == cls.evolve for rule in rule_engine.rule_list[level])
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def evolve(self, note, args):
        if note.voice in args[0]:
            note._evolve(args[1])

    @classmethod
    def mimic_constructor(cls, rule_engine):
        function = cls.mimic
        args = (sample(rule_engine.piece.voice_list,randrange(1,len(rule_engine.piece.voice_list)+1)),choice([randrange(0,9)]))
        level = 1
        precedence = 1
        preconditions = not any((rule.function == cls.mimic) for rule in rule_engine.rule_list[level]) #args[0] != args[1]
        return cls(rule_engine, function, args, preconditions, precedence, level)

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
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def transpose(self, note, args):
        """Transpose a note frequency"""
        if note.voice == args[0]:
            voice = args[0]
            transpose_interval = args[1]
            note.scale_position = (note.scale_position + transpose_interval)%len(note.piece.mode.scale)
            note.frequency = note._set_frequency()

    @classmethod
    def mute_constructor(cls, rule_engine):
        function = cls.mute
        args = (choice(rule_engine.piece.voice_list),)
        level = 0
        precedence = 3
        preconditions = (not any((rule.function == cls.mute or rule.function == cls.unmute) and rule.arguments[0] == args[0] for rule in rule_engine.rule_list[level])) and args[0].mute == 1
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def mute(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_mute_value = voice.mute
        voice.mute = 0
        print(f"MUTE {voice}: old mute = {old_mute_value}, new mute = {voice.mute}")

    @classmethod
    def unmute_constructor(cls, rule_engine):
        function = cls.unmute
        args = (choice(rule_engine.piece.voice_list),)
        level = 0
        precedence = 3
        preconditions = (not any((rule.function == cls.mute or rule.function == cls.unmute) and rule.arguments[0] == args[0] for rule in rule_engine.rule_list[level])) and args[0].mute == 0
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def unmute(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_mute_value = voice.mute
        voice.mute = 1
        print(f"UNMUTE {voice}: old mute = {old_mute_value}, new mute = {voice.mute}")

    @classmethod
    def unmuteall_constructor(cls, rule_engine):
        function = cls.unmuteall
        args = (rule_engine.piece.voice_list,)
        level = 0
        precedence = 3
        preconditions = (len([voice for voice in rule_engine.piece.voice_list if voice.mute == 1]) <= 4)
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def unmuteall(self, note, args):
        """Transpose a note frequency"""
        voice_list = args[0]
        for voice in voice_list:
            voice.mute = 1
        print(f"UNMUTEALL")


    @classmethod
    def resetbusy_constructor(cls, rule_engine):
        function = cls.resetbusy
        args = (choice(rule_engine.piece.voice_list),)
        precedence = 3
        level = 0
        preconditions = not any((rule.function == cls.morebusy or rule.function == cls.lessbusy or rule.function == cls.resetbusy) and rule.arguments[0] == args[0] for rule in rule_engine.rule_list[level])
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def resetbusy(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_busy_value = voice.busyness
        voice.busyness = random()/2
        print(f"RESETBUSY {voice}: old = {old_busy_value}, new = {voice.busyness}")


    @classmethod
    def morebusy_constructor(cls, rule_engine):
        function = cls.morebusy
        args = (choice(rule_engine.piece.voice_list),)
        precedence = 3
        level = 0
        preconditions = (not any((rule.function == cls.morebusy or rule.function == cls.lessbusy) and rule.arguments[0] == args[0] for rule in rule_engine.rule_list[level])) and args[0].busyness < 1
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def morebusy(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_busy_value = voice.busyness
        voice.busyness = voice.busyness*1.2
        print(f"MOREBUSY {voice}: old = {old_busy_value}, new = {voice.busyness}")

    @classmethod
    def lessbusy_constructor(cls, rule_engine):
        function = cls.lessbusy
        args = (choice(rule_engine.piece.voice_list),)
        level = 0
        precedence = 3
        preconditions = (not any((rule.function == cls.morebusy or rule.function == cls.lessbusy) and rule.arguments[0] == args[0] for rule in rule_engine.rule_list[level])) and args[0].busyness > 0.05
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def lessbusy(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_busy_value = voice.busyness
        voice.busyness = voice.busyness/1.2
        print(f"LESSBUSY {voice}: old = {old_busy_value}, new = {voice.busyness}")

    @classmethod
    def growline_constructor(cls, rule_engine):
        function = cls.growline
        args = (choice(rule_engine.piece.voice_list),)
        level = 0
        precedence = 3
        preconditions = not any((rule.function == cls.growline or rule.function == cls.shrinkline) and rule.arguments[0] == args[0] for rule in rule_engine.rule_list[level]) and args[0].line_length != rule_engine.piece.measure_lengths[-1]
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def growline(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_line_length = voice.line_length
        voice.line_length = choice([length for length in voice.piece.measure_lengths if length > old_line_length])
        # from classes import Note
        for i in range(voice.line_length - old_line_length):
            voice.line.note_list.append(voice.line._generate_note())

        print(f"GROWLINE {voice}: old = {old_line_length}, new = {voice.line_length}")

    @classmethod
    def shrinkline_constructor(cls, rule_engine):
        function = cls.shrinkline
        args = (choice(rule_engine.piece.voice_list),)
        level = 0
        precedence = 3
        preconditions = not any((rule.function == cls.shrinkline or rule.function == cls.growline) and rule.arguments[0] == args[0] for rule in rule_engine.rule_list[level]) and args[0].line_length != rule_engine.piece.measure_lengths[0]
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def shrinkline(self, note, args):
        """Transpose a note frequency"""
        voice = args[0]
        old_line_length = voice.line_length
        voice.line_length = choice([length for length in voice.piece.measure_lengths if length < old_line_length])

        voice.line.note_list = voice.line.note_list[:-(old_line_length - voice.line_length)]

        print(f"SHRINKLINE {voice}: old = {old_line_length}, new = {voice.line_length}")

    @classmethod
    def end_constructor(cls, rule_engine):
        function = cls.end
        args = (None,)
        level = 0
        precedence = 3
        preconditions = rule_engine.piece.mode.chord_position == 0 and rule_engine.section_number >= rule_engine.piece.max_sections
        return cls(rule_engine, function, args, preconditions, precedence, level)

    def end(self, note, args):
        """Transpose a note frequency"""
        print("END")

    def execute_rule(self, note):
        self.execution_count += 1
        self.function(self, note, self.arguments)
