# Collecting user input for bill splitting (subtotal, tax, tip)
# Function to collect inputs from user
def main():
    print("=== Even Bill Splitter ===")

    subtotal = float(input("Enter bill subtotal:$"))
    tax_pct = float(input("Enter tax percent: "))
    tip_pct = float(input("Enter tip percent: "))
    n_people = int(input("Enter number of people: "))

    tax = subtotal * (tax_pct / 100)
    tip = subtotal * (tip_pct / 100)
    final_total = subtotal + tax + tip
    each_person = final_total / n_people

    print("\n--- Summary ---")
    print(f"Subtotal:    ${subtotal:.2f}")
    print(f"Tax:         ${tax:.2f}")
    print(f"Tip:         ${tip:.2f}")
    print(f"Final Total: ${final_total:.2f}")
    print(f"Per Person:  ${each_person:.2f}")


if __name__ == "__main__":
    main()






