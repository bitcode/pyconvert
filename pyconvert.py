import os
import argparse
import pyheif
from PIL import Image
from tqdm import tqdm
from pyheif.error import HeifError

def convert_heic_to_jpeg(heic_path, jpeg_path):
    try:
        heif_file = pyheif.read(heic_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        image.save(jpeg_path, format="JPEG")
        return True
    except HeifError as e:
        print(f"Failed to convert {heic_path} due to error: {str(e)}")
        return False

def convert_all_heic_in_folder(folder_path):
    # get list of all heic files
    heic_files = [f for f in os.listdir(folder_path) if f.endswith('.heic') or f.endswith('.HEIC')]

    # create progress bar
    pbar = tqdm(total=len(heic_files), ncols=70)

    for heic_file in heic_files:
        base_name = os.path.splitext(heic_file)[0]
        jpeg_file = f"{base_name}.jpg"

        if convert_heic_to_jpeg(os.path.join(folder_path, heic_file), os.path.join(folder_path, jpeg_file)):
            # update progress bar only if conversion is successful
            pbar.update(1)

    pbar.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert all HEIC files in a folder to JPEG.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing the HEIC files.')

    args = parser.parse_args()

    convert_all_heic_in_folder(args.folder_path)
