import os
import random
import logging

import cx_Oracle
from faker import Faker
import pandas as pd
from sqlalchemy import create_engine

from providers import DegreeProvider, TimesProvider, SourceCodeProvider, ProgrammingLanguagesProvider
from providers import FrameworkProvider, ApplicationProvider

random.seed(111)


def pick_random_id(list_to_check, id_name):
    random_element = random.choice(list_to_check)
    return random_element[id_name]


class FakeIt:
    def __init__(self, num_of_developers=10, num_of_teams=10, num_of_frameworks=10, num_of_framework_versions=8,
                 num_of_app_modules=10):
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
        self.num_of_developers = num_of_developers
        self.num_of_teams = num_of_teams
        self.num_of_frameworks = num_of_frameworks
        self.num_of_app_modules = num_of_app_modules
        self.num_of_framework_versions = num_of_framework_versions

    def _create_locations(self):
        locations = []
        for idx in range(self.num_of_teams):
            locations.append(
                dict(location_id=idx, location_country=self.fake.country(), location_city=self.fake.city()))
        return locations

    def _create_base_frameworks(self):
        frameworks = []
        programming_languages = self._create_programming_languages()
        for idx in range(self.num_of_frameworks):
            chosen_programming_language = random.choice(programming_languages)
            framework = dict(framework_name=self.fake.framework_name())
            framework.update(chosen_programming_language)
            frameworks.append(framework)
        return frameworks

    def _create_programming_languages(self):
        programming_languages = []
        for idx in range(10):
            programming_languages.append(dict(**self.fake.full_programming_language_entry()))
        return programming_languages

    def _create_degrees(self):
        degrees = []
        for idx, degree in enumerate(self.possible_degrees):
            degrees.append(dict(degree_id=idx, degree_name=degree))
        return degrees

    def create_teams(self):
        teams_with_locations = []
        locations = self._create_locations()
        for idx in range(self.num_of_teams):
            chosen_location = random.choice(locations)
            team = dict(team_id=idx, team_name=self.fake.company())
            team.update(chosen_location)
            teams_with_locations.append(team)
        return teams_with_locations

    def create_developers(self):
        developers = []
        teams_with_locations = self.create_teams()
        degrees = self._create_degrees()
        for dev_id in range(self.num_of_developers):
            dev_team = random.choice(teams_with_locations)
            dev_degree = random.choice(degrees)
            developers.append(dict(dev_id=dev_id, dev_first_name=self.fake.first_name(),
                                   dev_last_name=self.fake.last_name(),
                                   **dev_degree, **dev_team))
        self.developers = developers
        return developers

    def create_times(self):
        times = []
        for idx in range(self.num_of_app_modules):
            times.append(self.fake.full_time_entry())
        self.times = times
        return times

    def create_source_codes(self):
        source_codes = []
        for idx in range(self.num_of_app_modules):
            source_codes.append(dict(code_id=idx, **self.fake.full_source_code_entry()))
        self.source_codes = source_codes
        return source_codes

    def create_frameworks(self):
        full_frameworks = []
        framework_id = 0
        base_frameworks = self._create_base_frameworks()
        for idx, base_framework in enumerate(base_frameworks):
            for _ in range(random.randint(4, self.num_of_framework_versions)):
                framework = dict(framework_id=framework_id,
                                 framework_version=self.fake.framework_version())
                framework.update(base_framework)
                full_frameworks.append(framework)
                framework_id += 1
        self.frameworks = full_frameworks
        return full_frameworks

    def create_application_modules(self):
        apps = []
        for idx in range(self.num_of_app_modules):
            foreign_keys = dict(dev_id=pick_random_id(self.developers, 'dev_id'),
                                framework_id=pick_random_id(self.frameworks, 'framework_id'),
                                day_id=self.times[idx]['day_id'],
                                code_id=pick_random_id(self.source_codes, 'code_id'),
                                days_of_develop=self.fake.days_of_develop())
            apps.append(dict(APP_MOD_ID=idx, **self.fake.app_module_entry(), **foreign_keys))
        return apps


def create_oracle_engine():
    sid_name = "orclwh"
    port = 1522
    database_ip = "217.173.198.136"
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    sid = cx_Oracle.makedsn(database_ip, port, sid=sid_name)
    cstr = f'oracle://{username}:{password}@{sid}'
    return create_engine(cstr, convert_unicode=False, echo=True)


def commit_to_database(dataframe: pd.DataFrame, name, connection, schema='S83993'):
    dataframe.to_sql(name=name, con=connection, schema=schema, if_exists='append', index=False)


def main():
    logging.basicConfig(level=logging.INFO)
    engine = create_oracle_engine()
    connection = engine.connect()
    fake_it = FakeIt(num_of_developers=250, num_of_frameworks=15, num_of_framework_versions=8,
                     num_of_teams=10, num_of_app_modules=1200)
    times = pd.DataFrame(fake_it.create_times())
    developers = pd.DataFrame(fake_it.create_developers())
    source_codes = pd.DataFrame(fake_it.create_source_codes())
    frameworks = pd.DataFrame(fake_it.create_frameworks())
    application_modules = pd.DataFrame(fake_it.create_application_modules())
    try:
        commit_to_database(developers, 'developers', connection)
        commit_to_database(source_codes, 'source_codes', connection)
        commit_to_database(frameworks, 'frameworks', connection)
        commit_to_database(times, 'times', connection)
        commit_to_database(application_modules, 'application_modules', connection)
    except Exception as err:
        logging.error(err)
        raise err
    finally:
        connection.close()
        engine.dispose()


if __name__ == '__main__':
    main()
