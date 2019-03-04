#!

""" Web scraping."""

import json
import requests
from lxml import html


def load_data(addres):
    """
    Load html page from url.
    :param addres: some url
    :return: <HTMLElement>
    """

    page_html = requests.get(addres).content.decode('utf8')
    tree = html.fromstring(page_html)
    return tree


def parse_html(filename):
    """
    Parsing <HTMLElement>.
    :param filename: result of load_data(adress)
    :return: list with nested tuples (ref, text)
    """

    parse_result = []
    parse_div = filename.xpath('./body/div[contains(@class, "cars-menu")]/'
                               'div[contains(@class, "cars-menu__wrapper")]//'
                               'div[contains(@class, "cars-menu__sem ")]')[:-2]
    for div in parse_div:
        car_a = div.xpath('./a[contains(@class, "menu_models_a")]')
        for a in car_a:
            ref = a.xpath('./@href')
            txt = a.xpath('./text()')
            parse_result.append((url + ref[0], txt[0]))
    return parse_result


def get_model_list(models):
    """
    Find the cheapest and most expensive car
    and price list for each model.
    :param models: result of parse_html(filename)
    :return: list with nested dict for each model
    """

    result_list = []
    for model in models:
        link_html = load_data(model[0])
        complect_colon = link_html.xpath('./body//div[@style="float:left;"]')[0]
        car_complect = [complect_colon.xpath('./p/text()')[i] for i in (-1, 0)]
        price_colon = link_html.xpath('./body/div[@id="primaryContainer"]//'
                                      'div[@id="configurator"]')[0]
        car_price = [price_colon.xpath('./div[@itemprop="offers"]/@price')[i] for i in (-1, 0)]
        price_list = link_html.xpath('//a[@id="all_compl"]/@href')
        price_pdf = url + price_list[0]
        dict_model = {'model': model[1],
                      'cheap': {'title': car_complect[-1],
                                'price': car_price[-1]},
                      'expensive': {'title': car_complect[0],
                                    'price': car_price[0]},
                      'price_list': price_pdf}
        result_list.append(dict_model)
    return json.dumps(result_list, ensure_ascii=False, indent=4)


def main():
    file_html = load_data(url)
    parser = parse_html(file_html)
    get_model_list(parser)


if __name__ == '__main__':
    url = 'https://www.lada.ru'
    main()
