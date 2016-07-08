# Crawler-to-scrape-data-from-www.tfod.in-and-creating-a-database-using-pymongo
import requests
from bs4 import BeautifulSoup
import re
import pymongo
from pymongo import MongoClient as Connection
pages = []

#for page method
firmUrl = []

#for firmProfile method
name = []
firmImageUrl = []
designation = []
email = []
website = []
phone = []
expertise = []
aboutMe = []
personalLocation = []
personalEmail = []
personalAddress = []
workProfile = []
workLocation = []
workEmail = []
workAddress = []
projectsPageUrl = []

#for firmProjectsGalleryPageLink
projectGalleryUrlList = []
projectGalleryTitleList = []
projectGalleryImagesUrlsList = []
projectGalleryImagesTitlesList = []

#for Image Gallery
projectGalleryTitleList1 = []


for i in range(1,25):
    pages.append('https://www.tfod.in/professionals/design-consultants/p/' + str(i))

def Page(url):
    
    try:
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    except FileNotFoundError:
        req = requests.get(url)
        req.raise_for_status()
        response = open(url.replace('https://','').replace('.','-').replace('/','-') + '.html', 'wb')
        for chunk in req.iter_content(100000):
            response.write(chunk)
        response.close()
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    
    for data in soup.findAll('div', {'class' : 'profile-name'}):
        if 'https://www.tfod.in' + data.find('a').attrs['href'].replace('../../..', '') in firmUrl:
            pass
        else:
            firmUrl.append('https://www.tfod.in' + data.find('a').attrs['href'].replace('../../..', ''))

def firmProfile(firmUrl):
    
    try:
        soup = BeautifulSoup(open(firmUrl.replace('/', '').replace('.', '') + '.html'), 'lxml')
    except FileNotFoundError:
        req = requests.get(firmUrl, verify = False)
        response = open(firmUrl.replace('/', '').replace('.', '') + '.html', 'wb')
        for chunk in req.iter_content(100000):
            response.write(chunk)
        response.close()
        soup = BeautifulSoup(open(firmUrl.replace('/', '').replace('.', '') + '.html'), 'lxml')
    
    firmImageUrl.append('https://www.tfod.in/' + soup.find('img', {'id' : 'PublicProfileImg'}).attrs['src'])
    
    projectsPageUrl.append('https://www.tfod.in/' + soup.find('a', {'id' : 'a_PublicProjects'}).attrs['href'])
    
    for data in  soup.findAll('div', {'class' : 'public-name-panel'}):
        name.append(data.find('h1',{'id' : 'ContentPlaceHolder2_h1_UserName'}).text)
        try:
            designation.append(data.find('div', {'id' : 'ContentPlaceHolder2_div_EMPStatus'}).find('span').text)
        except AttributeError:
            designation.append('Not Specified')
    
    for data in soup.findAll('div', {'class' : 'designation-experties'}):
        cells = data.find('div', {'class' : 'designation-about float_left'}).findAll('div', {'class' : 'public-contact-block'})
        email.append(cells[0].find('div', {'id' : 'ContentPlaceHolder2_div_UserEmail'}).find('a').text)
        website.append(cells[1].find('div', {'id' : 'ContentPlaceHolder2_div_UserWebSite'}).find('a').text)
        phone.append(cells[2].find('div', {'id' : 'ContentPlaceHolder2_div_UserPhone'}).find('a').text)
        expertise.append(data.find('div', {'id' : 'ContentPlaceHolder2_div_Experties'}).find('span', {'id' : 'ContentPlaceHolder2_span_Experties'}).text)
    
    for data in soup.findAll('div', {'class' : 'personal-work-profile-block'}):
        for item in data.find('div', {'class' : 'public-personal-block'}).findAll('div', {'id' : 'AbouMeDiv'}):
            aboutMe.append(item.find('div', {'class' : 'less-more-block'}).find('p').text.replace('\n\n', ' '))
        for item in data.find('div', {'class' : 'public-personal-block'}).findAll('div', {'class' : 'public-personal-address'}):
            personalLocation.append(item.find('dd', {'id' : 'ContentPlaceHolder2_dd_UserLocation'}).text)
            personalEmail.append(item.find('dd', {'id' : 'ContentPlaceHolder2_dd_UserEmail'}).text)
            personalAddress.append(item.find('dd', {'id' : 'ContentPlaceHolder2_dd_UserAddress'}).text)
        
        for item in data.find('div', {'class' : 'public-work-block'}).findAll('div', {'id' : 'WorkProfileDiv'}):
            workProfile.append(item.find('div', {'class' : 'less-more-block'}).find('p').text.replace('\n\n', ' '))
        for item in data.find('div', {'class' : 'public-work-block'}).findAll('div', {'class' : 'public-work-address'}):
            workLocation.append(item.find('dd', {'id' : 'ContentPlaceHolder2_dd_BusinessLocation'}).text)
            workEmail.append(item.find('dd', {'id' : 'ContentPlaceHolder2_dd_BusinessEmail'}).text)
            workAddress.append(item.find('dd', {'id' : 'ContentPlaceHolder2_dd_BusinessAddress'}).text)
        
        
        
def firmProjectsGalleryPageLink(url):
    
    try:
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    except FileNotFoundError:
        req = requests.get(url)
        req.raise_for_status()
        response = open(url.replace('https://','').replace('.','-').replace('/','-') + '.html', 'wb')
        for chunk in req.iter_content(100000):
            response.write(chunk)
        response.close()
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    
    projectGalleryUrl = []
    projectGalleryTitle = []
    projectGalleryTitle1 = []
    projectGalleryImagesUrls = []
    projectGalleryImagesTitles = []
    
    
    for data in soup.find('table', {'class' : 'project-table'}).findAll('td'):
        projectGalleryUrl.append('https://www.tfod.in/' + data.find('div', {'class' : 'photoMeta'}).find('div', {'class' : 'PhotoTitle'}).find('a').attrs['href'])
        projectGalleryTitle.append(data.find('div', {'class' : 'photoMeta'}).find('div', {'class' : 'PhotoTitle'}).find('a').text)
    
    projectGalleryUrlList.append(projectGalleryUrl)
    projectGalleryTitleList.append(projectGalleryTitle)
    
    for link in projectGalleryUrl:
        projectGalleryImagesUrls.append(ImageGallery(link)[0])
        projectGalleryImagesTitles.append(ImageGallery(link)[1])
    
    projectGalleryImagesUrlsList.append(projectGalleryImagesUrls)
    projectGalleryImagesTitlesList.append(projectGalleryImagesTitles)
    
    for url in projectGalleryUrl:
        try:
            soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
        except FileNotFoundError:
            req = requests.get(url)
            req.raise_for_status()
            response = open(url.replace('https://','').replace('.','-').replace('/','-') + '.html', 'wb')
            for chunk in req.iter_content(100000):
                response.write(chunk)
            response.close()
            soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
        
        name = soup.find('span', {'class' : 'public-heading-tag'}).find('span', {'class' : 'twiter_Name'}).text
    
        projectGalleryTitle1.append(name)
    
    projectGalleryTitleList1.append(projectGalleryTitle1)
    
    
def ImageGallery(url):
    
    try:
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    except FileNotFoundError:
        req = requests.get(url)
        req.raise_for_status()
        response = open(url.replace('https://','').replace('.','-').replace('/','-') + '.html', 'wb')
        for chunk in req.iter_content(100000):
            response.write(chunk)
        response.close()
        soup = BeautifulSoup(open(url.replace('https://','').replace('.','-').replace('/','-') + '.html'), 'lxml')
    
    ImageUrl = []
    ImageTitle = []
    ImageUrlList = []
    ImageTitleList = []    
    
    for data in soup.findAll('a', {'class' : 'thumbnailSlider'}):
        ImageUrl.append('https://www.tfod.in/' + data.attrs['href'])
        
    for data in soup.findAll('div', {'class' : 'PhotoTitle'}):
        ImageTitle.append(data.find('span').text)

    for i in range(len(ImageUrl)):
        ImageUrlList.append(ImageUrl[i])
        
        ImageTitleList.append(ImageTitle[i])
    
    return (ImageUrlList, ImageTitleList)
    
for url in pages:
    Page(url)

for link in firmUrl:
    firmProfile(link)

#firmProfile('https://www.tfod.in/Profile-atassociates')

for link in projectsPageUrl:
    firmProjectsGalleryPageLink(link)

#Page('https://www.tfod.in/professionals/design-consultants/p/2')
"""
for i in range(len(projectGalleryTitleList1)):
    print (len(projectGalleryTitleList1[i]), len(projectGalleryTitleList[i]))
    for j in range(len(projectGalleryTitleList1[i])):
        print (projectGalleryTitleList1[i][j] + ' : ' + projectGalleryTitleList[i][j])

for i in range(len(projectGalleryImagesUrlsList)):
    print (len(projectGalleryImagesUrlsList[i]))
    for j in range(len(projectGalleryImagesUrlsList[i])):
        print (len(projectGalleryImagesUrlsList[i][j]))
        for k in range(len(projectGalleryImagesUrlsList[i][j])):
            print (projectGalleryImagesUrlsList[i][j][k])
"""          
connection = Connection()
db = connection.hutstorytfod
firmCollection = db.firms
projectCollection = db.projects
imageGalleryCollection = db.images

"""
for i in range(len(projectGalleryTitleList)):
    for j in range(len(projectGalleryTitleList[i])):
        projectCollection.find_one_and_update({'ProjectImageUrl' : projectGalleryUrlList[i][j]},
                                {'$set' : {'ProjectImageTitle' : projectGalleryTitleList1[i][j]}})
""" 


for i in range(len(firmUrl)):
    insertFirmData = {"Name" : name[i],
                     "FirmImage" : firmImageUrl[i],
                     "Designation" : designation[i],
                     "Firm Page" : firmUrl[i],
                     "Email" : email[i],
                     "Wensite" : website[i],
                     "Phone" : phone[i],
                     "Expertise" : expertise[i],
                     "AboutMe" : aboutMe[i],
                     "PersonalLocation" : personalLocation[i],
                     "PersonalEmail" : personalEmail[i],
                     "PersoanlAddress" : personalAddress[i],
                     "WorkProfile" : workProfile[i],
                     "WorkLocation" : workLocation[i],
                     "WorkEmail" : workEmail[i],
                     "WorkAddress" : workAddress[i],
                     "Projects Page Url" : projectsPageUrl[i]}
    FIRMID = firmCollection.insert_one(insertFirmData).inserted_id
    
    for j in range(len(projectGalleryTitleList[i])):
        insertProjectData = {"ProjectImageTitle" : projectGalleryTitleList1[i][j],
                            "ProjectImageUrl" : projectGalleryUrlList[i][j],
                            "firmId" : FIRMID}
        PROJECTID = projectCollection.insert_one(insertProjectData).inserted_id
        
        for k in range(len(projectGalleryImagesUrlsList[i][j])):
            insertImageData = {"ImageOfProjectsTitle" : projectGalleryImagesTitlesList[i][j][k],
                              "ImageOfProjectsUrl" : projectGalleryImagesUrlsList[i][j][k],
                              "projectId" : PROJECTID}
            IMAGEID = imageGalleryCollection.insert_one(insertImageData).inserted_id

print ('1')
