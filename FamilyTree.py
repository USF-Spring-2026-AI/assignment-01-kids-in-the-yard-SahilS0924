# https://stackoverflow.com/questions/45072283/how-to-use-a-python-dictionary
from collections import defaultdict

from Person import Person
from PersonFactory import PersonFactory


class FamilyTree:
    # Driver class, builds tree from 1950 with 2 original parents and generates the rest of the family tree, then answers user queries about the tree.

    MAX_YEAR = 2120

    def __init__(self):
        self.factory = PersonFactory()
        self.people: list[Person] = []
        self.root1: Person | None = None
        self.root2: Person | None = None

    def init_tree(self, person1_info: dict, person2_info: dict) -> None:
        # Create the two founding people (born 1950), pair them as partners, then generate the rest of the family tree.
        year_born = 1950
        family_last_name = person1_info["last_name"]
        # Pick the life expectancy for the two founding people
        year_died1 = self.factory._pick_life_expectancy(year_born)
        self.root1 = Person(
            year_born,
            year_died1,
            person1_info["first_name"],
            person1_info["last_name"],
            person1_info["gender"],
        )

        year_died2 = self.factory._pick_life_expectancy(year_born)
        self.root2 = Person(
            year_born,
            year_died2,
            person2_info["first_name"],
            person2_info["last_name"],
            person2_info["gender"],
        )
        # Set founders as partners
        self.root1.set_partner(self.root2)
        self.root2.set_partner(self.root1)
        # Add the two founding people to the list of people
        self.people.append(self.root1)
        self.people.append(self.root2)
        # Generate the rest of the family tree
        self._generate_family(self.root1, family_last_name)

    def _generate_family(self, person: Person, family_last_name: str) -> None:
        # Recursively generate children and their partners for the person
        has_partner = person.get_partner() is not None
        num_children = self.factory.compute_num_children(person.year_born)

        # If no children, end early
        if num_children == 0:
            return
        # Compute the birth years of the children
        birth_years = self.factory.compute_child_birth_years(
            person.year_born, num_children
        )
        # Generate the children
        for year in birth_years:
            if year > self.MAX_YEAR:
                continue
            # Create the child
            child = self.factory.get_person(
                year_born=year, last_name=family_last_name
            )
            # Add the child to the person's children
            person.add_child(child)
            if has_partner:
                person.get_partner().add_child(child)
            # Add the child to the list of people

            self.people.append(child)

            # Attempt to give the child a partner from outside the family
            partner = self.factory.attempt_partner(child)
            if partner is not None:
                child.set_partner(partner)
                partner.set_partner(child)
                self.people.append(partner)

            self._generate_family(child, family_last_name)

    # User Querirs
    def total_people(self) -> int:
        # Return the total number of people in the tree
        return len(self.people)

    def people_by_decade(self) -> dict:
        # Count the number of people born in each decade
        # Sort the decades chronologically
        counts = defaultdict(int)
        for person in self.people:
            counts[person.get_birth_decade()] += 1
        return dict(sorted(counts.items()))

    def duplicate_names(self) -> list:
        # Return a sorted list of full names that repeat
        name_counts = defaultdict(int)
        for person in self.people:
            name_counts[person.get_name()] += 1
        return sorted(name for name, count in name_counts.items() if count > 1)

    # Interactive menu
    def run(self) -> None:
        menu = (
            "\nQuery Options:\n"
            "  (T)otal number of people in the tree\n"
            "  Total number of people in the tree for each (D)ecade\n"
            "  (N)ames Repeated\n"
            "  (Q)uit\n"
            "> "
        )
        # Loop until the user quits
        while True:
            choice = input(menu).strip().upper()
            # Total number of people in the tree
            if choice == "T":
                print(f"\nThe tree contains {self.total_people()} people total.")
            # Total number of people in the tree for each decade
            elif choice == "D":
                print()
                for decade, count in self.people_by_decade().items():
                    print(f"  {decade}: {count} people")
            # Names repeated
            elif choice == "N":
                dupes = self.duplicate_names()
                if not dupes:
                    print("\nThere are no duplicate names in the tree.")
                else:
                    print(f"\nThere are {len(dupes)} duplicate name(s) in the tree:")
                    for name in dupes:
                        print(f"  * {name}")
            # Quit
            elif choice == "Q":
                print("Goodbye!")
                break
            # Invalid input
            else:
                print("  Please enter T, D, N, or Q.")

    # Main function
    # Read the files, create the tree, and run the interactive menu
if __name__ == "__main__":
    print("Reading files...")
    tree = FamilyTree()

    print("Generating family tree...")
    tree.init_tree(
        person1_info={
            "first_name": "Desmond",
            "last_name": "Jones",
            "gender": "male",
        },
        person2_info={
            "first_name": "Molly",
            "last_name": "Jones",
            "gender": "female",
        },
    )

    tree.run()