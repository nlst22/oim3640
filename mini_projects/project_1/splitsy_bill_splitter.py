# Collecting user input for even bill splitting (subtotal, tax, tip)
# Function to collect inputs from user and math for the bill total

from colorama import Fore, Style, init
init()
##################################################
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
####################################################
def split_evenly(final_total, n_people):
    """Split the final total evenly among the number of people."""
    return final_total / n_people
##################################################
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

#################################################
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

##########################################
def run_even_split():
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

###############################
def collect_items(bucket_name):
    """
    Collect item prices for a given bucket (e.g., 'Person 1', 'Shared').

    The user enters one item price at a time.
    Typing 'done' ends the list.

    Parameters:
        bucket_name (str): Label for who/what the items belong to.

    Returns:
        list[float]: A list of item prices.
    """
    print(f"\nEnter items for {bucket_name}.")
    print("Type a price (e.g., 10.50). Type 'done' when finished.\n")

    items = []

    while True:
        raw = input(f"{bucket_name} item price: ").strip().lower()

        if raw in {"done", "d"}:
            break

        # Optional: allow quit during item entry
        if raw in {"q", "quit"}:
            print("Exiting item entry.")
            return items  # or raise KeyboardInterrupt if you prefer

        try:
            price = float(raw)
            if price <= 0:
                print("Item price must be greater than 0.")
                continue
            items.append(price)
        except ValueError:
            print("Please enter a valid number or 'done'.")

    return items


def run_uneven_split():
    """Run the itemized bill splitting workflow."""
    
    print("=== Itemized Bill Splitter ===")

    n_people = get_int("Enter number of people: ", 2)

    person_subtotals = []

    # Collect items for each person
    for i in range(1, n_people + 1):
        items = collect_items(f"Person {i}")
        subtotal = sum(items)
        person_subtotals.append(subtotal)

    # Collect shared items
    shared_items = collect_items("Shared")
    shared_total = sum(shared_items)

    # Split shared items evenly
    shared_per_person = shared_total / n_people

    # Compute base totals
    base_totals = []
    for subtotal in person_subtotals:
        base_totals.append(subtotal + shared_per_person)

    total_base = sum(base_totals)

    print("\nBase totals before tax/tip:")
    for i, amount in enumerate(base_totals, start=1):
        print(f"Person {i}: ${amount:.2f}")
    
    #Get tax and tip inputs (allow 0)
    tax_pct = get_float("Enter Tax % (e.g., 6.25): ", 0.01)   # allows 0 with your validator
    tip_pct = get_float("Enter Tip % (e.g., 20): ", )     # allows 0 with your validator

    # Compute tax, tip, and final total using the combined base
    tax, tip, final_total = compute_total(total_base, tax_pct, tip_pct)

    # Split tax and tip evenly across everyone
    tax_each = tax / n_people
    tip_each = tip / n_people

    # Final amount each person owes
    final_per_person = []
    for base in base_totals:
        final_per_person.append(base + tax_each + tip_each)
    
    line = "-" * 40
    bold_line = "=" * 40

    print("\n" + bold_line)
    print("   ITEMIZED SPLIT SUMMARY")
    print(bold_line)

    print("\nBase totals (before tax/tip):")
    for i, base in enumerate(base_totals, start=1):
        print(f"Person {i}: ${base:>8.2f}")

    print(line)
    print(f"Total base:      ${total_base:>8.2f}")
    print(f"Tax total:       ${tax:>8.2f}  (each: ${tax_each:>6.2f})")
    print(f"Tip total:       ${tip:>8.2f}  (each: ${tip_each:>6.2f})")
    print(f"Final total:     ${final_total:>8.2f}")

    print("\nFinal owed (tax/tip split evenly):")
    for i, owed in enumerate(final_per_person, start=1):
        print(f"{Fore.GREEN}Person {i} owes: ${owed:>8.2f}{Style.RESET_ALL}")

    print(bold_line)



def show_home_menu():
    """Display the home menu options."""
    print("\n" + "=" * 40)
    print("           BILL SPLITTER")
    print("=" * 40)
    print("1) Split a bill evenly")
    print("2) Split a bill by items (uneven)")
    print("3) Quit")
    print("=" * 40)
##############################
def main():
    """Home screen menu that routes to even or uneven split workflows."""
    while True:
        show_home_menu()
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            run_even_split()
        elif choice == "2":
            run_uneven_split()   # make sure this function exists
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
if __name__ == "__main__":
    main()






