import re
import dice

def Roll(eq):
    removed_whitespace_eq = eq.replace(' ', '')
    output = {
        'result': 0,
        'equation': eq,
        'dice breakdown': eq
    }
    print('Starting Roll', removed_whitespace_eq)

    chooser = r'\d+d\d+!?h\d+'
    for keep in re.findall(chooser, removed_whitespace_eq):
        print(f"keep: {keep}")

        if '!' in keep:
            isExploding = True
            keep = keep.replace('!', '')
        else:
            isExploding = False
        print(f"keep: {keep}")


        count = int(keep.split('d')[0])
        sides = int(keep.split('d')[1].split('h')[0])
        k = int(keep.split('h')[1])

        keep_die = dice.Die(sides, isExploding, False)

        keep_roll = keep_die.RollN(count)
        kept = sorted(keep_roll['dice'])[-k:]
        dropped = sorted(keep_roll['dice'])[0:count-k]
        
        output['equation'] = output['equation'].replace(keep, str(sum([sum(i) for i in kept])), 1)
        output['dice breakdown'] = output['dice breakdown'].replace(keep, str(kept), 1)
        
        output['result'] = sum([sum(i) for i in kept])
        #print(output['result'])

    dropper = r'\d+d\d+!?l\d+'
    for drop in re.findall(dropper, removed_whitespace_eq):
        print(f"drop: {drop}")

        if '!' in drop:
            isExploding = True
            drop = drop.replace('!','')
        else:
            isExploding = False
        print(f"drop: {drop}")

        count = int(drop.split('d')[0])
        sides = int(drop.split('d')[1].split('l')[0])
        r = int(drop.split('l')[1])

        reject_die = dice.Die(sides, isExploding, False)

        reject_roll = reject_die.RollN(count)
        kept = sorted(reject_roll['dice'])[0:r]
        dropped = sorted(reject_roll['dice'])[r-count:]

        output['equation'] = output['equation'].replace(drop, str(sum([sum(i) for i in kept])), 1)
        output['dice breakdown'] = output['dice breakdown'].replace(drop, str(kept), 1)

        output['result'] = sum([sum(i) for i in kept])
        #print(output['result'])

    pattern = r'\d+d\d+!?'
    for match in re.findall(pattern, removed_whitespace_eq):
        print(match)
        if match[-1:] == '!':
            isExploding = True
        else:
            isExploding = False

        count = int(match.split('d')[0])
        sides = int(match.split('d')[1].replace('!',''))

        match_die = dice.Die(sides, isExploding, False)
        
        match_roll = match_die.RollN(count)
        output['equation'] = output['equation'].replace(match, str(match_roll['result']), 1)
        output['dice breakdown'] = output['dice breakdown'].replace(match, str(match_roll['dice']), 1)

    try:
        output['result'] = eval(output['equation'])
        output['equation'] = eq
    except:
        print('')
    return output