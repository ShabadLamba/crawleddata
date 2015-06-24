from bs4 import BeautifulSoup
import socket
import requests
from re import sub

def city_List():
	cityList= []
	searchurl = "https://www.foodpanda.in"
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	string = ''
	for data in soup.find_all("select",{'id':'cityId'}):
		string += str(data)
	string = sub("option", "", string)
	string = sub("</option>", "", string)
	string = sub(">", "", string)
	string = sub("<", "", string)
	string = sub("value=", "", string)
	string= string.split('/')
	string= string[1:len(string)-2]
	string.pop(10)
	for item in string:
		item = sub(" ", "", item)
		item =  item.split("\"")
		cityList.append((item[1],item[2],searchurl))
	f = open("outputcity.txt",'w')
	f.write(str(cityList))
	f.close()
	return cityList
city_List()