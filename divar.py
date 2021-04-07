import requests as req
from bs4 import BeautifulSoup as BS
import time

mainUrl = "https://divar.ir/s"
city    = (input("specify city (example: 'tehran' or 'mashhad' ...) : ")).lower()
# city    = "tehran"
category= (input("specify category (example: 'website-services' or 'mobile-phones' or 'it-computer-jobs' ...) : ")).lower()
# category= "website-services"
referer = "%s/%s/%s"%(mainUrl, city, category)
# referer = "https://divar.ir/s/tehran/website-services"
startPage = int(input("Start page: "))

lastPage = ""

for i in range(startPage, 100):
    phones = []
    url = "https://divar.ir/s/%s/%s?page=%d"%(city, category, i)
    reqToGetTokens = req.get(url)
    if "post-card" not in reqToGetTokens.text:
        break

    contentAsBS = BS(reqToGetTokens.text, 'html.parser')
    post_cards = contentAsBS.select(".post-card-item .kt-post-card")

    print("#### Page %d"%i)

    for j in range(len(post_cards)):
        reqToGetPhone = req.get("https://api.divar.ir/v5/posts/%s/"%post_cards[j]['href'].split("/")[-1])
        if reqToGetPhone.ok == False:
            lastPage = "Error at page %d item %d"%(i, j + 1)
            break
        if '09' in reqToGetPhone.json()['widgets']['contact']['phone']:
            phones.append(reqToGetPhone.json()['widgets']['contact']['phone'])
        else:
            phones.append("only chat")
        print("### token -> %s"%post_cards[j]['href'].split("/")[-1])
        print("### phone -> %s"%phones[j])
        # tokens.append(post_cards[j]['href'].split("/")[-1])
        time.sleep(3)
    if lastPage != "":
        break
    with open('divar-%s-%s.txt'%(city, category), 'a') as f:
        for phone in phones:
            f.write("%s\n"%phone)
if lastPage: print(lastPage)            
