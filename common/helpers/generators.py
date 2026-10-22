from __future__ import annotations

from faker import Faker

fake = Faker()
Faker.seed(42)


class DataGenerator:
    """Generate random test data."""

    @staticmethod
    def email() -> str:
        return fake.unique.email()

    @staticmethod
    def username() -> str:
        return fake.user_name()

    @staticmethod
    def password() -> str:
        return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

    @staticmethod
    def first_name() -> str:
        return fake.first_name()

    @staticmethod
    def last_name() -> str:
        return fake.last_name()

    @staticmethod
    def full_name() -> str:
        return fake.name()

    @staticmethod
    def phone() -> str:
        return fake.phone_number()

    @staticmethod
    def address() -> str:
        return fake.address().replace("\n", ", ")

    @staticmethod
    def company() -> str:
        return fake.company()

    @staticmethod
    def text(length: int = 50) -> str:
        return fake.text(max_nb_chars=length)

    @staticmethod
    def uuid() -> str:
        return str(fake.uuid4())

    @staticmethod
    def user_payload() -> dict:
        """Generate a complete user payload."""
        return {
            "first_name": DataGenerator.first_name(),
            "last_name": DataGenerator.last_name(),
            "email": DataGenerator.email(),
            "password": DataGenerator.password(),
            "phone": DataGenerator.phone(),
        }
