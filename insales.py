from requests.auth import HTTPBasicAuth
import setup
import requests

from setup import INSALES_BASE_URL, INSALES_API_ID, INSALES_API_PASS, INSALES_PER_PAGE


def make_session():
    session = requests.Session()
    session.auth = HTTPBasicAuth(INSALES_API_ID, INSALES_API_PASS)
    return session


def update_stocks(index):
    endpoint = 'products/variants_group_update.json'
    api_endpoint = f'{INSALES_BASE_URL}/{endpoint}'
    setup.logger.debug(f"Sending data to {api_endpoint}")

    session = make_session()
    i = 0
    while index:
        package = index[:100]  # It’s possible to update at most 100 variants per request.
        index[:100] = []
        data = {"variants": package}
        response = session.put(api_endpoint, json=data)
        i += 1
        setup.logger.debug(f"Package {i} {response}")


def get_qty(session):
    url = INSALES_BASE_URL + '/products/count.json'
    with session.get(url) as response:
        return response.json()['count']


def get_page(page, session):
    endpoint = f'products.json?per_page={INSALES_PER_PAGE}&page={page}'
    api_endpoint = f'{INSALES_BASE_URL}/{endpoint}'
    setup.logger.debug(f"Getting page {page}: {api_endpoint}")
    with session.get(api_endpoint) as response:
        return response.json()


def get_variants():
    session = make_session()

    qty = get_qty(session)
    count = qty // INSALES_PER_PAGE + 1
    setup.logger.debug(f"{qty} items, {count} pages")
    goods = []
    for i in range(1, count+1):
        page = get_page(i, session)
        goods += page
    if setup.DEBUG:
        setup.save_debug_file('insales.json', goods)

    variants = {}
    for good in goods:
        for variant in good['variants']:
            try:
                variants[variant['sku']] = variant['id']
            except KeyError:
                continue
    if setup.DEBUG:
        setup.save_debug_file('variants.json', variants)
    return variants


if __name__ == '__main__':  # debug function
    get_variants()
