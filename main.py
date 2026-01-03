import os
import re
import csv
import pdfplumber

PDF_FOLDER = "pdfs"
OUTPUT_CSV = "output/data_mahasiswa.csv"

patterns = {
    "NIM": r"NIM\s*:\s*(.*)",
    "Nama Lengkap": r"Nama Lengkap\s*:\s*(.*)",
    "TTL": r"Tempat,\s*Tanggal Lahir\s*:\s*(.*)",
    "Agama": r"Agama\s*:\s*(.*)",
    "Alamat Asal": r"Alamat Asal\s*:\s(.*)",
    "Alamat di Malang": r"Alamat di Malang\s*:\s*(.*)",
    "Fakultas/Prodi":r"Fakultas/Program Studi\s*:\s*(.*)"

}

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_data(text):
    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[key] = match.group(1).strip().replace("\n", "")
        else:
            data[key] = ""
    return data

def main():
    all_data = []
    
    PDF_FOLDER = "pdfs"
    OUTPUT_CSV = "output/data_mahasiswa.csv"
  

    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(PDF_FOLDER, file)
            print(f"Processing: {file}")

            text = extract_text(pdf_path)
            data = extract_data(text)
            all_data.append(data)

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf") as csvfile:
        fieldnames = list(patterns.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(all_data)

    print("Data Berhasil Disimpan ke csv")    

    if __name__ == "__main__":
        main()
