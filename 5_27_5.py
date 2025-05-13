from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.support.ui import Select
import time
import random
from selenium.webdriver.chrome.options import Options

### 添加有反爬蟲機制的網頁處理方式

website = 'https://www.cpbl.com.tw/stats/recordall'
path = r'D:\Online Course\Udemy\PyWebScraping\chromedriver-win64\chromedriver.exe'

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
driver = webdriver.Chrome(path, options=options)
driver.get(website)

# 下拉選單選擇
Select(driver.find_element(By.ID, 'Position')).select_by_visible_text('投手成績')
time.sleep(random.uniform(1, 3))

# 點擊按鈕
search_button = driver.find_element(By.XPATH, "//div[@class='btn']/input[@type='button' and @value='查詢']")
search_button.click()
time.sleep(random.uniform(1, 3))

# 等待表格資料載入且 tr 數量大於1
WebDriverWait(driver, 10).until(
    lambda d: len(d.find_elements(By.TAG_NAME, 'tr')) > 1
)

players, avgs, games_list, pas = [], [], [], []

trs = driver.find_elements(By.TAG_NAME, 'tr')
for i in range(len(trs)):
    try:
        tds = driver.find_elements(By.TAG_NAME, 'tr')[i].find_elements(By.TAG_NAME, 'td')
        if len(tds) >= 5:
            player = tds[0].text
            avg = tds[1].text
            games = tds[2].text
            pa = tds[3].text
            print(player, avg, games, pa)
            players.append(player)
            avgs.append(avg)
            games_list.append(games)
            pas.append(pa)
        time.sleep(random.uniform(0.5, 1.5))  # 每列間也可加隨機等待
    except Exception as e:
        print(f"第{i}列發生錯誤: {e}")

df = pd.DataFrame({
    'player': players,
    'avg': avgs,
    'games': games_list,
    'pa': pas
})

df.to_csv('player_score.csv', index=False)
driver.quit()