from typing import Callable
from finance_calculations import percentage


class Category:
    postfix: str
    calculator: Callable[[str], float]

    def __init__(self, postfix: str, calculator: Callable[[str], float]):
        self.postfix = postfix
        self.calculator = calculator


class CategoriesConfig:
    companies = ["SBER", "ROSN", "VTB", "TCSG", "OZON", "FIVE", "SFIN", "PLZL", "CRTX", "STZ", "UBER"]
    categories = {
        "percentage": Category("%", percentage.calculate_return)
    }
