from lxml import etree
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import argparse
from halo import Halo 
import random


driver_path = "/home/kali/Downloads/geckodriver"
find_xpath = "//span[@class='spec-asset-identifier break-words']/strong"


def enum(driver, url):
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    # print(html)
    res = etree.HTML(html)
    # print(res)
    ress  = res.xpath(find_xpath)
    res_list = [i.text for i in ress]
    return res_list


def process_file(driver, filename, output_file):
    try:
        with open(filename, "r") as urls, open(output_file, "a") as output, Halo(text="Loading...", spinner="dots") as loading:
            for url in urls:
                url = url.strip()
                if url:
                    loading.start(f"Enumerating {url}")
                    res = enum(driver, url)
                    time.sleep(random.randint(1,10)) # may misinterpret as ddos
                    loading.stop()
                    res_str = "\n".join(str(i) for i in res)
                    print(res_str) 
                    output.write(res_str)
    except FileNotFoundError:
        print("File not found!")
        exit()


def main():
    parser = argparse.ArgumentParser(description="Dumping xpath variable from website(s)")
    parser.add_argument("-u", "--url", type=str, help="url to dump")
    parser.add_argument("-f", "--file", type=str, help="file path of urls")
    parser.add_argument("-o", "--output", type=str, help="output file path", default="output.txt")
    args = parser.parse_args()

    url = args.url
    file = args.file
    output = args.output

    # setup browser
    s = Service(driver_path)
    options = Options()
    options.add_argument("--headless");
    driver = webdriver.Firefox(service=s, options=options)

    if url:
        with Halo(text="Loading...", spinner="dots") as loading:
            loading.start(f"Enumerating {url}...")
            res = enum(driver, url)
            loading.stop()
            print("\n".join(str(i) for i in res)) 
    elif file:
        process_file(driver, file, output)

    driver.quit()


if __name__ == "__main__":
    main()
