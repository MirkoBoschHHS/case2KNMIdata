import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.figure_factory as ff
from st_aggrid import AgGrid


def download_data():
    # Niks aan veranderen standaard waardes
    api_url = "https://api.dataplatform.knmi.nl/open-data"
    api_key = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6ImNjOWE2YjM3ZjVhODQwMDZiMWIzZGIzZDRjYzVjODFiIiwiaCI6Im11cm11cjEyOCJ9"
    api_version = "v1"

    # Waardes die kunnen worden veranderd
    dataset_name = "knmi14_gemiddelde_temperatuur"
    dataset_version = "3.2"

    # Maak een URL aan
    endpoint = f"{api_url}/{api_version}/datasets/{dataset_name}/versions/{dataset_version}/files"  # /{filename}/url"

    # Verkrijg alle bischikbare files
    get_file_response = requests.get(endpoint, headers={"Authorization": api_key})
    # print(get_file_response.json())

    file_nr = 2  # Maakt het uit welke we kiezen???
    filename = get_file_response.json()['files'][file_nr]['filename']

    endpoint = f"{api_url}/{api_version}/datasets/{dataset_name}/versions/{dataset_version}/files/{filename}/url"
    get_file_response = requests.get(endpoint, headers={"Authorization": api_key})

    download_url = get_file_response.json().get("temporaryDownloadUrl")
    dataset_file_response = requests.get(download_url)

    return dataset_file_response.text

    # with open('Output.txt', 'w') as f:
    #     f.write(dataset_file_response.text)

    data = pd.read_csv('Output.txt', skip_blank_lines=True, skiprows=13, delim_whitespace=True)
    data.set_axis(
        ['Datum', "Valkenburg ZH", "De Kooy NH", "Schiphol NH", "De Bilt UT", "Leeuwarden FR", "Deelen GE", "Eelde GR",
         "Twenthe DR", "Vlissingen ZE", "Rotterdam ZH", "Gilze-Rijen NB", "Eindhoven NB", "Volkel NB", "Maastricht LI"],
        axis=1, inplace=True)

    return data


st.title('Hallo')

st.markdown("tweede test")





map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

# st.write(download_data())

# st.map(map_data)




# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
       hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)


