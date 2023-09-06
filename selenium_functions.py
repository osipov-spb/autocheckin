from time import sleep

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import telegram_url, chat_main_url, chat_id


def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver# chrome_options=chrome_options


def auth_user(user, pass_code=''):
    step_1_success = False
    step_2_success = False
    step_3_success = False

    if pass_code == '':
        user.driver.get(telegram_url)

        # step 1 log in with phone button
        try_counter = 10
        while try_counter > 0 and not step_1_success:
            try:
                user.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/button').click()
                step_1_success = True
                break
            except:
                pass

            try:
                user.driver.find_element(By.CLASS_NAME, 'c-ripple').click()
                step_1_success = True
                break
            except:
                pass

            sleep(1)
            if try_counter == 1:
                break
            try_counter = try_counter - 1

        if not step_1_success:
            return step_1_success

        # step 2 enter phone number
        try_counter = 10
        while try_counter > 0 and not step_2_success:
            try:
                phone_field = user.driver.find_element(By.XPATH,
                                                       '//*[@id="auth-pages"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]')

                it = 30
                while it > 0:
                    phone_field.send_keys('\ue003')
                    sleep(0.05)
                    it = it - 1

                for letter in user.phone_number:
                    phone_field.send_keys(letter)
                    sleep(0.1)

                step_2_success = True
                break
            except:
                pass

            try:
                phone_field = user.driver.find_element(By.XPATH,
                                                       '/html/body/div[2]/div/div[1]/div/div/form/div[2]/input')

                it = 30
                while it > 0:
                    phone_field.send_keys('\ue003')
                    sleep(0.05)
                    it = it - 1

                for letter in user.phone_number:
                    phone_field.send_keys(letter)
                    sleep(0.1)

                step_2_success = True
                break
            except Exception as exc:
                print(exc)

            sleep(1)
            if try_counter == 1:
                break
            try_counter = try_counter - 1

        if not step_2_success:
            return step_2_success

        # step 3 press submit button
        try_counter = 10
        while try_counter > 0:
            try:
                next_button = user.driver.find_element(By.XPATH,
                                                       '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/button[1]/div')
                next_button.click()

                step_3_success = True
                break
            except Exception as exc:
                print(exc)

            try:
                next_button = user.driver.find_element(By.XPATH,
                                                       '/html/body/div[2]/div/div[1]/div/div/form/button[1]/div')
                next_button.click()

                step_3_success = True
                break
            except Exception as exc:
                print(exc)

            sleep(1)
            if try_counter == 1:
                break
            try_counter = try_counter - 1

        return step_3_success
    else:
        pass_code = pass_code[::-1]

        # step 1 enter code
        try_counter = 10
        while try_counter > 0:
            try:
                pass_field = user.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div[2]/input')
                for letter in pass_code:
                    pass_field.send_keys(letter)
                    sleep(0.3)
                step_1_success = True
                break
            except:
                pass

            try:
                pass_field = user.driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[4]/div/div[3]'
                                                                '/div/input')
                for letter in pass_code:
                    pass_field.send_keys(letter)
                    sleep(0.3)
                step_1_success = True
                break
            except:
                pass

            try:
                pass_field = user.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[4]/div/div[3]/div/input')
                for letter in pass_code:
                    pass_field.send_keys(letter)
                    sleep(0.3)
                step_1_success = True
                break
            except:
                pass

            sleep(1)
            if try_counter == 1:
                break
            try_counter = try_counter - 1

        if not step_1_success:
            return step_1_success

        # step 2 verify
        try_counter = 10
        while try_counter > 0:
            try:
                user.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[1]/div/div[1]/button/div[2]')
                step_2_success = True
                break
            except:
                pass

            try:
                user.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div/div[1]/div[1]/button/div')
                step_2_success = True
                break
            except:
                pass

        if step_2_success:
            user.auth_complete = True

        return step_2_success


def check_user(user, check_type):
    result = False
    try_counter = 10
    while try_counter > 0:
        try:
            url = chat_main_url+chat_id
            while user.driver.current_url != url:
                user.driver.get('https://google.com')
                user.driver.get(url)

            type_field = user.driver.find_element(By.XPATH, '//*[@id="editable-message-text"]')

            for letter in 'Главное меню':
                type_field.send_keys(letter)
                sleep(0.3)
            type_field.send_keys('\ue007')
            sleep(1)
            found_elements_main = user.driver.find_elements(By.TAG_NAME, 'button')
            for main_element in found_elements_main:
                found_elements = main_element.find_elements(By.CLASS_NAME, 'inline-button-text')
                for element in found_elements:
                    if element.text == 'Уведомления':
                        main_element.click()
            sleep(1)

            found_elements_main = user.driver.find_elements(By.TAG_NAME, 'button')
            for main_element in found_elements_main:
                found_elements = main_element.find_elements(By.CLASS_NAME, 'inline-button-text')
                for element in found_elements:
                    if element.text == 'Назад':
                        main_element.click()

            result = True
            break
        except Exception as exc:
            print(exc)
            sleep(1)
            if try_counter == 1:
                break
            try_counter = try_counter - 1
    return result
