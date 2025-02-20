import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)  # Неявное ожидание всех элементов
    driver.set_window_size(1920, 1080)

    # Переход на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver
    driver.quit()


@pytest.fixture
def login(driver):
    """Фикстура для авторизации пользователя"""
    driver.find_element(By.ID, 'email').send_keys('dambieva1908@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('190810')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Ожидание загрузки главной страницы
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends")
    )


def test_show_all_pets(driver, login):
    """Тест проверки входа в аккаунт"""
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"


def test_pets_cards(driver, login):
    """Тест: проверка карточек питомцев (фото, имя, описание)"""

    # Переход на страницу "Мои питомцы"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@href='/my_pets']"))).click()

    # Получаем все карточки питомцев
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != '', f"❌ Фото отсутствует у питомца №{i + 1}"
        assert names[i].text != '', f"❌ Отсутствует имя у питомца №{i + 1}"
        assert descriptions[i].text != '', f"❌ Отсутствует описание у питомца №{i + 1}"

        # Ожидание, что описание содержит возраст и породу
        assert ', ' in descriptions[i].text, f"❌ Описание питомца №{i + 1} некорректное"
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0, f"❌ Отсутствует порода у питомца №{i + 1}"
        assert len(parts[1]) > 0, f"❌ Отсутствует возраст у питомца №{i + 1}"


def test_pets_table(driver, login):
    """Тест: проверка таблицы питомцев (имена, породы, возраст)"""

    # Переход на страницу "Мои питомцы"
    my_pets_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@href='/my_pets']"))
    )
    my_pets_link.click()

    # Ожидание загрузки таблицы питомцев
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody'))
    )

    # Ожидание всех строк таблицы
    pets_count = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr'))
    )

    pets_data = []
    for pet in pets_count:
        name = WebDriverWait(pet, 5).until(EC.presence_of_element_located((By.XPATH, './td[1]'))).text.strip()
        breed = WebDriverWait(pet, 5).until(EC.presence_of_element_located((By.XPATH, './td[2]'))).text.strip()
        age = WebDriverWait(pet, 5).until(EC.presence_of_element_located((By.XPATH, './td[3]'))).text.strip()

        assert name != '', f"❌ Отсутствует имя у питомца"
        assert breed != '', f"❌ Отсутствует порода у питомца"
        assert age != '', f"❌ Отсутствует возраст у питомца"

        pets_data.append((name, breed, age))

    # Проверка уникальности питомцев
    pet_counter = {}
    for pet in pets_data:
        pet_counter[pet] = pet_counter.get(pet, 0) + 1

    duplicates = {pet: count for pet, count in pet_counter.items() if count > 1}

    assert not duplicates, f"❌ Обнаружены дублирующиеся питомцы: {duplicates}"


def test_pets_have_unique_names(driver, login):
    """Тест: проверка уникальности имен питомцев"""

    # Переход на страницу "Мои питомцы"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@href='/my_pets']"))).click()

    # Ожидание загрузки списка питомцев
    names = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]'))
    )

    # Проверка на уникальность
    names_texts = [name.text.strip() for name in names]
    assert len(names_texts) == len(set(names_texts)), f"❌ Найдены дублирующиеся имена: {names_texts}"


def test_no_duplicate_pets(driver, login):
    """Тест: проверка отсутствия дубликатов питомцев"""

    # Переход на страницу "Мои питомцы"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@href='/my_pets']"))).click()

    # Ожидание загрузки таблицы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody')))

    # Собираем данные о питомцах
    pets_count = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr'))
    )

    pets_data = []
    for pet in pets_count:
        name = pet.find_element(By.XPATH, './td[1]').text.strip()
        breed = pet.find_element(By.XPATH, './td[2]').text.strip()
        age = pet.find_element(By.XPATH, './td[3]').text.strip()

        if name and breed and age:
            pets_data.append((name, breed, age))

    # Проверка уникальности данных питомцев
    pet_counter = {}
    for pet in pets_data:
        pet_counter[pet] = pet_counter.get(pet, 0) + 1

    duplicates = {pet: count for pet, count in pet_counter.items() if count > 1}

    assert not duplicates, f"❌ Найдены дублирующиеся питомцы: {duplicates}"
