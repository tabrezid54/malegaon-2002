import pytesseract
from pdf2image import convert_from_path
import cv2
import os
import argparse
import json
import re
from tqdm import tqdm

# ---------- Arguments ----------
parser = argparse.ArgumentParser(description="Hindi PDF OCR → JSON for Voter List")
parser.add_argument("-i", "--input", required=True, help="Input PDF file")
parser.add_argument("-o", "--output", required=True, help="Output JSON file")
args = parser.parse_args()

PDF_FILE = args.input
OUTPUT_JSON = args.output
TMP_DIR = "ocr_pages"
os.makedirs(TMP_DIR, exist_ok=True)

# ---------- OCR Config ----------
OCR_CONFIG = (
    "--oem 3 --psm 6 "
    "-c preserve_interword_spaces=1 "
    "-c tessedit_char_blacklist='‘’“”\"(){}[]|' "
    "-c load_system_dawg=0 -c load_freq_dawg=0 "
)

# ---------- Convert PDF to Images ----------
print("📌 Converting PDF to images...")
pages = convert_from_path(PDF_FILE, dpi=350)
image_paths = []
for i, page in enumerate(pages):
    img_path = f"{TMP_DIR}/page_{i+1}.png"
    page.save(img_path, "PNG")
    image_paths.append(img_path)

# ---------- OCR & Extract voters ----------
relation_words = ["प", "प्‌", "ब", "व", "।"]
gender_words = ["स्त्री", "स्‍त्री", "स्त्री.", "पुरुष", "पुरुष.", "पु", "पु."]
voters = []

print("🔍 Running OCR & extracting data...")
for page_idx, img_path in enumerate(tqdm(image_paths, desc="OCR Pages")):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=1.7, fy=1.7, interpolation=cv2.INTER_CUBIC)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 15
    )
    text = pytesseract.image_to_string(thresh, lang="hin+Devanagari", config=OCR_CONFIG)

    # ---------- Extract Yadi No & Page No ----------
    yadi_no = "UNKNOWN"
    page_no = str(page_idx + 1)
    yadi_match = re.search(r"यादी\s*भाग\s*क्रमांक[^0-9]*(\d+)", text)
    if yadi_match:
        yadi_no = yadi_match.group(1)

    # ---------- Parse voter lines ----------
    for line in text.split("\n"):
        ln = re.sub(r"\s+", " ", line).strip()
        if not re.match(r"^\d{1,4}\s", ln):
            continue

        parts = ln.split(" ")
        idx = 0
        source_line = ln  # store original line

        # Serial No
        serial_no = parts[idx]
        idx += 1

        # Address: next one or two tokens until a name is detected
        address_tokens = []
        while idx < len(parts) and not re.match(r"^[\u0900-\u097F]", parts[idx]):
            address_tokens.append(parts[idx])
            idx += 1
        if not address_tokens:
            address_tokens.append(parts[idx-1])
        address = " ".join(address_tokens).strip()

        # Name until relation
        name_tokens = []
        while idx < len(parts) and parts[idx] not in relation_words:
            name_tokens.append(parts[idx])
            idx += 1
        name = " ".join(name_tokens).strip()

        # Relation
        relation = ""
        if idx < len(parts) and parts[idx] in relation_words:
            relation = parts[idx]
            idx += 1

        # Father/Husband Name until gender
        father_tokens = []
        while idx < len(parts) and parts[idx] not in gender_words and not re.match(r"^\d{1,3}$", parts[idx]):
            father_tokens.append(parts[idx])
            idx += 1
        father_name = " ".join(father_tokens).strip()

        # Gender
        gender = ""
        if idx < len(parts) and parts[idx] in gender_words:
            gender = parts[idx]
            idx += 1

        # Age
        age = ""
        if idx < len(parts) and re.match(r"^\d{1,3}$", parts[idx]):
            age = parts[idx]
            idx += 1

        # EPIC No: last 7-15 alphanumeric
        epic_no = ""
        if idx < len(parts) and re.match(r"^[A-Za-z0-9]{7,15}$", parts[idx]):
            epic_no = parts[idx]

        voters.append({
            "serial_no": serial_no,
            "address": address,
            "name": name,
            "relation_type": relation,
            "father_husband_name": father_name,
            "gender": gender,
            "age": age,
            "epic_no": epic_no,
            "yadi_no": yadi_no,
            "page_no": page_no,
            "pdf_file": os.path.basename(PDF_FILE),
            "source": source_line
        })

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(voters, f, ensure_ascii=False, indent=2)

print(f"✔ Completed! Total records: {len(voters)}")
print(f"📁 JSON saved → {OUTPUT_JSON}")

# ---------- Cleanup temporary OCR images ----------
print("🧹 Removing temporary OCR images...")
for img in image_paths:
    try:
        os.remove(img)
    except:
        pass

try:
    os.rmdir(TMP_DIR)
except:
    pass

print("🗑 Cleanup completed.")

