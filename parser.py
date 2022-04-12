import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import time
import csv


# def test_request(url, retry=5): headers = { "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,
# image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "user-agent": "Mozilla/5.0 (
# X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36" }
#
#     try:
#         response = requests.get(url=url, headers=headers)
#         print(f"[+] {url} {response.status_code}")
#     except Exception as ex:
#         time.sleep(3)
#         if retry:
#             print(f"[INFO] retry={retry} => {url}")
#             return test_request(url, retry=(retry - 1))
#         else:
#             raise
#     else:
#         return response


def get_source_html():
    service = Service(r'C:\Users\msi\PycharmProjects\kino\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options,
                              service=service)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    # films_url_list = []
    # url = "https://www.kinopoisk.ru/lists/movies/popular-films/?page=1"
    # driver.get(url)
    # time.sleep(5)
    # driver.quit()

    #
    # 
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(
    #     service=service
    # )
    # driver.maximize_window()

    films_url_list = []
    with open('films.csv', 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file)
        writer.writerow((
            'name', 'year', 'country', 'genre', 'director', 'rating'
        ))

    with open('films.txt') as file:
        films = file.readlines()
    for url in films:
        try:
            driver.get(url=url)
            time.sleep(15)
            response = driver.page_source
            soup = BeautifulSoup(response, 'lxml')

            try:
                name = soup.find('h1',
                                 class_='styles_title__3eC_X styles_root__33Zsw styles_root__16Q7H styles_rootInLight__1kpWr').find(
                    'span').text
                name = name[:-7]
            except Exception:
                name = soup.find('h1',
                                 class_='styles_title__3eC_X styles_root__33Zsw styles_root__16Q7H styles_rootInDark__2yuxZ').find(
                    'span').text
                name = name[:-7]

            try:
                year = soup.find_all('div', class_='styles_rowDark__1Nmd2 styles_row__Rg4Gz')[0].find('a', {
                    'class': 'styles_linkDark__Vwdrd styles_link__29O_P'}).text
            except Exception:
                year = soup.find_all('div', class_='styles_rowLight__3xIw3 styles_row__Rg4Gz')[0].find('a', {
                    'class': 'styles_linkLight__58PB8 styles_link__29O_P'}).text

            try:
                countries_html = soup.find_all('div', class_='styles_rowDark__1Nmd2 styles_row__Rg4Gz')[1].find_all('a',
                                                                                                                    {
                                                                                                                        'class': 'styles_linkDark__Vwdrd styles_link__29O_P'})
            except Exception:
                countries_html = soup.find_all('div', class_='styles_rowLight__3xIw3 styles_row__Rg4Gz')[1].find_all(
                    'a', {
                        'class': 'styles_linkLight__58PB8 styles_link__29O_P'})
            # country = [i.text for i in countries_html]
            countries = []
            for i in countries_html:
                countries.append(i.text)
            country = ', '.join(countries)

            try:
                genres = soup.find('div',
                                   class_='styles_valueDark__2w72W styles_value__1tR_i styles_root__14D2m').find_all(
                    'a', class_='styles_linkDark__Vwdrd styles_link__29O_P')
            except Exception:
                genres = soup.find('div',
                                   class_='styles_valueLight__1CXJr styles_value__1tR_i styles_root__14D2m').find_all(
                    'a', class_='styles_linkLight__58PB8 styles_link__29O_P')
            # genre = [i.text for i in genres]
            genre_list = []
            for i in genres:
                genre_list.append(i.text)
            genre = ', '.join(genre_list)

            try:
                directors_html = soup.find_all('div', class_='styles_rowDark__1Nmd2 styles_row__Rg4Gz')[4].find_all('a',
                                                                                                                    class_='styles_linkDark__Vwdrd styles_link__29O_P')
            except Exception:
                directors_html = soup.find_all('div', class_='styles_rowLight__3xIw3 styles_row__Rg4Gz')[
                    4].find_all('a', class_='styles_linkLight__58PB8 styles_link__29O_P')

            # director = [i.text for i in directors_html]
            directors_list = []
            for i in directors_html:
                directors_list.append(i.text)
            director = ', '.join(directors_list)

            try:
                rating = soup.find('span', class_='styles_value__3ena4').find('span').text
            except Exception:
                rating = '0'
            with open('films.csv', 'a', encoding='cp1251', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (name, year, country, genre, director, rating)
                )

            # director = soup.find('a', class_='base-movie-main-info_link__3BnCh')
            # age_restrictions = soup.find('a', class_='base-movie-main-info_link__3BnCh')

            # for film in films:
            #     film_url = 'https://www.kinopoisk.ru'+film.get('href')
            #     films_url_list.append(film_url)
            #
            # with open('films_url_list.txt', 'a') as file:
            #     for item in films_url_list:
            #         file.write(f'{item}\n')

        # driver.find_elements(By.CLASS_NAME('base-movie-main-info_link__3BnCh'))

        except Exception as ex:
            print(ex)

    driver.close()
    driver.quit()


def main():
    get_source_html()

    # for i in range(1, 21):
    # url = f'https://www.kinopoisk.ru/lists/movies/popular-films/?page=3'
    # headers = {
    #     'accept': '* / *',
    #     'user-agent': 'Mozilla/5.0 '
    #                   '(Windows NT 10.0; Win64; x64) '
    #                   'AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 '
    #                   'Yowser/2.5 Safari/537.36'}

    # films_url_list = []

    # q = requests.get(url, headers)
    # response = q.content
    # src = q.text
    #
    # with open('index_list.html', 'w', encoding='utf-8') as file:
    #     file.write(src)

    # soup = BeautifulSoup(response, 'lxml')
    # films = soup.find_all('a', class_='base-movie-main-info_link__3BnCh')
    #
    # for film in films:
    #     film_url = 'https://www.kinopoisk.ru'+film.get('href')
    #     films_url_list.append(film_url)
    #
    # with open('films_url_list2.txt', 'a') as file:
    #     for item in films_url_list:
    #         file.write(f'{item}\n')


if __name__ == '__main__':
    main()
