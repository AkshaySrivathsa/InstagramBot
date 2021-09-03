from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import info
import time
number = 0


class InstagramBot:

    def __init__(self):
        self.driver = webdriver.Chrome('/home/akshay/Downloads/chromedriver')
        self.driver.get('https://instagram.com')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.username = info.username
        self.password = info.password
        self.find_user = info.find_user

    def login(self):
        user_name = self.driver.find_element_by_css_selector('input[name="username"]')
        user_name.send_keys(self.username)
        user_password = self.driver.find_element_by_css_selector('input[name="password"]')
        user_password.send_keys(self.password)
        submit = self.driver.find_element_by_css_selector('button[type="submit"]')
        submit.click()
        time.sleep(5)
        not_now1 = self.driver.find_element_by_css_selector('button[class="sqdOP yWX7d    y3zKF     "]')
        not_now1.click()
        not_now2 = self.driver.find_element_by_css_selector('button[class="aOOlW   HoLwm "]')
        not_now2.click()

    def search(self):
        _search = self.driver.find_element_by_css_selector('input[type="text"]')
        _search.send_keys(self.find_user)
        time.sleep(2)
        _search.send_keys(Keys.RETURN * 2)
        number_of_posts = self.driver.find_element_by_css_selector('span[class="g47SY "]')
        global number
        number = int(number_of_posts.text)

    def likeAndComment(self):
        try:
            click_post = self.driver.find_element_by_css_selector('div[class="eLAPa"]')
            click_post.click()
            time.sleep(2)
            for i in range(number):
                like = self.driver.find_element_by_css_selector('span[class="fr66n"]')
                like.click()
                if i == 0:
                    comment = self.driver.find_element_by_css_selector('textarea[class="Ypffh"]')
                    comment.click()
                    comment = self.driver.find_element_by_css_selector('textarea[class="Ypffh focus-visible"]')
                    comment.send_keys("Great post! Make sure to check out my account "
                                      "and make sure to follow my account"
                                      " also Dont forget Leave a like on my posts")
                    comment.send_keys(Keys.RETURN)
                _next = self.driver.find_element_by_css_selector('a[class=" _65Bje  coreSpriteRightPaginationArrow"]')
                _next.click()
        except Exception:
            print("user has not posted anything")


if __name__ == '__main__':
    bot = InstagramBot()
    bot.login()
    bot.search()
    bot.likeAndComment()
