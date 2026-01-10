from pyscript import documents
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import none_of
from selenium.webdriver.support.wait import WebDriverWait
import time

location = "test"
new_url = "test"
def on_submit(event):
    ##nonlocal location
    global new_url
    print("in pyscript")
    global location
    input_text=document.querySelector("#eng")
    location = input_text.value
    print("Location " + location)
    new_url = getUrlForLocation(location)
    ##start_search()

def getUrlForLocation(location):
    options = Options()
    options.add_argument("--headless")
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.com/maps")
        search_box = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,"searchboxinput")))
        search_box.send_keys(location)
        search_box.send_keys(Keys.ENTER)
        #WebDriverWait(driver, 10).until(EC.url_contains("place"))
        time.sleep(3)
        focus_url = driver.current_url
        print(focus_url)
        return focus_url
    except Exception as e:
        print("in exception"+e)
        return None
    finally:
        if driver:
            driver.quit()

def create_cards(dictionary, card_container, custom_font):
    global current_card_index
    print(current_card_index)
    print("starting list")
    for item in dictionary:
        print(item["name"])
    for item in dictionary[current_card_index:current_card_index+3]:
        card = tk.Frame(card_container, width = 400, height = 130, bd = 2, padx = 10, pady = 10, relief = "groove")
        card.pack_propagate(False)
        card.pack(padx = 10, pady = 10)
        name_ele=document.createElement('h2')
        name_ele.innerText=item["name"]
        label2 = tk.Label(card, text=item["location"], wraplength=220,font = custom_font)
        location_ele = document.createElement('h2')
        location_ele.innerText = item["location"]
        label3 = tk.Label(card, text=item["rating"],font = custom_font)
        rating_ele = document.createElement('h2')
        rating_ele.innerText = item["rating"]
        label4 = tk.Label(card, text=showStars(item["rating"]),font = custom_font)
        stars_ele = document.createElement('h2')
        stars_ele.innerText = showStars(item["rating"])
        card.bind("<Button-1>", lambda event, current = item: on_card_click(current["website"]))
        for widget in card.winfo_children():
            widget.bind("<Button-1>", lambda event, current = item: on_card_click(current["website"]))
    current_card_index += 3