import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

def select_date(year, month, day):
    # params: int year, int month, int day
    # return: void 
    # 处理网站中的日期选择框，选择一个日期
    Select(driver.find_element(By.ID, "calendarYear")).select_by_value(str(year)) # 2001 - 2014
    Select(driver.find_element(By.ID, "calendarMonth")).select_by_value(str(month - 1)) # 1 ~ 12

    date_ele = driver.find_element(By.ID, "calendarTable").find_elements(By.TAG_NAME, "td")

    for i in date_ele:
        if i.text == str(day):
            i.click()
            return

year = 0
month = 0
day = 0
type = ""

try:
    year = int(sys.argv[1][:4])
    month = int(sys.argv[1][4:6])
    day = int(sys.argv[1][6:])
    type = sys.argv[2]
except Exception:
    raise ValueError("invalid arguments")

driver = webdriver.Chrome()


# 访问货币代号网站，并将输入的货币代号转为中文
driver.get("https://www.11meigui.com/tools/currency")

temp = driver.find_element(By.ID, "desc").find_elements(By.TAG_NAME, "tr")
for row in temp:
    eles = row.find_elements(By.TAG_NAME, "td")
    if len(eles) != 6:
        continue
    if eles[4].text[:] == type:
        type = eles[1].text[:]
        break 

print(year, month, day, type)

# 访问中国银行外汇网站
driver.get("https://www.boc.cn/sourcedb/whpj/")

# 获取选择开始日期和结束日期的元素
temp = driver.find_elements(By.CLASS_NAME, "search_ipt")
start_date_ele = temp[1]
end_date_ele = temp[2]

# 选择开始和结束日期
try:
    start_date_ele.click()
    select_date(year, month, day)

    end_date_ele.click()
    select_date(year, month, day)
except Exception:
    raise ValueError("invalid date")

# 选择货币种类
try:
    Select(driver.find_element(By.ID, "pjname")).select_by_value(type)
except Exception:
    raise ValueError("invalid currency type")

# 发送查询请求，跳转到下一页面
driver.find_elements(By.CLASS_NAME, "search_btn")[1].click()

# 获取表中第一个现汇卖出价
try:
    res = driver.find_element(By.CLASS_NAME, "odd").find_elements(By.TAG_NAME, "td")[4].text
except Exception:
    raise ValueError("not found")

# 打印结果，并写入文件
print(res)
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write(f"{year}.{month}.{day}, {type}, {res}\n")