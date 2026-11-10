# Resistor Combination Calculator
# Author: Nwabueze Emmanuel, ND2 Mechatronics Engineering, YabaTech
#
# What it does:
#   1. Asks how many resistors you have and the value of each (in ohms).
#   2. Calculates and prints the total resistance in series and in parallel.
#
# MY TWISTS:
#   A. Resistor colour code decoder: the user types the colour bands of a
#      real resistor and the program works out its value, tolerance and the
#      range the real value could be in. The colours are stored in dictionaries.
#   B. LED resistor calculator: looks up the LED voltage from its colour,
#      works out the resistor needed to run it safely, then finds the nearest
#      real (E12 standard) resistor you can buy. It also uses the math module
#      to find the highest voltage a 1/4 W resistor can safely take.

# Import the math module so we can use math.sqrt() (square root) later.
import math

# List of standard E12 resistor values (first two digits of each value).
# Real resistors come in these values multiplied by 1, 10, 100 and so on.
E12_BASE = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]

# Dictionary of typical LED forward voltages (colour -> volts)
LED_VOLTAGES = {"red": 2.0, "yellow": 2.1, "green": 2.2, "blue": 3.0, "white": 3.0}

# Dictionaries for the resistor colour code (colour -> number)
# Band 1 and band 2 give the first and second digit of the value.
COLOUR_DIGITS = {"black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
                 "green": 5, "blue": 6, "violet": 7, "grey": 8, "white": 9}
# Band 3 is the multiplier (what the two digits are multiplied by).
MULTIPLIERS = {"black": 1, "brown": 10, "red": 100, "orange": 1000, "yellow": 10000,
               "green": 100000, "blue": 1000000, "gold": 0.1, "silver": 0.01}
# Band 4 is the tolerance in percent (how far the real value may be from the marked value).
TOLERANCES = {"brown": 1, "red": 2, "gold": 5, "silver": 10}


# Ask for a number greater than zero. If the input is wrong, the function
# calls itself again (recursion) until the user types a good value.
def get_positive_number(prompt):
    try:
        value = float(input(prompt))  # convert the typed text to a decimal number
    except ValueError:
        # the user typed letters or symbols instead of a number
        print("  Please type a number only (for example 220 or 4.7).")
        return get_positive_number(prompt)
    if value <= 0:
        print("  The value must be greater than zero.")
        return get_positive_number(prompt)
    return value


# Ask for a whole number of at least 1, calling itself again if the input is wrong.
def get_resistor_count():
    try:
        count = int(input("How many resistors do you have? "))  # text to whole number
    except ValueError:
        print("  Please type a whole number (for example 3).")
        return get_resistor_count()
    if count < 1:
        print("  You need at least one resistor.")
        return get_resistor_count()
    return count


# Recursive function: adds the resistor at "index" to the sum of the rest.
# It stops (base case) when the index goes past the end of the list.
def series_sum(values, index):
    if index == len(values):
        return 0
    return values[index] + series_sum(values, index + 1)


# Series: total resistance is the sum of all resistors.
def series_resistance(values):
    return series_sum(values, 0)


# Parallel: 1/Rtotal = 1/R1 + 1/R2 + ...  Returns Rtotal.
def parallel_resistance(values):
    reciprocal_sum = 0
    for r in values:
        reciprocal_sum = reciprocal_sum + 1 / r
    return 1 / reciprocal_sum


# Option 1 of the menu: one full series/parallel calculation.
def run_calculator():
    count = get_resistor_count()

    resistors = []  # list that stores every resistor value
    for i in range(count):
        value = get_positive_number("Enter value of resistor " + str(i + 1) + " (ohms): ")
        resistors.append(value)

    # Main calculations
    r_series = series_resistance(resistors)
    r_parallel = parallel_resistance(resistors)

    print("\n--- RESULTS ---")
    print("Total resistance in series:  ", round(r_series, 2), "ohms")
    print("Total resistance in parallel:", round(r_parallel, 2), "ohms")


# Find the nearest standard E12 resistor that is EQUAL TO OR ABOVE the target.
# Going up (never down) keeps an LED safe. Returns None if nothing is big enough.
def find_standard_value(target):
    all_values = []  # will hold every standard value, smallest first
    for multiplier in [1, 10, 100, 1000, 10000, 100000]:
        for base in E12_BASE:
            all_values.append(base * multiplier)

    for value in all_values:
        if value >= target:
            return value  # the first one that is big enough is the nearest
    return None


# Option 2 of the menu - TWIST B: choose the right resistor for an LED.
def run_led_calculator():
    print("\n--- LED Resistor Calculator ---")
    v_supply = get_positive_number("Enter supply voltage (V), e.g. 5: ")

    # Show the colours stored in the dictionary
    print("Known LED colours:")
    for colour in LED_VOLTAGES:
        print("  -", colour, LED_VOLTAGES[colour], "V")
    colour = input("Type the LED colour (small letters) or press Enter to type the voltage yourself: ")

    # Look the colour up in the dictionary, or ask for the voltage directly
    if colour in LED_VOLTAGES:
        v_led = LED_VOLTAGES[colour]
        print("Using", v_led, "V for a", colour, "LED.")
    else:
        v_led = get_positive_number("Enter LED forward voltage (V), e.g. 2: ")

    # The supply must be higher than the LED voltage or the LED will not light
    if v_supply <= v_led:
        print("  The supply voltage must be higher than the LED voltage.")
        return

    current_ma = get_positive_number("Enter wanted LED current (mA), e.g. 20: ")
    current = current_ma / 1000  # convert milliamps to amps

    # Ohm's law: R = (Vsupply - Vled) / I
    exact_r = (v_supply - v_led) / current
    print("\nExact resistor needed:", round(exact_r, 2), "ohms")

    standard_r = find_standard_value(exact_r)
    if standard_r == None:
        print("  That value is larger than the standard resistors in my list.")
        return

    # Work out what really happens with the real resistor we picked
    real_current = (v_supply - v_led) / standard_r
    resistor_power = real_current * real_current * standard_r  # P = I x I x R
    print("Nearest standard (E12) resistor:", standard_r, "ohms")
    print("Real LED current with that resistor:", round(real_current * 1000, 2), "mA")
    print("Power the resistor must handle:", round(resistor_power * 1000, 2), "mW")

    # From P = V x V / R we get V = square root of (P x R).
    # math.sqrt() comes from the math module we imported at the top.
    max_voltage = math.sqrt(0.25 * standard_r)
    print("Highest voltage a 1/4 W resistor of this value can take:", round(max_voltage, 2), "V")

    # Choose a message depending on the power
    if resistor_power > 0.25:
        print("  Warning: this is more than a 1/4 W resistor can handle. Use a higher power rating.")
    elif resistor_power > 0.125:
        print("  A 1/4 W resistor is fine for this.")
    else:
        print("  A small 1/8 W or 1/4 W resistor is fine for this.")


# Ask for a colour and keep asking (recursion) until it is found in the
# dictionary that is passed in. Returns the colour the user typed.
def get_colour(prompt, colour_dict):
    colour = input(prompt)
    if colour in colour_dict:
        return colour
    # Build one line listing the colours that are allowed for this band
    options = ""
    for name in colour_dict:
        options = options + name + ", "
    print("  I do not know that colour. Choose from:", options)
    return get_colour(prompt, colour_dict)


# Option 3 of the menu - TWIST A: decode a 4-band resistor colour code.
def run_colour_decoder():
    print("\n--- Resistor Colour Code Decoder (4 bands) ---")
    print("Type each colour in small letters, from the first band to the last.")

    band1 = get_colour("Band 1 (first digit): ", COLOUR_DIGITS)
    band2 = get_colour("Band 2 (second digit): ", COLOUR_DIGITS)
    band3 = get_colour("Band 3 (multiplier): ", MULTIPLIERS)
    band4 = get_colour("Band 4 (tolerance): ", TOLERANCES)

    # Look each colour up in its dictionary and work out the value
    digits = COLOUR_DIGITS[band1] * 10 + COLOUR_DIGITS[band2]  # e.g. red red -> 22
    value = digits * MULTIPLIERS[band3]
    tolerance = TOLERANCES[band4]

    # The real resistor can be a little lower or higher than the marked value
    lowest = value * (1 - tolerance / 100)
    highest = value * (1 + tolerance / 100)

    print("\nResistor value:", round(value, 2), "ohms")
    # Also show the value in a friendlier unit when it is large
    if value >= 1000000:
        print("  That is", round(value / 1000000, 2), "megohms")
    elif value >= 1000:
        print("  That is", round(value / 1000, 2), "kilohms")
    print("Tolerance:", tolerance, "%")
    print("The real value is between", round(lowest, 2), "and", round(highest, 2), "ohms")


# Main menu: keeps coming back until the user chooses to quit.
def main():
    print("=== Resistor Combination Calculator ===")
    running = True
    while running:
        print("\nMENU")
        print("  1. Series and parallel resistance calculator")
        print("  2. LED resistor calculator")
        print("  3. Resistor colour code decoder")
        print("  4. Quit")
        choice = input("Choose 1, 2, 3 or 4: ")

        if choice == "1":
            run_calculator()
        elif choice == "2":
            run_led_calculator()
        elif choice == "3":
            run_colour_decoder()
        elif choice == "4":
            running = False
        else:
            print("  Please type 1, 2, 3 or 4.")
    print("Thank you for using the calculator. Goodbye!")


main()
