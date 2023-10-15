import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pars_auchan(text):
    """Парсит данные с сайта Auchan
    :param text: html страницы с товарами
    """
    product_list_result = []

    soup = BeautifulSoup(text, 'html.parser')

    all_card_products = soup.find('div', class_='css-3nngaf-Layout')

    if all_card_products:
        elements_inside_div = all_card_products.find_all('div', class_='css-n9ebcy-Item')
        for card_product in elements_inside_div:
            if "Нет в наличии" in card_product.get_text():
                continue
            # Получаем id продукта
            id_product = card_product['data-offer-id']

            article = card_product.find('article')
            script = article.find('script')

            # Получить текстовое содержимое тега script
            json_script_data = script.string
            # Распарсить JSON-данные
            data_script_dict = json.loads(json_script_data)

            # Получаем название продукта
            name = data_script_dict["name"]

            # Получаем бренд продукта
            brand = data_script_dict["brand"]

            link = card_product.find('a', class_='productCardPictureLink')['href']
            link_product = "https://www.auchan.ru" + link

            product_price = card_product.find('div', class_='productCardPriceData')
            promo_price = product_price.find('div', class_='active css-xtv3eo')
            regular_price = product_price.find('div', class_='active css-1hxq85i')

            if promo_price:
                promo_price = promo_price.get_text(strip=True).split("C")[0]

            if regular_price is not None:
                regular_price = regular_price.get_text()
            else:
                regular_price = promo_price
                promo_price = None

            product_list = [id_product, name, link_product, regular_price, promo_price, brand]
            product_list_result.append(product_list)

    return product_list_result


def get_html_for_moscow(url):
    """Достаёт html страницы с товарами для Москвы
    :param url: url адрес товаров
    """
    the_path = 'chromedriver/chromedriver.exe'
    driver = uc.Chrome(driver_executable_path=the_path)
    driver.get(url)
    # time.sleep(10)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/main/div/div/div[3]')))
    text = driver.page_source

    driver.close()
    driver.quit()

    return text


def get_html_for_spb(url):
    """Достаёт html страницы с товарами для Санкт-Петербурга
    :param url: url адрес товаров
    """
    the_path = 'chromedriver/chromedriver.exe'
    driver = uc.Chrome(driver_executable_path=the_path)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    # time.sleep(5)
    wait.until(EC.presence_of_element_located((By.ID, 'currentRegionName')))

    button = driver.find_element(By.ID, value='currentRegionName')
    button.click()
    # time.sleep(5)
    wait.until(EC.presence_of_element_located((By.ID, 'regions')))

    select_element = driver.find_element(By.ID, value='regions')
    select = Select(select_element)

    select.select_by_value('2')

    button_save = driver.find_element(By.CSS_SELECTOR, value='#selectShop')

    action_chains = ActionChains(driver)
    # Навести курсор на элемент
    action_chains.move_to_element(button_save).perform()
    # Выполнить клик
    action_chains.click().perform()

    # Дождитесь изменения контента (здесь ждем 10 секунд, можно изменить по необходимости)
    # wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/main/div/div/div[2]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/main/div/div/div[3]')))

    driver.get(url)

    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/main/div/div/div[2]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/main/div/div/div[3]')))

    text = driver.page_source

    driver.close()
    driver.quit()

    return text


def parse_product_moscow(url_page):
    text = get_html_for_moscow(url_page)
    return pars_auchan(text)


def parse_product_spb(url_page):
    text = get_html_for_spb(url_page)
    return pars_auchan(text)


def create_result_list_for_location(list_for_location):
    """Соединяет все списки в результирующий список для записи в .xlsx файл
    :param list_for_location: список со списками товаров
    """
    result_list_product = [
        ["id товара из сайта", "наименование", "ссылка на товар", "регулярная цена", "промо цена", "бренд"],
    ]

    for list_res in list_for_location:
        for li in list_res:
            result_list_product.append(li)

    return result_list_product


def count_pages_moscow(url):
    """Считает количество страниц в категории в Москве
    :param url: url адрес товаров
    """
    text = get_html_for_moscow(url)

    soup = BeautifulSoup(text, 'html.parser')

    pagination = soup.find('div', class_='css-zq55uw')
    ul = pagination.find('ul')
    all_li = ul.find_all('li')
    count_pages = len(all_li) - 1
    print(count_pages)
    return count_pages


def count_pages_spb(url):
    """Считает количество страниц в категории в Санкт-Петербурге
    :param url: url адрес товаров
    """
    text = get_html_for_spb(url)

    soup = BeautifulSoup(text, 'html.parser')

    pagination = soup.find('div', class_='css-zq55uw')
    ul = pagination.find('ul')
    all_li = ul.find_all('li')
    count_pages = len(all_li) - 1
    print(count_pages)
    return count_pages
