import hmac
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

# Define HASH_SECRET matching the default developer fallback key in verifier.py
HASH_SECRET = b"veri-scholars-dev-key-change-in-production"

def compute_file_hmac(filepath):
    """Computes the HMAC-SHA256 signature of a file's bytes matching verifier.py."""
    mac = hmac.new(HASH_SECRET, digestmod=hashlib.sha256)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            mac.update(chunk)
    return mac.hexdigest()

# 1. Calculate true hashes for our four success certificates
print("--- SUCCESS CERTIFICATE HASHES ---")
success_files = {
    "JHK-2025-CS-042": "demo_certificates/JHK-2025-CS-042.png",
    "JHK-2024-ME-109": "demo_certificates/JHK-2024-ME-109.png",
    "JHK-2025-EE-201": "demo_certificates/JHK-2025-EE-201.png",
    "JHK-2023-EC-304": "demo_certificates/JHK-2023-EC-304.png"
}

computed_hashes = {}
for cert_id, path in success_files.items():
    if os.path.exists(path):
        file_hash = compute_file_hmac(path)
        computed_hashes[cert_id] = file_hash
        print(f"ID: {cert_id} -> HMAC Hash: {file_hash}")

# Write these computed hashes into a python file so we can update database seeds
print("\nComputed Hashes Dictionary ready for database.py integration:")
print(computed_hashes)


# 2. Generate Failure Cases
try:
    font_path_title = "C:\\Windows\\Fonts\\georgiab.ttf"
    font_path_text = "C:\\Windows\\Fonts\\arial.ttf"
    
    font_title = ImageFont.truetype(font_path_title, 40)
    font_subtitle = ImageFont.truetype(font_path_text, 20)
    font_label = ImageFont.truetype(font_path_text, 24)
    font_val = ImageFont.truetype(font_path_title, 26)
    font_id = ImageFont.truetype(font_path_text, 20)
    font_stamp = ImageFont.truetype(font_path_title, 64)
except Exception:
    font_title = font_subtitle = font_label = font_val = font_id = font_stamp = ImageFont.load_default()

# ----------------- FAILURE CASE A: Fake Certificate ID -----------------
# Looks perfectly authentic, but the Certificate ID JHK-2025-CS-999 is NOT in the database.
img_fake = Image.new('RGB', (1200, 800), color='#FDFBF7')
draw = ImageDraw.Draw(img_fake)
draw.rectangle([20, 20, 1180, 780], outline='#D4AF37', width=5)
draw.rectangle([30, 30, 1170, 770], outline='#1E293B', width=2)
draw.text((600, 100), "BOARD OF HIGHER EDUCATION", fill='#1E293B', font=font_subtitle, anchor="mm")
draw.text((600, 160), "CERTIFICATE OF ACHIEVEMENT", fill='#9A7B1C', font=font_title, anchor="mm")
draw.text((600, 280), "NAME", fill='#64748B', font=font_label, anchor="mm")
draw.text((600, 320), "Aditi Sharma", fill='#1E293B', font=font_val, anchor="mm")
draw.line([400, 340, 800, 340], fill='#9A7B1C', width=1)
draw.text((600, 440), "B.Tech Computer Science", fill='#1E293B', font=font_val, anchor="mm")
draw.text((600, 500), "INSTITUTION", fill='#64748B', font=font_label, anchor="mm")
draw.text((600, 545), "Birla Institute of Technology, Mesra", fill='#1E293B', font=font_val, anchor="mm")
draw.text((600, 600), "Graduation Year: 2025", fill='#475569', font=font_val, anchor="mm")
draw.text((150, 710), "CERTIFICATE ID: JHK-2025-CS-999", fill='#1E293B', font=font_id) # Fake ID
img_fake.save("demo_certificates/FAIL_FAKE_ID_JHK-2025-CS-999.png")
print("Generated FAIL_FAKE_ID_JHK-2025-CS-999.png")


# ----------------- FAILURE CASE B: Name Tampering -----------------
# Uses valid ID JHK-2025-CS-042, but the name is tampered from "Aditi Sharma" to "Aarav Sharma".
img_name_tamper = Image.new('RGB', (1200, 800), color='#FDFBF7')
draw = ImageDraw.Draw(img_name_tamper)
draw.rectangle([20, 20, 1180, 780], outline='#D4AF37', width=5)
draw.rectangle([30, 30, 1170, 770], outline='#1E293B', width=2)
draw.text((600, 100), "BOARD OF HIGHER EDUCATION", fill='#1E293B', font=font_subtitle, anchor="mm")
draw.text((600, 160), "CERTIFICATE OF ACHIEVEMENT", fill='#9A7B1C', font=font_title, anchor="mm")
draw.text((600, 280), "NAME", fill='#64748B', font=font_label, anchor="mm")
draw.text((600, 320), "Aarav Sharma", fill='#1E293B', font=font_val, anchor="mm") # Tampered name
draw.line([400, 340, 800, 340], fill='#9A7B1C', width=1)
draw.text((600, 440), "B.Tech Computer Science", fill='#1E293B', font=font_val, anchor="mm")
draw.text((600, 500), "INSTITUTION", fill='#64748B', font=font_label, anchor="mm")
draw.text((600, 545), "Birla Institute of Technology, Mesra", fill='#1E293B', font=font_val, anchor="mm")
draw.text((600, 600), "Graduation Year: 2025", fill='#475569', font=font_val, anchor="mm")
draw.text((150, 710), "CERTIFICATE ID: JHK-2025-CS-042", fill='#1E293B', font=font_id)
img_name_tamper.save("demo_certificates/FAIL_NAME_TAMPERED_JHK-2025-CS-042.png")
print("Generated FAIL_NAME_TAMPERED_JHK-2025-CS-042.png")


# ----------------- FAILURE CASE C: Hash/Document Tampering -----------------
# Contains 100% correct text matching JHK-2025-CS-042 and Aditi Sharma, but has a visible red
# "VOID" security stamp placed diagonally. This shifts the binary bytes (and thus the cryptographic hash),
# which fails the tamper-proof blockchain seal verification.
img_hash_tamper = Image.new('RGB', (1200, 800), color='#FDFBF7')
draw = ImageDraw.Draw(img_hash_tamper)
draw.rectangle([20, 20, 1180, 780], outline='#D4AF37', width=5)
draw.rectangle([30, 30, 1170, 770], outline='#1E293B', width=2)
draw.text((600, 100), "BOARD OF HIGHER EDUCATION", fill='#1E293B', font=font_subtitle, anchor="mm")
draw.text((600, 160), "CERTIFICATE OF ACHIEVEMENT", fill='#9A7B1C', font=font_title, anchor="mm")
draw.text((600, 280), "NAME", fill='#64748B', font=font_label, anchor="mm")
draw.text((600, 320), "Aditi Sharma", fill='#1E293B', font=font_val, anchor="mm")
draw.line([400, 340, 800, 340], fill='#9A7B1C', width=1)
draw.text((600, 440), "B.Tech Computer Science", fill='#1E293B', font=font_val, anchor="mm")
draw.text((600, 500), "INSTITUTION", fill='#64748B', font=font_label, anchor="mm")
draw.text((600, 545), "Birla Institute of Technology, Mesra", fill='#1E293B', font=font_val, anchor="mm")
draw.text((600, 600), "Graduation Year: 2025", fill='#475569', font=font_val, anchor="mm")
draw.text((150, 710), "CERTIFICATE ID: JHK-2025-CS-042", fill='#1E293B', font=font_id)

# Draw red VOID stamp across the certificate
draw.text((600, 380), "VOID / TAMPERED", fill='#DC2626', font=font_stamp, anchor="mm")
img_hash_tamper.save("demo_certificates/FAIL_HASH_TAMPERED_JHK-2025-CS-042.png")
print("Generated FAIL_HASH_TAMPERED_JHK-2025-CS-042.png")
