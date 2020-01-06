import logging

from faker import Faker
import random
from providers import DegreeProvider, TimesProvider, SourceCodeProvider, ProgrammingLanguagesProvider
from providers import FrameworkProvider, ApplicationProvider

random.seed(123456)


def pick_random_id(list_to_check, id_name):
    random_element = random.choice(list_to_check)
    return random_element[id_name]


class FakeIt:
    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(DegreeProvider)
        self.fake.add_provider(TimesProvider)
        self.fake.add_provider(SourceCodeProvider)
        self.fake.add_provider(ProgrammingLanguagesProvider)
        self.fake.add_provider(FrameworkProvider)
        self.fake.add_provider(ApplicationProvider)
        self.possible_degrees = [
            'Associate of Arts',
            "Bachelor's degree",
            "Master's degree",
            "Doctoral degree"
        ]
        self.developers = []
        self.times = []
        self.source_codes = []
        self.frameworks = []

    def _create_locations(self):
        locations = []
        for idx in range(10):
            locations.append(
                dict(location_id=idx, location_country=self.fake.country(), location_city=self.fake.city()))
        return locations

    def create_teams(self):
        teams_with_locations = []
        locations = self._create_locations()
        for idx in range(10):
            chosen_location = random.choice(locations)
            team = dict(team_id=idx, team_name=self.fake.company())
            team.update(chosen_location)
            teams_with_locations.append(team)
        return teams_with_locations

    def _create_degrees(self):
        degrees = []
        for idx, degree in enumerate(self.possible_degrees):
            degrees.append(dict(degree_id=idx, degree_name=degree))
        return degrees

    def create_developers(self):
        developers = []
        teams_with_locations = self.create_teams()
        for dev_id in range(10):
            dev_team = random.choice(teams_with_locations)
            developers.append(dict(dev_id=dev_id, dev_first_name=self.fake.first_name(),
                                   dev_last_name=self.fake.last_name(),
                                   team_id=dev_team.team_id, team_name=dev_team.team_name,
                                   location_id=dev_team.location_id, location_country=dev_team.location_country,
                                   location_city=dev_team.location_city))
        self.developers = developers
        return developers

    def create_times(self):
        times = []
        for idx in range(10):
            times.append(dict(day_id=idx, **self.fake.full_time_entry()))
        self.times = times
        return times

    def create_source_codes(self):
        source_codes = []
        for idx in range(10):
            source_codes.append(dict(code_id=idx, **self.fake.full_source_code_entry()))
        self.source_codes = source_codes
        return source_codes

    def _create_programming_languages(self):
        programming_languages = []
        for idx in range(10):
            programming_languages.append(dict(**self.fake.full_programming_language_entry()))
        return programming_languages

    def _create_base_frameworks(self):
        frameworks = []
        programming_languages = self._create_programming_languages()
        for idx in range(10):
            chosen_programming_language = random.choice(programming_languages)
            framework = dict(framework_id=idx, framework_name=self.fake.framework_name())
            framework.update(chosen_programming_language)
            frameworks.append(framework)
        return frameworks

    def create_full_frameworks(self):
        full_frameworks = []
        framework_id = 0
        base_frameworks = self._create_base_frameworks()
        for idx, base_framework in enumerate(base_frameworks):
            for _ in range(random.randint(4, 10)):
                framework = dict(framework_id=framework_id,
                                 framework_version=self.fake.framework_version())
                framework.update(base_framework)
                full_frameworks.append(framework)
                framework_id += 1
        self.frameworks = full_frameworks
        return full_frameworks

    def create_applications(self):
        apps = []
        for idx in range(10):
            apps.append(dict(app_id=idx, **self.fake.app_module_entry()))
        return apps


def main():
    logging.basicConfig(level=logging.INFO)
    fake_it = FakeIt()
    times = fake_it.create_times()
    locations = fake_it._create_locations()
    degrees = fake_it._create_degrees()
    teams = fake_it.create_teams()
    source_codes = fake_it.create_source_codes()
    full_frameworks = fake_it.create_full_frameworks()
    apps = fake_it.create_applications()


if __name__ == '__main__':
    main()
