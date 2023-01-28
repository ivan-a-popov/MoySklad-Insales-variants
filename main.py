import moysklad
import insales
import setup


def make_index(stocks, variants):
    index = []
    for key, qty in stocks.items():
        try:
            variant_id = variants[key]
        except KeyError:
            setup.logger.warning(f"Article {key} not found in InSales.")
            continue
        else:
            index.append({"id": variant_id, "quantity": qty})
    setup.logger.debug(f"{len(index)} articles matched.")
    return index


if __name__ == '__main__':
    setup.logger.debug("Getting data from moysklad:")
    stocks = moysklad.get_goods()
    setup.logger.debug("Getting data from InSales")
    variants = insales.get_variants()
    setup.logger.debug("Preparing index of goods to update")
    index = make_index(stocks, variants)
    if setup.DEBUG:
        setup.save_debug_file('index.json', index)
    setup.logger.debug("Updating stocks in InSales")
    insales.update_stocks(index)
