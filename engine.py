
class RuleEngine():
    """Determines which rules to apply to piece"""

    def __init__(self):
        self.rule_list = []
        self.construct_rule_objects()

    def construct_rule_objects(self):
        pass

    def select_section_rules(self):
        #self.rule_list.append(Rule(note._evolve))
        pass

class Rule():
    """Create a rule to be applied to piece"""

    def __init__(self, function):
        self.function = "mimic"
        self.execution_level = "note"
        self.count = 0
        self.precedence = 0
        self.preconditions = ""
        self.arguments = ""
        self.probability = 0.5

    def rule_constructor(self):
        pass
