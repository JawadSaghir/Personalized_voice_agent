from together import Together
client = Together(api_key="tgp_v1_gQCicCu_60bun2sUMbu4wTDtcYthV-KtcUTaj4xKKPU")  # Replace with your actual API key
from together import Together
import requests


def image_generation():
    response = client.images.generate(
        prompt="make the high quality 4k image of mountains with snow  ",
        model="black-forest-labs/FLUX.1-schnell-Free",
        width=1792,
        height=768,
        steps=2
    )
    image_url = response.data[0].url
    # Optional: Download and save the image
    img_data = requests.get(image_url).content
    with open("image.jpg", "wb") as f:
        f.write(img_data)
    print("✅ Image is saved Successfully'")
image_generation()