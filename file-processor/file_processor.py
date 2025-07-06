import os
import logging
import csv
import statistics
import pydicom
import datetime
from typing import Optional, List, Tuple
from PIL import Image
import numpy as np

class FileProcessor:
    def __init__(self, base_path: str, log_file: str = "processor.log"):
        self.base_path = base_path
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(filename=log_file, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def list_folder_contents(self, folder_name: str, details: bool = False) -> None:
        folder_path = os.path.join(self.base_path, folder_name)
        try:
            elements = os.listdir(folder_path)
            print(f"Folder: {folder_path}")
            print(f"Number of elements: {len(elements)}")

            for el in elements:
                full_path = os.path.join(folder_path, el)
                if os.path.isfile(full_path):
                    info = f"  - {el} (File"
                    if details:
                        size = os.path.getsize(full_path) / (1024 * 1024)
                        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
                        info += f", {size:.1f} MB, Last Modified: {mod_time})"
                    else:
                        info += ")"
                    print(info)
                else:
                    mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
                    print(f"  - {el} (Folder, Last Modified: {mod_time})")
        except FileNotFoundError:
            self.logger.error(f"Folder not found: {folder_path}")
            print("Error: Folder not found.")

    def read_csv(self, filename: str, report_path: Optional[str] = None, summary: bool = False) -> None:
        file_path = os.path.join(self.base_path, filename)
        try:
            with open(file_path, newline='') as csvfile:
                reader = list(csv.DictReader(csvfile))
                if not reader:
                    print("Empty CSV file.")
                    return
                headers = reader[0].keys()
                print(f"Columns: {list(headers)}")
                print(f"Rows: {len(reader)}")

                num_cols = {}
                non_num_cols = {}

                for h in headers:
                    try:
                        nums = [float(row[h]) for row in reader if row[h]]
                        avg = statistics.mean(nums)
                        std = statistics.stdev(nums) if len(nums) > 1 else 0.0
                        num_cols[h] = (avg, std)
                    except ValueError:
                        values = [row[h] for row in reader]
                        freq = {v: values.count(v) for v in set(values)}
                        non_num_cols[h] = freq

                print("Numeric Columns:")
                for k, (avg, std) in num_cols.items():
                    print(f"  - {k}: Average = {avg:.2f}, Std Dev = {std:.2f}")

                if summary:
                    print("Non-Numeric Summary:")
                    for k, freq in non_num_cols.items():
                        print(f"  - {k}: Unique Values = {len(freq)}")

                if report_path:
                    os.makedirs(report_path, exist_ok=True)
                    with open(os.path.join(report_path, "report.txt"), "w") as f:
                        for k, (avg, std) in num_cols.items():
                            f.write(f"{k}: Avg={avg:.2f}, StdDev={std:.2f}\n")
                    print(f"Saved summary report to {report_path}")

        except Exception as e:
            self.logger.error(f"Error reading CSV: {e}")
            print("Error: Cannot read CSV file.")

    def read_dicom(self, filename: str, tags: Optional[List[Tuple[int, int]]] = None, extract_image: bool = False) -> None:
        file_path = os.path.join(self.base_path, filename)
        try:
            ds = pydicom.dcmread(file_path)
            print(f"Patient Name: {ds.get('PatientName', 'N/A')}")
            print(f"Study Date: {ds.get('StudyDate', 'N/A')}")
            print(f"Modality: {ds.get('Modality', 'N/A')}")

            if tags:
                for tag in tags:
                    value = ds.get(tag, "N/A")
                    print(f"Tag {tag}: {value}")

            if extract_image and hasattr(ds, 'pixel_array'):
                arr = ds.pixel_array
                if arr.ndim == 3:
                    arr = arr[0]  # Tomar la primera imagen si es un stack
                img = Image.fromarray(arr)
                img_path = os.path.join(self.base_path, filename.replace(".dcm", ".png"))
                img.save(img_path)
                print(f"Extracted image saved to {img_path}")

        except Exception as e:
            self.logger.error(f"Error reading DICOM: {e}")
            print("Error: Cannot read DICOM file.")
