"""
download_file(file_url, save_directory): This function is responsible for downloading an individual file given its URL and saving it to the specified directory. It takes two parameters:
file_url: The URL of the file to be downloaded.
save_directory: The directory where the downloaded file will be saved.

The function sends a GET request to the file_url, retrieves the file content, and saves it to the specified save_directory.

download_files_from_thread(thread_url, save_directory): This function is the main function that downloads all the files (images and webms) from a 4chan thread. It takes two parameters:

thread_url: The URL of the 4chan thread from which files will be downloaded.
save_directory: The directory where the downloaded files will be saved.

The function sends a GET request to the thread_url and extracts the image and webm URLs using regular expressions. For each file URL, it spawns a new thread using the Thread class, calling the download_file function to download the file. The function waits for all threads to finish before printing a completion messag

"""

import os
import requests
import re
from threading import Thread

def download_file(file_url, save_directory):
    file_url = 'https:' + file_url
    filename = os.path.join(save_directory, os.path.basename(file_url))

    #send a GET request to the file URL
    file_response = requests.get(file_url)

    #save the file to the specified directory
    with open(filename, 'wb') as file:
        file.write(file_response.content)

    print(f"Downloaded: {filename}")


def download_files_from_thread(thread_url, save_directory):
    #create the save directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    #send a GET request to the thread URL
    response = requests.get(thread_url)

    #extract image and webm URLs using regex
    file_urls = re.findall(r'href="(//is2\.4chan\.org/\w+/\d+\.(?:\w+|webm))"', response.text)

    #create and start a thread for each file download
    threads = []
    for file_url in file_urls:
        t = Thread(target=download_file, args=(file_url, save_directory))
        t.start()
        threads.append(t)

    #wait for all threads to finish
    for t in threads:
        t.join()

    print("All files downloaded!")


#must be a 4chan thread.
#directory will be created if not already existing.
thread_url = input("Input Thread: ")
save_directory = input("Input Dump Directory: ")
download_files_from_thread(thread_url, save_directory)