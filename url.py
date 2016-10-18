from pyshorteners import Shortener

url = 'http://www.google.com'
api_key = 'AIzaSyAU_zzFUPzICsSUuwpBHE-OUaqDwN-4JaQY'
shortener = Shortener('Google', api_key=api_key)
print("My short url is {}".format(shortener.short(url)))

