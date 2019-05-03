from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium import webdriver
import time, bs4, re, os

username = "username"
password = "password"
address = "https://e-learning.pcz.pl/mod/hvp/view.php?id=10713"  # change id

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

browser = webdriver.Chrome(chrome_options=options)
browser.get(address)

usernameEle = browser.find_element_by_id('username')
passwordEle = browser.find_element_by_id('password')

usernameEle.send_keys(username)
passwordEle.send_keys(password)
passwordEle.submit()

pageHtml = browser.page_source
# print(html)
htmlSoup = bs4.BeautifulSoup(pageHtml, features="html.parser")
js = htmlSoup.select('script[type="text/javascript"]')
# print(js[1].getText())
quizHtml = js[1].getText()

wait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it("h5p-iframe-47"))
inputBoxes = browser.find_elements_by_class_name('h5p-text-input')
buttons = browser.find_elements_by_class_name('h5p-progressbar-part-has-task')
summary = browser.find_element_by_class_name('progressbar-part-summary-slide')

reg = re.compile(r"(\*)([\/\\()_\dA-Za-z&;.<>!-]+[ \/\\()_\dA-Za-z&;,.<>!-]{0,})(: [a-z]+\?)?(\*)")
matches = reg.findall(quizHtml)  # list with 3 groups ['*', 'answer', '*']
answers = []  # not formatted answer
formAnswers = []  # formatted answers
readyAnswers = []  # formatted answers without other options
temp = []  # because something broke
for i in range(len(matches)):
    answers.append(matches[i][1])
    temp.append(answers[i])
    formAnswers.append(temp[i].encode('utf-8').decode("unicode_escape").encode('utf-8').decode("unicode_escape").replace(r'\/', '  |lub|  '))  # I couldnt find a proper way

# creating txt file for classmates
if(not os.path.exists('answers')):
    os.makedirs('answers')

file = open('./answers/answers.txt', 'w')

for answer in formAnswers:
    file.write(answer + "\n")

file.close()
# ----------------------------

for i in range(len(formAnswers)):
    readyAnswers.append(re.sub(r"  \|lub\|.*", "", formAnswers[i]))

j = 0
for i in range(len(readyAnswers)):
    inputBoxes = browser.find_elements_by_class_name('h5p-text-input')
    try:
        inputBoxes[i].send_keys(readyAnswers[i])
        # time.sleep(0.1)
    except:  # whats the error name ? I have no idea
        buttons[j].click()
        j += 1
        time.sleep(0.5)
        inputBoxes[i].send_keys(readyAnswers[i])

summary.click()
time.sleep(3)
browser.close()
