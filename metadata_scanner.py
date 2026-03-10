# Sean Sampson
# A01072945

import exifread
import base64
import os
from datetime import datetime
from PIL import Image

def try_decode(data):
    """ Tries to decode Base64 covert channels """
    try:
        return base64.b64decode(data, validate=True).decode('utf-8')
    except:
        return None

def extract_metadata(image_path):
    """ Extracts all the metadata from the image files """
    risk_score = 0
    alerts = []
    captured_metadata = {}
    
    print(f"\nAnalyzing: {image_path}")
    
    try:
        with open(image_path, "rb") as f:
            tags = exifread.process_file(f)
            for tag, val in tags.items():
                val_str = str(val)
                captured_metadata[tag] = val_str
                
                if any(k in tag for k in ['GPSLatitude', 'GPSLongitude']):
                    print(f"|GPS Location   | {val_str}")
                    risk_score += 5
                    alerts.append(f"Privacy Leak: {tag} present")
                
                elif any(k in tag for k in ['Software', 'Comment', 'Copyright', 'Description', 'MakerNote']):
                    print(f"|{tag:<15}| {val_str}")
                    if len(val_str) > 5:
                        risk_score += 10
                        alerts.append(f"Covert Channel detected in {tag}")

            if 'EXIF DateTimeOriginal' in tags:
                file_mtime = datetime.fromtimestamp(os.path.getmtime(image_path)).strftime('%Y:%m:%d %H:%M:%S')
                if str(tags['EXIF DateTimeOriginal']) > file_mtime:
                    risk_score += 5
                    alerts.append("Forensic Anomaly: Timestamp mismatch")
    except:
        pass

    try:
        img = Image.open(image_path)
        for key, val in img.info.items():
            if isinstance(val, (bytes, bytearray)):
                continue
                
            val_str = str(val).strip()
            label = f"Image {key}"
            captured_metadata[label] = val_str
            
            if "Part" in val_str or any(k in key.lower() for k in ['comment', 'desc', 'software']):
                print(f"|{label:<15}| {val_str}")
                risk_score += 10
                alerts.append(f"Covert Channel detected in PNG {key}")

    except:
        pass

    print(f"Total Risk Score: {risk_score}")
    for a in alerts:
        print(f"{a}")
    return captured_metadata

def main():
    """ Main function """
    valid_exts = ('.png', '.jpg', '.jpeg')
    files = [f for f in os.listdir('.') if f.lower().endswith(valid_exts)]
    found_parts = []
    
    for file_name in sorted(files):
        metadata = extract_metadata(file_name)
        for tag_name, raw_val in metadata.items():
            decoded = try_decode(raw_val)
            if decoded:
                found_parts.append(decoded)
            elif "Part" in str(raw_val) and str(raw_val) not in found_parts:
                found_parts.append(str(raw_val))

    print("\n" + "="*50)
    print("RECONSTRUCTED FULL SECRET MESSAGE:")
    print(" ".join(dict.fromkeys(found_parts)) if found_parts else "Nothing found")
    print("="*50)

if __name__ == "__main__":
    main()