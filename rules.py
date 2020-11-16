from random import choice, randrange

class RuleEngine():
    """Determines which rules to apply to piece"""

    def __init__(self, piece):
        self.rule_list = []
        self.piece = piece

    def select_section_rules(self):
        """Return a list of Rules to apply to a section of Notes"""

        self.rule_list = []
        # while rule != play:
            # select rule
            # test preconditions
            # if preconditions hold, add rule to list
        #self.rule_list.append(Rule(choice([[self.mimic,(choice(self.piece.voice_list),choice(self.piece.voice_list))],[self.evolve,(0.7,)]])))
        for __ in range(3):
            rule = choice([Rule.evolve_constructor(self.rule_list),Rule.mimic_constructor(self.piece)])
            print(f"{rule.preconditions} - {rule}")
            if rule.preconditions:
                self.rule_list.append(rule)
        return self.rule_list


class Rule():
    """Create a rule to be applied to piece"""

    def __init__(self, function, args, preconditions):
        self.function = function # function name
        self.arguments = args # tuple with arguments
        self.preconditions = preconditions
        #self.prob = 1
        #self.execution_level = "note"
        #self.execution_count = 0
        #self.precedence = 0

    def __str__(self):
        """Return string representation"""
        return self.function.__name__ #+ str(self.arguments)

    def __repr__(self):
        """Return string representation."""
        return self.__str__()

    @classmethod
    def evolve_constructor(cls, rule_list):
        function = cls.evolve
        args = (0.7,)
        preconditions = not any(rule.function == cls.evolve for rule in rule_list)
        return cls(function, args, preconditions)

    def evolve(self, note, prob):
        note._evolve(prob[0])

    @classmethod
    def mimic_constructor(cls, piece):
        function = cls.mimic
        args = (choice(piece.voice_list),choice(piece.voice_list),choice([0,randrange(1,8)]))
        preconditions = args[0] != args[1]
        return cls(function, args, preconditions)

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

    def execute_rule(self, note):
        #self.execution_count += 1
        self.function(self, note, self.arguments)
