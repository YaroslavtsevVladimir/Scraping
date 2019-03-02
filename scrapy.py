#!

""" Web scraping."""

import json
import requests
from lxml import html


def load_data(addres):
    """
    Load html page from url.
    :param addres: some url.
    :return: <HTMLElement>.
    """

    page_html = requests.get(addres).content.decode('utf8')
    tree = html.fromstring(page_html)
    return tree


def parse_html(filename):
    """
    Parsing <HTMLElement>.
    :param filename: result of load_data(adress).
    :return: list with links and model name.
    """

    parse_result = []
    parse_div = filename.xpath('./body/div[contains(@class, "cars-menu")]/'
                               'div[contains(@class, "cars-menu__wrapper")]//'
                               'div[contains(@class, "cars-menu__sem ")]')[:-2]
    for div in parse_div:
        car_refs = div.xpath('./a[contains(@class, "menu_models_a")]')
        for elem in car_refs:
            a_ref = elem.xpath('./@href')
            parse_result.append(url + a_ref[0])
            n_txt = elem.xpath('./text()')
            parse_result.append(n_txt[0])
    return parse_result


def get_model_list(links):
    """
    Find the cheapest and most expensive car
    and price list for each model.
    :param links: result of parse_html(filename).
    :return: list with nested dict for each model
            in json format.
    """

    result_list = []
    model_names = links[1::2]
    model_refs = links[::2]
    for ref, model in zip(model_refs, model_names):
        link_html = load_data(ref)
        car_name = [link_html.xpath('./body//div[@style="float:left;"]/p/text()')[i] for i in (-1, 0)]

        car_price = [link_html.xpath('./body/div[@id="primaryContainer"]//'
                                     'div[@id="configurator"]/div[@itemprop="offers"]/'
                                     '@price')[i] for i in (-1, 0)]
        price_list = link_html.xpath('//a[@id="all_compl"]/@href')
        price_pdf = url + price_list[0]
        dict_model = {'model': model,
                      'cheap': {'title': car_name[-1],
                                'price': car_price[-1]},
                      'expensive': {'title': car_name[0],
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
