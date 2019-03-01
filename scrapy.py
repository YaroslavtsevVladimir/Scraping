#!

"""Web scraping."""

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
    :return: list without last 3 items
    """

    result = []

    parse_div = filename.xpath('//body//'
                               'div[@class="cars-menu__wrapper clearfix"]//'
                               'div[@class="cars-menu__sem clearfix"]')[:-2]

    for div in parse_div:
        car_a = div.xpath('./a[@class="cars-menu__base-name menu_models_a"]/@href')
        for ref in car_a:

            result.append('%s%s' % (url, ref))

    return result


def get_model_list(links):
    """
    Find the cheapest and most expensive car
    for each model and price list.
    :param links: result of parse_html(filename, url)
    :return: list with nested dict for each model
    """

    result_list = []

    for link in links:
        link = load_data(link)

        header = link.xpath('//h1[@id="text17"]/text()')
        car_name = [link.xpath('//body//div[@style="float:left;"]/p/text()')[i] for i in (-1, 0)]
        car_price = [link.xpath('//body//div[@style="float:right;"]//'
                                'div[@class="old_new_price"]/p/text()')[i] for i in (-1, 1)]
        price_list = link.xpath('//a[@id="all_compl"]/@href')
        price_pdf = ('%s%s' % (url, price_list[0]))

        dict_model = {'model': header[0].replace('\xa0\n', '').replace('   ', ''),
                      'cheap': {'title': car_name[-1],
                                'price': car_price[-1].replace(' ', '').replace('\n', '')},
                      'expensive': {'title': car_name[0],
                                    'price': car_price[0].replace(' ', '').replace('\n', '')},
                      'price_list': price_pdf}

        result_list.append(dict_model)

    return result_list


def get_json(listing):
    """
    Get result of find_car(links) in json format.
    :param listing: result of find_car(links)
    :return: file data_json.json
    """

    with open('data_json.json', 'w') as result_file:
        return json.dump(listing, result_file, ensure_ascii=False, indent=4)


def main():
    """
    main
    :return: None
    """
    file_html = load_data(url)
    parser = parse_html(file_html)
    res = get_model_list(parser)
    get_json(res)


if __name__ == '__main__':

    url = 'https://www.lada.ru'
    main()
