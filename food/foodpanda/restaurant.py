from bs4 import BeautifulSoup
import socket
import requests
from re import sub
from re import search
from locality import find_foodpanda_valid_locality,find_locality

cityName = 'Bangalore'
localities = find_foodpanda_valid_locality(cityName,find_locality(cityName))
def find_all_restaurants(loca):
	searchurl = "https://www.foodpanda.in/location-suggestions?cityId=11&area=%s" % (loca[0][1])
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	data = BeautifulSoup(str(soup.find_all("div",{'class':'vendor__title'})))
	restaurants = []
	for link in data.find_all("a"):
		uniqueId = search('/restaurant/(.+?)">', str(link)).group(1)
		restaurantName = link.text
		restaurants.append((str(uniqueId),str(restaurantName)))
	return restaurants

def restaurant_info(restaurantsData):
	searchurl = "https://www.foodpanda.in/restaurant/%s" % (restaurantsData[0][0])
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	restaurantsData[0] += (str(soup.find('address').text),)
	restaurantsData[0] += ((soup.find('i',{'class':'stars'}))['content'],)
	details = sub("(?m)^\s+","",str(soup.find('ul',{'class':'cart__empty__elements'}).text)).split('\n')
	print details
	deliveryFee = None
	deliveryTime = None
	paymentOption = None
	deliveryMinAmount = None
	Voucher = None
	picupTime = None
	for index,item in enumerate(details):
		if(item == 'Delivery time:'):
			deliveryTime = details[index+1]
		elif(item == 'Online payment available'):
			paymentOption = item
		elif(item == 'Delivery fee'):
			deliveryFee = details[index+1]
		elif(item == 'Delivery min.:'):			
			deliveryMinAmount = details[index+1]
		elif(item == 'Accepts Vouchers'):
			Voucher = item
	if(soup.find("dt",{"class":"vendor-pickup-time"}) != None ):
		soup = BeautifulSoup(soup.find("dt",{"class":"vendor-pickup-time"}))
		data = soup.find('dd').text
		picupTime = (sub("(?m)^\s+","",str(data).split("\n"))).pop(0)
	restaurantsData[0] += (deliveryFee,deliveryTime,picupTime,deliveryMinAmount,paymentOption,Voucher,searchurl,localities[0][0],)
	print restaurantsData

	#for index,item in enumerate(restaurantsData):
	#	soup.
def food_info(restaurantsData):
	searchurl = "https://www.foodpanda.in/restaurant/%s" % (restaurantsData[0][0])
	f = requests.get(searchurl)
	html = f.text
	soup = BeautifulSoup(html)
	for data in soup.find_all('div',{'class':'menu-item__content-wrapper'}):
		soup2 = BeautifulSoup(str(data))
		dish_name = soup2.find('div', {'class': 'menu-item__title'}).text
		for val in soup2.find_all('article', {'class': 'menu-item__variation'}):
			print (sub("(?m)^\s+","",dish_name)), (sub("(?m)^\s+","",val.text))
		# print (sub("(?m)^\s+","",data.text))
	


restaurantsData = find_all_restaurants(localities)
restaurant_info(restaurantsData)
food_info(restaurantsData)