import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.figure_factory as ff
import plotly.express as px
import io
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

    da = io.StringIO(dataset_file_response.text)
    data = pd.read_csv(da, skip_blank_lines=True, skiprows=13, delim_whitespace=True)

    data.set_axis(
        ['Datum', "Valkenburg ZH", "De Kooy NH", "Schiphol NH", "De Bilt UT", "Leeuwarden FR", "Deelen GE", "Eelde GR",
         "Twenthe DR", "Vlissingen ZE", "Rotterdam ZH", "Gilze-Rijen NB", "Eindhoven NB", "Volkel NB", "Maastricht LI"],
        axis=1, inplace=True)

    return data

def line_chart(data2):
    df = pd.DataFrame(data2)
    num = 19810000
    year = df[df['Datum'] > num]

    Schiphol_Leeuwarden = year[
        ["Datum", 'Gemiddelde', 'Valkenburg ZH', 'De Kooy NH', 'Schiphol NH', 'De Bilt UT', 'Leeuwarden FR',
         'Deelen GE', 'Eelde GR', 'Twenthe DR', 'Vlissingen ZE', 'Rotterdam ZH', 'Gilze-Rijen NB',
         'Eindhoven NB', 'Volkel NB', 'Maastricht LI']]
    Schiphol_Leeuwarden['Dates'] = pd.to_datetime(Schiphol_Leeuwarden['Datum'], format='%Y%m%d')


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Gemiddelde"],
                   name="Gemiddelde"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Valkenburg ZH"],
                   name="Valkenburg ZH"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["De Kooy NH"],
                   name="De Kooy NH"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Schiphol NH"],
                   name="Schiphol NH"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["De Bilt UT"],
                   name="De Bilt UT"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Leeuwarden FR"],
                   name="Leeuwarden FR"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Deelen GE"],
                   name="Deelen GE"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Eelde GR"],
                   name="Eelde GR"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Twenthe DR"],
                   name="Twenthe DR"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Vlissingen ZE"],
                   name="Vlissingen ZE"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Rotterdam ZH"],
                   name="Rotterdam ZH"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Gilze-Rijen NB"],
                   name="Gilze-Rijen NB"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Eindhoven NB"],
                   name="Eindhoven NB"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Volkel NB"],
                   name="Volkel NB"),
    )

    fig.add_trace(
        go.Scatter(x=Schiphol_Leeuwarden["Dates"],
                   y=Schiphol_Leeuwarden["Maastricht LI"],
                   name="Maastricht LI"),
    )

    fig.update_layout(
        title_text="Temperatuur over de tijd van alle meetpunten en het gemiddelde"
    )

    fig.update_xaxes(title_text="Tijd in maanden (met scrollbar)")

    fig.update_yaxes(title_text="Temperatuur in graden Culsius (°C)",
                     secondary_y=False)

    dropdown_buttons = [
        {'label': 'Gemiddelde', 'method': 'update', 'args':
            [{'visible': [True, False, False, False, False,
                          False, False, False, False, False,
                          False, False, False, False, False]},
             {'title': 'Gemiddelde'}]},

        {'label': 'Valkenburg ZH', 'method': 'update', 'args':
            [{'visible': [False, True, False, False, False,
                          False, False, False, False, False,
                          False, False, False, False, False]},
             {'title': 'Valkenburg ZH'}]},

        {'label': 'De Kooy NH', 'method': 'update', 'args':
            [{'visible': [False, False, True, False, False,
                          False, False, False, False, False,
                          False, False, False, False, False]},
             {'title': 'De Kooy NH'}]},

        {'label': 'Schiphol NH', 'method': 'update', 'args':
            [{'visible': [False, False, False, True, False,
                          False, False, False, False, False,
                          False, False, False, False, False]},
             {'title': 'Schiphol NH'}]},

        {'label': "De Bilt UT", 'method': "update", 'args':
            [{"visible": [False, False, False, False, True,
                          False, False, False, False, False,
                          False, False, False, False, False]},
             {'title': 'De Bilt UT'}]},

        {'label': "Leeuwarden FR", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          True, False, False, False, False,
                          False, False, False, False, False]},
             {'title': 'Leeuwarden FR'}]},

        {'label': "Deelen GE", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, True, False, False, False,
                          False, False, False, False, False]},
             {'title': 'Deelen GE'}]},

        {'label': "Eelde GR", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, False, True, False, False,
                          False, False, False, False, False]},
             {'title': 'Eelde GR'}]},

        {'label': "Twenthe DR", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, False, False, True, False,
                          False, False, False, False, False]},
             {'title': 'Twenthe DR'}]},

        {'label': "Vlissingen ZE", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, False, False, False, True,
                          False, False, False, False, False]},
             {'title': 'Vlissingen ZE'}]},

        {'label': "Rotterdam ZH", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, False, False, False, False,
                          True, False, False, False, False]},
             {'title': 'Rotterdam ZH'}]},

        {'label': "Gilze-Rijen NB", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, False, False, False, False,
                          False, True, False, False, False]},
             {'title': 'Gilze-Rijen NB'}]},

        {'label': "Eindhoven NB", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, False, False, False, False,
                          False, False, True, False, False]},
             {'title': 'Eindhoven NB'}]},

        {'label': "Volkel NB", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, False, False, False, False,
                          False, False, False, True, False]},
             {'title': 'Volkel NB'}]},

        {'label': "Maastricht LI", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, False, False, False, False,
                          False, False, False, False, True]},
             {'title': 'Maastricht LI'}]},

        {'label': "Leeg", 'method': "update", 'args':
            [{"visible": [False, False, False, False, False,
                          False, False, False, False, False,
                          False, False, False, False, False]},
             {'title': 'Leeg'}]}]

    fig.update_layout({
        'updatemenus':
            [{'type': "dropdown",
              'x': 1.2,
              'y': 1.16,
              'showactive': True,
              'active': 0,
              'buttons': dropdown_buttons}]
    })

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    fig.update_layout(title_x=0.5)
    return fig


# Eerst maar is de data downloaden van de KNMI website
data = download_data()

#de data even netjes zetten en een gemiddelde in gooien.
data2 = data.drop(index=[0,1,2,3])
data2['Gemiddelde'] = round(data2.iloc[:,1:14].mean(axis=1),1)
# data2.head() # De kolom 'Datum' is op deze manier niet handig dus die verwijderen
# Vervolgens een nieuwe kolom voor de datum invoegen die wel correct is (time series)





st.title('Hoe varrieert de data in Nederland in de periode van 1981 tot 2010')

# st.code(download_data.py)





st.title("Hoe is de temperatuur over de periode per meet punt?")
fig = line_chart(data2)
fig.update_layout(height=500, width=1000)

st.plotly_chart(fig)
fig




# st.write(data['Valkenburg ZH'])