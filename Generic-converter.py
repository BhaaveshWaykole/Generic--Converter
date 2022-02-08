
# defining the conversion rates. This allows us to generate a list of possible conversions and actually calculate. 
# base types are metre, gram, litre, byte, square metre, metres-per-second, second, pascal, radian
rates = {
    # kilometre, metre, centimetre, millimetre, inch, feet, yard, mile
    'length': {'km': 1000, 'm': 1, 'cm': 0.01, 'mm': 0.001, 'in': 0.0254, 'ft': 0.305, 'yd': 0.9144, 'mi': 1609.344},
    
    # pounds, kilograms, grams, milligrams
    'weight': {'lbs': 453.6, 'kg': 1000, 'g': 1, 'mg': 0.001},
    
    # gallon, litre, millilitre
    'volume': {'gal': 3.785, 'l': 1, 'ml': 0.001},
    
    # gigibyte, mebibyte, kikibyte, byte
    'data': {'gb': 1073741824, 'mb': 1048576, 'kb': 1024, 'b': 1},
    
    # square-kilometre, square-metre, square-centimetre, square-inch, square-foot, hectare, acre 
    'area': {'km-sq': 1000000, 'm-sq': 1, 'cm-sq': 0.0001, 'in-sq': 0.000645, 'ft-sq': 0.093, 'ha': 10000, 'ac': 4046.86},
    
    # kilometres-per-hour, metres-per-second, miles-per-hour, feet-per-second, knots 
    'speed': {'kmph': 0.278, 'mps': 1, 'mph': 0.447, 'fps': 0.3048, 'kn':0.514},

    # week, day, hour, minute, second
    'time': {'w': 604800, 'd': 86400, 'hr': 3600, 'min': 60, 's': 1},

    # bar, atmospheric pressure, torr, pascal
    'pressure': {'bar': 100000, 'atm': 101325, 'torr': 133.322, 'pa': 1},
    
    # degree, radian
    'angle': {'deg': 0.01745, 'rad': 1}
    }

# dictionary with ANSI escape sequences to make it easier to print colored text in the terminal
logger = {
    'end': '\033[0m',
    'uline': '\033[4m',
    'head': '\033[96m',
    'err': '\033[91m',
    'result': '\033[92m',
    'warn': '\033[93m',    
    }


# the generic converter class. This lets us initialize a calculator object which can be used at a later stage
class Generic_Converter:
    # init function prints the instructions and the available conversion rates
    def __init__(self):
        out = f'\n{logger["head"]}{logger["uline"]}Generic Converter{logger["end"]} by Bhaavesh Waykole, Shashank Thakkar, Sarthak Tripathi\n\nHow this works: Upon entering a value in a particular unit, the program will convert it to all corresponding rates. Enter "quit" or "exit" to leave the program.\n\nThe available units: '        
        # the loop iterates through the keys of the rates dictionary and gets all the keys (the corresponding units)
        for index, key in enumerate(rates):
            # indices start from 0, so we add 1 to start the output list from 1. 
            # ', '.join is used to join the keys (the units) in a single string separates by a comma and a space
            out += f'\n{index + 1}) {key.title()} - ' + ', '.join(rates[key].keys())
        print(out)

    # the convert method takes 3 arguments:
    # param: the type of conversion - length, weight, volume, data
    # val: the numberical value to convert
    # unit: the current unit to convert from
    def Convert(self, param, val, unit):
        # in the first step, the value is converted to the base type. This allows for easier converions at
        # a later stage without additional calculations.
        base = val * rates[param][unit]

        out = []
        # the for loop iterates through the key-value pairs and converts our value to every type available. Each converted value
        # is formatted as a string along with the rates and appended to a list.
        for key, value in rates[param].items():
            if key != unit:
                converted = base * 1/value
                out.append(f'{converted}' + ' ' + key)

# the function finally prints a string of the elements separated with newline and a bullet point.
        print(f'{logger["result"]}{val} {unit} was converted to its corresponding types. Results:{logger["end"]}\n•', '\n• '.join(out))

# this function is used to fetch input and then calls the parse function after removing the leading and trailing spaces, if any and lowering the string.
def Fetch():
    out = input("\nEnter the data you want to convert: ").strip().lower()
    
    # If input is exit, quit the program. Otherwise, continue parsing
    if (out == 'exit') or (out == 'quit'):
        print(f'{logger["warn"]}Exited the program.{logger["end"]}')
        quit()
    else:
        return Parse(out)

# parse(inp) parses the given string, inp, and returns the conversion type (weight, length etc.), value and the unit. 
def Parse(inp:str):    
    value = ''
    unit = ''
    param = ''    
    # formatted is the cleansed inp after removing all spaces from it. the for loop adds the characters that aren't equal to the space.
    formatted = ''
    for i in inp:
        if i != ' ':
            formatted += i    
    # to separate the units from the number, we iterate through the formatted input and try to convert each character to an int.
    # if there are no exceptions, then the character is a digit, so it gets appended to the value variable.
    # if there is an exception, there are 3 cases:
        # 1) the character is a decimal point - in this case, we append the character to the value variable
        # 2) the character is first letter of the unit - because we know the index of this character, we can easily take the string from this point forth as the unit.
        # 3) invalid character - we separate the string as if it were a valid character of a unit because this is handled later anyway.
    for index, char in enumerate(formatted):
        try:
            # tring to convert the character to an int
            int(char)
        except:
            #if exception, check if character is decimal and do as described above
            if char == '.':
                value += char
            else:
                unit = formatted[index:]
                break
        else:
            # no exceptions, add character to value
            value += char
    # we use the for loop to iterate through the key-value pairs of the rates dictionary.
    # here, the key is a conversion type (like length, weight etc.) and the value is a dictionary with units and their conversion rates
    # with that we get the keys of the value dictionary, which is a list of units in that conversion type.
    # finally, we check if the unit exists in that list, if it does, we set param to the key (the conversion type) and break.
    for key, val in rates.items():
        if unit in rates[key].keys():
            param = key
            break
    # once separated completely, we convert value to float so it can be passed in the Convert method.
    if value != '':
        value = float(value)
    else:
        value = None
    # if the unit was invalid and therefore not present in the dictionary, param remained as an empty string. We raise an exception
    # to error out of the program with a more descriptive error than the default type error raised during Convert().
    if (param == '') or (value == None):
        # more descriptive error
        print(f'{logger["err"]}Your unit does not match, check and try again!{logger["end"]}')
        # we return None, None, None, True to avoid the error when using Fetch()
        # the boolean is the error flag.
        return None, None, None, True
    else:
        # if param is not an empty string, we have everything and return it.
        return param, value, unit, False

# making a Generic_Converter object
calc = Generic_Converter()

while True:
    # using the fetch function to get input and parse it.
    param, val, unit, err = Fetch()    
    if err:
        continue
    # using the Convert() method to convert the data received.
    calc.Convert(param, val, unit)