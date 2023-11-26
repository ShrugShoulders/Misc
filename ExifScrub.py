"""
Exif Scrub will remove all metadata and exif data from all images from the given directory. 
process_image uses pillow to open the image, gets it's exif/metadata then removes it. 
scrub_metadata opens up multiple threads so that large directories of images can be processed at once.
"""


import os
import glob
from PIL import Image
from threading import Thread

def process_image(image_path):
    try:
        image = Image.open(image_path)

        # Remove all EXIF and other metadata
        image_without_metadata = Image.new(image.mode, image.size)
        image_without_metadata.putdata(list(image.getdata()))

        # Save the image without metadata
        image_without_metadata.save(image_path)
        print(f"Processed: {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")

def scrub_metadata(images):
    threads = []
    for image in images:
        thread = Thread(target=process_image, args=(image,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All images processed successfully.")

# Provide the directory containing the images
# Windows users will need to use a double back slash \\ example: "C:\\Users\\user\\OneDrive\\Pictures"
print("Enter in the image directory")
print("Windows users will need to use a double back slash \\\\ example: C:\\\\Users\\\\user\\\\OneDrive\\\\Pictures")
image_directory = input("Image Directory: ")

# Get a list of all supported image files in the directory
image_files = glob.glob(os.path.join(image_directory, "*.jpg")) + \
              glob.glob(os.path.join(image_directory, "*.jpeg")) + \
              glob.glob(os.path.join(image_directory, "*.png"))

scrub_metadata(image_files)