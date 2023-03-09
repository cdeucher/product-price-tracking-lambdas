from scraping import scrap
import pytest
import simplejson as json


def test_scrap():
    price, title = scrap(
        "https://www.amazon.com.br/Mentes-perigosas-psicopata-comemorativa-anivers%C3%A1rio/dp/8525067326")
    assert price == "49,90"
    assert title == "Mentes Perigosas: Psicopatas e seus crimes (Edição comemorativa de 10 anos)"
