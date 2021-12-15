from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import xlsxwriter
from PIL import Image
from os import getcwd, remove
import info
import time


class InstagramBot:

    def __init__(self):
        self.driver = webdriver.Chrome(info.webdriver)
        self.driver.get('https://instagram.com')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.username = info.username
        self.password = info.password
        self.find_user = info.find_user
        self.action = ActionChains(self.driver)

    def login(self):
        try:
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
        except Exception:
            print("Wrong username/password pls try again")

    def search(self):
        try:
            _search = self.driver.find_element_by_css_selector('input[type="text"]')
            _search.send_keys(self.find_user)
            time.sleep(2)
            _search.send_keys(Keys.RETURN * 2)
        except Exception:
            print('user not found')

    def getInfo(self):
        output = []
        likes_comments = []
        final_result = []
        number = 0
        likes = []
        comments = []
        dates = []
        content = []
        required_size = (100, 100)
        number_of_posts = self.driver.find_element_by_css_selector('span[class="g47SY "]')
        print("total number of posts: " + number_of_posts.text)
        number += int(number_of_posts.text)
        account_name = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/header'
                                                         '/section/div[1]/h2').text
        followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/header/section'
                                                      '/ul/li[2]/a/span').text
        following = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/header/section'
                                                      '/ul/li[3]/a/span').text
        if number != 0:
            try:
                for i in range(int(number_of_posts.text)):
                    number_of_likes_and_comments = self.driver.find_elements_by_css_selector('div[class="_9AhH0"]')
                    self.action.move_to_element([i for i in number_of_likes_and_comments][i]).perform()
                    number_of_likes_and_comments = self.driver.find_element_by_css_selector('div[class="qn-0x"]')
                    likes_comments.append([number_of_likes_and_comments.text])
                for i in likes_comments:
                    for j in i:
                        final_result.append(j.split('\n'))
                for k, l in zip(final_result, range(number)):
                    likes.append(k[0])
                    comments.append(k[1])
                click_post = self.driver.find_element_by_css_selector('div[class="eLAPa"]')
                click_post.click()
                for i in range(number):
                    date = self.driver.find_element_by_css_selector('time[class="_1o9PC Nzb55"]')
                    dates.append([date.get_attribute('title')])
                    try:
                        description = self.driver.find_element_by_xpath('/html/body/div[6]/div['
                                                                        '2]/div/article/div/div[2]/div/div/div['
                                                                        '2]/div[1]/ul/div/li/div/div/div[2]/span')
                        content.append(description.text)
                    except Exception:
                        content.append('NO Description')
                    with open(f'Post{i + 1}.png', 'wb') as file:
                        img = self.driver.find_element_by_xpath(
                            '/html/body/div[6]/div[2]/div/article/div/div[1]/div/div')
                        file.write(img.screenshot_as_png)
                        time.sleep(1.5)
                    _next = self.driver.find_element_by_css_selector('div[class=" l8mY4 feth3"]'). \
                        find_element_by_css_selector('button[class="wpO6b  "]')
                    _next.click()
            except Exception:
                pass

            file = getcwd()
            for i in range(number):
                im = Image.open(f'{getcwd()}\\Post{i + 1}.png')
                im = im.resize(required_size, Image.ANTIALIAS)
                im.save(f'{getcwd()}\\resized_Post{i + 1}.png')

            workbook = xlsxwriter.Workbook(f'{account_name}.xlsx')
            worksheet = workbook.add_worksheet()
            format2 = workbook.add_format({'border': 2})
            format5 = workbook.add_format({'border': 5})
            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:B', 10)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 18)
            worksheet.set_column('E:E', 50)
            worksheet.write('A1', f'Account name: {account_name}', format2)
            worksheet.write('B1', f'Number of Posts: {number}', format2)
            worksheet.write('C1', f'Followers: {followers}', format2)
            worksheet.write('D1', f'Following: {following}', format2)
            worksheet.write('A2', 'Post-Image', format2)
            worksheet.write('B2', 'Likes', format2)
            worksheet.write('C2', 'Comments', format2)
            worksheet.write('D2', 'Date', format2)
            worksheet.write('E2', 'Description', format2)
            worksheet.set_default_row(120)
            for i in range(number):
                worksheet.insert_image(f'A{i + 3}', f'{getcwd()}/resized_Post{i + 1}.png')
                worksheet.write(f'B{i + 3}', likes[i], format2)
                worksheet.write(f'C{i + 3}', comments[i], format2)
                worksheet.write(f'D{i + 3}', dates[i][0], format2)
                worksheet.write(f'E{i + 3}', content[i], format2)
            workbook.close()
            for i in range(number):
                remove(f'{getcwd()}\\Post{i + 1}.png')
                remove(f'{getcwd()}\\resized_Post{i + 1}.png')
        else:
            print('No posts uploaded')


if __name__ == '__main__':
    bot = InstagramBot()
    bot.login()
    bot.search()
    bot.getInfo()
