import tkinter as tk
import json
import requests
import urllib.request
from io import BytesIO
from PIL import ImageTk, Image

def display_image(image_url: str) -> None:
    image_label.place(x=300, y=200)

    with urllib.request.urlopen(image_url) as url:
        image_data = url.read()
    
    image_stream = BytesIO(image_data)
    image = ImageTk.PhotoImage(Image.open(image_stream))
    image_label.config(image=image)
    image_label.image = image

def get_image_url() -> str:
    headers = {"Authorization": "* include your authorization code here *"}

    url = "https://api.edenai.run/v2/image/generation"
    payload = {
        "providers": "openai",
        "text": input_field.get(),
        "resolution": "256x256",
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['openai']['items'][0]["image_resource_url"]

def render_image():
    print("clicked")
    try:
        image_label.place_forget()
        error_label.place_forget()
        image_url = get_image_url()
    except KeyError:
        error_label.place(x=350, y=120)
    else:
        print(image_url)
        display_image(image_url)

window = tk.Tk()
window.title("AI Image Generator")
window.geometry("800x600")

error_label = tk.Label(window, text="Prompt cannot be empty!", fg="red")

input_field = tk.Entry(window, width=40, font=('Helvetica', 12))
input_field.place(x=225, y=50)

image_label = tk.Label(window)

generate_button = tk.Button(window, text="Create", height=1, width=12, command=render_image)
generate_button.place(x=360, y=90)

window.mainloop()