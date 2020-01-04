import random
import string

from faker import Faker
from faker.providers import BaseProvider

from random import randrange
from datetime import timedelta, datetime


def pick_random_date(start_date, end_date):
    change = end_date - start_date
    int_delta = (change.days * 24 * 60 * 60) + change.seconds
    random_second = randrange(int_delta)
    return start_date + timedelta(seconds=random_second)


class DegreeProvider(BaseProvider):
    def degree_name(self):
        return random.choice([
            'Associate of Arts',
            "Bachelor's degree",
            "Master's degree",
            "Doctoral degree"
        ])


class SourceCodeProvider(BaseProvider):
    def code_lines_added(self, min=10, max=2000):
        return random.randint(min, max)

    def code_lines_deleted(self, min=10, max=2000):
        return random.randint(min, max)

    def code_files(self, min=2, max=100):
        return random.randint(min, max)

    def code_functions(self, min=10, max=500):
        return random.randint(min, max)

    def code_classes(self, min=1, max=100):
        return random.randint(min, max)

    def code_test_cover(self):
        return round(random.random() * 100, 2)

    def code_coupling(self):
        return round(random.random() * 100, 2)

    def full_source_code_entry(self):
        return {
            "code_lines_added": self.code_lines_added(),
            "code_lines_deleted": self.code_lines_deleted(),
            "code_files": self.code_files(),
            "code_functions": self.code_functions(),
            "code_classes": self.code_classes(),
            "code_test_cover": self.code_test_cover(),
            "code_coupling": self.code_coupling(),

        }


class TimesProvider(BaseProvider):
    def full_time_entry(self, start_date=datetime(year=2005, month=1, day=1),
                        end_date=datetime(year=2010, month=12, day=31)):
        picked_date = pick_random_date(start_date, end_date)
        return {
            "year": picked_date.year,
            "month": picked_date.month,
            "month_desc": picked_date.strftime("%B"),
            "day": picked_date.day,
            "hour": picked_date.hour,
            "week_num": picked_date.strftime("%U"),
        }


class FrameworkProvider(BaseProvider):
    def framework_name(self):
        return random.choice(
            ["Framework A", "Framework B", "Framework C", "Framework D"]
        )

    def framework_version(self):
        major = random.randint(1, 5)
        minor = random.randint(1, 5)
        bug_fix = random.randint(1, 5)
        return f"{major}.{minor}.{bug_fix}"


class ProgrammingLanguagesProvider(BaseProvider):
    def full_programming_language_entry(self):
        return random.choice([
            {"prog_lang_id": 1, "prog_lang_name": "C#", "prog_lang_version": "4.3"
             },
            {"prog_lang_id": 2, "prog_lang_name": "C", "prog_lang_version": "ANSI C 1999",
             },
            {"prog_lang_id": 3, "prog_lang_name": "Python", "prog_lang_version": "2.7.15",
             },
            {"prog_lang_id": 4, "prog_lang_name": "Python", "prog_lang_version": "3.6",
             },
            {"prog_lang_id": 5, "prog_lang_name": "Java", "prog_lang_version": "1.8",
             },
            {"prog_lang_id": 6, "prog_lang_name": "Java", "prog_lang_version": "11",
             },
            {"prog_lang_id": 7, "prog_lang_name": "Java", "prog_lang_version": "10",
             },
            {"prog_lang_id": 8, "prog_lang_name": ".Net Core", "prog_lang_version": "2.2",
             },
            {"prog_lang_id": 8, "prog_lang_name": ".Net Core", "prog_lang_version": "3.1",
             }
        ]
        )


class ApplicationProvider(BaseProvider):
    def app_name(self):
        return "".join(random.choices(string.ascii_uppercase, k=random.randint(4, 6)))

    def app_type(self):
        return random.choice(["type A", "type B", "type C", "type D"])

    def app_module_entry(self):
        return {
            "app_mod_name": "".join(random.choices(string.ascii_uppercase, k=random.randint(4, 6))),
            "app_mod_ver": f"{random.randint(0, 10)}.{random.randint(0, 10)}.{random.randint(0, 10)}"
        }

    def days_of_develop(self):
        return random.randint(10, 256)
