from PythonTools.debug import debug_message, init_debug, error
from PythonTools.renderer import Menu, clear
from PythonTools.tools import get_user_input_of_type

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

    def calc_total_cost(self):
        total_cost = 0

        for pet in self.pets:
            total_cost += pet.yearly_cost

        return total_cost

class Human:
    experience = []

    def __init__(self, name, spare_time, age, life_expectancy):
        self.name = name
        self.age = age
        self.spare_time = spare_time
        self.life_expectancy = life_expectancy

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
    life_expectancy = get_user_input_of_type(float, "Enter the human's life expectancy: ")

    human = Human(name, spare_time, age, life_expectancy)

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
    while True:
        menu = Menu("Create Menu", ["Create Household", "Create Pet", "Create Human", "Back"])

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

            case "Back":
                return

def calc_income_eligibility(household, pet, human):
    # Calculate the income eligibility
    available_funds = household.disposable_income - household.household_expenditure
    funds_with_pet = available_funds / (abs(available_funds) + household.calc_total_cost())
    time_with_pet = human.spare_time / (abs(human.spare_time) + pet.min_time_required)

    debug_message(f"Avaliable funds: {available_funds}")
    debug_message(f"Funds with pet: {funds_with_pet}")
    debug_message(f"Time with pet: {time_with_pet}")

    return (funds_with_pet + time_with_pet) > 1.5

def calc_floor_space_eligibility(household, pet, human):
    floor = household.floor_space / (abs(household.floor_space) + pet.min_floor_space)
    has_experience = human.experience.count(pet.name) > 0
    return (floor + (0.1 * has_experience)) > 0.6

def calc_age_eligibility(human, pet):
    return (human.life_expectancy - (human.age + pet.life_expectancy)) > 0

def maths_menu():

    # Ask which household to use
    hh_chosen = Menu("Select a household", [household.name for household in households]).get_input()
    household = [household for household in households if household.name == hh_chosen][0]

    # Ask which human to use
    human_chosen = Menu("Select a human", [human.name for human in household.humans]).get_input()
    human = [human for human in household.humans if human.name == human_chosen][0]

    overall_eligibility = True
    message = ""
    # Loop through each pet
    for pet in household.pets:
        household_eligibility = calc_income_eligibility(household, pet, human)
        floor_eligibility = calc_floor_space_eligibility(household, pet, human)
        age_eligibility = calc_age_eligibility(human, pet)

        if not household_eligibility:
            overall_eligibility = False
            message += f"{pet.name} is not eligible due to income and time\n"

        if not floor_eligibility:
            overall_eligibility = False
            message += f"{pet.name} is not eligible due to floor space\n"

        if not age_eligibility:
            overall_eligibility = False
            message += f"{pet.name} is not eligible due to age\n"

    print(message)


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
                    print(f" == Household: {household.name} ==")
                    print(" - " + str(household))
                    print(" -- Humans:")
                    for human in household.humans:
                        print(" --- " + str(human))

                    print(" -- Pets:")
                    for pet in household.pets:
                        print(" --- " + str(pet))

                input("Press enter to continue...")

            case "Do maths":
                maths_menu()

            case "Quit":
                print("Quitting")


if __name__ == "__main__":
    init_debug()
    main()
