from faker import Faker
from faker.generator import Generator
import random
from providers import DegreeProvider, TimesProvider, SourceCodeProvider, ProgrammingLanguagesProvider, FrameworkProvider

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


class FakeIt:
    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(DegreeProvider)
        self.fake.add_provider(TimesProvider)
        self.fake.add_provider(SourceCodeProvider)
        self.fake.add_provider(ProgrammingLanguagesProvider)
        self.fake.add_provider(FrameworkProvider)
        self.possible_degrees = [
            'Associate of Arts',
            "Bachelor's degree",
            "Master's degree",
            "Doctoral degree"
        ]

    def create_locations(self):
        locations = []
        for idx in range(10):
            locations.append(
                RootModel(location_id=idx, location_country=self.fake.country(), location_city=self.fake.city()))
        return locations

    def create_teams(self):
        teams_with_locations = []
        locations = self.create_locations()
        for idx in range(10):
            chosen_location = random.choice(locations)
            team = RootModel(team_id=idx, team_name=self.fake.company())
            teams_with_locations.append(team + chosen_location)
        return teams_with_locations

    def create_degrees(self):
        degrees = []
        for idx, degree in enumerate(self.possible_degrees):
            degrees.append(RootModel(degree_id=idx, degree_name=degree))
        return degrees

    def create_developers(self):
        developers = []
        teams_with_locations = self.create_teams()
        for dev_id in range(10):
            dev_team = random.choice(teams_with_locations)
            developers.append(RootModel(dev_id=dev_id, dev_first_name=self.fake.first_name(),
                                        dev_last_name=self.fake.last_name(),
                                        team_id=dev_team.team_id, team_name=dev_team.team_name,
                                        location_id=dev_team.location_id, location_country=dev_team.location_country,
                                        location_city=dev_team.location_city))
        return developers


    def create_times(self):
        times = []
        for idx in range(10):
            times.append(RootModel(day_id=idx, **self.fake.full_time_entry()))
        return times

    def create_source_codes(self):
        source_codes = []
        for idx in range(10):
            source_codes.append(RootModel(code_id=idx, **self.fake.full_source_code_entry()))
        return source_codes

    def create_programming_languages(self):
        programming_languages = []
        for idx in range(10):
            programming_languages.append(RootModel(**self.fake.full_programming_language_entry()))
        return programming_languages

    def create_frameworks(self):
        frameworks = []
        programming_languages = self.create_programming_languages()
        for idx in range(10):
            chosen_programming_language = random.choice(programming_languages)
            framework = RootModel(framework_name=self.fake.framework_name())
            updated_framework = framework + chosen_programming_language
            frameworks.append(updated_framework)
        return frameworks

    def create_full_frameworks(self):
        full_frameworks = []
        framework_id = 0
        frameworks = self.create_frameworks()
        for idx, framework in enumerate(frameworks):
            for _ in range(random.randint(4, 10)):
                full_frameworks.append(RootModel(framework_id=framework_id,
                                                 framework_version=self.fake.framework_version()) + framework)
                framework_id += 1
        return full_frameworks


fake_it = FakeIt()
times = fake_it.create_times()
locations = fake_it.create_locations()
degrees = fake_it.create_degrees()
teams = fake_it.create_teams()
source_codes = fake_it.create_source_codes()
full_frameworks = fake_it.create_full_frameworks()
print(locations)
print(degrees)
print(teams)
print(times)
print(source_codes)
print(full_frameworks[0].check_keys())
for e in full_frameworks:
    print(e)
