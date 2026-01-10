from pyscript import document
def on_submit(event):
    nonlocal location
    global new_url
    input_text=document.querySelector("#eng")
    location.set(input_text.value)
    print("Location " + location.get())
    ##new_url = getUrlForLocation(location.get())
    ##start_search()

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