import sys
from selenium import webdriver
import numpy as np
import pandas as pd
import time
from PyQt5.QtWidgets import *



class Main(QWidget):
    
    def __init__(self):
        super(Main,self).__init__()
        self.setFixedSize(1280*0.6,720*0.6)
        
        self.InterFace()

        self.show()

    def InterFace(self):

        self.usernameLabel = QLabel("Mail")
        self.usernameLabel.setFixedWidth(60)
        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setFixedWidth(250)

        self.passwordLabel = QLabel("Password")
        self.passwordLabel.setFixedWidth(60)
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setFixedWidth(250)

        self.YatakOdasıLabel = QLabel("Bedroom")
        self.YatakOdasıLabel.setFixedWidth(60)
        self.YatakOdasıComboBox = QComboBox()
        self.YatakOdasıComboBox.setFixedWidth(250)
        self.YatakOdasıComboBox.addItems(["All", "1", "2", "3", "4", "5", "6"])

        self.BanyoLabel = QLabel("Bathroom")
        self.BanyoLabel.setFixedWidth(60)
        self.BanyoComboBox = QComboBox()
        self.BanyoComboBox.setFixedWidth(250)
        self.BanyoComboBox.addItems(["All", "1", "1.5", "2", "3", "4", "5"])

        self.ApartmanCheckBox = QCheckBox("Apartman ")
        self.ApartmanCheckBox.setFixedWidth(250)
        self.MustakilCheckBox = QCheckBox("House")
        self.MustakilCheckBox.setFixedWidth(250)
        self.OdaCheckBox = QCheckBox("Room Only")
        self.OdaCheckBox.setFixedWidth(250)
        self.SıraEvCheckBox = QCheckBox("Townhouse")
        self.SıraEvCheckBox.setFixedWidth(250)

        self.MinValLabel = QLabel("Minimum")
        self.MinValLabel.setFixedWidth(60)
        self.MinVal = QLineEdit()
        self.MinVal.setFixedWidth(250)

        self.MaxValLabel = QLabel("MAximum")
        self.MaxValLabel.setFixedWidth(60)
        self.MaxVal = QLineEdit()
        self.MaxVal.setFixedWidth(250)

        self.ApplyButton = QPushButton("Apply")

        HBox0 = QHBoxLayout()
        HBox0.addStretch()
        HBox0.addWidget(self.usernameLabel)
        HBox0.addWidget(QLabel(" : "))
        HBox0.addWidget(self.usernameLineEdit)

        HBox1 = QHBoxLayout()
        HBox1.addStretch()
        HBox1.addWidget(self.passwordLabel)
        HBox1.addWidget(QLabel(" : "))
        HBox1.addWidget(self.passwordLineEdit)

        VB = QVBoxLayout()
        VB.addLayout(HBox0)
        VB.addLayout(HBox1)

        GroupBox1 = QGroupBox("Login")
        GroupBox1.setLayout(VB)
        GroupBox1.setFixedHeight(150)

        HBox2 = QHBoxLayout()
        HBox2.addWidget(self.YatakOdasıLabel)
        HBox2.addWidget(QLabel(" : "))
        HBox2.addWidget(self.YatakOdasıComboBox)

        HBox3 = QHBoxLayout()
        HBox3.addWidget(self.BanyoLabel)
        HBox3.addWidget(QLabel(" : "))
        HBox3.addWidget(self.BanyoComboBox)

        HBox4 = QHBoxLayout()
        HBox4.addWidget(self.MinValLabel)
        HBox4.addWidget(QLabel(" : "))
        HBox4.addWidget(self.MinVal)

        HBox5 = QHBoxLayout()
        HBox5.addWidget(self.MaxValLabel)
        HBox5.addWidget(QLabel(" : "))
        HBox5.addWidget(self.MaxVal)

        VBox0 = QVBoxLayout()
        VBox0.addLayout(HBox2)
        VBox0.addLayout(HBox3)
        VBox0.addWidget(self.ApartmanCheckBox)
        VBox0.addWidget(self.MustakilCheckBox)
        VBox0.addWidget(self.OdaCheckBox)
        VBox0.addWidget(self.SıraEvCheckBox)
        VBox0.addLayout(HBox4)
        VBox0.addLayout(HBox5)
        
        GroupBox2 = QGroupBox("-")
        GroupBox2.setLayout(VBox0)
        GroupBox2.setFixedWidth(400)

        VBox1 = QVBoxLayout()
        VBox1.addWidget(GroupBox1)
        VBox1.addWidget(GroupBox2)

        HB = QHBoxLayout()
        HB.addStretch()
        HB.addWidget(self.ApplyButton)
        VBox1.addLayout(HB)

        self.setLayout(VBox1)

        self.ApplyButton.clicked.connect(self.clickApply)
       



    def clickApply(self):


        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        
        minPrice = self.MinVal.text()
        maxPrice = self.MaxVal.text()
        bedroomNumber = self.YatakOdasıComboBox.currentText()
        bathroomNumber = self.BanyoComboBox.currentText()


        rentType = ""
        if self.ApartmanCheckBox.isChecked():
            rentType += "apartment-condo%2C"
        
        if self.MustakilCheckBox.isChecked():
            rentType += "house%2C"

        if self.OdaCheckBox.isChecked():
            rentType += "private_room-shared_room%2C"

        if self.SıraEvCheckBox.isChecked():
            rentType += "townhouse%2C"

        # rentType.replace(' ','%2C')
        
        # print(rentType)
        step_1 = self.generate_link(minPrice,maxPrice,bedroomNumber,bathroomNumber,rentType)        
        self.login(username,password,step_1)
        


    def login(self, username,password,link2):
        # bu fonksiyonun amacı bizim kendi kullanıcı bilgilerimiz ile siteye giriş yapmamızı sağlıyor.
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(chrome_options=options)

        link = "https://www.facebook.com/marketplace/category/propertyrentals/"
        driver.get(link)
        time.sleep(1)
        
        username_button = driver.find_element_by_xpath('//*[@id="email"]')
        username_button.send_keys(username)
        time.sleep(1)
        
        password_button = driver.find_element_by_xpath('//*[@id="pass"]')
        password_button.send_keys(password)
        
        time.sleep(1)
        login_button = driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
        time.sleep(3)
        driver.get(link2)
        time.sleep(10)
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
        
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        ####
        time.sleep(60)
        ####
        urls = list()
        # base_url = str(driver.current_url)
        time.sleep(3)
        for item in driver.find_elements_by_tag_name('a'):
            print(item.get_attribute('href'))
            if '/marketplace/item' in item.get_attribute('href'):
                urls.append(item.get_attribute('href'))
        time.sleep(3)
        # driver.close()
        count = 0
        df = pd.DataFrame()
        price_list = list()
        
        score_list =list()
        Furnishings = list()
        Ceiling = list()
        Basement = list()
        Cat_and_dog = list()
        building_details = list()
        listing_date = list()
        date_available = list()
        heating = list()
        air_conditioning = list()
        Outdoor = list()
        Dishwasher = list()
        Lease_type = list()
        rental_type = list()
        Fireplace = list()
        Dishwasher = list()
        Oven = list()
        Parking = list()
        bedrooms = list()
        bathrooms = list()
        Refrigerator = list()
        Area = list()
        walk_list = list()
        transit_list = list()
        bike_list = list()
        Microwave = list()
        address_list = list()
        laundry = list()
        url_links = list()
        walk_in_closet = list()
        
        for item in urls:
            print(count)
            count+=1
            driver.get(item)
            url_links.append(item)
            time.sleep(15)
            html = driver.page_source
            list_html = html.split('>')

            #Price
            price = driver.find_element_by_class_name('ku2m03ct').text 
            price = price.split('/')
            price = price[0]

            price_list.append(price)
            print(price_list)
            #####
            features_1 = list()

            sub_score_list = list()
            for item in range(len(list_html)):
                
                if 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw oo9gr5id hzawbc8m' in list_html[item]:
                    features_1.append(list_html[item+1])
                if 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain hzawbc8m' in list_html[item]:
                    sub_score_list.append(list_html[item+1])

            new_value = list()
            all_value = ""
            for item in features_1:
                all_value += item

            new_value = all_value.split('</span')
            new_value.pop()

            new_value_str = ""

            for item in new_value:
                new_value_str += (item + " ")

            ####
            # print('===================')
            # print(score_list)
            # print('===================')
            if 'Unfurnished' in new_value_str:
                Furnishings.append('Unfurnished')
            else:
                Furnishings.append('')
            print('Furnishings',Furnishings)
            ####

            if 'Refrigerator' in new_value_str:
                Refrigerator.append('Refrigerator')
            else:
                Refrigerator.append('')
            print('Refrigerator ',Refrigerator)
            ####

            if 'Ceiling Fan' in new_value_str:
                Ceiling.append('Ceiling Fan')
            else:
                Ceiling.append('')
            print('Ceiling ',Ceiling)
            ####

            if 'Basement' in new_value_str:
                Basement.append('Basement')
            else:
                Basement.append('')
            print('Basement',Basement)
            ####

            if 'Dog and cat friendly' in new_value_str:
                Cat_and_dog.append('Dog and cat friendly')
            else:
                Cat_and_dog.append('')
            print('Cat and dog',Cat_and_dog)
            ####
            if 'Walk-in Closet' in new_value_str:
                walk_in_closet.append('Walk-in Closet')
            else:
                walk_in_closet.append('')
            ### Building Details List Part
            count_build = 0
 
            sub_build = ''
            if 'Doorman' in new_value_str:
                sub_build += 'Doorman ,'
                count_build +=1 
            if 'Concierge' in new_value_str: # Concierge</span olacak
                sub_build += 'Concierge ,'
                count_build +=1 
            if "Lift" in new_value_str or 'Elevator' in new_value_str: # Elevator</span olacak
                sub_build += 'Elevator ,'
                count_build +=1
            if 'Fitness Center' in new_value_str: # Fitness Center</span
                sub_build += 'Fitness Center ,'
                count_build +=1
            if "Residents' lounge" in new_value_str: # Resident Lounge</span
                sub_build += "Residents' lounge ,"
                count_build +=1
            if "Swimming pool" in new_value_str: #Swimming Pool</span
                sub_build += 'Swimming pool ,'
                count_build +=1
            if "Rooftop patio" in new_value_str: # Roof Deck</span
                sub_build += 'Rooftop patio ,'
                count_build +=1
            if 'Secured Entry' in new_value_str:
                sub_build += 'Secured Entry ,'
                count_build +=1
            if "Bike Parking" in new_value_str: # Bike Parking</span
                sub_build += 'Biking Parking '
                count_build +=1
            if count_build == 0:
                sub_build += ""
                building_details.append(sub_build)
            else:
                building_details.append(sub_build)
            print('building details ',building_details)
            #####
            if 'Laundry available' in new_value_str:
                laundry.append('Laundry available')
            elif 'Laundry in building' in new_value_str:
                laundry.append('Laundry in building')
            elif 'In-unit laundry' in new_value_str:
                laundry.append('In-unit laundry')
            else:
                laundry.append('')
            #####

            if 'Listed over a week ago' in new_value_str:
                listing_date.append('Listed over a week ago')
            elif 'Listed about a day ago' in new_value_str:
                listing_date.append('Listed about a day ago')
            elif 'hours ago' in new_value_str:
                k = new_value_str.find('Listed')
                listing_date.append(new_value_str[k-1:k+17])
            else:
                listing_date.append('')
            print("Listing Date: ",listing_date)
            ####
            if 'now' in new_value_str:
                date_available.append('Available now')
            elif 'Available' in new_value_str:
                j = new_value_str.find('Available')
                date_available.append(new_value_str[j-1:j+21])
            else:
                date_available.append('')
            print("Date available: ",date_available)
            ####

            if "Central heating" in new_value_str: # Heating available</span
                heating.append('Central heating')
            elif "Gas heating" in new_value_str: # Heating available</span
                heating.append('Gas heating')
            elif 'Heating available' in new_value_str:
                heating.append('Heating available')
            elif 'Radiator heating' in new_value_str:
                heating.append('Radiator heating')
            else:
                heating.append("")
            print('Heating ',heating)
            ####

            if "AC available" in new_value_str:
                air_conditioning.append('AC available')
            elif 'Central AC' in new_value_str:
                air_conditioning.append('Central AC')
            else:
                air_conditioning.append('')
            print('Air conditioning ',air_conditioning)
            ####

            if 'Balcony' in new_value_str:
                Outdoor.append('Balcony')
            else:
                Outdoor.append("")
            print('Outdoor ',Outdoor)
            ####

            if 'Dishwasher' in  new_value_str:
                Dishwasher.append('Dishwasher')
            else:
                Dishwasher.append('')
            print('dishwasher ',Dishwasher)
            ####
            ####

            if 'Lease' in new_value_str:
                l = new_value_str.find('Lease')
                Lease_type.append(new_value_str[l-10:l+5])
            elif 'tenancy' in new_value_str:
                l = new_value_str.find('tenancy')
                Lease_type.append(new_value_str[l-7:l+8])
            else:
                Lease_type.append('')
            print('Lease Type: ',Lease_type)
            ####
            # Apartment | House | Room Only | Townhouse
            # House Type
            bb = 0
            if 'Apartment' in new_value_str: # Apartment olacak
                rental_type.append('Apartment')
                bb +=1
            elif 'House' in new_value_str: # House Olacak
                rental_type.append('House')
                bb += 1
            elif 'Room Only' in new_value_str: #Room Only olacak
                rental_type.append('Room Only')
                bb += 1
            elif 'Townhouse' in new_value_str:
                rental_type.append('Townhouse')
                bb += 1
            if bb == 0:
                rental_type.append('')
            print('rental type: ',rental_type)
            ####

            if 'Fireplace' in new_value_str:
                Fireplace.append('Fireplace')
            else:
                Fireplace.append('')
            print('fireplace ',Fireplace)
            ####

            if 'Oven' in new_value_str:
                Oven.append('Oven')
            else:
                Oven.append('')
            print('oven ',Oven)
            ####

            if 'Parking available' in new_value_str:
                Parking.append('Parking available')
            elif 'Garage parking' in new_value_str:
                Parking.append('Garage parking')
            elif 'Street parking' in new_value_str:
                Parking.append('Street parking')
            else:
                Parking.append('')
            print('parking',Parking)
            ####

            if 'bed' in new_value_str:
                x = new_value_str.find('bed')
                bedrooms.append(new_value_str[x-2:x+5])
            else:
                bedrooms.append("")
            if 'bath' in new_value_str:
                y = new_value_str.find('bath')
                bathrooms.append(new_value_str[y-2:y+5])
            else:
                bathrooms.append('')
            print('bedrooms',bedrooms)
            print('bathrooms',bathrooms)
            ####

            if 'square' in new_value_str:
                z = new_value_str.find('square')
                Area.append(new_value_str[(z-4):(z+13)])
            else:
                Area.append('')
            print('Area: ',Area)
            ####
            print('====================================')
            for item in sub_score_list:
                # 100 üzerinden yerine out of 100 yapılacak unutma !!!!!!!!!!!!
                # startswith yerine endwith yapacaksın unutma!!!!!
                if item[0] == '<':
                    sub_score_list.remove(item)
                if not item[0].isnumeric():
                    sub_score_list.remove(item)

            if len(sub_score_list) == 4:    
                sub_score_list.pop()
            # score_list.pop()


            if len(sub_score_list) == 3:
                walk_list.append(sub_score_list[0][:-6])
                transit_list.append(sub_score_list[1][:-6])
                bike_list.append(sub_score_list[2][:-6])
            elif len(sub_score_list) == 2:
                walk_list.append(sub_score_list[0][:-6])
                transit_list.append(sub_score_list[1][:-6])
                bike_list.append("")
            else:
                walk_list.append(sub_score_list[0][:-6])
                transit_list.append("")
                bike_list.append("")



            print('walk list',walk_list)
            print('transit list ',transit_list)
            print('bike list',bike_list)
            print('sub score list',sub_score_list)
            print('========================================')

            ####


            if 'Microwave' in new_value_str:
                Microwave.append('Microwave')
            else:
                Microwave.append('')
            print('microwave: ',Microwave)


            #######
            try:
                address_list.append(features_1[0][:-6])
            except:
                address_list.append("")
            print('address list',address_list)
        
        df['address_list'] = np.array(address_list)
        
        df['Price'] = np.array(price_list)

        df['Furnishings'] = np.array(Furnishings)

        df['Refrigerator'] = np.array(Refrigerator)

        df['Ceiling'] = np.array(Ceiling)

        df['Basement'] = np.array(Basement)

        df['Cat and dog'] = np.array(Cat_and_dog)

        df['Building details'] = np.array(building_details)

        df['Listing date'] = np.array(listing_date)

        df['Date available'] = np.array(date_available)

        df['Heating'] = np.array(heating)

        df['Air conditioning'] = np.array(air_conditioning)

        df['Outdoor'] = np.array(Outdoor)

        df['Dishwasher'] = np.array(Dishwasher)

        df['Lease type'] = np.array(Lease_type)

        df['Rental type'] = np.array(rental_type)

        df['Fireplace'] = np.array(Fireplace)

        df['Oven'] = np.array(Oven)

        df['Parking'] = np.array(Parking)

        df['bedrooms'] = np.array(bedrooms)

        df['bathrooms'] = np.array(bathrooms)

        df['Area'] = np.array(Area)
        
        df['Laundry'] = np.array(laundry)
        
        df['Walk-in Closet'] = np.array(walk_in_closet)

        df['Walk Score'] = np.array(walk_list)

        df['Transit Score'] = np.array(transit_list)
        
        df['Bike Score'] = np.array(bike_list)
        
        df['Url'] = np.array(url_links)
        
            
        df.to_excel('deneme.xlsx',index=False)
        driver.close()
        
            
    def generate_link(self, minPrice,maxPrice,bedroomNumber,bathroomNumber,rentType):
        #Bu fonksiyonu yazma sebebimiz selenium ile normalde otomatik seçimler yapmak yerine vakit kaybetmek yerine  otomatik link üzerinden kendi linkimizi oluşturabiliyoruz
        #bu da bize büyük bir avantaj sağlıyor.
        link = f"https://www.facebook.com/marketplace/category/propertyrentals?minPrice={minPrice}&maxPrice={maxPrice}&minBathrooms={bathroomNumber}&minBedrooms={bedroomNumber}&propertyType={rentType}&exact=false"
        return link 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MAIN = Main()
    sys.exit(app.exec_())
    


# if '__main__' == __name__:
#     username = "oktaydabak54@gmail.com"
#     password = "Ballislife54."
    
#     minPrice = "100"
#     maxPrice = "1000"
#     bedroomNumber = "1"
#     bathroomNumber = "1"
#     rentType = "apartment-condo"
#     cityName = "Toronto"
    
    
#     step_1 = generate_link(minPrice,maxPrice,bedroomNumber,bathroomNumber,rentType)
#     
    
#     run = login(username,password,step_1)

    