
# coding: utf-8

# In[3]:


import requests
import pandas
from bs4 import BeautifulSoup

proxies = {
  'https': 'http://94.79.121.4:8080',
}

r = requests.get("https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", proxies=proxies)

c = r.content
soup = BeautifulSoup(c, "html.parser")
page_nr = soup.find_all("a", {"class": "Page"})[-1].text
print(page_nr)


# In[4]:


list_of_dicts = []
base_url = "https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

for page in range(0, int(page_nr)*10, 10):
    r = requests.get(base_url + str(page) + ".html", proxies=proxies)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all_divs = soup.find_all("div", {"class":"propertyRow"})


    for item in all_divs:
        house_dict = {}

        house_dict["Address"] = item.find_all("span", {"class":"propAddressCollapse"})[0].text
        try:
            house_dict["Locality"] = item.find_all("span", {"class":"propAddressCollapse"})[1].text
        except:
            house_dict["Locality"] = None
        house_dict["Price"] = item.find("h4", {"class":"propPrice"}).text.replace("\n", "").replace(" ", "")

        try:
            house_dict["Beds"] = item.find_all("span", {"class":"infoBed"}).text
        except:
            house_dict["Beds"] = None

        try:
            house_dict["Area"] = item.find_all("span", {"class":"infoSqFt"}).text
        except:
            house_dict["Area"] = None

        try:
            house_dict["Full Baths"] = item.find_all("span", {"class":"infoValueFullBath"}).text
        except:
            house_dict["Full Baths"] = None

        try:
            house_dict["Half Baths"] = item.find_all("span", {"class":"infoValueHalfBath"}).text
        except:
            house_dict["Half Baths"] = None

        for column_group in item.find_all("div", {"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}), column_group.find_all("span", {"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    house_dict["Lot Size"] = feature_name.text

        list_of_dicts.append(house_dict)
        

df = pandas.DataFrame(list_of_dicts)


# In[5]:


df


# In[6]:


df.to_csv("PagesOutput.csv")

