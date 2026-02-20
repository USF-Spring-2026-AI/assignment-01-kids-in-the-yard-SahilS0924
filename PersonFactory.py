# https://stackoverflow.com/questions/41585078/how-do-i-read-and-write-csv-files started with this and went down the rabbit hole to get to this point
# https://stackoverflow.com/questions/36150257/probability-distribution-function-python used this to help with the random choice function
# https://stackoverflow.com/questions/72955906/python-csv-dictreader used this to help with the csv reader function
# https://www.geeksforgeeks.org/python/zip-in-python/ used this to help with the zip function
import csv
import math
import random

from Person import Person


class PersonFactory:

   # Reads all data CSV files and generates Person objects

    def __init__(self):
        self.life_expectancy = {}
        self.birth_marriage_rates = {}
        self.first_names = {}
        self.last_names = {}
        self.rank_probabilities = {}
        self.gender_name_probability = {}
        self.read_files()

    def read_files(self) -> None:
        # Read all required CSV data files 
        self._read_life_expectancy()
        self._read_birth_marriage_rates()
        self._read_first_names()
        self._read_last_names()
        self._read_rank_probabilities()

    def _read_life_expectancy(self) -> None:
        # Read the life expectancy file
        with open("life_expectancy.csv", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                year = int(row["Year"])
                expectancy = float(row["Period life expectancy at birth"])
                self.life_expectancy[year] = expectancy

    def _read_birth_marriage_rates(self) -> None:
        # Read the birth and marriage rates file
        with open("birth_and_marriage_rates.csv", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                decade = row["decade"].strip()
                self.birth_marriage_rates[decade] = {
                    "birth_rate": float(row["birth_rate"]),
                    "marriage_rate": float(row["marriage_rate"]),
                }

    def _read_first_names(self) -> None:

        with open("first_names.csv", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                decade = row["decade"].strip()
                gender = row["gender"].strip().lower()
                name = row["name"].strip()
                frequency = float(row["frequency"])
                # If the decade is not in the first names dictionary, create an empty dictionary for that decade
                if decade not in self.first_names:
                    self.first_names[decade] = {"male": [], "female": []}
                # Add the name and frequency to the first names dictionary
                self.first_names[decade][gender].append((name, frequency))

    def _read_last_names(self) -> None:
        # Read the last names file
        with open("last_names.csv", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                decade = row["Decade"].strip()
                rank = int(row["Rank"])
                last_name = row["LastName"].strip()
                # If the decade is not in the last names dictionary, create an empty list for that decade
                if decade not in self.last_names:
                    self.last_names[decade] = []
                # Add the last name and rank to the last names dictionary
                self.last_names[decade].append((last_name, rank))

    def _read_rank_probabilities(self) -> None:
        # Read the rank to probability file
        with open("rank_to_probability.csv", newline="") as csv_file:
            content = csv_file.read().strip()
            # The file contains raw comma-separated values (no header)
            probabilities = [float(p.strip()) for p in content.split(",") if p.strip()]
            for index, probability in enumerate(probabilities):
                rank = index + 1
                self.rank_probabilities[rank] = probability


    def _year_to_decade_key(self, year: int) -> str:
        # Convert the year to the decade key
        decade_start = (year // 10) * 10
        exact_key = f"{decade_start}s"
        return exact_key

    def _nearest_decade_key(self, year: int, mapping: dict) -> str:

        decade_start = (year // 10) * 10
        exact_key = f"{decade_start}s"
        if exact_key in mapping:
            return exact_key

        # Find the nearest available decade
        available = sorted(
            int(k.rstrip("s")) for k in mapping.keys()
        )
        nearest = min(available, key=lambda d: abs(d - decade_start))

    def _pick_life_expectancy(self, year_born: int) -> int:
        # Pick the life expectancy for the person
        # If the year is in the life expectancy dict, use the life expectancy for that year
        # Else, find the nearest year in the dict and use the life expectancy for that year
        # Add a random offset of -10 to 10 years to the life expectancy
        if year_born in self.life_expectancy:
            base = self.life_expectancy[year_born]
        else:
            nearest_year = min(
                self.life_expectancy.keys(),
                key=lambda y: abs(y - year_born),
            )
            base = self.life_expectancy[nearest_year]

        offset = random.uniform(-10, 10)
        return year_born + round(base + offset)

    def _pick_gender(self) -> str:
        # Returns M or F with equal probability
        return random.choice(["male", "female"])

    def _pick_first_name(self, year_born: int, gender: str) -> str:
       
       # Chooses a first name weighted by the frequency data for the birth decade and gender
        decade_key = self._nearest_decade_key(year_born, self.first_names)
        name_list = self.first_names.get(decade_key, {}).get(gender, [])

        if not name_list:
            return "John"
        # Choose a first name using probabilities for the birth decade and gender
        names, weights = zip(*name_list)
        return random.choices(names, weights=weights, k=1)[0]

    def _pick_last_name(self, year_born: int) -> str:
        # Choose a last name using probabilities for the birth decade
        # If no last name, return "Smith"
        decade_key = self._nearest_decade_key(year_born, self.last_names)
        surname_list = self.last_names.get(decade_key, [])

        if not surname_list or not self.rank_probabilities:
            return "Smith"

        names = [name for name, _ in surname_list]
        weights = [
            self.rank_probabilities.get(rank, 0.001)
            for _, rank in surname_list
        ]
        return random.choices(names, weights=weights, k=1)[0]

    # Pulblic methods for generating Person objects

    def get_person(self, year_born: int, last_name: str = None) -> Person:
      
        # Create and return a fully populated Person object.

        gender = self._pick_gender()
        first_name = self._pick_first_name(year_born, gender)
        chosen_last_name = last_name if last_name is not None else self._pick_last_name(year_born)
        year_died = self._pick_life_expectancy(year_born)

        return Person(year_born, year_died, first_name, chosen_last_name, gender)

    def get_marriage_rate(self, year_born: int) -> float:
        # Return the marriage rate for the decade they were born in
        decade_key = self._nearest_decade_key(year_born, self.birth_marriage_rates)
        return self.birth_marriage_rates[decade_key]["marriage_rate"]

    def get_birth_rate(self, year_born: int) -> float:
       # Return the birth rate for the decade they were born in
        decade_key = self._nearest_decade_key(year_born, self.birth_marriage_rates)
        return self.birth_marriage_rates[decade_key]["birth_rate"]

    def attempt_partner(self, person: Person) -> Person | None: 
       # Use the marriage rate to see if the person gets a partner. If so, make a new Person born within 10 years of their age
        
        marriage_rate = self.get_marriage_rate(person.year_born)
        if random.random() > marriage_rate:
            return None

        partner_year_born = person.year_born + random.randint(-10, 10)
        partner_year_born = max(partner_year_born, 1900)

        # Partners from outside the family get a randomly last name
        return self.get_person(year_born=partner_year_born, last_name=None)

    def compute_child_birth_years( self, elder_parent_year: int, num_children: int) -> list:
        # Children must be born between elder_parent_year + 25 and elder_parent_year + 45
        first_year = elder_parent_year + 25
        last_year = elder_parent_year + 45

        #If there’s only 1 child, there’s no spacing to worry about.
        if num_children == 1:
            return [random.randint(first_year, last_year)] 

        #Else, distribute the children evenly across the window.
        step = (last_year - first_year) / (num_children - 1)
        return [round(first_year + i * step) for i in range(num_children)]

    def compute_num_children(self, year_born: int) -> int:
        # Determines how many children someone has. The base birth rate 1.5 defines the range, rounded up via math.ceil.
        birth_rate = self.get_birth_rate(year_born)
        #Ensures no negative children
        low = math.ceil(birth_rate - 1.5)
        high = math.ceil(birth_rate + 1.5)
        low = max(low, 0)
        high = max(high, 0)

        return random.randint(low, high)