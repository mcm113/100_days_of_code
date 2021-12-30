"""
A programme for a coin-operated coffee machine that makes 3 drinks:

    1) Espresso
    2) Latte
    3) Cappuccino

Each drink requires a set amount of milk/coffee/water. The machine starts with finite resources.

Programme Requirements:
    1) Take user order, check sufficient resources, process coins and provide change and make coffee
    2) An inventory report of current resources.

The machine accepts these coins:
    1) Penny $0.01
    2) Nickel $0.05
    3) Dime $0.10
    4) Quarter $0.25
"""
import time

# Dictionary of drinks (as keys). Values: ingredients (water/milk/coffee) and cost
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 0.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 1,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 1.10,
    }
}

# Starting resources for the coffee machine (intentionally small to test)
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

# Starting coin float
money = {
    "Quarters": {"value": 0.25, "Quantity": 10},
    "Dimes": {"value": 0.10, "Quantity": 10},
    "Nickels": {"value": 0.05, "Quantity": 10},
    "Pennies": {"value": 0.01, "Quantity": 10}
}


def sufficent_resources(drink, resources):
    """Function to check if the machine has enough resources to make the drink ordered. 

    Args:
        drink (str): [The drink that was ordered]
        resources (dict): Contains current values for each ingredient in machine

    Returns:
        [str]: Insufficent {ingredient} or sufficient resources if the drink can be made
    """
    for ingredient in MENU[drink]["ingredients"]:
        if resources[ingredient] - MENU[drink]["ingredients"][ingredient] < 0:
            return "Insufficient " + ingredient
    return "Sufficient resources"


def money_calculator(money):
    """Function to calculate money in the machine

    Args:
        money (dict): Coins in machine, their value and quantity

    Returns:
        float: total money in $ currently in machine
    """
    total_money = 0
    for coins in money:
        total_money += money[coins]["value"] * money[coins]["Quantity"]
    return total_money


def inventory_report(resources, money):
    """Prints a report of current inventory of ingredients and money supply

    Args:
        resources (dict): Amount of coffee/water/milk in machine
        money ([dict): Coins in machine, their value and quantity 
    """
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g\n")
    total_money = money_calculator(money)
    for coins in money:
        print(f"{coins}: {money[coins]['Quantity']:.0f}")
    print(f"Total money: ${total_money:.2f}")


def make_coffee(drink, resources):
    """Function that deducts drink ingredients from the current resources

    Args:
        drink (str): The drink that was ordered
        resources (dict): Contains current values for each ingredient in machine

    Returns:
        [str]: Insufficent {ingredient} or sufficient resources if the drink can be made
    """
    for ingredient in MENU[drink]["ingredients"]:
        resources[ingredient] -= MENU[drink]["ingredients"][ingredient]

    print(f"Please wait. Your {drink} is being made.")
    time.sleep(5)
    print(f"Your {drink} is ready")


def change_giver(excess_money, money):
    """Function to distribute change if person pays too much

    Args:
        excess_money (float): amount paid over the cost of the drink
        money (dict): Coins in machine, their value and quantity
    """

    print("Change given: ")
    for coin in money:
        if excess_money == 0:
            break
        change_given = round(excess_money, 2) // money[coin]["value"]
        if change_given > money[coin]["Quantity"]:
            change_given = money[coin]["Quantity"]
            money[coin]["Quantity"] = 0
        else:
            money[coin]["Quantity"] -= change_given
        print(f"{coin}: {change_given:.0f}")
        excess_money -= change_given * money[coin]["value"]


def enter_money(drink, money):

    cost_of_drink = MENU[drink]["cost"]
    money_entered = 0

    print(f"{drink.upper()}: ${cost_of_drink:.2f}. Please insert coins.")

    # Prompt user to enter change
    for coins in money:
        coins_entered = int(input(f"How many {coins} do you want to enter?: "))
        money_entered += coins_entered * money[coins]["value"]
        # Increase machine money supply
        money[coins]["Quantity"] += coins_entered

        if money_entered < cost_of_drink:
            print(f"Amount remaining: ${cost_of_drink - money_entered :.2f}")
        else:
            break

    if money_entered < cost_of_drink:
        # refund coins
        change_giver(money_entered, money)
        return "Insufficient funds. Coins refunded"

    elif money_entered > cost_of_drink:
        change_giver(money_entered - cost_of_drink, money)
        return "Successful"

    else:
        return "Successful"


def order_coffee():

    """Function to order coffee. A user is prompted for a drink.

    1) The function calls sufficient_resource function to check if it has enough resources
    2) If it does, it calls the enter_money function to process the funds
    3) If enough money has been entered, it will make the coffee

    """    

    while True:
        user_input = input(
            "What would you like? (espresso/latte/cappuccino): ")

        if user_input == "report":
            return inventory_report(resources, money)

        else:

            if sufficent_resources(user_input, resources) == "Sufficient resources":
                # if sufficient resources ask for money
                if enter_money(user_input, money) == "Successful":
                    # if enough money entered, make coffee
                    make_coffee(user_input, resources)
                else:
                    # if not enough money entered:
                    print("Insufficient funds. Coins refunded.")
            else:
                # insufficient resources to make coffee
                print(sufficent_resources(user_input, resources))

        repeat = input("Do you want another coffee: 'Y' or 'N?: ")
        if repeat.lower() == "n":
            break


order_coffee()
