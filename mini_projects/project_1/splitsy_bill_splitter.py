# Collecting user input for even bill splitting (subtotal, tax, tip)
# Function to collect inputs from user and math for the bill total

from colorama import Fore, Style, init
init()

def compute_total(subtotal, tax_pct, tip_pct):
    """ Calculate tax, tip, and final total for a bill.
    Parameters:
    subtotal (float): The pre-tax cost of the bill.
    tax_pct (float): Tax percentage (e.g., 6.25 for 6.25%).
    tip_pct (float): Tip percentage (e.g., 20 for 20%).
    Returns:
    tuple: (tax_amount, tip_amount, final_total)
    """
    tax = subtotal * (tax_pct / 100)
    tip = subtotal * (tip_pct / 100)
    final_total = subtotal + tax + tip
    return tax, tip, final_total

def split_evenly(final_total, n_people):
    """Split the final total evenly among the number of people."""
    return final_total / n_people

def get_float(prompt, min_value=0):
    """
    Prompt the user for a floating point number and validate the input.

    Parameters:
        prompt (str): The message shown to the user.
        min_value (float): The minimum acceptable value.

    Returns:
        float: A valid number entered by the user.
    """

    while True:
        try:
            value = float(input(prompt))

            if value <= min_value:
                print(f"Value must be at least {min_value}. Please try again.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")

def get_int(prompt, min_value=1):
    """
    Prompt the user for an integer and validate the input.

    Parameters:
        prompt (str): The message shown to the user.
        min_value (int): The minimum acceptable value.

    Returns:
        int: A valid integer entered by the user.
    """

    while True:
        try:
            value = int(input(prompt))

            if value < min_value:
                print(f"Value must be at least {min_value}. Please try again.")
                continue

            return value

        except ValueError:
            print("Please enter a valid whole number.")

def main():
    """ first print a welcome message and then collect user input for the bill subtotal, tax percentage, tip percentage, and number of people to split the bill among. Then call the compute_total function to calculate the tax, tip, and final total. Finally, call the split_evenly function to calculate how much each person owes and print a summary of the bill and the amount each person owes. """
    print("=== Even Bill Splitter ===")

    subtotal = get_float("Enter bill subtotal: $")
    tax_pct = get_float("Enter Tax % (e.g., 6.25): ", 0.01)
    tip_pct = get_float("Enter Tip % (e.g., 20): ", 0)
    n_people = get_int("Enter number of people: ", 1)

    tax, tip, final_total = compute_total(subtotal, tax_pct, tip_pct)
    each_person = split_evenly(final_total, n_people)

    line = "-" * 40
    bold_line = "=" * 40

    print("\n" + bold_line)
    print("        EVEN BILL SPLIT SUMMARY")
    print(bold_line)

    print(f"Subtotal:        ${subtotal:>8.2f}")
    print(f"Tax:             ${tax:>8.2f}")
    print(f"Tip:             ${tip:>8.2f}")
    print(f"Final Total:     ${final_total:>8.2f}")

    print(line)

    print(f"Split between:   {n_people} people")
    print(f"{Fore.GREEN}Each person owes ${each_person:>8.2f}{Style.RESET_ALL}")

    print(bold_line)

if __name__ == "__main__":
    main()

