from bs4 import BeautifulSoup
import socket
import requests
from re import sub,search
from city import city_List


cityList = city_List()
def find_locality(cityName):
	searchurl = "http://www.commonfloor.com/localities/index/city/%s" % (cityName)
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	localities=[]
	data = soup.find('tbody')
	data= str(sub("(?m)^\s+", "", str(data.text)))
	data = data.split('\n')
	for item in data:
		if item.isalpha():
			localities.append(item)
	return localities
def find_foodpanda_valid_locality(cityName,localities):
	foodpanda_locality = []
	searchurl = "https://www.foodpanda.in/location-suggestions?cityId=11&area=Koramangala"
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	if(soup.find('h1',{'class':'h2'})):
		heading = sub(":","",soup.find('h1',{'class':'h2'}).text)
		heading = heading.strip()
		if heading=="Suggestions":		
			tempraroy_list = []
			for data in soup.find_all('a',{'class':'list-group-item'}):
				tempraroy_list.append(search('area_id=(.+?)">', str(data)).group(1))
			for item in tempraroy_list:
				foodpanda_locality.append((item,))
			tempraroy_list[:] = []
			for data in soup.find_all('div',{'class':'content-block location-suggestions'}):
				tempraroy_list= sub("(?m)^\s+","",data.text).split('\n')
			tempraroy_list.pop(0) 												# poping "Suggestion" string
			tempraroy_list.pop(len(tempraroy_list)-1)				 							# poping whitespace
			for cityTuple in cityList:
				if(cityTuple[1]==cityName):
					for index,locality in enumerate(tempraroy_list):
						searchurl= 'http://www.foodpanda.in/restaurants?area_id=%s' % (foodpanda_locality[index][0]) 
						foodpanda_locality[index] += ((str(locality),str(cityTuple[0]),searchurl,))
			return foodpanda_locality
	else:
		print "Papa Jones"

loca = find_locality('Bangalore')
find_foodpanda_valid_locality('Bangalore',loca)
