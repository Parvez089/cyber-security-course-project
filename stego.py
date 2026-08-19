# stego.py: LSB Image Steganography with Visual Difference Map

from PIL import Image
import numpy as np
import io

def hide_data(image_bytes, secret_message):
    image = Image.open(io.BytesIO(image_bytes))
    
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        image = image.convert('RGBA')
        channels = 4
    else:
        image = image.convert('RGB')
        channels = 3
        
    img_arr = np.array(image)
    
    secret_message += "#####"
    binary_msg = ''.join(format(ord(i), '08b') for i in secret_message)
    data_index = 0
    length = len(binary_msg)
    
    height, width, _ = img_arr.shape
    total_pixels = height * width * 3
    
    if length > total_pixels:
        raise ValueError("Error: Image is too small to hold this secret message!")
        
    for row in img_arr:
        for pixel in row:
            for channel in range(3):
                if data_index < length:
                    pixel[channel] = (pixel[channel] & 254) | int(binary_msg[data_index])
                    data_index += 1
                else:
                    break
            if data_index >= length:
                break
        if data_index >= length:
            break
            
    encoded_img = Image.fromarray(img_arr)
    
    output_io = io.BytesIO()
    encoded_img.save(output_io, format="PNG")
    return output_io.getvalue()

def extract_data(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img_arr = np.array(image)
    
    binary_data = ""
    for row in img_arr:
        for pixel in row:
            for channel in range(3):
                binary_data += str(pixel[channel] & 1)
                
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_text = ""
    for byte in all_bytes:
        decoded_text += chr(int(byte, 2))
        if decoded_text.endswith("#####"):
            return decoded_text[:-5]
    return decoded_text

def get_difference_map(original_bytes, stego_bytes):
    # মূল ছবি ও স্টেগো ইমেজের পিক্সেল তুলনা করে ডিফারেন্স ম্যাপ তৈরি করা
    img1 = Image.open(io.BytesIO(original_bytes)).convert('RGB')
    img2 = Image.open(io.BytesIO(stego_bytes)).convert('RGB')
    
    arr1 = np.array(img1, dtype=np.int16)
    arr2 = np.array(img2, dtype=np.int16)
    
    # অ্যাবসোলিউট ডিফারেন্স বের করা এবং খালি চোখে দেখার জন্য স্কেল করা
    diff = np.abs(arr1 - arr2)
    diff_scaled = np.clip(diff * 100, 0, 255).astype(np.uint8)
    
    return Image.fromarray(diff_scaled)