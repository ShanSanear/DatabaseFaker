from faker import Faker
from faker.generator import Generator
import random
from providers import DegreeProvider, TimesProvider, SourceCodeProvider, ProgrammingLanguagesProvider, FrameworkProvider

possible_degrees = [
    'Associate of Arts',
    "Bachelor's degree",
    "Master's degree",
    "Doctoral degree"
]


class RootModel:
    def __init__(self, **kwargs):
        self.data = {**kwargs}

    def __add__(self, other):
        self.data.update(other.data)
        return self

    def __str__(self):
        # print("Data keys:", list(self.data.keys()))
        return ",".join((str(x) for x in self.data.values()))

    def __repr__(self):
        return str(self)

    def __getattr__(self, item):
        if item in self.data:
            return self.data[item]
        super(RootModel, self).__getattr__(item)

    def check_keys(self):
        return ",".join(self.data.keys())


fake = Faker()
fake.add_provider(DegreeProvider)
fake.add_provider(TimesProvider)
fake.add_provider(SourceCodeProvider)
fake.add_provider(ProgrammingLanguagesProvider)
fake.add_provider(FrameworkProvider)

locations = []
for idx in range(10):
    locations.append(RootModel(location_id=idx, location_country=fake.country(), location_city=fake.city()))

teams_with_locations = []
for idx in range(10):
    chosen_location = random.choice(locations)
    team = RootModel(team_id=idx, team_name=fake.company())
    teams_with_locations.append(team + chosen_location)

degrees = []
for idx, degree in enumerate(possible_degrees):
    degrees.append(RootModel(degree_id=idx, degree_name=degree))

developers = []
for dev_id in range(10):
    dev_team = random.choice(teams_with_locations)
    dev_location = random.choice(locations)
    developers.append(RootModel(dev_id=dev_id, dev_first_name=fake.first_name(),
                                dev_last_name=fake.last_name(),
                                team_id=dev_team.team_id, team_name=dev_team.team_name,
                                location_id=dev_team.location_id, location_country=dev_team.location_country,
                                location_city=dev_team.location_city))

times = []
for idx in range(10):
    times.append(RootModel(day_id=idx, **fake.full_time_entry()))

source_codes = []
for idx in range(10):
    source_codes.append(RootModel(code_id=idx, **fake.full_source_code_entry()))

programming_languages = []

for idx in range(10):
    programming_languages.append(RootModel(**fake.full_programming_language_entry()))

frameworks = []
for idx in range(10):
    chosen_programming_language = random.choice(programming_languages)
    framework = RootModel(framework_id=idx,
                          framework_name=fake.framework_name(),
                          framework_version=fake.framework_version())
    updated_framework = framework + chosen_programming_language
    frameworks.append(updated_framework)

print(locations)
print(degrees)
print(teams_with_locations)
print(times)
print(source_codes)
print(frameworks[0].check_keys())
for e in frameworks:
    print(e)
