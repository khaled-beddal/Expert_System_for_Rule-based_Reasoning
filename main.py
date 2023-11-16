


# importing the "re" module in Python. ( for regular expressions )
import re

class Rule:
    def __init__(self, rule_string):
        # Initialize a Rule object with a given rule string
        self.rule_string = rule_string

        # Initialize premises and actions lists for the rule
        self.premises = []
        self.actions = []

        # Parse the rule string
        # by use a regular expression to match and capture specific parts 
        match = re.match(r"R(\d+): IF (.*) THEN (.*)", rule_string)
        if not match:
            raise ValueError("Invalid rule format: {}".format(rule_string))


        # Assigning Captured Groups

        # Extracts the rule number from the first capturing group of the match object ((\d+)) and converts it to an integer.
        self.rule_number = int(match.group(1))
        # Extracts the premises from the second capturing group and splits them into a list using "," as the delimiter.
        self.premises = match.group(2).split(",")
        # Extracts the actions from the third capturing group and splits them into a list.
        self.actions = match.group(3).split(",")

class ExpertSystem:
    def __init__(self, rule_base_file, fact_base):

        # Initialize an ExpertSystem object with a rule base file and a fact base

        self.rule_base = self.parse_rule_base(rule_base_file)
        self.fact_base = fact_base
        self.rule_order = []  # Keeps track of the order in which rules are applied

    def parse_rule_base(self, rule_base_file):
        # Parse the rule base file and return a list of Rule objects
        with open(rule_base_file, "r") as f:
            rules = []
            for line in f:
                rule = Rule(line.strip())
                rules.append(rule)
            return rules




    # --------------------------------------------------------------------------------------------------
    # Functions for forward chaining -------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------




    def forward_chaining(self):

        # Forward chaining to derive new facts until the goal is achieved

        new_facts = self.fact_base.copy()  # Initialize with the initial fact_base

        while True:
            applicable_rules = []

            # Check for rules whose premises are satisfied and have not been applied yet
            for rule in self.rule_base:
                if rule.rule_number not in self.rule_order and all(fact in self.fact_base for fact in rule.premises):
                    applicable_rules.append(rule)

            if not applicable_rules:
                break

            # Apply the first applicable rule, add its actions to the fact base
            rule = applicable_rules[0]
            self.rule_order.append(rule.rule_number)
            self.fact_base.extend(rule.actions)
            new_facts.extend(rule.actions)

            # Goal achieved, return the new facts
        return new_facts




    # --------------------------------------------------------------------------------------------------
    # Functions for backward chaining ------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------




    def backward_chaining(self, goal):
        # Backward chaining to derive the fact base needed to achieve the goal
        subgoals = [goal]
        rule_order_backward = []  # Keeps track of the order in which rules are applied

        while subgoals:
            subgoal = subgoals.pop()

            applicable_rules = []
            # Check for rules whose actions include the current subgoal

            for rule in self.rule_base:
                if subgoal in rule.actions and all(fact in self.fact_base for fact in rule.premises):
                    applicable_rules.append(rule)

            if not applicable_rules:
                # Subgoal is not achievable
                continue

            for rule in applicable_rules:
                # Add the premises of the rule to the subgoals
                subgoals.extend(rule.premises)
                rule_order_backward.append(rule.rule_number)

            # Add the subgoal to the fact base only if it's not already present
            if subgoal not in self.fact_base:
                # Add the subgoal to the fact base
                self.fact_base.append(subgoal)

        # Reverse the order for readability
        rule_order_backward.reverse()
        self.rule_order.extend(rule_order_backward)
        # Return the fact base after backward chaining
        return self.fact_base




    # --------------------------------------------------------------------------------------------------
    # Output the set of rules used & the new basis of facts. -------------------------------------------
    # --------------------------------------------------------------------------------------------------




if __name__ == "__main__":

    # Define the rule base file and initial fact base
    rule_base_file = "./rule_base.txt"
    fact_base = ["pressure is low"]


    # Create an instance of the ExpertSystem with the specified rule base file and fact base
    expert_system = ExpertSystem(rule_base_file, fact_base)

    # Forward chaining -----------------------------------------------------

    new_facts_forward = expert_system.forward_chaining()
    # Print the final fact base & rule order
    print("Forward Chaining - New facts base:", new_facts_forward)
    print("Forward Chaining - Rule order:", expert_system.rule_order)


    print("_____________________________________________________\n")


    # Backward chaining -----------------------------------------------------

    # Reset fact base for backward chaining
    expert_system.fact_base = fact_base
    expert_system.rule_order = []

    # Backward chaining with a specific goal
    goal = "clouds"

    new_facts_backward = expert_system.backward_chaining(goal)
    # Print the final fact base & rule order
    print("Backward Chaining - New Fact base:", new_facts_backward)
    print("Backward Chaining - Rule order:", expert_system.rule_order)
