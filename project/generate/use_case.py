from abc import ABC, abstractmethod

from project.generate.models.entities import Country, Product, Category
from project.generate.services.parse import IParseService


class IGenerateUseCase(ABC):

    @abstractmethod
    async def create_file(self, category: Category, country: Country):
        """
        :param category:
        :param country:
        :return:
        """

    @abstractmethod
    async def get_categories(self) -> list[str]:
        """
        :return: list of Categories titles
        """

    @abstractmethod
    async def get_countries(self, category: Category) -> list[str]:
        """
        :param category:
        :return:
        """


class GenerateUseCase(IGenerateUseCase):

    def __init__(self, parse: IParseService):
        self.parse = parse

    async def create_file(self, category: Category, country: Country):
        await self.parse.get_products(category.link, country.name)

    async def get_categories(self) -> list[str]:
        categories = await self.parse.get_categories()
        return [category.title for category in categories]

    async def get_countries(self, category: Category) -> list[str]:
        # need to add postgres or delete method and add countries to main request
        names = ["КНДР", "Нидерланды", "Республика Корея", "Россия", "Таиланд", "Япония"]
        countries = [Country(name=name) for name in names]
        return[country.name for country in countries]
