from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from conversation import conversation_script_2

chrome_driver_path = r"C:\Workspace\Python\chromedriver.exe"

# Cấu hình tài khoản
accounts = {
    "A": {
        "name": "1",
        "chrome_path": "C:\\Others\\Facebook Accounts\\caytienbmt05\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Facebook Accounts\\caytienbmt05\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9400  # Cổng Remote Debugging riêng
    },
    "B": {
        "name": "2",
        "chrome_path": "C:\\Others\\Facebook Accounts\\caytienbmt09\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Facebook Accounts\\caytienbmt09\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9401  # Cổng Remote Debugging riêng
    },
    "C": {
        "name": "3",
        "chrome_path": "C:\\Others\\Facebook Accounts\\legiangbmt017\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Facebook Accounts\\legiangbmt017\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9402  # Cổng Remote Debugging riêng
    },
    # "A": {
    #     "name": "4",
    #     "chrome_path": "C:\\Others\\Facebook Accounts\\lttskda\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "C:\\Others\\Facebook Accounts\\lttskda\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9403  # Cổng Remote Debugging riêng
    # },
    # "B": {
    #     "name": "5",
    #     "chrome_path": "C:\\Others\\Facebook Accounts\\n17dcqt014\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "C:\\Others\\Facebook Accounts\\n17dcqt014\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9404  # Cổng Remote Debugging riêng
    # },
    # "C": {
    #     "name": "6",
    #     "chrome_path": "C:\\Others\\Facebook Accounts\\thanhtruong1691\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "C:\\Others\\Facebook Accounts\\thanhtruong1691\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9405  # Cổng Remote Debugging riêng
    # },
}

# Hàm khởi tạo Selenium
def init_driver(account):
    options = webdriver.ChromeOptions()
    options.binary_location = account["chrome_path"]
    options.add_argument(f"--user-data-dir={account['user_data_dir']}")  # Thư mục dữ liệu riêng
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument(f"--remote-debugging-port={account['debug_port']}")  # Cổng Debug riêng
    options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ tối đa
    # Có thể chạy headless, nhưng muốn reset để có thể mở GUI thì cần xóa hết Chrome session
    options.add_argument("--headless")
    options.add_argument("--disable-gpu") # Tắt GPU (tăng hiệu năng khi chạy headless)

    # Sử dụng webdriver-manager để tự động tải ChromeDriver
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service, options=options)

def send_message(driver,  message):
    try:
        # Chờ nhóm chat tải xong
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "x9f619")]'))
        )

        # Chờ ô nhập liệu tin nhắn sẵn sàng
        message_box = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true" and @aria-label="Tin nhắn"]'))
        )

        # Chèn nội dung bằng JavaScript
        message_box.click()
        message_box.send_keys(message)

        # Chờ thời gian ngẫu nhiên từ 30 đến 60 giây
        wait_time = random.randint(8, 15)
        print(f"Chờ {wait_time} giây trước khi gửi tin nhắn...")
        time.sleep(wait_time)

        # Nhấn ENTER để gửi
        message_box.send_keys(Keys.ENTER)
        print(f"Đã gửi: {message}")

    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn: {e}")
        print("Debug HTML:")
        print(driver.page_source)


def scroll_to_bottom(driver):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Chờ một chút để nội dung tải đầy đủ
        print("Đã cuộn xuống cuối màn hình.")
    except Exception as e:
        print(f"Lỗi khi cuộn màn hình: {e}")


# Hàm chờ và nhận tin nhắn từ nhóm
def wait_for_new_message(driver, expected_message):
    try:
        # Cuộn màn hình trước khi tìm kiếm
        scroll_to_bottom(driver)

        # Lấy danh sách tất cả các thẻ <span> chứa tin nhắn trong nhóm
        messages = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.XPATH, '//div[@class="html-div xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp x11i5rnm x12nagc x1mh8g0r x1yc453h x126k92a x18lvrbx"]')
        )

        # Duyệt qua từng tin nhắn để kiểm tra nội dung
        for message in messages:
            message_text = message.text.strip()  # Lấy nội dung văn bản và loại bỏ khoảng trắng thừa
            if message_text == expected_message:
                print(f"Nhận được tin nhắn khớp: {message_text}")
                return True

        print("Không tìm thấy tin nhắn khớp.")
        return False
    except Exception as e:
        print(f"Lỗi khi nhận tin nhắn: {e}")
        return False



# Hàm chính
def main():
    # Khởi tạo trình duyệt cho cả hai tài khoản
    drivers = {key: init_driver(account) for key, account in accounts.items()}

    try:
        # Mở Telegram Web
        for driver in drivers.values():
            driver.get("https://www.facebook.com/messages/t/9331467936886129")
        time.sleep(5)

        # Duyệt qua kịch bản hội thoại
        for step in conversation_script_2:
            sender = step["sender"]
            receiver = step["response"]

            # Gửi tin nhắn từ người gửi
            send_message(drivers[sender], step["message"])

            time.sleep(5)

            # Kiểm tra tin nhắn mới
            received = wait_for_new_message(drivers[receiver], step["message"])
            if received:
                send_message(drivers[receiver], step["reply"])

    except Exception as e:
        print(f"Lỗi xảy ra trong quá trình chạy: {e}")

    finally:
        # Đóng tất cả trình duyệt
        for driver in drivers.values():
            driver.quit()

if __name__ == "__main__":
    main()
