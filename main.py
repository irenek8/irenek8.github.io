import arrr
from pyscript import document
def translate_english(event):
    input=document.querySelector("#eng")
    eng=input.value
    output=document.querySelector("#output")
    output.innerText=arrr.translate(eng)