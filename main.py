import datetime
from parsers import auchan_parser
from data import excel_writer
from tqdm import tqdm

from parsers.auchan_parser import count_pages_moscow, count_pages_spb


def get_data_moscow(url_first_page):
    count_pages_for_moscow = count_pages_moscow(url_first_page)

    list_all_product_msk = []

    page_for_msk = 1

    for _ in tqdm(range(count_pages_for_moscow), desc="Парсинг Москва"):
        url = f'{url_first_page}?page={page_for_msk}'
        list_product_moscow = auchan_parser.parse_product_moscow(url)
        list_all_product_msk.append(list_product_moscow)

        page_for_msk += 1

    return list_all_product_msk


def get_data_spb(url_first_page):
    count_pages_for_spb = count_pages_spb(url_first_page)

    list_all_product_spb = []

    page_for_spb = 1

    for _ in tqdm(range(count_pages_for_spb), desc="Парсинг Санкт-Петербург"):
        url = f'{url_first_page}?page={page_for_spb}'
        list_product_spb = auchan_parser.parse_product_spb(url)
        list_all_product_spb.append(list_product_spb)

        page_for_spb += 1

    return list_all_product_spb


def main():
    url_first_page = "https://www.auchan.ru/catalog/zamorozhennye-produkty/morozhenoe-deserty/"
    before_time = datetime.datetime.now()

    all_product_msk = get_data_moscow(url_first_page)
    all_product_spb = get_data_spb(url_first_page)

    result_list_product_msk = auchan_parser.create_result_list_for_location(all_product_msk)
    result_list_product_spb = auchan_parser.create_result_list_for_location(all_product_spb)

    data = {
        'Москва': result_list_product_msk,
        'Санкт-Петербург': result_list_product_spb
    }

    excel_filename = excel_writer.create_n_write_xlsx(data)
    after_time = datetime.datetime.now()

    result_time = after_time - before_time
    print(f"Время сбора данных: {result_time}")
    print(f"Результат записан в файл: {excel_filename}")


if __name__ == '__main__':
    main()
