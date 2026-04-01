from PIL import Image
import stepic

try:
    stego_img = Image.open("profile_secret.png")

    decoded_data = stepic.decode(stego_img)

    print("--- Extraction Successful ---")
    print("Recovered Port Data:")
    print(decoded_data) 
except FileNotFoundError:
    print("Error: 'profile_secret.png' not found. Did you run exfiltrate.py first?")