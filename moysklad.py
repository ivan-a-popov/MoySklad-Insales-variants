import requests
import setup

from setup import MOYSKLAD_BASE_URL, MOYSKLAD_TOKEN, MOYSKLAD_PER_PAGE


def get_page(url, session):
    setup.logger.debug(url)
    with session.get(url) as response:
        return response.json()


def get_goods():
    endpoint = f'entity/assortment?limit={MOYSKLAD_PER_PAGE}'
    next_href = f'{MOYSKLAD_BASE_URL}/{endpoint}'
    goods_with_article = {}

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {MOYSKLAD_TOKEN}'})

    while next_href:
        page = get_page(next_href, session)
        for good in page['rows']:
            try:
                goods_with_article[good['article']] = good['quantity']
            except KeyError:
                continue
        try:
            next_href = page['meta']['nextHref']
        except KeyError:
            break

    if setup.DEBUG:
        setup.save_debug_file('goods_with_article.json', goods_with_article)

    return goods_with_article


if __name__ == '__main__':  # debug function
    get_goods()
