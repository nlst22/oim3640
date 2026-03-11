# Bill Splitter (Terminal App)

## Overview
Bill Splitter is a Python terminal application that helps users divide a bill among multiple people. The app supports two different splitting methods:

1. **Even Split** – divides the total bill equally among everyone.
2. **Itemized Split (Uneven)** – allows users to enter individual item costs for each person and shared items, then calculates how much each person owes.

The program also calculates **tax and tip** and displays a clear summary of the bill.

This project was built to practice:
- Writing and organizing Python functions
- Handling user input
- Input validation and error handling
- Control flow using loops and conditionals
- Designing a simple terminal-based user interface

---

# Features

## Even Bill Split
Users enter:
- Bill subtotal
- Tax percentage
- Tip percentage
- Number of people

The program calculates:
- Tax amount
- Tip amount
- Final bill total
- Amount each person owes

---

## Itemized (Uneven) Bill Split
Users enter:
- Number of people
- Individual item prices for each person
- Shared item prices

The program then:
1. Calculates each person's **base subtotal**
2. Splits shared items evenly among everyone
3. Calculates total tax and tip
4. Splits tax and tip evenly among all people
5. Displays how much each person owes

---

# Example Program Flow

## Home Menu
```console
========================================
           BILL SPLITTER
========================================
1) Split a bill evenly
2) Split a bill by items (uneven)
3) Quit
========================================
Choose an option:
```
## Example 1: Even Bill Split

```console

=== Even Bill Splitter ===

Enter bill subtotal: $100
Enter Tax % (e.g., 6.25): 6
Enter Tip % (e.g., 20): 20
Enter number of people: 2

========================================
        EVEN BILL SPLIT SUMMARY
========================================
Subtotal:        $ 100.00
Tax:             $   6.00
Tip:             $  20.00
Final Total:     $ 126.00
----------------------------------------
Split between:   2 people
Each person owes $  63.00
========================================
```
## Example 2: Uneven Split

```console
=== Itemized Bill Splitter ===

Enter number of people: 2

Enter items for Person 1
Person 1 item price: 10
Person 1 item price: 14
Person 1 item price: done

Enter items for Person 2
Person 2 item price: 12
Person 2 item price: 17
Person 2 item price: done

Enter items for Shared
Shared item price: 15
Shared item price: done

Enter Tax % (e.g., 6.25): 6
Enter Tip % (e.g., 20): 20

========================================
        ITEMIZED SPLIT SUMMARY
========================================

Base totals (before tax/tip)
Person 1: $ 31.50
Person 2: $ 36.50

----------------------------------------
Total base:      $ 68.00
Tax total:       $  4.08
Tip total:       $ 13.60
Final total:     $ 85.68

Final owed (tax/tip split evenly)
Person 1 owes: $ 40.34
Person 2 owes: $ 45.34
```
---

# Installation

## 1. Install Python
This program requires **Python 3.8 or higher**.

Check your version:

```bash
python --version

pip install colorama

python splitsy_bill_splitter.py
