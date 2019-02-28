#!
"""Web scraping."""

import json
import requests
from lxml import html


def load_data(addres):
    """

    :param addres:
    :return:
    """
    file_html = requests.get(addres).content.decode('utf8')
    tree = html.fromstring(file_html)
    return tree


def parse_html(filename, url):
    """

    :param filename:
    :param url:
    :return:
    """
    result = []
    car_div = filename.xpath('//div[@class="col-lg1-3 col-sm1-6 mb-sm1-5 mb-xs-5"]')[0]
    car_ul = car_div.xpath('./ul[@class="list-unstyled"]')

    for li in car_ul:
        for i in li:
            link = i.xpath('./a/@href')
            result.append('%s%s' % (url, link[0]))

    return result[:-3]


def find_car(links):
    """

    :param links:
    :return:
    """
    result_list = []

    try:
        for link in links:
            link = load_data(link)

            header = link.xpath('//h1[@id="text17"]/text()')
            car_name = [link.xpath('//div[@style="float:left;"]/p/text()')[i] for i in (-1, 1)]
            car_price = [link.xpath('//p[@class="kompl_price"][1]/text()')[i] for i in (-1, 1)]
            price_list = link.xpath('//a[@id="all_compl"]/@href')
            price_pdf = ('%s%s' % (url, price_list[0]))

            cheap = {'title': car_name[-1],
                     'price': car_price[-1].replace(' ', '').replace('\\n', '')}

            expensive = {'title': car_name[1],
                         'price': car_price[1].replace(' ', '').replace('\\n', '')}

            dict_car = {'model': header[0].replace('\xa0\n', '').replace('   ', ''),
                        'cheap': cheap,
                        'expensive': expensive,
                        'price_list': price_pdf}

            result_list.append(dict_car)
    except:
        pass
    return result_list


def get_json(listing):
    """

    :param listing:
    :return:
    """
    with open('data_json', 'w') as result_file:
        # return json.dumps(listing, indent=4)
        return json.dump(listing, result_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':

    url = 'https://www.lada.ru'
    f = load_data(url)
    parser = parse_html(f, url)
    res = find_car(parser)
    get_json(res)
