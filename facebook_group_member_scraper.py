import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.parse import unquote, parse_qs
import json, os, time, requests, sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyotp
import random

global driver

headers_api_facebook = {
    "Host": "www.facebook.com",
    "Connection": "keep-alive",
    "Content-Length": "2185",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "viewport-width": "633",
    "X-FB-Friendly-Name": "CometPageReviewsRecommendationsPostsPaginationQuery",
    "X-FB-LSD": "mrTeHtpoHoe3uTAP-2Btuy",
    "Content-Type": "application/x-www-form-urlencoded",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua-platform": "\"Windows\"",
    "Accept": "*/*",
    "Origin": "https://www.facebook.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cookie": ""
}

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)

else:
    application_path = os.path.dirname(os.path.abspath(__file__))

os.chdir(application_path)

# group_url = 'https://www.facebook.com/groups/selftaughtprogrammers/members'

group_url = "https://www.facebook.com/groups/PAPArtstore/members"

group_id_name = "PAPArtstore"

FACEBOOK_USERNAME = ""
FACEBOOK_PASSWORD = ""

creds = {"username": "",
         "password": "", "authenticator": ""}

COOKIES = {}
FORM_DATA = {}

MEMBERS_TYPE = None

capture = False

CHROME_BINARY_LOCATION = 'chromedriver_windows.exe'

facebook_session_profile = os.path.join(application_path, "session_profile")

if not os.path.exists(group_id_name):
    os.makedirs(group_id_name)

last_cursor = ""

if os.path.exists(os.path.join(group_id_name, 'all_members.json')):
    with open(os.path.join(group_id_name, 'all_members.json')) as f:
        all_members = json.load(f)
else:
    all_members = []

if os.path.exists(os.path.join(group_id_name, 'last_cursor.txt')):
    with open(os.path.join(group_id_name, 'last_cursor.txt'), encoding='utf8') as f:
        last_cursor = f.read().strip()


def cookies(driver, credentials):
    driver.get("https://www.facebook.com")

    username_xpath = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input"

    username_box = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, username_xpath)))

    for char in credentials.get("username"):
        username_box.send_keys(char)
        time.sleep(random.randrange(1, 5) / 10)

    password_xpath = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input"

    password_box = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, password_xpath)))

    for char in credentials.get("password"):
        password_box.send_keys(char)
        time.sleep(random.randrange(1, 5) / 10)

    button_xpath = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button"

    login_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, button_xpath)))

    login_button.click()

    auth_code = "/html/body/div[1]/div[2]/div[1]/div/form/div/div[2]/ul/li[3]/span/input"

    auth_box = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, auth_code)))

    google_auth = pyotp.TOTP(credentials.get("authenticator")).now()

    for char in google_auth:
        auth_box.send_keys(char)
        time.sleep(random.randrange(1, 5) / 10)

    submit_code = "/html/body/div[1]/div[2]/div[1]/div/form/div/div[3]/div[1]/button"

    submit_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, submit_code)))

    submit_button.click()

    continue_path = "/html/body/div[1]/div[2]/div[1]/div/form/div/div[3]/div[1]/button"

    continue_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, continue_path)))

    continue_button.click()

    time.sleep(2)

    return driver.get_cookies()


def initialize_chrome():
    global driver
    try:
        options = uc.options.ChromeOptions()
        # options.binary_location = CHROME_BINARY_LOCATION
        options.add_argument(f'--user-data-dir={facebook_session_profile}')
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument('--log-level=3')
        options.add_argument('--blink-settings=imagesEnabled=false')
        driver = uc.Chrome(options=options, use_subprocess=True, enable_cdp_events=True)
        driver.add_cdp_listener('Network.requestWillBeSent', capturedata)
        print("Done Initialization")
    except json.JSONDecodeError as e:
        os.remove('session_profile\Default\Preferences')
        initialize_chrome()


def facebook_login():
    global COOKIES
    driver.get('https://www.facebook.com/login')
    time.sleep(1)
    if 'home.php' in driver.current_url or "welcome" in driver.current_url:
        while not COOKIES.get('presence'):
            COOKIES = {c['name']: c['value'] for c in driver.get_cookies()}
    else:
        COOKIES = {c['name']: c['value'] for c in cookies(driver, credentials=creds)}
        #print(COOKIES)


def capturedata(eventdata):
    global MEMBERS_TYPE
    if not capture:
        return
    if FORM_DATA:
        return
    data = str(eventdata["params"]["request"])
    if ("graphql") in data and ('GroupsCometMembersPageNewForumMembersSectionRefetchQuery' in data):

        request_data = eventdata["params"]["request"]

        for k, v in request_data['headers'].items():
            headers_api_facebook[k] = v

        for k, v in parse_qs(request_data['postData'].strip()).items():
            FORM_DATA[k] = v[0]

        MEMBERS_TYPE = "new_forum_members"

    elif "graphql" in data and ('GroupsCometMembersPageNewMembersSectionRefetchQuery' in data):
        request_data = eventdata["params"]["request"]
        for k, v in request_data['headers'].items():
            headers_api_facebook[k] = v

        for k, v in parse_qs(request_data['postData'].strip()).items():
            FORM_DATA[k] = v[0]

        MEMBERS_TYPE = "new_members"


def get_group_html(url):
    driver.get(url)
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v lrazzd5p q66pz984"]')))
    return driver.page_source


initialize_chrome()

facebook_login()

html = get_group_html(group_url)
capture = True
wait = 0
while not FORM_DATA:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    wait += 1
    if wait > 10:
        break

capture = False
driver.quit()

if not FORM_DATA:
    print("Failed to capture data, try again!")
    sys.exit(1)
variables = json.loads(FORM_DATA['variables'])

if last_cursor:
    variables['cursor'] = last_cursor
else:
    variables['cursor'] = None

FORM_DATA['variables'] = json.dumps(variables)

print(COOKIES)
encoded_cookie = f"sb=q{(COOKIES['sb'])}; wd={(COOKIES['wd'])}; datr={(COOKIES['datr'])}; c_user={(COOKIES['c_user'])}; xs={(COOKIES['xs'])}; fr={(COOKIES['fr'])}; presence={(COOKIES['presence'])}"

headers_api_facebook['Cookie'] = encoded_cookie
headers_api_facebook['Referer'] = group_url
headers_api_facebook['Accept-Encoding'] = "gzip, deflate"

print("Member Extration Started...")

error_retry = 0

while True:
    if error_retry > 6:
        break

    r = requests.post("https://www.facebook.com/api/graphql/", data=FORM_DATA, headers=headers_api_facebook,
                      cookies=COOKIES)

    if not r.status_code == 200:
        error_retry += 1
        time.sleep(1)
        continue

    json_data = r.json()

    json_data = json_data['data']['node'][MEMBERS_TYPE]

    if not json_data:
        error_retry += 1
        time.sleep(1)
        continue

    for result in json_data['edges']:
        info_dict = {}
        node = result['node']
        info_dict['Profile Name'] = node['name']
        info_dict['Profile Url'] = node['url']
        if info_dict not in all_members:
            all_members.append(info_dict)

    next_page = json_data.get('page_info', {})

    with open(os.path.join(group_id_name, 'all_members.json'), 'w', encoding='utf8') as f:
        f.write(json.dumps(all_members, indent=4))

    if next_page.get('has_next_page'):
        next_cursor = next_page.get('end_cursor')
        current_cursor = json.loads(FORM_DATA['variables'])
        current_cursor['cursor'] = next_cursor
        print(FORM_DATA)
        print('\n')
        FORM_DATA['variables'] = json.dumps(current_cursor)
        with open(os.path.join(group_id_name, 'last_cursor.txt'), 'w', encoding='utf8') as f:
            f.write(next_cursor)
    else:
        print("No more results")

print(f"Total found {len(all_members)}.")
