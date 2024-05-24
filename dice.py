import random

class Die:
    def __init__(self, value, canAceUp, canAceDown):
        self.value = value
        self.canAceUp = canAceUp
        self.canAceDown = canAceDown
    def Roll(self):
        rolls = []
        this_roll = random.randint(1, self.value)

        if not self.canAceUp:
            rolls.append(this_roll)
        else:
            while this_roll == self.value:
                rolls.append(this_roll)
                this_roll = random.randint(1, self.value)
            rolls.append(this_roll)
        output = {
            'result': sum(rolls),
            'dice': rolls
        }
        return output
    def RollN(self, count):
        output = {
            'result': 0,
            'dice': []
        }
        for i in range(count):
            r = self.Roll()
            output['result'] += r['result']
            output['dice'].append(r['dice'])
        return output


global standard_dice
standard_dice = {
    'd4': Die(4, False, False),
    'd6': Die(6, False, False),
    'd8': Die(8, False, False),
    'd10': Die(10, False, False),
    'd12': Die(12, False, False),
    'd20': Die(20, False, False)
}

global savage_dice
savage_dice = {
    'd4': Die(4, True, False),
    'd6': Die(6, True, False),
    'd8': Die(8, True, False),
    'd10': Die(10, True, False),
    'd12': Die(12, True, False),
    'd20': Die(20, False, False)
}

def Wild_Roll(die, wild_die):
    if type(die) == type(wild_die) == type(Die(1,0,0)):
        die_roll = die.Roll()
        wild_roll = wild_die.Roll()
        output = {
            'crit_fail': False,
            'trait_fail': False,
            'result': 0,
            'dice': []
        }
        if die_roll['result'] == wild_roll['result'] == 1:
            output['critfail'] = True
            output['trait_fail'] = True
            output['result'] = 1
            output['dice'] = [1]
        elif die_roll['result'] > wild_roll['result']:
            output['result'] = die_roll['result']
            output['dice'] = die_roll['dice']
        else:
            output['result'] = wild_roll['result']
            output['dice'] = wild_roll['dice']
            if die_roll['result'] == 1:
                output['trait_fail'] = True
    else:
        raise ValueError('One or both arguments: ({}, {}) is not type roll.Die'.format(die, wild_die))
        return 0
    return output