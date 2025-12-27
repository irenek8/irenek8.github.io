from pyscript import document
def on_submit():
    nonlocal location
    global new_url
    input_text=document.querySelector("#eng")
    location.set(input_text.value)
    print("Location " + location.get())
    ##new_url = getUrlForLocation(location.get())
    ##start_search()