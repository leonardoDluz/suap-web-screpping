from abc import abstractmethod, ABC
from selenium import webdriver
from selenium.webdriver.common.by import By
from ..dtos.suap_login_dto import SuapLoginDTO


class Suap(ABC):
    def __init__(self, suap_login_info: SuapLoginDTO) -> None:
        self._username = suap_login_info.username
        self._password = suap_login_info.password

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self._driver = webdriver.Chrome(options=options)

    @abstractmethod
    def get_content(self) -> dict:
        pass

    def _login(self) -> None:
        driver = self._driver
        driver.get("https://suap.ifsp.edu.br/accounts/login/?next=/")

        username_input = driver.find_element(By.ID, "id_username")
        username_input.send_keys(self._username)

        password_input = driver.find_element(By.ID, "id_password")
        password_input.send_keys(self._password)

        submit_input = driver.find_element(
            By.XPATH, '//*[@id="login"]/form/div[5]/input'
        )
        submit_input.click()
