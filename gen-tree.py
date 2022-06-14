from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
import pandas as pd
from pathlib import Path
from datetime import date
import numpy as np
import requests
import urllib.parse
import folium
import json
from os.path import exists

file_path = "laverty.ged"
csv_headers = ["birth_date","fullname","firstname","surname"]
df = pd.DataFrame()

m = folium.Map(location=[-33.8651, 151.2099], zoom_start=3)


pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)

# Initialize the parser
gedcom_parser = Parser()

# Parse your file
gedcom_parser.parse_file(file_path)

root_child_elements = gedcom_parser.get_root_child_elements()

def get_age(person):
    age = 0
    if person.is_deceased and person.get_death_year() > 0 and person.get_birth_year() > 0 :
        age = person.get_death_year() - person.get_birth_year()
    elif not person.is_deceased() and person.get_birth_year() > 0 :
        age = date.today().year - person.get_birth_year()
    return age

def get_coordinates(address):
    # print(response[0]["lat"])
    # print(response[0]["lon"])
    addr = address.replace(" ","_").replace(",","")
    if exists(f"places/{addr}.json"):
        #print(f"Opening file : {addr}")
        f = open(f"places/{addr}.json", encoding="utf8")
        response = json.load(f)
    else:
        #print(f"Searching OM Api : {addr}")
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        response = requests.get(url).json()
        with open(f"places/{addr}.json", 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=4)

    return response

def add_marker(data):

    #print(coordinates)

    if data["birthplace"]:
        coordinates_birth = get_coordinates(data["birthplace"])
        if coordinates_birth:
            label_birth = "<b>Birth</b>\n" + data["fullname"] + "\n<b>" + str(data["birthyear"]) + "</b>\n" + data["birthplace"]
            #print(coordinates_birth)
            folium.Marker(
                location=[coordinates_birth[0]["lat"], coordinates_birth[0]["lon"]],
                popup=folium.Popup(label_birth, show=True),
                icon=folium.Icon(color='green', icon="user"),
            ).add_to(m)      

    if data["deathplace"]:
        coordinates_death = get_coordinates(data["deathplace"])
        if coordinates_death:
            label_death = "<b>Death</b>\n" + data["fullname"] + "\n<b>" + str(data["deathyear"]) + "</b>\n" + data["deathplace"]
            #print(coordinates_death)
            folium.Marker(
                location=[coordinates_death[0]["lat"], coordinates_death[0]["lon"]],
                popup=folium.Popup(label_death, show=True),
                icon=folium.Icon(color='red', icon="plus"),
            ).add_to(m)       

    if data["burialplace"]:
        coordinates_burial = get_coordinates(data["burialplace"])
        if coordinates_burial:
            label_burial = "<b>Burial</b>\n" + data["fullname"] + "\n<b>" + str(data["deathyear"])  + "</b>\n" + data["burialplace"]
            #print(coordinates_death)
            folium.Marker(
                location=[coordinates_burial[0]["lat"], coordinates_burial[0]["lon"]],
                popup=folium.Popup(label_burial, show=True),
                icon=folium.Icon(color='purple', icon="plus"),
            ).add_to(m)      

def get_profile(person):
    if element.get_birth_year():
        profile_path = str(element.get_birth_year())
    fullname = "_".join(element.get_name())    
    profile_path = '<img src="' + profile_path + "_" + fullname.lower() + '">'
    return profile_path


def process_person(element):
    text = ""
    (first, last) = element.get_name()
    #firstname = first.split(" ")[0]
    text += f"{first} {last}"
    
    (first, last) = element.get_name()

    fullname = " ".join(element.get_name())
    pointer = element.get_pointer().replace("@","")
    birth_data = element.get_birth_data()
    if element.get_birth_year() == -1 :
        birth_year = 0
    else:
        birth_year = element.get_birth_year()
    birth_date = birth_data[0] if 0 < len(birth_data) else None
    birth_place = birth_data[1] if 1 < len(birth_data) else None
    if element.get_death_year() == -1 :
        death_year = 0
    else:
        death_year = element.get_death_year()
    death_data = element.get_death_data()
    death_place = death_data[1] if 1 < len(death_data) else None
    burial_data = element.get_burial_data()
    burial_place = burial_data[1] if 1 < len(burial_data) else None
    age = get_age(element)
    data = {
            # "profile": get_profile(element),
            "id": pointer,
            "birthyear" : birth_year,
            "surname": last,
            "firstname": first,
            "birthdate": birth_date, 
            "birthplace": birth_place,
            "deathyear": death_year,
            "deathplace": death_place,
            "burialplace": burial_place,
            "age": age,
            "fullname": fullname,   
        }

    return data


# Iterate through all root child elements
for element in root_child_elements:
    if isinstance(element, IndividualElement):
        df_dict = pd.DataFrame([process_person(element)])
        df = pd.concat([df, df_dict], ignore_index=True)

#df = df[df['deathyear'] > 0]

df = df[df['birthyear'] > 1791]

#df = df[df['birthyear'] > 1980]

df.sort_values("birthyear", ascending=False, inplace=True,)
df.drop('id', axis=1, inplace=True)
#df.drop('fullname', axis=1, inplace=True)
df = df.reset_index(drop=True)
df.index = df.index + 1

cell_hover = {  # for row hover use <tr> instead of <td>
    'selector': 'td:hover',
    'props': [('background-color', '#ffffb3')]
}
# index_names = {
#     'selector': '.index_name',
#     'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
# }
headers = {
    'selector': 'th:not(.index_name)',
    'props': 'background-color: #000066; color: white;'
}

def url_to_image_html(imageUrl):
  return f"<img src='{imageUrl}' width='120'/>"

with pd.option_context('display.precision', 1):
    df_style = df.style
    df_style.hide_index()
# df_style.set_table_styles([cell_hover, index_names, headers])

html = df_style.format().set_table_styles([cell_hover, headers])

html = html.render(escape=False)

#render dataframe as html
# html = df.to_html()

#write html to file
text_file = open("list.html", "w")
text_file.write(html)
text_file.close()

print("============   Generating Map   ==============")

for index, person in df.iterrows():
    if person["birthplace"]:
        add_marker(person)

m.save("map.html")