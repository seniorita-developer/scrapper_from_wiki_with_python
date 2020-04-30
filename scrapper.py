import unicodedata
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


url = 'https://en.wikipedia.org/wiki/List_of_rabbit_breeds'
html = urlopen(url)

# Create an instance of the BeautifulSoup class to parse our document
soup = BeautifulSoup(html, 'html.parser')

data = soup.find_all('table')

# List of parameter names
list_table_names = ['breed', 'image', 'sizes', 'fur_type', 'ear_type', 'colors', 'ARBA_recognised',
                    'BRC_recognised', 'origins']

# Create list of lists to hold our data. Each list stored particular parameter, ex. size or ear type
all_data_list = [[], [], [], [], [], [], [], [], []]

for table in data:
    # Get all the rows
    rows = table.find_all('tr')

    for row in rows:
        # Get all the cells
        cells = row.find_all('td')

        if len(cells) > 8:
            # Get each parameter from each row
            for i in range(0, 9):

                if i != 1:
                    # Get data from cells except an image field
                    temp = unicodedata.normalize("NFKD", cells[i].text).replace(u'\u2014', 'Unknown').replace('\n', ' ')
                else:
                    # Get image link
                    for img in cells[1].find_all('img', src=True):
                        temp = img['src']
                all_data_list[i].append(temp.replace(u'\u2013', '').replace(u'\u0301', ''))


# Create list of dictionaries to store our data
result_list = []

for i in range(0, len(all_data_list[0])):
    temp = {
        list_table_names[0]: all_data_list[0][i],
        list_table_names[1]: all_data_list[1][i],
        list_table_names[2]: all_data_list[2][i],
        list_table_names[3]: all_data_list[3][i],
        list_table_names[4]: all_data_list[4][i],
        list_table_names[5]: all_data_list[5][i],
        list_table_names[6]: all_data_list[6][i],
        list_table_names[7]: all_data_list[7][i],
        list_table_names[8]: all_data_list[8][i]
            }
    result_list.append(temp)

# Write data to JSON
with open('rabbit_breeds.txt', 'w') as outfile:
    json.dump(result_list, outfile)
