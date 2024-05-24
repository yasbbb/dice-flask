import random
import re

def evaluate(eq):
    result, dice = roll(eq)
    if type(result) == int:
        result = str(result)
    if not result.isnumeric():
        status = 'error'
        err = result
        result = '0'
    else:
        err = ''
        status = 'success'

    output = {
        'result': result,
        'dice': dice,
        'error': err,
        'status': status,
        'equation': eq
    }
    return output

def roll(eq, diedict=None):
    eq = eq.replace(' ','')
    if not diedict:
        diedict = {}
    # == BASE CASE ==
    if eq.isnumeric() or type(eq) == int:
        return eq, diedict
    
    # print(f"EQ: {eq}")

    atom = r'\d+d\d+!?'
    # print(f"Atoms found: {re.search(atom,eq)} | {re.findall(atom, eq)}")
    bracket = r'\[[^\[\]]+\][hl]\d+'
    # print(f"Brackets found: {re.search(bracket, eq)} | {re.findall(bracket, eq)}")
    array = r'\[[^\[\]]+\]'
    # print(f"Naked arrays found: {re.search(array, eq)} | {re.findall(array, eq)}")

    # == CASE ONE ==
    # Evaluate all atomic rolls (XdY) and replace with arrays
    # of all X rolls of dietype Y
    indmarker = 0
    if re.search(atom, eq):
        # print("Running Atomic Case")
        for match in re.findall(atom, eq):
            if '!' in match:
                canAce = True
                match = match.replace('!','')
            else:
                canAce = False


            count = int(match.split('d')[0])
            die = int(match.split('d')[1])

            arr = []
            for i in range(count):
                if canAce:
                    val = random.randint(1, die)
                    totalroll = 0
                    while val == die:
                        totalroll += val  
                        val = random.randint(1, die)
                    totalroll += val
                    arr.append(str(totalroll))
                else:
                    val = random.randint(1, die)
                    arr.append(str(val))
            
            join = ','.join(arr)
            output = f'[{join}]'

            replacestr = f"{match}{'!' if canAce else ''}"
            if match in diedict.keys():
                diedict[f"{match}({indmarker})"] = arr
                indmarker += 1
            else:
                diedict[match] = arr
            eq = eq.replace(replacestr, output, 1)
        return roll(eq, diedict)

    # == CASE TWO ==
    # Now, if no more atomic equations exist, we evaluate any choose
    # choose equations (identified by XdY(h/l)Z)
    # where h => keep the highest Z values
    # and l => keep the lowest Z values
    elif re.search(bracket, eq):
        # print("Running Bracketed Case")
        for match in re.findall(bracket, eq):
            # print(f"Bracket Match: {match}")
            if 'h' in match:
                choosetype = 'highest'
                splitchar = 'h'
            else:
                choosetype = 'lowest'
                splitchar = 'l'

            count = int(match.split(splitchar)[1])
            strarr = match.split(splitchar)[0]
            arr = [int(num) for num in strarr.replace('[','').replace(']','').split(',')]
            arr = sorted(arr)

            if choosetype == 'highest':
                res = arr[-count:]
            else:
                res = arr[:count]

            eq = eq.replace(match, str(sum(res)), 1)
        return roll(eq, diedict)
    
    # == CASE THREE ==
    # If an array doesn't have any choose operator, then we want
    # the sum of the remaining values
    elif re.search(array, eq):
        # print("Running Arraysum Case")
        for match in re.findall(array, eq):
            # print(match)
            arr = [int(num) for num in match.replace('[','').replace(']','').split(',')]
            arrsum = sum(arr)
            eq = eq.replace(match, str(arrsum), 1)
        return roll(eq, diedict)

    # == CASE FOUR ==
    # If all the other operations have completed
    # then we try to evaluate the remaining simple
    # mathematical equation
    else:
        # print("Last eval step")
        try:
            evaluated = eval(eq)
            return evaluated, diedict
        except:
            return f"bad equation: {eq}", diedict

    return f"bad equation: {eq}", diedict
