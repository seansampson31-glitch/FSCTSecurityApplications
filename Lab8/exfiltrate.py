from PIL import Image
import stepic

carrier = Image.open("profile.png")

footprint_data = "CONF_TOOL_SCAN: 80, 443, 3478, 5060".encode('utf-8')

stego_image = stepic.encode(carrier, footprint_data)

stego_image.save("profile_secret.png")

print("Data hidden successfully.")