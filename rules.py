from random import choice, randrange

class RuleEngine():
    """Determines which rules to apply to piece"""

    def __init__(self, piece):
        self.rule_list = []
        self.piece = piece

    def select_section_rules(self):
        """Return a list of Rules to apply to a section of Notes"""

        self.rule_list = [[],[]]
        # while rule != play:
            # select rule
            # test preconditions
            # if preconditions hold, add rule to list
        #self.rule_list.append(Rule(choice([[self.mimic,(choice(self.piece.voice_list),choice(self.piece.voice_list))],[self.evolve,(0.7,)]])))
        for __ in range(6):
            rule = choice([Rule.evolve_constructor(self.rule_list),Rule.mimic_constructor(self.piece),Rule.chordchange_constructor(self.piece, self.rule_list)]) #Rule.transpose_constructor(self.piece)
            print(f"{rule} - {rule.preconditions}")
            if rule.preconditions:
                self.rule_list[rule.level].append(rule)
        self.rule_list[1].sort(key=lambda x: x.precedence)
        return self.rule_list


class Rule():
    """Create a rule to be applied to piece"""

    def __init__(self, function, args, preconditions, precedence, level):
        self.function = function # function name
        self.arguments = args # tuple with arguments
        self.preconditions = preconditions
        self.precedence = precedence
        self.level = level
        #self.prob = 1
        #self.execution_level = "note"
        #self.execution_count = 0

    def __str__(self):
        """Return string representation"""
        return self.function.__name__ #+ str(self.arguments)

    def __repr__(self):
        """Return string representation."""
        return self.__str__()

    @classmethod
    def chordchange_constructor(cls, piece, rule_list):
        function = cls.chordchange
        args = (piece,)
        preconditions = not any(rule.function == cls.chordchange for rule in rule_list[0])
        precedence = 0
        level = 0
        return cls(function, args, preconditions, precedence, level)

    def chordchange(self, note, args):
        piece = args[0]
        piece._set_mode()
        # for voice in piece.voice_list:
        #     for item in voice.line:
        #         Rule.transpose(self,item,(item.voice,choice([0,2,4])))

    @classmethod
    def evolve_constructor(cls, rule_list):
        function = cls.evolve
        args = (randrange(7,11)/10,)
        preconditions = not any(rule.function == cls.evolve for rule in rule_list[1])
        precedence = 0
        level = 1
        return cls(function, args, preconditions, precedence, level)

    def evolve(self, note, args):
        note._evolve(args[0])

    @classmethod
    def mimic_constructor(cls, piece):
        function = cls.mimic
        args = (choice(piece.voice_list),choice(piece.voice_list),choice([0,randrange(0,1)]))
        preconditions = args[0] != args[1]
        precedence = 1
        level = 1
        return cls(function, args, preconditions, precedence, level)

    def mimic(self, note, args):
        """Turn note into target_voice note"""
        if note.voice == args[0]:
            target_voice = args[1]
            offset = args[2]
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
        preconditions = True
        precedence = 2
        level = 1
        return cls(function, args, preconditions, precedence, level)

    def transpose(self, note, args):
        """Transpose a note frequency"""
        if note.voice == args[0]:
            voice = args[0]
            transpose_interval = args[1]
            note.scale_position = (note.scale_position + transpose_interval)%len(note.piece.mode[0])
            note._set_frequency()

    def execute_rule(self, note):
        #self.execution_count += 1
        self.function(self, note, self.arguments)
