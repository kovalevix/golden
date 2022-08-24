from functools import cache

from project.generate.use_case import IGenerateUseCase, GenerateUseCase
from project.generate.services.parse import IParseService, ParseService


def get_parse_service() -> IParseService:
    service = ParseService()
    return service


@cache
def get_use_case() -> IGenerateUseCase:
    parse = get_parse_service()
    use_case = GenerateUseCase(parse)
    return use_case
