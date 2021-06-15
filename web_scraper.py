from bs4 import BeautifulSoup
import requests
import csv


def get_link(file_name, link1, link2):
    '''
    Scrape all the user profile links from the website onto a csv file 

        Parameters:
            file_name (str): path of csv file
            link1 (str): url of website that have all user profile links
            link2 (str): url for concatenation with a user profile link  
    '''

    csv_file = open(file_name, 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['profile link'])

    for i in range(1, 4):
        source = requests.get(
            f'{link1}?pageno={i}').text

        soup = BeautifulSoup(source, 'lxml')

        links = soup.find_all('a', class_='h2 m0 truncate max-width-85')

        for link in links:
            user_link = link['href']
            user_link = f"{link2}{user_link}"
            csv_writer.writerow([user_link])

    csv_file.close()

    return


def get_info(link_file, dest_file):
    '''
    Scrape user's name, ethnicity and gender onto a csv file

    Parameters:
        link_file (str): file name with user profile's link
        dest_file (str): destination file name 
    '''

    csv_file = open(dest_file, 'w', encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['name', 'ethnicity', 'gender'])

    with open(link_file, newline='') as f:
        reader = csv.reader(f)
        links = list(reader)

    for link in links:

        source = requests.get(link[0]).text
        soup = BeautifulSoup(source, 'lxml')
        try:
            name = soup.find(
                'h2', class_='truncate m0').text
        except:
            name = None

        try:
            ethnicity = soup.find_all(
                'div', class_='overview-details')[2]
            ethnicity = ethnicity.find_all(
                'div', class_='row flex items-stretch')[5]
            ethnicity = ethnicity.find_all('div', class_='p1')[1].text
        except:
            ethnicity = None

        try:
            gender = soup.find_all(
                'div', class_='overview-details')[1]
            gender = gender.find_all('div', class_='row flex items-stretch')[0]
            gender = gender.find_all(
                'div', class_='height-12 flex items-center')[0].text
        except:
            gender = None

        csv_writer.writerow([name, ethnicity, gender])

    csv_file.close()

    return


get_link(file_name='men_brazil.csv',
         link1='https://www.brazilcupid.com/en/men/brazil',
         link2='https://www.brazilcupid.com')

get_info(link_file='dataset_2.csv', dest_file='user_profile_2.csv')
