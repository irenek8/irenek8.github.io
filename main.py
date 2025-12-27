from pyscript import document
"""
def translate_english(event):
    input=document.querySelector("#eng")
    eng=input.value
    output=document.querySelector("#output")
    output.innerText=arrr.translate(eng)
"""

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import threading

from selenium.webdriver.support.expected_conditions import none_of
from selenium.webdriver.support.wait import WebDriverWait

restaurant_names = []
restaurant_links = []
restaurant_data = []
##service = Service()

def on_card_click(website):
    print("You've clicked on card")
    browser = webdriver.Chrome()
    browser.get(website)

def getInput():
    root = tk.Tk()
    root.title("Input Location")
    location = tk.StringVar()

    def on_submit():
        nonlocal location
        location.set(entry.get())
        print("Location " + location.get())
        root.destroy()

    label = tk.Label(root,text="Enter a location ")
    label.pack(pady=5, padx=5)
    entry = tk.Entry(root, width=50)
    entry.pack(pady=5, padx=5)
    submit = tk.Button(root, text="Search", command=on_submit)
    submit.pack(pady=15, padx=15)
    root.mainloop()
    return location.get()

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
        return focus_url
    except Exception as e:
        print("in exception"+e)
        return None
    finally:
        if driver:
            driver.quit()



def getRestaurants(url):
    print("in getRestaurants")
    global restaurant_data
    global restaurant_names
    global restaurant_links
    restaurant_data.clear()
    restaurant_names.clear()
    restaurant_links.clear()
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    ##for i,url in enumerate(urls):
    browser.get(url)
    time.sleep(10)
    new_restaurant_names = []
    new_restaurant_links = []
    try:
        restaurants = browser.find_elements(By.CLASS_NAME, "hfpxzc")
        for restaurant in restaurants[:10]:
            label = restaurant.get_attribute("aria-label")
            print(label)
            restaurant_names.append(label)
            new_restaurant_names.append(label)
            restaurantLink = restaurant.get_attribute("href")
            print(restaurantLink)
            restaurant_links.append(restaurantLink)
            new_restaurant_links.append(restaurantLink)
    except:
        print("not found 3")
    getDetails(browser, new_restaurant_names, new_restaurant_links)
    browser.quit()
    print("after getRestaurant ", len(restaurant_data))
    return restaurant_data

def scrapeRestaurants(url):
    global restaurant_data
    global restaurant_names
    global restaurant_links

    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    ##for i,url in enumerate(urls):
    browser.get(url)
    time.sleep(10)

    panel = browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')

    for _ in range(10):
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", panel)
        time.sleep(2)

    print("scroll")

    new_restaurant_names = []
    new_restaurant_links = []

    try:
        restaurants = browser.find_elements(By.CLASS_NAME, "hfpxzc")
        for restaurant in restaurants[:10]:
            label = restaurant.get_attribute("aria-label")
            print("looking at ",label)
            if label not in restaurant_names:
                restaurant_names.append(label)
                restaurantLink = restaurant.get_attribute("href")
                print("added to list ",restaurantLink)
                new_restaurant_links.append(restaurantLink)
                new_restaurant_names.append(label)
            else:
                print(label," already in restaurant names")
    except:
        print("not found 3")
    getDetails(browser, new_restaurant_names, new_restaurant_links)
    browser.quit()
    return restaurant_data

def getDetails(browser, names_list, links_list):
    global restaurant_data
    ##global restaurant_names
    ##global restaurant_links
    for i, url in enumerate(links_list):
        browser.get(url)
        time.sleep(1)
        location = "Not found"
        stars = "Not found"
        website = "Not found"
        try:
            location = browser.find_element(By.CLASS_NAME, "Io6YTe")
        except:
            print("Not found")

        try:
            website = browser.find_element(By.CSS_SELECTOR, '[data-item-id = "authority"]')
            website = website.get_attribute("href")
        except:
            print("Not found")

        try:
            rating = browser.find_element(By.CLASS_NAME, "ceNzKf")
            stars = rating.get_attribute("aria-label")
        except:
            print("Not found")
        restaurant_data.append({
            "name": names_list[i],
            "location": location.text,
            "rating": stars,
            "website": website})

def clear_cards(card_container):
    for card in card_container.winfo_children():
        card.destroy()

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
        label = tk.Label(card, text = item["name"],font = custom_font)
        label.pack()
        label2 = tk.Label(card, text=item["location"], wraplength=220,font = custom_font)
        label2.pack()
        label3 = tk.Label(card, text=item["rating"],font = custom_font)
        label3.pack()
        label4 = tk.Label(card, text=showStars(item["rating"]),font = custom_font)
        label4.pack()
        card.bind("<Button-1>", lambda event, current = item: on_card_click(current["website"]))
        for widget in card.winfo_children():
            widget.bind("<Button-1>", lambda event, current = item: on_card_click(current["website"]))
    current_card_index += 3

def showStars(stars):
    num_stars = stars.replace(" stars", "")
    count = float(num_stars)
    star_display = ""
    for i in range(5):
        if count>0.6:
            star_display = star_display+"★"
        elif count >= 0.4 or count<=0.6:
            star_display = star_display+"½"
        else:
            star_display = star_display+"☆"
        count=count-1
    return star_display

##Start of code
##location = getInput()
###new_url = getUrlForLocation(location)
###print(new_url)
###list = getRestaurants(new_url)
###print(list)
###showRestaurants(list)

new_url = ""


def on_submit():
    nonlocal location
    global new_url
    input_text=document.querySelector("#eng")
    location.set(input_text.value)
    print("Location " + location.get())
    new_url = getUrlForLocation(location.get())
    start_search()

def start_search(self):
    self.loading["text"] = "Loading..."
    self.thread = threading.Thread(target = self.run_scraper)
    self.thread.start()


def run_scraper(self):
    list = getRestaurants(new_url)
    self.after(0, self.showRestaurants,list)

def showRestaurants(self, dictionary):
    global current_card_index
    if self.first_call:
        self.loading["text"] = ""
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        try:
            self.custom_font = tkFont.Font(family="Nunito", size=14, weight="normal")
        except:
            self.custom_font = tkFont.Font(family="Arial", size=14, weight="normal")
            print("Custom font not found.")

        label = tk.Label(frame, text="Restaurants", font=("Nunito", 30))
        label.pack()

        cards_per_page = 3
        global current_card_index
        current_card_index = 0
        print("first card setup", current_card_index)

        self.card_container = tk.Frame(frame)
        self.card_container.pack()
        clear_cards(self.card_container)
        create_cards(dictionary, self.card_container, self.custom_font)
        print(len(dictionary))

        def on_next():
            print("print button")
            list = scrapeRestaurants(new_url)
            clear_cards(self.card_container)
            create_cards(list, self.card_container, self.custom_font)
            print(len(dictionary))

        def on_clear():
            clear_cards(self.card_container)

        next = tk.Button(self, text="Next", command=on_next)
        next.pack(pady=15, padx=15)
        clear = tk.Button(self, text="Clear", command=on_clear)
        clear.pack(pady=15, padx=15)
        self.first_call = False
    else:
        print("Second search call")
        current_card_index = 0
        clear_cards(self.card_container)
        create_cards(dictionary, self.card_container, self.custom_font)