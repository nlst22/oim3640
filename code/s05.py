## This Session: Functions

# A product costs $100 how much tax will be payed? 

# product_price = 100 # in dollars
# tax_rate = 0.0625 # 6.25% tax
# tax = product_price * tax_rate
# print (f'The tax for a product which costs ${product_price} is {tax}')

# def calc_tax():
#     product_price = 100 # in dollars
#     tax_rate = 0.0625 # 6.25% tax
#     tax = product_price * tax_rate
#     print (f'The tax for a product which costs ${product_price} is {tax}.')

# calc_tax()

computer_price = 2500
iphone_price = 999

def calc_tax(product_price):
    """Calculate product tax given the product price and return the tax amount."""
    tax_rate = 0.0625 # 6.25% tax
    tax = product_price * tax_rate
    #print (f'The tax for a product which costs ${product_price} is {tax}.')
    # if the function does not reutrn any vale explicitly, it returns None by default  --> so instead of print, we use return
    return tax # returning the tax value --> now the function can be used in expressions

calc_tax(computer_price)
calc_tax(iphone_price)
calc_tax(250)

total_tax = calc_tax(computer_price) + calc_tax(iphone_price) # get nonetype error
print (total_tax)

###

computer_price = 2500
iphone_price = 999
ny_rate = 0.08875
ca_rate = 0.0725

def calc_tax(product_price, tax_rate):
    """Calculate product tax given the product price and tax rate and return the tax amount."""
    #tax_rate = 0.0625 # 6.25% tax --> now we dont need this line as tax_rate is passed as parameter
    tax = product_price * tax_rate
    #print (f'The tax for a product which costs ${product_price} is {tax}.')
    # if the function does not reutrn any vale explicitly, it returns None by default  --> so instead of print, we use return
    return tax # returning the tax value --> now the function can be used in expressions

tax_computer= calc_tax(computer_price, ny_rate)
tax_iphone= calc_tax(iphone_price, ca_rate)
print (f'The tax for computer is {tax_computer} and for iphone is {tax_iphone}.')



# ## Review from last session
# a = input("Enter an integer: ") # how to make sure input is integer
# try:
#     a = int(input("Enter an integer: "))
# except ValueError:
#     print("Invalid input. Please enter an integer.")
#     a = int(input("Enter an integer: "))
# a = int(a)
# print(type(a))

# # Check odd or even 
# if a % 2 == 0: 
#     print ("Even")
# else:
#     print ("Odd")

# a = 2 
# 1 + a # ab exoresssion, which evaluates to 3 but does not do anything with it
# print (1 + a) # now it prints 3 



# for i in range(5):
#     print(i)

# for x in range (4):
#     print (x)

# names = ["Alice", "Bob", "Charlie"]
# for name in names:
#     print(name)
