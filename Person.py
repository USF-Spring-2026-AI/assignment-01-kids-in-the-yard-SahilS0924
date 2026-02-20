class Person:
  
   # Person Object: An individual in the simulated family tree.

    def __init__(
        self,
        year_born: int,
        year_died: int,
        first_name: str,
        last_name: str,
        gender: str,
    ):
        # Core identity data
        self.year_born = year_born
        self.year_died = year_died
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender

        # Relationship attributes (start empty)
        self.partner = None      # Will store a Person object
        self.children = []       # List of Person objects

    def get_age(self) -> int:
        # Return person's age
        return self.year_died - self.year_born

    def get_name(self) -> str:
        # Return the person's full name as 
        return f"{self.first_name} {self.last_name}"

    def get_partner(self):
        # Return this person's partner, or None if not married
        return self.partner

    def get_children(self) -> list:
        # Return this person's list of children
        return self.children

    def get_gender(self) -> str:
        # Return the person's gender (M or F)
        return self.gender

    def get_birth_decade(self) -> int:
        # Return the decade the person was born in    
        return (self.year_born // 10) * 10

    def set_partner(self, partner) -> None:
        # Assign a partner to a person
        self.partner = partner

    def add_child(self, child) -> None:
        # Add a child to this person's children list
        self.children.append(child)

    def __str__(self) -> str:
        # Human-readable representation of a person
        return f"{self.get_name()} ({self.year_born}-{self.year_died})"

    def __repr__(self) -> str:
        # Used to print lists of Person objects when called
        return self.__str__()
