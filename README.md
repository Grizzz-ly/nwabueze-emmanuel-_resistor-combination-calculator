# Resistor Combination Calculator

## What it does
This program asks how many resistors you have and the value of each one, then calculates the total resistance when they are connected in series and in parallel. It checks every input, so typing a letter or a negative number gives a helpful message instead of a crash. It also has a resistor colour code decoder and an LED resistor calculator.

## How to run it

**On a phone (Pydroid 3):**
1. Install Pydroid 3 from the Google Play Store.
2. Open the app, paste the code from `resistor_combination_calculator.py` (or open the file).
3. Tap the yellow play button to run it, then type your answers in the console.

**On a computer (VS Code):**
1. Install Python 3 and VS Code, and add the Python extension in VS Code.
2. Open the folder containing `resistor_combination_calculator.py`.
3. Open the file and click the Run button (the triangle at the top right), then type your answers in the terminal.

## Sample output

Series and parallel calculator (menu option 1):

```
MENU
  1. Series and parallel resistance calculator
  2. LED resistor calculator
  3. Resistor colour code decoder
  4. Quit
Choose 1, 2, 3 or 4: 1
How many resistors do you have? 3
Enter value of resistor 1 (ohms): 100
Enter value of resistor 2 (ohms): 200
Enter value of resistor 3 (ohms): 300

--- RESULTS ---
Total resistance in series:   600.0 ohms
Total resistance in parallel: 54.55 ohms
```

LED resistor calculator (menu option 2):

```
--- LED Resistor Calculator ---
Enter supply voltage (V), e.g. 5: 5
Known LED colours:
  - red 2.0 V
  - yellow 2.1 V
  - green 2.2 V
  - blue 3.0 V
  - white 3.0 V
Type the LED colour (small letters) or press Enter to type the voltage yourself: green
Using 2.2 V for a green LED.
Enter wanted LED current (mA), e.g. 20: 20

Exact resistor needed: 140.0 ohms
Nearest standard (E12) resistor: 150 ohms
Real LED current with that resistor: 18.67 mA
Power the resistor must handle: 52.27 mW
Highest voltage a 1/4 W resistor of this value can take: 6.12 V
  A small 1/8 W or 1/4 W resistor is fine for this.
```

Resistor colour code decoder (menu option 3):

```
--- Resistor Colour Code Decoder (4 bands) ---
Type each colour in small letters, from the first band to the last.
Band 1 (first digit): yellow
Band 2 (second digit): violet
Band 3 (multiplier): red
Band 4 (tolerance): silver

Resistor value: 4700 ohms
  That is 4.7 kilohms
Tolerance: 10 %
The real value is between 4230.0 and 5170.0 ohms
```

## My own twist
I added two extra features that were not in the brief:

1. **Resistor colour code decoder.** The user types the four colour bands of a real resistor. The program looks each colour up in a dictionary, works out the resistor's value, and shows the tolerance and the range the real value could be in. If the user types a colour that does not exist, the program shows the allowed colours and asks again.
2. **LED resistor calculator with a standard value finder.** The user enters the supply voltage and picks an LED colour (a dictionary stores the typical voltage for each colour), or types the voltage directly. The program calculates the exact resistor needed, then searches a list of standard E12 resistor values to find the nearest real resistor that is equal to or above the answer, so the LED stays safe. It also shows the real LED current, the power the resistor must handle, and the highest voltage a 1/4 W resistor of that value can safely take (calculated with `math.sqrt()` from Python's math module).

## What I learned
- How to check input before using it, so the program does not crash when someone types a letter instead of a number.
- That a calculated answer is not always a resistor you can actually buy, which is why I added the standard E12 value finder.

## Author
Nwabueze Emmanuel, ND2 Mechatronics Engineering, YabaTech.
