from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

def url_to_soup(url):
    resp = requests.get(url)
    text = resp.text
    soup = BeautifulSoup(text, 'lxml')
    return soup

home_path = "https://www.pgatour.com"

categories_path = "https://www.pgatour.com/stats/categories."

categories_to_parse = [
                 "ROTT_INQ.html","RAPP_INQ.html", "RARG_INQ.html", 
                 "RPUT_INQ.html","RSCR_INQ.html", "RSTR_INQ.html",
                 "RMNY_INQ.html", "RPTS_INQ.html"
                 ]


soup_categories = list() 
for tab in categories_to_parse: # Store soups of different categories, e.g., Off The Tee
    soup = url_to_soup(categories_path+tab)
    soup_categories.append(soup)


stat_table_name = list()
stat_table_href = list()
a_tags_list = list()


for soup in soup_categories: # Div blocks for different type of tables in each categories
    a_tags_table_list = soup.find_all('div', 'table-content clearfix') 
    for table in a_tags_table_list:
        for a_tags in table.find_all('a'): # a tags for all tables 
            stat_table_name.append(a_tags.text)
            stat_table_href.append(a_tags.attrs['href'])
            a_tags_list.append(a_tags)
        
df_stat_table = pd.DataFrame({'stat_table_name':stat_table_name, 
                               'stat_table_href':stat_table_href})    

process = 0 # For progess bar
length = len(stat_table_href) # For progess bar
no_content_page = list() 
df_list = list() # List of result tables as DataFrame

for a_tags in a_tags_list:
    
    href = a_tags.attrs['href'] # /stats/stat.02674.html

    text_content = a_tags.text
    
    process += 1
    print(f'Progress: {process}/{length} links processed')
    
    stat_rows = list() #Receive data by row
    soup = url_to_soup(home_path + href) # https://www.pgatour.com/stats/stat.02674.html
    table = soup.find(id = 'statsTable') # Data table
    
    columns = list()
    try: # Empty tables cause error
        
        for th in table.find('tr').find_all('th'): # Table Header
            if th.text.replace('\n', '') == 'PLAYER NAME': # PLAYER NAME as key shouldn't has any prefix
                columns.append(th.text.replace('\n', ''))
            else: # Others add informative prefix
                columns.append(text_content + " - " + th.text.replace('\n', '')) 
        
        trs = table.find_all('tr')[1:] 
        for tr in trs:
            stat_rows.append([td.text.replace('\n', '').replace('\xa0', '').strip() 
                              for td in tr.find_all('td')
                              ]) 
        
    except AttributeError:
        no_content_page.append(href)
        continue

    tmp_df = pd.DataFrame(data = stat_rows, columns = columns)   
    df_list.append(tmp_df)

 
driving_distance = df_list[3]

pga_database = sqlite3.connect('C:/Users/gn023/Desktop/Python_Scripts/Web_Crawler/pga_database.db')

for i in range(len(df_list)):
    df_list[i].to_sql(stat_table_name[i], con = pga_database, if_exists='replace', index = False)

pga_database.commit()

pga_database.close()




