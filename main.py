#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os, shutil
import requests
import wget

import re
from bs4 import BeautifulSoup
import cssutils

# Get the way to the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def initialization(project_name, url, page_url):
    '''Project Initialization. Download index.html'''
    response = requests.get(url=page_url, headers=headers)
    os.mkdir(f"./downloads/{project_name}")
    os.mkdir(f"./downloads/{project_name}/css")
    os.mkdir(f"./downloads/{project_name}/js")
    os.mkdir(f"./downloads/{project_name}/img")
    os.mkdir(f"./downloads/{project_name}/fonts")
    os.mkdir(f"./downloads/{project_name}/other")
    with open(f"./downloads/{project_name}/index.html",mode='w') as index_file:
        index_file.write(response.text)

def processing_tags(project_name, url):
    index_file = open(f"./downloads/{project_name}/index.html", mode='r')
    index_content = index_file.read()
    index_file.close()
    index_content = index_content.replace('href="/', f'href="{url}')
    index_content = index_content.replace('src="/', f'src="{url}')
    index_content = index_content.replace('href="css/', f'href="{url}css/')
    index_content = index_content.replace('href="img/', f'href="{url}img/')
    index_content = index_content.replace('href="style/', f'href="{url}style/')
    index_content = index_content.replace('href="image/', f'href="{url}image/')
    index_content = index_content.replace('href="styles/', f'href="{url}styles/')
    index_content = index_content.replace('href="images/', f'href="{url}images/')
    index_content = index_content.replace('src="js/', f'src="{url}js/')
    index_content = index_content.replace('src="javascript/', f'src="{url}javascript/')
    index_content = index_content.replace('src="img/', f'src="{url}img/')
    index_content = index_content.replace('src="image/', f'src="{url}image/')
    index_content = index_content.replace('src="images/', f'src="{url}images/')
    #index_file = open(f"./downloads/{project_name}/index.html",mode='w')
    #index_file.write(index_content)
    #index_file.close()
    html = BeautifulSoup(index_content, 'lxml')
    tags_link = html.find_all('link')
    tags_src = html.find_all(['script','img'])
    print("************ <link> **************")
    print(tags_link)
    hrefs = []

    for tag in tags_link:
        hrefs.append(tag["href"])
        
    print("************ href=\"\" **************")
    print(hrefs)
    
    print("************ .css **************")
    
    for href in hrefs:
        if href != url and href != url[:-2]:
            if href[-4:] == ".css":
                try:
                    wget.download(href,f"downloads/{project_name}/css/")
                except:
                    print(f"\nException occured with url:{href}\n")
            elif href[-4:] == ".png" or href[-4:] == ".jpg" or href[-4:] == ".webp" or href[-4:] == ".gif":
                    try:
                        wget.download(href,f"downloads/{project_name}/img/")
                    except:
                        print(f"\nException occured with url:{href}\n")
            else:
                try:
                    wget.download(href,f"downloads/{project_name}/other/")
                except:
                    print(f"\nException occured with url:{href}\n")
    
    print("************ <script> **************")
    #print(tags_src)
    srcs = []

    for tag in tags_src:
        try:
            srcs.append(tag["src"])
        except KeyError:
            print(f"\nException occured with tag:{tag}\n")
            
    print("************ src=\"\" **************")
    print(srcs)
    
    print("************ .css **************")
    
    for src in srcs:
        if src != url and src != url[:-2]:
            if src[-3:] == ".js":
                try:
                    wget.download(src,f"downloads/{project_name}/js/")
                except:
                    print(f"\nException occured with url:{src}\n")
            elif src[-4:] == ".png" or src[-4:] == ".jpg" or src[-4:] == "webp" :
                    try:
                        wget.download(src,f"downloads/{project_name}/img/")
                    except:
                        print(f"\nException occured with url:{src}\n")
            else:
                try:
                    wget.download(src,f"downloads/{project_name}/other/")
                except:
                    print(f"\nException occured with url:{src}\n")
    
    #print("************ <script> **************")
    #print(tags_src)

def filesort(project_name):
    os.chdir(f"./downloads/{project_name}/other/")
    for filename in os.listdir():
        if filename[-3:] == ".js":
            print(filename,f"../js/{filename}")
            shutil.move(filename,f"../js/{filename}")
        elif filename[-4:] == ".css":
            print(filename,f"../css/{filename}")
            shutil.move(filename,f"../css/{filename}")
        elif filename[-4:] == ".png" or filename[-4:] == ".jpg" or filename[-4:] == "webp" or filename[-4:] == ".gif":
            print(filename,f"../img/{filename}")
            shutil.move(filename,f"../img/{filename}")
    # Change the current working directory
    os.chdir(current_dir)


def extract_css_urls(css_text):
    urls = []
    regex = r"url\(['\"]?(.*?)['\"]?\)"

    for match in re.findall(regex, css_text):
        urls.append(match)

    return urls


def extract_images_from_index(project_name):
    index_file = open(f"./downloads/{project_name}/index.html", mode='r')
    index_content = index_file.read()
    index_file.close()
    urls = []
    soup = BeautifulSoup(index_content, 'lxml')
    # Извлечение URL-адресов из стилей внутри тега <style>
    style_tags = soup.find_all('style')
    for style_tag in style_tags:
        css_text = style_tag.string
        if css_text:
            urls += extract_css_urls(css_text)
    
    for tag in soup.find_all(['a', 'div', 'style']):
        if 'style' in tag.attrs:
            style = tag['style']
            if 'background' in style:
                if 'url(' in style:
                    url = re.search(r'url\((.*?)\)', style)
                    if url:
                        urls.append(url.group(1))
            elif 'background-image' in style:
                url = style.split('url(')[-1].strip(')')
                urls.append(url)
    # Remove empty elements
    for i,url in enumerate(urls):
        if url == "":
            urls.pop(i)
    # Downloads
    for url in urls:
        if url[-4:] == ".png" or url[-4:] == ".jpg" or url[-4:] == "webp" or url[-4:] == ".gif":
            wget.download(url,f"./downloads/{project_name}/img/")
        elif url[-5:] == ".woff":
            wget.download(url,f"./downloads/{project_name}/fonts/")
    print("\n\n*** urls in extract_images_from_index(project_name) ***")
    print(urls)



def extract_images_from_styles(project_name, target_url):
    os.chdir(f"./downloads/{project_name}/css/")
    urls = []
    for filename in os.listdir():
        with open(filename, 'r') as css_file:
            css_text = css_file.read()
        urls += extract_css_urls(css_text)
    
    # Downloads
    for url in urls:
        try:
            if url[-4:] == ".png" or url[-4:] == ".jpg" or url[-4:] == "webp" or url[-4:] == ".gif":
                if url[0] == "/":
                    url =  target_url + url[1:]
                wget.download(url,out=f"../img/")
            elif url[-5:] == ".woff":
                wget.download(url,out=f"../fonts/")
        except:
            print(f"\nException occured with url:{url}\n")
    print("\n\n*** urls in extract_images_from_styles(project_name) ***")
    print(urls)
    # Change the current working directory
    os.chdir(current_dir)


def localization_index(project_name, url):
    with open(f"./downloads/{project_name}/index.html",mode='r') as index_file:
        index_content = index_file.read()
    
    # example: url = "https://example.org/"
    
    # imgur.com
    index_content = index_content.replace('https://i.imgur.com', './img')
    
    # exotic
    index_content = index_content.replace(f'{url}source/css/lblue', './css')
    index_content = index_content.replace(f'{url}assets/css/fcss', './css')
    
    # source ./source/format/file.format
    index_content = index_content.replace(f'{url}source/img', './img')
    index_content = index_content.replace(f'{url}source/css', './css')
    index_content = index_content.replace(f'{url}source/js', './js')
    index_content = index_content.replace(f'{url}source/fonts', './fonts')
    index_content = index_content.replace(f'{url}source/font', './fonts')
    
    # assets ./assets/format/file.format
    index_content = index_content.replace(f'{url}assets/img', './img')
    index_content = index_content.replace(f'{url}assets/css', './css')
    index_content = index_content.replace(f'{url}assets/js', './js')
    index_content = index_content.replace(f'{url}assets/fonts', './fonts')
    index_content = index_content.replace(f'{url}assets/font', './fonts')
    
    # classic ./format/file.format
    index_content = index_content.replace(f'{url}img', './img')
    index_content = index_content.replace(f'{url}css', './css')
    index_content = index_content.replace(f'{url}js', './js')
    index_content = index_content.replace(f'{url}fonts', './fonts')
    index_content = index_content.replace(f'{url}font', './fonts')
    
    with open(f"./downloads/{project_name}/index.html",mode='w') as index_file:
        index_file.write(index_content)


def main():
    # project_name = "Kazuha" # input("Project: ")
    # url = "https://kazuha.store/" # input("URL: ")
    project_name = input("Project: ")
    url = input("Main URL: ")
    page_url = input("Page URL: ")
    initialization(project_name, url, page_url)
    processing_tags(project_name, url)
    filesort(project_name)
    extract_images_from_index(project_name)
    extract_images_from_styles(project_name, url)
    localization_index(project_name, url)
    input("\n\nDone!")


if __name__ == "__main__":
    main()
