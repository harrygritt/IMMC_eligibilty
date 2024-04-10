from PythonTools.debug import debug_message, init_debug, error
from PythonTools.renderer import Menu, clear
from PythonTools.tools import get_user_input_of_type

HUMAN_LIFE_EXPECTANCY = 0
MIN_OWNER_AGE = 0
MIN_OWNER_AGE = 0

num_pets = 0  # prev pets plus posible new pets
total_cost = 0

households = []


class Household:
    pets = []
    humans = []

    def __init__(self, name, disposable_income, household_expenditure, floor_space):
        self.name = name
        self.disposable_income = disposable_income
        self.household_expenditure = household_expenditure
        self.floor_space = floor_space

    def __str__(self):
        return f'Name: {self.name} Disposable income: {self.disposable_income}, Expenditure: {self.household_expenditure}, Floor space: {self.floor_space}'

class Human:
    experience = []

    def __init__(self, name, spare_time, age):
        self.name = name
        self.age = age
        self.spare_time = spare_time

    def __str__(self):
        return f'Name: {self.name}, Age: {self.age}, Spare time: {self.spare_time}, Has experience with: {self.experience}'


class Pet:
    def __init__(self, name, yearly_cost, min_time_required, min_floor_space, life_expectancy):
        self.name = name
        self.yearly_cost = yearly_cost
        self.min_time_required = min_time_required
        self.min_floor_space = min_floor_space
        self.life_expectancy = life_expectancy

    def __str__(self):
        return f'Name: {self.name}, Yearly cost: {self.yearly_cost}, Min time required: {self.min_time_required}, Min floor space: {self.min_floor_space}'


def create_pet(household):
    # Get the pet's details
    name = get_user_input_of_type(str, "Enter the pet's name: ")
    yearly_cost = get_user_input_of_type(float, "Enter the pet's yearly cost: ")
    min_time_required = get_user_input_of_type(float, "Enter the pet's minimum time required: ")
    min_floor_space = get_user_input_of_type(float, "Enter the pet's minimum floor space: ")
    life_expectancy = get_user_input_of_type(float, "Enter the pet's life expectancy: ")

    # Create the pet
    pet = Pet(name, yearly_cost, min_time_required, min_floor_space, life_expectancy)
    household.pets.append(pet)


def create_human(household):
    # Get the human's details
    name = get_user_input_of_type(str, "Enter the human's name: ")
    age = get_user_input_of_type(int, "Enter the human's age: ")
    spare_time = get_user_input_of_type(float, "Enter the human's spare time: ")

    human = Human(name, spare_time, age)

    # get what the human has experience with
    while True:
        options = [pet.name for pet in household.pets]
        options.append("Done")
        experience = Menu("Select what the human has experience with", options).get_input()
        if experience == "Done":
            break

        # Check if the experience is not already in the list
        if experience not in human.experience:
            human.experience.append(experience)

    # Create the human
    household.humans.append(human)


def create_household():
    # Get the household's details
    name = get_user_input_of_type(str, "Enter the household's name: ")
    disposable_income = get_user_input_of_type(float, "Enter the household's disposable income: ")
    household_expenditure = get_user_input_of_type(float, "Enter the household's expenditure: ")
    floor_space = get_user_input_of_type(float, "Enter the household's floor space: ")

    # Create the household
    household = Household(name, disposable_income, household_expenditure, floor_space)
    households.append(household)


def create_menu():
    menu = Menu("Create Menu", ["Create Household", "Create Pet", "Create Human"])

    match menu.get_input():
        case "Create Pet":
            if len(households) == 0:
                error("No households have been created yet, please create a household first.")
                create_menu()
                return

            hh_name = Menu("Select a household", [household.name for household in households]).get_input()
            household = [household for household in households if household.name == hh_name][0]
            create_pet(household)
        case "Create Human":
            if len(households) == 0:
                error("No households have been created yet, please create a household first.")
                create_menu()
                return

            hh_name = Menu("Select a household", [household.name for household in households]).get_input()
            household = [household for household in households if household.name == hh_name][0]
            create_human(household)
        case "Create Household":
            create_household()

def calc_income_eligibility(household, pet, human):
    # Calculate the income eligibility
    available_funds = household.disposable_income - household.household_expenditure
    funds_with_pet = available_funds / (abs(available_funds) + pet.yearly_cost)
    time_with_pet = human.spare_time / (abs(human.spare_time) + pet.min_time_required)

    debug_message(f"Avaliable funds: {available_funds}")
    debug_message(f"Funds with pet: {funds_with_pet}")
    debug_message(f"Time with pet: {time_with_pet}")

    return (funds_with_pet + time_with_pet) > 1.5

def calc_floor_space_eligibility(household, pet, human):
    floor = household.floor_space / (abs(household.floor_space) + pet.min_floor_space)
    has_experience = human.experience.count(pet.name) > 0
    return (floor + (0.1 * has_experience)) > 0.6

def maths_menu():
    menu = Menu("Maths Menu", ["Calculate total cost", "Calculate income & time eligibility", "Calculate floor space & expeirence eligibility", "Calculate age eligibility"])
    menu_option = menu.get_input()

    # Ask which household to use
    household = Menu("Select a household", [household.name for household in households]).get_input()
    household = [household for household in households if household.name == household][0]

    # Ask which pet to use
    pet = Menu("Select a pet", [pet.name for pet in household.pets]).get_input()
    pet = [pet for pet in household.pets if pet.name == pet][0]

    # Ask which human to use
    human = Menu("Select a human", [human.name for human in household.humans]).get_input()
    human = [human for human in household.humans if human.name == human][0]

    match menu_option:
        case "Calculate total cost":
            # Calculate the total cost
            total_cost = sum([pet.yearly_cost for pet in pets])
            print(f"The total cost is: {total_cost}")

        case "Calculate income & time eligibility":
            household_eligibility = calc_income_eligibility(household, pet, human)
            if household_eligibility:
                print("The household is eligible")
            else:
                print("The household is not eligible")

        case "Calculate floor space & expeirence eligibility":
            floor_eligibility = calc_floor_space_eligibility(household, pet, human)
            if floor_eligibility:
                print("The household is eligible")
            else:
                print("The household is not eligible")


        case "Calculate age eligibility":
            # Calculate the age eligibility
            age_eligibility = human.age - HUMAN_LIFE_EXPECTANCY

def main():
    while True:
        main_menu = Menu("Main Menu", ["Create Pet/Household/Human", "View All", "Do maths", "Quit"])
        match main_menu.get_input():
            case "Create Pet/Household/Human":
                print("Creating a household")
                create_menu()

            case "View All":
                clear()
                print("Households:")
                for household in households:
                    print(" - " + str(household))

                    print(" - Humans:")
                    for human in household.humans:
                        print(" -- " + str(human))

                    print(" - Pets:")
                    for pet in household.pets:
                        print(" -- " + str(pet))

                input("Press enter to continue...")

            case "Do maths":
                print("Doing maths")
                maths_menu()

            case "Quit":
                print("Quitting")


if __name__ == "__main__":
    init_debug()
    main()
