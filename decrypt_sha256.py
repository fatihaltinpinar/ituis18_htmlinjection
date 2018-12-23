from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

myUrl = 'https://md5decrypt.net/en/Api/api.php?email=batuhanfaik@hotmail.com&code=2dc2a95396e8186a&hash_type=sha256&hash=7ca6e264880d73246ffc076f15b42a2aa5857021e4f3beb06c3c83332ce59722'
shaPage = urlopen(myUrl)
shaHTML = shaPage.read()
shaPage.close()

shaSoup = soup(shaHTML, "html.parser")

print(shaSoup)