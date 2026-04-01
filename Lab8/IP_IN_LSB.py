from PIL import Image

def set_LSB(value, bit):
    if bit == '0':
        return value & 254
    else:
        return value | 1

def hide_ip():
    img = Image.open("company_logo.png").convert("RGBA")
    
    pixels = list(img.getdata())
    
    message = "TARGET:192.168.1.50"
    new_pixels = []
    
    for i in range(len(message)):
        char_bin = bin(ord(message[i]))[2:].zfill(8)
        
        p1 = pixels[i*2]
        p2 = pixels[i*2 + 1]
        
        new_p1 = tuple(set_LSB(p1[j], char_bin[j]) for j in range(4))
        new_p2 = tuple(set_LSB(p2[j], char_bin[j+4]) for j in range(4))
        
        new_pixels.append(new_p1)
        new_pixels.append(new_p2)
    
    new_pixels.extend(pixels[len(message)*2:])
  
    img.putdata(new_pixels)
    img.save("company_logo_stego.png")
    print("Success: company_logo_stego.png has been created.")

if __name__ == "__main__":
    hide_ip()