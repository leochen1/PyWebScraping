from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.support.ui import Select
import time

website = 'https://www.cpbl.com.tw/stats/recordall'
path = r'D:\Online Course\Udemy\PyWebScraping\chromedriver-win64\chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(website)

# 下拉選單選擇
dropdown = Select(driver.find_element_by_id('Position')).select_by_visible_text('投手成績')

time.sleep(3)

# 點擊按鈕
search_button = driver.find_element(By.XPATH, "//div[@class='btn']/input[@type='button' and @value='查詢']")
search_button.click()

# 等待表格資料載入且 tr 數量大於1
WebDriverWait(driver, 10).until(
    lambda d: len(d.find_elements(By.TAG_NAME, 'tr')) > 1
)

players, avgs, games_list, pas = [], [], [], []

# 重新抓 tr，每次都即時抓 td，避免 stale
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
    except Exception as e:
        print(f"第{i}列發生錯誤: {e}")

# 存檔 csv
df = pd.DataFrame({
    'player': players,
    'avg': avgs,
    'games': games_list,
    'pa': pas
})

df.to_csv('player_score.csv', index=False)

driver.quit()

