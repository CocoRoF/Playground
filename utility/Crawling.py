import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# 크롤링 유틸
# str 또는 list 형태의 url을 입력받아 처리함.
# str 형태의 경우 str을 리턴하며, list 형태의 경우 값이 포함된 list를 리턴함

class Norm_Crawler():
    """
    After Select Selection, Every Items' Form Should be SAME. \n
    Every Item will be saved as 'STR'type. \n 
    .\n
    If insert An ULR, return A STR. \n
    If insert list of ULRs, return List of STRs.
    """
    
    def __init__(self, url: str|list, headless=True, sleep_time=1):
        self.url = url
        self.chrome_options = Options()
        if headless==True:
            self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        
        if type(self.url) == str:
            self.driver.get(self.url)
            time.sleep(sleep_time)
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
        if type(self.url) == list:
            self.soup = []
            for url in self.url:
                self.driver.get(url)
                time.sleep(sleep_time)
                temp_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                self.soup.append(temp_soup)
    
    # Beautiful Soup로 파싱한 데이터 출력    
    def show_soup(self):        
        if type(self.url) == str:
            return self.soup
        
        if type(self.url) == list:
            return self.soup

    # Soup.select Method를 통해 특정 부분 선택
    def select_soup(self, selection: str, show=False):
        if type(self.url) == str:
            self.item = self.soup.select(selection)
            if show == True:
                return self.item      

        if type(self.url) == list:
            self.item = []
            for soup in self.soup:
                temp_item = soup.select(selection)
                self.item.append(temp_item)
            
            if show == True:
                return self.item
    
    def Data_check(self):
        for i in self.item:
            print(i)
    
    # Str Cutting. start Str와 End Str 사이에 있는 데이터를 출력함. 이 때 start str과 end str은 고유해야 할 것. (이 값을 토대로, 문장이 둘로 나뉘어야 함)
    def cutting(self, start_str: str, end_str: str, show=False):
        if type(self.url) == str:
            self.str_result = []
            for text in self.item:
                text = str(text)
                text = text.split(start_str)
                if len(text) == 2:
                    text = text[1]
                else:
                    print('Split Error, Result Length = {}, Need to Check start_str' .format(len(text)))
                text = text.split(end_str)    
                if len(text) == 2:
                    text = text[0]
                else:
                    print('Split Error, Result Length = {}, Need to Check end_str' .format(len(text)))
                self.str_result.append(text)
                
            print('Cutting Done. Data Length = {}' .format(len(self.str_result)))
            if show == True:
                return self.str_result
            
        if type(self.url) == list:
            self.str_result = []
            for item in self.item:
                temp_result = []
                for text in item:
                    text = str(text)
                    text = text.split(start_str)
                    if len(text) == 2:
                        text = text[1]
                    else:
                        print('Split Error, Result Length = {}, Need to Check start_str' .format(len(text)))
                    text = text.split(end_str)    
                    if len(text) == 2:
                        text = text[0]
                    else:
                        print('Split Error, Result Length = {}, Need to Check end_str' .format(len(text)))
                    temp_result.append(text)    
                self.str_result.append(temp_result)
                    
                print('Cutting Done. Number of Dataset = {}' .format(len(self.str_result)))
                if show == True:
                    return self.str_result