import os
import time
import requests
from selenium import webdriver


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

        # build the google query

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))   #pasting q as queryulr will be searched inside the cromedriver

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)              # dis will js scroll down along the web page

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()      #only if we click on an image on the web pageit will pop up
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')   #insect element on page-for di tag 2 hfer available , we need to choose which we want for we run a for loop
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):   # checks if d source (src) holds d htt
                    image_urls.add(actual_image.get_attribute('src'))   #from d 2 href 1 which we need is added here

            image_count = len(image_urls)   #counts no of urls of images in d list

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break                #if 8 images are downloaded den break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path:str,url:str, counter):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):      # if folder exist here so if not condition dont work,if not exist it will create
        os.makedirs(target_folder)
# below line will just open a web browser
    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)  # wen downloading image wait for 0.5 ms b/w 2 images

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1


# My Chrome version - Version 85.0.4183.102
# pip install -e requirements.txt

# How to execute this code
# Step 1 : pip install selenium. pillow, requests
# Step 2 : make sure you have chrome/mozilla installed on your machine
# Step 3 : Check your chrome version ( go to three dot then help then about google chrome )
# Step 4 : Download the same chrome driver from here  " https://chromedriver.storage.googleapis.com/index.html "
# if same version not found ,go for the nearest available,download and add the zip file in the same folder(project)
# Step 5 : put it inside the same folder of this code


DRIVER_PATH = './chromedriver.exe'
search_term = 'birds'
# num of images you can pass it from here  by default it's 10 if you are not passing
number_images = 8
search_and_download(search_term=search_term, driver_path=DRIVER_PATH , number_images=number_images)
# if we r not givin number_images=number_images, den the default num(10-given on top) of imaged will b saved