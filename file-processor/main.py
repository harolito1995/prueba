import os
from file_processor import FileProcessor

# Limpiar logs automáticamente
log_path = "./logs/processor.log"
if os.path.exists(log_path):
    with open(log_path, "w") as f:
        pass

processor = FileProcessor(base_path="./data", log_file=log_path)

# List contents
processor.list_folder_contents("test_folder", details=True)

# Read CSV
processor.read_csv("test_folder/sample-02-csv.csv", report_path="./reports", summary=True)

# Read DICOM
processor.read_dicom("test_folder/sample-02-dicom.dcm", tags=[(0x0010, 0x0010), (0x0008, 0x0060)], extract_image=True)
