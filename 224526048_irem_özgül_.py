beautifulsoup 
requests

from bs4 import BeautifulSoup as bs
import requests

sayfa = requests.get("https://onedio.com/yasam/astroloji")

sayfa_icerik = bs(sayfa.text,"html.parser")

gerekli_kisim =sayfa_icerik.findAll("div",{"class":"col c-ftohbr order-13 order-sm-15"})


for i in gerekli_kisim:
    haberler = i.find("div",{"class":"post t-2 t-2-1"})
    
 https://onedio.com/yasam/astroloji= haberler.find("a")
    print(haber_link_ve_baslik.text.strip())
    print(https://onedio.com/yasam/astroloji["href"])
    haber_listesi.append(
      (haber_link_ve_baslik["href"],
       haber_link_ve_baslik.text.strip())
      )
  
print(haber_listesi[0][1])
print(haber_listesi[1][1])
print(haber_listesi[2][1])
print(haber_listesi[3][1])

