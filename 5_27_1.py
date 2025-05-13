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

trs = driver.find_elements(By.TAG_NAME, 'tr')
for i in range(len(trs)):
    try:
        # 每次都重新抓 tr，避免 stale
        tr = driver.find_elements(By.TAG_NAME, 'tr')[i]
        print(tr.text)
    except Exception as e:
        print(f"第{i}列發生錯誤: {e}")

driver.quit()