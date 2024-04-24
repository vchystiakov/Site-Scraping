# library for scraping
from bs4 import BeautifulSoup
# library for working with requests
import requests
# library for working with json data
import json

# CREATING FILE WITH COLLECTED EVERY PERSON LINK ON SITE
# list of all persons url
persons_url_list = []

# for all sets of members with step 12 gets it's data content and save it in result variable
for i in range(0, 762, 12):
    url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={
        i}'
    data = requests.get(url)
    result = data.content

    # creating object with scraped data, lxml - parser type
    soup = BeautifulSoup(result, 'lxml')
    # collecting all persons links by method find_all using tag a
    persons = soup.find_all('a')

    # for every person take their page link and save it in person_url_List
    for person in persons:
        person_page_url = person.get('href')
        persons_url_list.append(person_page_url)

# creating file and saving person url in every line
    with open('person_url_list.txt', 'a') as file:
        for line in persons_url_list:
            file.write(f'{line}\n')


# open created file for reading
with open('person_url_list.txt', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

    # empty list with all persons data
    data_dict = []
    # creating counter for seeing result of every iteration(writing person data in json file)
    count = 0
    # for every line with url in lines list
    for line in lines:
        # sending get request for every line in lines list and saving it in result variable
        q = requests.get(line)
        result = q.content
        # creating parsing object
        soup = BeautifulSoup(result, 'lxml')
        # finding persons info by method find using class parametr and h3 tag
        person = soup.find(class_='bt-biografie-name').find('h3').text
        # splitting person info into elements of list
        person_name_company = person.strip().split(',')
        # first element of list is person's name
        person_name = person_name_company[0]
        # second element of list is person's company
        person_company = person_name_company[1].strip()

        # social_networks links parsing
        social_networks = soup.find_all(class_='bt-link-extern')

        # list with all persons social networks
        social_networks_urls = []
        # for every link in social networks add it to social_networks_urls list
        for item in social_networks:
            social_networks_urls.append(item.get('href'))

        # uniting all data and saving it in dictionary
        data = {
            "person_name": person_name,
            "person_company": person_company,
            "social_networks": social_networks_urls
        }

        # increment counter after every iteration
        count += 1
        print(f'#{count}: {line} is done!')
        # after every iteration adds each person data
        data_dict.append(data)

        # writing all data in json file
        with open('data.json', 'w') as json_file:
            # indent - interval in writing file
            json.dump(data_dict, json_file, indent=4)
