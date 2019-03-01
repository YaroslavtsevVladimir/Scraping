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

    file_html = requests.get(addres).content.decode('utf8')
    tree = html.fromstring(file_html)
    return tree


def parse_html(filename, url):
    """
    Parsing <HTMLElement>.
    :param filename: result of load_data(adress)
    :param url: some url
    :return: list without last 3 items
    """

    result = []

    car_div = filename.xpath('//body//div[@class="cars-menu__wrapper clearfix"]//'
                             'div[@class="cars-menu__sem clearfix"]')[:-2]

    for div in car_div:
        car_a = div.xpath('./a[@class="cars-menu__base-name menu_models_a"]/@href')
        for ref in car_a:

            result.append('%s%s' % (url, ref))

    return result


def find_car(links):
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
        car_name = [link.xpath('//div[@style="float:left;"]/p/text()')[i] for i in (-1, 0)]
        car_price = [link.xpath('//p[@class="kompl_price"][1]/text()')[i] for i in (-1, 0)]
        price_list = link.xpath('//a[@id="all_compl"]/@href')
        price_pdf = ('%s%s' % (url, price_list[0]))

        cheap = {'title': car_name[-1],
                 'price': car_price[-1].replace(' ', '').replace('\n', ' ')}

        expensive = {'title': car_name[0],
                     'price': car_price[0].replace(' ', '').replace('\n', ' ')}

        dict_car = {'model': header[0].replace('\xa0\n', '').replace('   ', ''),
                    'cheap': cheap,
                    'expensive': expensive,
                    'price_list': price_pdf}

        result_list.append(dict_car)

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
    f = load_data(url)
    parser = parse_html(f, url)
    res = find_car(parser)
    get_json(res)


if __name__ == '__main__':

    url = 'https://www.lada.ru'
    main()
