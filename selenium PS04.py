from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class WikiNavigator:
    def __init__(self):
        # Изменяем инициализацию драйвера для Firefox
        self.driver = webdriver.Firefox()
        self.current_page = None
        self.paragraphs = []
        self.links = []

    def search_wikipedia(self, query):
        self.driver.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
        search_box = self.driver.find_element(By.ID, "searchInput")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        self._update_page_info()

    def _update_page_info(self):
        self.current_page = self.driver.current_url
        self.paragraphs = self.driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p")
        self.links = self.driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output a[href^='/wiki/']")

    def show_paragraphs(self):
        for i, p in enumerate(self.paragraphs[:5], 1):
            print(f"\nПараграф {i}:")
            print(p.text[:200] + "..." if len(p.text) > 200 else p.text)
            if i % 3 == 0:
                input("\nНажмите Enter для продолжения...")

    def show_links_menu(self):
        print("\nДоступные связанные статьи:")
        unique_links = list({link.text: link for link in self.links if link.text}.values())[:10]
        for i, link in enumerate(unique_links, 1):
            print(f"{i}. {link.text}")
        return unique_links

    def navigate(self):
        while True:
            print("\nТекущая статья:", self.driver.title)
            choice = input("\n1. Листать параграфы\n2. Перейти на связанную статью\n3. Выйти\nВыбор: ")

            if choice == '1':
                self.show_paragraphs()
            elif choice == '2':
                links = self.show_links_menu()
                link_choice = input("Введите номер статьи (или 0 для отмены): ")
                if link_choice.isdigit() and 0 < int(link_choice) <= len(links):
                    links[int(link_choice)-1].click()
                    time.sleep(2)
                    self._update_page_info()
            elif choice == '3':
                self.driver.quit()
                print("Программа завершена.")
                return
            else:
                print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    navigator = WikiNavigator()
    query = input("Введите ваш поисковый запрос: ")
    navigator.search_wikipedia(query)
    navigator.navigate()
