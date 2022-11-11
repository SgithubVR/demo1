#start of program

print("Hello! Welcome to the Lucky Invest Platform. Lets see how lucky you are :).")
wallet = input("Please note, investment amount should be more than 30,000 and will be locked for a year. How much do you want to invest?")

#profit is the calculating field
profit = 0
try:
    wallet = int(wallet)
except ValueError:
    print("That's not an int!")
if wallet < 30000:
    raise Exception("Sorry, number is too low")

print("You have deposited", wallet, "Dollars in your Wallet! Lets Roll!")

