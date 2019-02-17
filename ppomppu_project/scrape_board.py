#! /usr/bin/python3
# -*- coding:utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from requests import get

file_read = open('/home/pi/project/ppomppu_project/num.txt', 'r', encoding='UTF8')
file_write = open('/home/pi/project/ppomppu_project/num.txt', 'a', encoding='UTF8')

site = 'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu'
r = get(site)
soup = BeautifulSoup(r.content.decode('euc-kr','replace'), "html.parser")

exam = soup.findAll("tr", {"class":"list1"})

for i in range(0,10):
    number=exam[i].find('td', {'class':'eng list_vspace'}).text
    title=exam[i].find('font').text
    recommendation=exam[i].find('td', {'class': 'eng list_vspace'}).find_next('td', {'class': 'eng list_vspace'}).find_next('td',{'class': 'eng list_vspace'}).text
    reco_num=recommendation.split('-')

    if len(reco_num) == 1:
        continue

    if int(reco_num[0]) >= 10:
        print("번호:"+number.strip()+",  제목:"+title+",  추천수:"+reco_num[0])
        url_address="http://www.ppomppu.co.kr/zboard/"
        url_address += exam[i].find('a').find_next('a').find_next('a')['href']
        print(url_address)
        payload = "{'text': '" + title + ", 추천수:" + reco_num[0] + "\n" + url_address + "'}"

        num_dup = False

        for line in file_read:
            if number.strip() in line:
                num_dup = True
                break

        if num_dup==False:
            r = requests.post("https://hooks.slack.com/services/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", data=payload.encode('utf-8'))
            print(number.strip(), file=file_write)


exam1 = soup.findAll("tr", {"class":"list0"})

for i in range(0,10):
    number=exam1[i].find('td', {'class':'eng list_vspace'}).text
    title=exam1[i].find('font').text
    recommendation=exam1[i].find('td', {'class': 'eng list_vspace'}).find_next('td', {'class': 'eng list_vspace'}).find_next('td',{'class': 'eng list_vspace'}).text
    reco_num=recommendation.split('-')

    if len(reco_num) == 1:
        continue

    if int(reco_num[0]) >= 10:
        print("번호:"+number.strip()+",  제목:"+title+",  추천수:"+reco_num[0])
        url_address = "http://www.ppomppu.co.kr/zboard/"
        url_address += exam1[i].find('a').find_next('a').find_next('a')['href']
        print(url_address)

        payload = "{'text': '" + title + ", 추천수:" + reco_num[0] + "\n" + url_address + "'}"

        num_dup = False

        for line in file_read:
            if number.strip() in line:
                num_dup = True
                break

        if num_dup == False:
            r = requests.post("https://hooks.slack.com/services/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",data=payload.encode('utf-8'))
            print(number.strip(), file=file_write)

file_read.close()
file_write.close()

