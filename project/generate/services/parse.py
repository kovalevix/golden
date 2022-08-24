import requests
import asyncio
from functools import cache
from sys import platform
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

from project.generate.models.entities import Category, Country, Product


class IParseService(ABC):

    @abstractmethod
    async def get_categories(self) -> list[Category]:
        """
        :return: list of Category class
        """

    @abstractmethod
    async def get_pages_amount(self, category: Category) -> int:
        """
        :param  category: category`s href
        :return: amount of pages in category
        """

    @abstractmethod
    async def get_category_id(self,  category: Category) -> int:
        """
        :param  category: category`s href
        :return: category`s id
        """

    @abstractmethod
    async def get_page_of_products(self, category: Category, country: Country, page: int) -> list[Product]:
        """
        :param category:
        :param country:
        :param page:
        :return:
        """

    @abstractmethod
    async def get_products(self, link: str, country: str) -> list[Product]:
        """
        :param link:
        :param country:
        :return:
        """


class ParseService(IParseService):

    async def get_categories(self) -> list[Category]:
        url = "https://goldapple.by/"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        # first of <a> elements with such class name is not category title
        categories = soup.find_all('a', attrs={'class': 'ogg-menu__link_with-categories'})[1:]
        return [
            Category(
                id=None, title=category['href'].split("/")[-1], link=category['href']
            ) for category in categories
        ]

    async def get_pages_amount(self, category: Category) -> int:
        page = requests.get(category.link)
        soup = BeautifulSoup(page.text, 'html.parser')
        products_amount = int(soup.find('span', attrs={'class': 'toolbar-number'}).text)
        # page consist of 20 products
        return products_amount//20 + 1 if products_amount != 0 else 0

    async def get_category_id(self, category: Category) -> int:
        page = requests.get(category.link)
        soup = BeautifulSoup(page.text, 'html.parser')
        return int(soup.find('div', attrs={'class': 'i-flocktory'})['data-fl-category-id'])

    async def get_page_of_products(self, category: Category, country: Country, page: int) -> list[Product]:
        if not category.id:
            return []
        url = f"https://goldapple.by/web_scripts/discover/category/products?cat={category.id}&page={page}"
        page = requests.get(url)
        products = page.json()['products']
        return [
            Product(
                name=product['name'],
                category=category,
                country=country,
                price=product['price_object']['amount'],
                link=product['url'],
                photo=product['image_url'],
            ) for product in products if product['is_saleable'] and country.name == product['country']
        ]

    @cache
    async def get_products(self, link: str, name: str) -> list[Product]:
        products = []
        category = Category(id=None, title=link.split("/")[-1], link=link)
        country = Country(name=name)
        category.id = await self.get_category_id(category)
        amount = await self.get_pages_amount(category)
        for page in range(1, amount):
            arr = await self.get_page_of_products(category, country, page)
            products.extend(arr)
        return products
