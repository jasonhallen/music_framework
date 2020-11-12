
class RuleEngine():
    """Determines which rules to apply to piece"""

    def __init__(self):
        self.rule_list = []

    def select_section_rules(self):
        self.rule_list.append(Rule(note._evolve))

class Rule():
    """Create a rule to be applied to piece"""

    def __init__(self, function):
        self.function = function
        self.count = 0

def evolve():
    pass
