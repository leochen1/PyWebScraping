from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website = 'https://www.cpbl.com.tw/stats/recordall'
path = r'D:\Online Course\Udemy\PyWebScraping\chromedriver-win64\chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(website)

# 點擊按鈕
search_button = driver.find_element(By.XPATH, "//div[@class='btn']/input[@type='button' and @value='查詢']")
search_button.click()

# 等待表格資料載入且 tr 數量大於1
WebDriverWait(driver, 10).until(
    lambda d: len(d.find_elements(By.TAG_NAME, 'tr')) > 1
)

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
    except Exception as e:
        print(f"第{i}列發生錯誤: {e}")

driver.quit()