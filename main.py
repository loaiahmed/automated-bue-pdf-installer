# import requests
# from bs4 import BeautifulSoup

# with open('testWeb.html', 'r') as html_file:
#     content = html_file.read();
#     # print(content)
#     soup = BeautifulSoup(content, 'html.parser')
#     tags = soup.find_all('tr')
#     print(tags)
#     print(soup.getText())

payload = {
    'username': 'loay222929',
    'password': 'ahl21tc9'
}

# Use 'with' to ensure the session context is closed after use.
# with requests.Session() as s:
#     res = s.get('https://learn1.bue.edu.eg/login/index.php')
#     signin = BeautifulSoup(res._content, 'html.parser')
#     inputs = signin.find_all('input')
#     for tag in inputs:
#         # print(tag.attrs)
#         if tag.attrs['name'] == 'logintoken':
#             payload['logintoken'] = tag.attrs['value']
#             break
#     print(payload)
#     p = s.post('https://learn1.bue.edu.eg/login/index.php', data=payload)

    
#     dashboard = BeautifulSoup(p.content, 'html.parser')
    
#     courses = dashboard.find('ul', class_= 'list-group')
    # print(courses)
    # buttons = courses.find_all('a')
    # courses = dashboard.find_all('li', class_= 'list-group-item course-listitem')
    # print(buttons)
    # for course in courses:
    #     print(course.find('div', class_= 'col-md-6 p-0 d-flex align-items-center'))

import os
from selenium import webdriver


download_dir = r"C:\Users\LoaiSalem9\Documents\CODE\Python\automated-bue-pdf-installer\testing"
# profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
#                "download.default_directory": download_dir , "download.extensions_to_open": "applications/pdf"}
# options = webdriver.ChromeOptions()
# options.add_experimental_option("prefs", profile)

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": download_dir, #Change default directory
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})

driver = webdriver.Chrome(executable_path=r'C:\Users\LoaiSalem9\Documents\CODE\Python\chromedriver-win64\chromedriver.exe', options=options)
driver.get('https://learn1.bue.edu.eg/login/index.php')
driver.maximize_window()

driver.implicitly_wait(3)

title = driver.title
print(title)
usernameEntry = driver.find_element_by_id('username')
passwordEntry = driver.find_element_by_id('password')
loginbtn = driver.find_element_by_id('loginbtn')

usernameEntry.send_keys(payload['username'])
passwordEntry.send_keys(payload['password'])
loginbtn.click()

driver.implicitly_wait(3)

courses = driver.find_elements_by_xpath("//div[@class='col-md-6 d-flex align-items-center']/div/a")
for i in range(len(courses)):       # searching twice i know inefficent i hate it too but it works so ye fuck it
    driver.implicitly_wait(3)
    courses = driver.find_elements_by_xpath("//div[@class='col-md-6 d-flex align-items-center']/div/a")
    
    download_path = download_dir+ "\\" + courses[i].text.replace("\n", "=")
    os.mkdir(download_path)
    params = { 'behavior': 'allow', 'downloadPath': download_path }
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

    courses[i].click()
    # print("courses loop: " + str(i) + ", " + str(len(courses)))

    driver.implicitly_wait(3)


    # going through weeks...
    # weeks = driver.find_elements_by_partial_link_text("WEEK")
    weeks = driver.find_elements_by_xpath("//ul[@id='multi_section_tiles']/li/a/div/span/h3")
    for j in range(len(weeks)):     # doing it again i know but again it fucking works
        driver.implicitly_wait(3)
        # weeks = driver.find_elements_by_partial_link_text("WEEK")
        weeks = driver.find_elements_by_xpath("//ul[@id='multi_section_tiles']/li/a/div/span/h3")
        weeks[j].click() 
        
        print("weeks loop: " + str(j) + ", " + str(len(weeks)))
        driver.implicitly_wait(3)


        #installing pdfs here...
        materials = driver.find_elements_by_xpath("//ul/li/div/div/a/img[@src='https://learn1.bue.edu.eg/theme/image.php/adaptable/core/1695034957/f/pdf-24' or @src='https://learn1.bue.edu.eg/theme/image.php/adaptable/core/1695034957/f/powerpoint-24']")
        if materials:
            for material in materials:
                driver.implicitly_wait(3)
                try:
                    material.click()
                except:
                    print("didn't work")
        driver.refresh()
        driver.implicitly_wait(3)
        try: 
            courseHome = driver.find_element_by_xpath("//i[@title='Course home']")
            courseHome.click()
        except:
            driver.back()
            print("backed")
        # driver.implicitly_wait(3)
    
    driver.refresh()
    driver.implicitly_wait(3)
    # driver.execute_script("window.history.go(-1)")
    # dashboard = driver.find_element_by_link_text("Dashboard")
    dashboard = driver.find_element_by_xpath("//div[@id='main-navbar']/div/div/nav/ul/li/a[@title='Dashboard']/i")
    dashboard.click()

driver.quit()