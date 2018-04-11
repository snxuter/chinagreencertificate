import requests
from bs4 import BeautifulSoup
from time import sleep
from time import time
from random import randint
from IPython.core.display import clear_output
from warnings import warn


companyname = []
prices = []
peopbuys = []
addresses = []
projects = []
onlinedates = []
links = []

shop_price = []
shop_inventory = []
shop_sold = []
shop_total = []
shop_projectsize = []
shop_projecttype = []
shop_individual_Num = []
shop_individual_Time = []
shop_individual_Price = []
shop_projectN = []


start_time = time()
loops = 0



pages = [str(i) for i in range(1,104)]
#pages = [str(i) for i in range(102,103)]
#pages = [str(i) for i in range(1,3)]
for page in pages:
    pagename="http://www.greenenergy.org.cn/gctrade/shop/product/listproductCategoryId.jhtml?projectType=&province=&city=&companyId=&companyName=&startPrice=&endPrice=&keyword=&orderType=priceDesc&pageSize=5&searchProperty=&orderProperty=&orderDirection=&pageNumber="+page
    response = requests.get(pagename)
    ## Pause the loop
    sleep(randint(8,15))

    ## Monitor the loops
    loops += 1
    elapsed_time =  time() - start_time
    print('Loops:{}; Frenquency:{} loops/s'.format(loops, loops/elapsed_time))
    clear_output(wait = True)

    ## Throu a warning for non-200 status codes
    if response.status_code !=200:
        warn('Request:{}; Status code: {}'.format(loops, response.status_code))

    ## Break the loop if the number of loops is greater than expected
    if loops >102:
        warn('Number of loops was greater than expected.')
        break
    ## Parse the content of the request with BeautifulSoup
    page_html = BeautifulSoup(response.text,'html.parser')

    # Select all 5 product containers from a single page
    prodinf = page_html.find('div', class_ ='SeContent_C')
    gnctf_container = prodinf.find_all('li', class_='clearfix')

    #For every item of the five products
    for container in gnctf_container:

        name = container.find('span', class_='jtName').text
        companyname.append(name)

        price = container.find('span', class_='ww').text
        price = filter(lambda ch: ch in '0123456789.',price)
        price = float(price)
        prices.append(price)

        peopbuy = container.find('span', class_='peoP').text
        peopbuy = filter(lambda ch: ch in '0123456789.',peopbuy)
        peopbuy = int(peopbuy)
        peopbuys.append(peopbuy) 

        address = container.find('span', class_='add').text
        addresses.append(address)
        
        projectinfo =  container.find_all('p')
        projects.append(projectinfo[0].text.strip())
        onlinedates.append(projectinfo[1].text.strip())

        ## save all sub-links with purchased items to array(links)
        link = container.find('a')
        links.append(link.get('href'))


##  subroutine to open clickable sublinks and then get informations(number, date, and 
## type of RE project) about sold items
def getLinksInfo(url):
        ## 
        respones = requests.get(url)
        page_html = BeautifulSoup(respones.text,'html.parser')
        shopitem = page_html.find('div', class_='shop_xq_right_top')
        items = shopitem.find_all('li')
        sold_shop = items[8].text
        sold_shop = filter(lambda ch: ch in '0123456789.',sold_shop)
        inventory_shop = items[7].text
        inventory_shop = filter(lambda ch: ch in '0123456789.',inventory_shop)
        price_shop =  items[1].find('span', id='dj').text
        ## get the project infor. (project size and type)
        salecontent = page_html.find('div', class_='shop_xxnr1')
        saleinfo = salecontent.find_all('li', class_='gsmc_1')
        REtype = saleinfo[1].text.strip()
        REsize = saleinfo[3].text.strip()
        return sold_shop, inventory_shop, price_shop, REtype, REsize

##  subroutine to open clickable sublinks and then get informations(number, date, and 
## type of RE project) about sold items
def getLinksInfoPurchase(url):
        ## create two arrays to store number and date of sold items
        saleNum = []
        saleList = []
        ## 
        respones = requests.get(url)
        page_html = BeautifulSoup(respones.text,'html.parser')
        shopitem = page_html.find('div', class_='shop_xq_right_top')
        items = shopitem.find_all('li')
        sold_shop = items[8].text
        sold_shop = filter(lambda ch: ch in '0123456789.',sold_shop)
        inventory_shop = items[7].text
        inventory_shop = filter(lambda ch: ch in '0123456789.',inventory_shop)
        price_shop =  items[1].find('span', id='dj').text
        ## get the project infor. (project size and type)
        salecontent = page_html.find('div', class_='shop_xxnr1')
        saleinfo = salecontent.find_all('li', class_='gsmc_1')
        REtype = saleinfo[1].text.strip()
        REsize = saleinfo[3].text.strip()
        ## get the sale infor. (number of items sold, purchase time)
        salelistcontent = page_html.find('div', id='shop_xxnr3')
        salelistinfo = salelistcontent.find_all('tr',{"class":["one","two"]})
        for infoSa in salelistinfo:
            infotable = infoSa.find_all('td')
            ##print infotable[2].text
            saleNum.append(int(infotable[2].text))
            saleList.append(infotable[3].text)
            ##print int(infotable[2].text), infotable[3].text
        return sold_shop, inventory_shop, price_shop, REtype, REsize, saleNum, saleList

### on each page, there are clickable buttons for each green certificate. Here we are
### going to get information from these sublinks of each item.
hostname = 'http://www.greenenergy.org.cn'
i = 0
## projectN tracks the series NO. of GC projects on the website
projectN = 0
NumofCerti = []
purchasetime = []
for link in links:
    web = hostname+link
    ## links has the same series NO. with peopbuys (and others)
    NumofPeobuy = peopbuys[i]
    if NumofPeobuy >0:
        a, b, c, pjtype, pjsize, NumofCerti, purchasetime = getLinksInfoPurchase(web)
        shop_sold.append(int(a))
        shop_inventory.append(int(b))
        shop_price.append(float(c))
        shop_total.append(int(a)+int(b))
        shop_projecttype.append(pjtype)
        shop_projectsize.append(pjsize)
        ### shop_individual_Num and sho_individual_Time have the same array size
        for numvalue in NumofCerti:
            shop_individual_Num.append(numvalue)
            ### to track the Series NO. of each purchase activity
            shop_projectN.append(projectN)
            shop_individual_Price.append(float(c))
        for timevalue in purchasetime:
            shop_individual_Time.append(timevalue)
    else:    
        a, b, c, pjtype, pjsize = getLinksInfo(web)
        shop_sold.append(int(a))
        shop_inventory.append(int(b))
        shop_price.append(float(c))
        shop_total.append(int(a)+int(b))
        shop_projecttype.append(pjtype)
        shop_projectsize.append(pjsize)
    i +=1
    projectN +=1




import pandas as pd
### list of green certificates, date of issued, price, and company information 
test_pd =  pd.DataFrame({'company': companyname,
                            'price':prices,
                            'No.People':peopbuys,
                            'address':addresses,
                            'project':projects,
                            'onlinedate':onlinedates,
                            'project type':shop_projecttype,
                            'project size':shop_projectsize,
                            'Inventory':shop_inventory,
                            'Sold':shop_sold,
                            'ShopPrice':shop_price,
                            'TotalGC':shop_total})
### to save to excel file "greencft.xlsx" of information of green certificates listed on 102 pages
Gcertif =  test_pd[['company','price','No.People','address','project','onlinedate','project type', 'project size', 'Inventory', 'Sold', 'ShopPrice', 'TotalGC']]
import openpyxl
Gcertif.to_excel('greencftV2.xlsx')

### save statistic data to values.xlsx file
statisticmatrix = test_pd[['Inventory', 'Sold', 'ShopPrice','TotalGC']]
statisticmatrix.to_excel('valuesV2.xlsx')

##  to save purchase record into excel file purchaserecord.xlsx
purchaseinfo = pd.DataFrame({'NumPurchased:': shop_individual_Num,
                            'TimePurchased:': shop_individual_Time,
                            'PricePurchased:':shop_individual_Price,
                            'Series NO.:': shop_projectN})
if shop_individual_Num:
    purchaseinfo.to_excel('purchaserecord.xlsx')
