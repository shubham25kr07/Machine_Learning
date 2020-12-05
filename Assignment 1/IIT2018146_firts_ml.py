import requests
from bs4 import BeautifulSoup, Comment
import re
import numpy as np
import pandas as pd
import urllib.request, urllib.parse, urllib.error 
import csv


csvpath="data.csv"


def save_data(hotel_name,hotel_cityname,hotel_countryname,hotel_starrating,hotel_price,hotel_amenities,hotel_description):
	with open(csvpath, 'a+') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([hotel_name,hotel_cityname,hotel_countryname,hotel_starrating,hotel_price,hotel_amenities,hotel_description])



save_data("hotel_name","hotel_cityname","hotel_countryname","hotel_starrating","hotel_price","hotel_amenities","hotel_description")

#===========================================================================================================================================#

def Parsewebpage(city_url,city_name,country_name):

	j=0
	for i in city_url:
		URL2=i
		header2={
		'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
		}
		fhand2 = requests.request("GET", URL2, headers=header2)
		soup2 = BeautifulSoup(fhand2.text, 'html.parser')


		# all hotellist in a particular city
		hotel_list=[]
		for x in soup2.findAll('div',attrs={'class','listingRowOuter'}):
			hotel_list.append(x)

		# for each hotel 
		for  hotel in hotel_list:

			hotel_name=""
			hotel_cityname=""
			hotel_countryname=""
			hotel_starrating=""
			hotel_price=""
			hotel_amenities=""
			hotel_description=""

			#hotel_name
			for x in hotel.findAll('p',class_="latoBlack font22 blackText appendBottom12"):
				hotel_name=x.get_text()


			#hotel_cityname
			#hotel_countryname
			hotel_cityname=city_name[j]
			hotel_countryname=country_name[j]


			#hotel_starrating
			rr= hotel.find('div',attrs={'class':'noShrink appendLeft20'})
			if rr.find('div',attrs={'class' : 'makeFlex right appendBottom5 hrtlCenter whiteText'}):
				rrr= rr.find('div',attrs={'class' : 'makeFlex right appendBottom5 hrtlCenter whiteText'})
				if rrr.find('span',attrs={'itemprop' : 'ratingValue'}):
					rating= rrr.find('span',attrs={'itemprop' : 'ratingValue'})
					hotel_starrating=rating.get_text()
			else:
				hotel_starrating="NIL"


			#hotel_description
			for x in hotel.findAll('div',class_="appendBottom10 font12 darkText"):
				y=x.get_text().replace('\n','')
				word=y.split()
				string =' '.join(word)
				hotel_description=string


			#hotel_amenities
			for x in hotel.findAll('ul',class_="amenList darkText"):
				listt=[]
				for jj in x.findAll('li'):
					y=jj.find('span').get_text()
					listt.append(y)
				hotel_amenities=','.join(listt)


			#hotel_price
			for x in hotel.findAll('p',class_="latoBlack font26 blackText appendBottom5"):
				y=x.get_text().replace('\n','')
				word=y.split()
				hotel_price=word[1]

			save_data(hotel_name,hotel_cityname,hotel_countryname,hotel_starrating,hotel_price,hotel_amenities,hotel_description)
			# print(hotel_name+" "+hotel_cityname+" "+hotel_countryname+" "+hotel_starrating+" "+hotel_price+" "+hotel_amenities+" "+hotel_description)

		j=j+1

#================================================================================================================================================#

URL1="https://www.makemytrip.com/hotels/"
header1={
	'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
}

fhand1=requests.request("GET", URL1, headers=header1)
soup1 = BeautifulSoup(fhand1.text, 'html.parser')



retrive_data=[]
city_name=[]
country_name=[]
city_url=[]


for i in soup1.findAll('ul', class_="makeFlex column font12"):
	for j in i.findAll('li',class_="appendBottom5"):
		for k in j.findAll('a',class_="darkGreyText"):
			retrive_data.append(k)



for i in retrive_data:
	#print(i)
	x=i.get('href')
	y=i.get_text()
	word=y.split();
	if len(word)==3:
		if word[0]=="Hotels":
			if word[1]=="In":
				city_name.append(word[2])
				country_name.append("India")
				city_url.append(x)
				#print(x)

Parsewebpage(city_url,city_name,country_name)

city_name.clear()
country_name.clear()
city_url.clear()
retrive_data.clear()

#================================================================================================================================#

URL11="https://www.makemytrip.com/hotels-international/"
header11={
	'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
}

fhand11=requests.request("GET", URL11, headers=header11)
soup11 = BeautifulSoup(fhand11.text, 'html.parser')

for i in soup11.findAll('ul', class_="makeFlex column font12"):
	for j in i.findAll('li',class_="appendBottom5"):
		for k in j.findAll('a',class_="darkGreyText"):
			retrive_data.append(k)


for i in retrive_data:
	#print(i)
	x=i.get('href')
	y=i.get_text()
	word=y.split();
	if len(word)==3:
		if word[0]=="Hotels":
			if word[1]=="In":
				# print(word)
				city_name.append(word[2])
				xx=x.split('/')
				# print(xx[4])
				country_name.append(xx[4])
				city_url.append(x)


Parsewebpage(city_url,city_name,country_name)


city_name.clear()
country_name.clear()
city_url.clear()
retrive_data.clear()

#=====================================================================================================================================#

# print(soup1.prettify())