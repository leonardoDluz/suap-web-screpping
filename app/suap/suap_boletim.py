import time
from selenium.webdriver.common.by import By
from ..dtos.suap_login_dto import SuapLoginDTO
from .suap import Suap
import pandas as pd


class SuapBoletim(Suap):
    def __init__(self, suap_login_info: SuapLoginDTO) -> None:
        super().__init__(suap_login_info)

    def get_content(self, period: str) -> dict:
        self._login()
        driver = self._driver

        time.sleep(1)
        driver.get(f"https://suap.ifsp.edu.br/edu/aluno/{self._username}/?tab=boletim")

        self.__select_period(period)
        return self.__get_table()

    def __select_period(self, period: str) -> None:
        try:
            driver = self._driver
            time.sleep(1)

            # period_select = driver.find_element(By.ID, "ano_periodo")
            period_options = driver.find_elements(By.TAG_NAME, "option")

            for op in period_options:
                if op.text == period:
                    op.click()

        except Exception as e:
            print(e)

    def __get_table(self) -> list[dict]:
        try:
            driver = self._driver
            time.sleep(1)

            table_df = pd.read_html(driver.page_source)[1]
            table_df = self.__sanitize_table(table_df)
            # table_dict_list = self.__to_dict(table_df)
            # print(table_dict_list)  

            return table_df.to_dict('split', index=False)

        except Exception as e:
            print(e)

    def __sanitize_table(self, table_df: pd.DataFrame) -> pd.DataFrame:
        try:
            table_df.drop(
                [
                    "Diário",
                    "Opções",
                    ("NAF", "N"),
                    ("NAF", "F"),
                    ("Unnamed: 22_level_0", "Unnamed: 22_level_1"),
                    ("Unnamed: 23_level_0", "Unnamed: 23_level_1"),
                    ("Unnamed: 24_level_0", "Unnamed: 24_level_1"),
                    ("Unnamed: 25_level_0", "Unnamed: 25_level_1"),
                    ("Unnamed: 26_level_0", "Unnamed: 26_level_1"),
                    ("Unnamed: 27_level_0", "Unnamed: 27_level_1"),
                ],
                axis=1,
                inplace=True,
            )

            last_index = table_df.index[-1]
            table_df.drop(last_index, axis=0, inplace=True)
            return table_df

        except Exception as e:
            print(e)

    


