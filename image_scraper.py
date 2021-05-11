from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import shutil
import os
import argparse
from PIL import Image
import numpy as np
t0 = time.time()
count = 0

searchWordArray = ['alamy', 'dreamstime', 'dissolve', 'istock', 'canstock', 'gettyimages', '123rf', 'shutterstock',
               'featurepics', 'depositphotos', 'sciencephoto', 'photocase', 'barewalls', 'fotosearch', 'cloudstockphotos',
               'crushpixel', 'bigstock', 'sciencesource', 'fotostock', 'photovault', 'picfair', 'bigstock', 'envato']
npSearchWordArray = np.array(searchWordArray)
#header import selenium for controlling the chrome browser through webdriver
# time for tracking time
#requests we can send http/1.1 requests using python and do stuff on the web
#shutil more file operations than os
#interaction with os system
#argparse is a command line parsing tool
#numpy for vectorizing and then broadcasting string search

def VectorizeAndSearch(npSearchArray, imgLink):
    broadcast = np.char.find(imgLink, npSearchArray)
    if (np.any(broadcast > 0)): #if any value in broadcast array > 0, then a match was found during hyperthreading
        return True
    else:
        return False

#process img
def process_img(inp, img, directory):
    # process image
    response = requests.get(img, stream=True)
    im = Image.open(response.raw)
    w, h = im.size
    if (w >= 520 and h >= 520):
        print(f'Img meets requirements at {im.size} ')
        save_img(inp, img, directory)

    else:
        print(f'Img fails requirements at {im.size}')



#save image... it will overwrite any image within its naming scheme
def save_img(inp, img, directory):
    try:
        global count
        filename = inp + str(count+1) + '.jpg'
        response = requests.get(img, stream=True)
        image_path = os.path.join(directory, filename)
        with open(image_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        count += 1
        print(f'{count} Files added to directory')

    except Exception:
        pass

#the scraper engine
def find_urls(inp, url, driver, directory):
    global count
    driver.get(url) #load url
    for _ in range(500): #iterate below 500 times
        driver.execute_script("window.scrollBy(0,10000)") #executes JS window.scrollBy() method.  scroll down
        try:
            driver.find_element_by_css_selector('.mye4qd').click() #click on picture
        except:
            continue
    for j, imgurl in enumerate(driver.find_elements_by_xpath('//img[contains(@class,"rg_i Q4LuWd")]')): #find <img> web elements
        try:
            if (count < n_Images):
                imgurl.click()
                # get <img> url below
                img = driver.find_element_by_xpath(
                '//body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute(
                "src")
                #look for watermarked images using list in header and url string search (vectorized approach, no looping)
                if (VectorizeAndSearch(npSearchWordArray,img)):  # if any value in a > 0
                    print(f'Watermark found, does not meet criteria... {img}')
                    time.sleep(1.5)
                else:
                    print(f'Watermark not found...processing image... {img}')
                    process_img(inp, img, directory)
                    time.sleep(1.5)


               
            else:
                break
                print(f'{count} Images reached.  Operation successfully completed. Quitting now')
                quit()


        except:
            pass

# cmd line tool to use this python script, all variables here are global
if __name__ == "__main__": #once python script is opened in cmd prompt then __name__ variable is issued as well as it becomes __main__
    parser = argparse.ArgumentParser(description='Crawl Internet images')
    parser.add_argument('-e', '--search_engine', default='google', type=str, metavar='', help='google or bing' )
    parser.add_argument('-s', '--search', default='bananas', type=str, metavar='', help='search term')
    parser.add_argument('-d', '--directory', default='../Downloads/', type=str, metavar='', help='save directory')
    parser.add_argument('-n', '--n_Images', default=100, type=int, metavar='', help='Number of Images to scrape')
    args = parser.parse_args()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    directory = args.directory
    inp = args.search
    n_Images = args.n_Images
    if not os.path.isdir(directory):
        os.makedirs(directory)
    if (args.search_engine == 'google'):
        url = 'https://www.google.com/search?q=' + str(
        inp) + '&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947'
    elif (args.search_engine == 'bing'):
        url = 'https://www.bing.com/images/search?q=' + str(
            inp) + '&qs=n&form=QBILPG&sp=-1&pq=image&sc=8-5&cvid=40073FFB827449EF95D096B8525B4F1E&first=1&scenario=ImageBasicHover'
    find_urls(inp, url, driver, directory)
