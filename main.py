# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable
import csv



def worker_thread(search_key):
    image_scraper = GoogleImageScraper(
        webdriver_path, 
        image_path, 
        search_key, 
        number_of_images, 
        headless, 
        min_resolution, 
        max_resolution, 
        max_missed)
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls, keep_filenames)

    #Release resources
    del image_scraper

if __name__ == "__main__":
    records = []
    # opening the CSV file
    with open('Car_Models_new.csv', mode ='r')as file:
      # reading the CSV file
      csvFile = csv.reader(file)

      # displaying the contents of the CSV file
      for line in csvFile:
        records.append(line)
    records = records[1:]
    car_brands_to_update = ["Land Rover", "Alfa Romeo", "Lucid Motors", "Tata Motors"]
    for record in records:
      if record[2] in car_brands_to_update:
        record[2] = record[2].replace(' ', '_')

    joined_list = [record[2] + ' ' + record[3] for record in records]
    # print(joined_list[15])
    # print(len(joined_list))
    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    # search_keys = list(set(["Mahindra Alturas G4","t-shirt"]))
    search_keys = joined_list[354:]
    #Parameters
    number_of_images = 2                # Desired number of images
    headless = True                     # True = No Chrome GUI
    min_resolution = (0, 0)             # Minimum desired image resolution
    max_resolution = (9999, 9999)       # Maximum desired image resolution
    max_missed = 10                     # Max number of failed images before exit
    number_of_workers = 4               # Number of "workers" used
    keep_filenames = False              # Keep original URL image filenames
    #Run each search_key in a separate thread
    #Automatically waits for all threads to finish
    #Removes duplicate strings from search_keys
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, search_keys)
