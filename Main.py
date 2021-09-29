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

    file_nr = 0  # Maakt het uit welke we kiezen???
    filename = get_file_response.json()['files'][file_nr]['filename']

    endpoint = f"{api_url}/{api_version}/datasets/{dataset_name}/versions/{dataset_version}/files/{filename}/url"
    get_file_response = requests.get(endpoint, headers={"Authorization": api_key})

    download_url = get_file_response.json().get("temporaryDownloadUrl")
    dataset_file_response = requests.get(download_url)

    da = io.StringIO(dataset_file_response.text)
    data = pd.read_csv(da, skip_blank_lines=True, skiprows=7, delim_whitespace=True)



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




st.title('Case 2: Blogpost')
st.write(' 	- Marcel Zwagerman	500889946\n'
         '  - Sjoerd Fijne		500828895\n'
         '  - Mirko Bosch		500888784\n'
         '  - Martijn Draper	500888847')

st.title('Inhoudsopgave')
st.write('  - Samenvatting\n'
         '  - API ophalen van KNMI\n'
         '  - Data bewerken\n'
         '  - Visualisatie')


st.title('Samenvatting')
st.write('Wij hebben een API opgehaald van de KNMI website. Deze data hebben we eerst opgeschoond en gegevens toegevoegd zoals het gemiddelde en standaard deviatie. We hebben vervolgens een globale weergave gemaakt en zijn opzoek gegaan naar een gemiddelde temperatuur stijging, ......')


st.title('API ophalen van KNMI')
st.write('Een API ophalen van het KNMI. KNMI staat voor Koninklijk Nederlands Meteorologisch Instituut.Deze website is van de overheid en delen openbare API\'s waarvan wij er een hebben gebruikt.Deze website legt volledig uit hoe je een API kan inladen in je Jupiter Notebook. We hebben het stappenplan volledig gevolgd en uiteindelijk ingeladen in ons notebook. Hieronder zie je een schematische weergave van de data tabel die we hebben ingeladen.')

st.write(data.head(7))

st.write("Deze data is nu ingeladen maar de eerste 4 regels zijn afwijkend van de rest. Als we kijken naar wat dit is zien we onderanderen de coördinaten. De kolom zijn nu de stations nummers.")

link = '[KNMI API example](https://developer.dataplatform.knmi.nl/example-scripts)'
st.markdown(link, unsafe_allow_html=True)

st.title('Data bewerken')
st.write('Voordat we echt kunnen gaan spelen met onze data moeten we de data opschonen. Dit hebben we gedaan door eerst de kolommen een naam te geven. Dit konden we afleiden van het KNMI website. Hier is bijvoorbeeld nummer 240 de locatie op Schiphol. Hieronder zie je een afbeelding waar zo makelijk te herleiden is welk nummer bij welk station hoort.')

# Afbeelding toevoegen: KNMI_meetpunten.png

st.write('Na het toevoegen van de kolommen kwamen we erachter dat we nog een aantal rijen moesten laten vallen, want die behoorde niet tot de dataset. We hebben ook een controlle gedaan of er missende gegevens zijn, maar gelukkig waren er geen missende gegevens. \n \nWe hebben de dataset gekoppieerd waarbij een dataset de datum als een index is en een dataset waarbij de datum een kolom is. Dit hebben we gedaan voor enkele visualisaties die je later in deze blog gaat zien. Na deze aanpassingen hebben we een gemiddelde en een standaard deviatie toegevoegd aan de datasets')

data.set_axis(
        ['Datum', "Valkenburg ZH", "De Kooy NH", "Schiphol NH", "De Bilt UT", "Leeuwarden FR", "Deelen GE", "Eelde GR",
         "Twenthe DR", "Vlissingen ZE", "Rotterdam ZH", "Gilze-Rijen NB", "Eindhoven NB", "Volkel NB", "Maastricht LI"],
        axis=1, inplace=True)

#de data even netjes zetten en een gemiddelde in gooien.
data2 = data.drop(index=[0,1,2,3])
data2['Gemiddelde'] = round(data2.iloc[:,1:14].mean(axis=1),1)
# data2.head() # De kolom 'Datum' is op deze manier niet handig dus die verwijderen
# Vervolgens een nieuwe kolom voor de datum invoegen die wel correct is (time series)

data3 = data2.drop(columns='Datum')
data3['Datum'] = pd.date_range("1981-01-01", periods=len(data3), freq="D")
data_clean = data3.set_index('Datum')
# data_clean.head() # Nu is de data clean

# We voegen een kolom toe met de gemiddelde temperatuur van alle weerstations
# En ook een kolom met de standaarddeviatie
data_clean['Gemiddelde'] = round(data_clean.mean(axis=1),1)
data_clean['Standaarddeviatie'] = round(data_clean.std(axis=1),1)


st.write(data2.head())
st.write(data_clean.head())


st.title('Visualisatie')
st.header('Temperatuur in Nederland, 1981 - 2011')

fig = line_chart(data2)
fig.update_layout(height=500, width=1000)

st.plotly_chart(fig)

st.write('Deze interactieve lijngrafiek gebruikt alle data van de dataset. Op de verticale as is de temperatuur te lezen en op de horizontale as de tijd. Elke meetpunt kan worden geselecteerd en de periode kan je zelf ook aangeven door de selecteren. Dit is een duidelijke globale weergave van de dataset waarmee we nu het volgende mee wilden onderzoeken:\n'
         '- Is er sprake van opwarming van de aarde en hoeveel dan?\n'
         '- Boxplot?\n'
         '- Histogram?\n'
         '- ahhhh')

st.header('Gemiddelde temperatuur per maand, 1981 - 2011')

st.title("Hier een grafiek")

st.write('Deze spreidingsdiagram geeft een globale weergave aan van temperatuurstijging in Nederland. We moeten er meteen bijzeggen dat dit te weinig data hebben waardoor er toevalligheid kan zijn. En we hebben het gemiddelde genomen van elke maand, dus dat veranderd de trendlijn ook een beetje. (Daarvoor hebben we een tweede grafiek gemaakt waar wel alle data is gebruikt en waar de trendline nauwkeuriger is.) We hebben het gemiddelde van elke maand een apparte kleur gegeven zodat je duidelijk kan aflezen wat voornamelijkst de warmste maanden zijn en wat de koudste maanden.')

st.header('Opwarming van de aarde')

st.title("Hier een grafiek GRAFIEK 0.0447443 * Tijd (jaren) + -78.2203 0.000120045 * Tijd (dagen) + 10.4651")

st.header('Extreme waardes')

st.title("Hier een tabel")

st.write('Hierboven zie je een tabel van de top 10 koudste en warmste dagen van de periode 1981 - 2011. Je moet nagaan dat dit de gemiddelde temperatuur is van de hele dag. Dus er is om de zoveel tijd weer nieuwe meting gedaan en daarvan is het gemiddelde gedaan. Dus dat wil zeggen dat 27,9 °C niet de maximale temperatuur is, maar het gemiddelde. "Juli 2006 warmste maand in zeker 300 jaar" zegt het KNMI.')

st.title("Links")
st.write("https://docs.streamlit.io/en/stable/getting_started.html#add-text-and-data"
         "https://docs.streamlit.io/en/stable/api.html#magic-commands"
         "https://www.clo.nl/indicatoren/nl022613-temperatuur-mondiaal-en-in-nederland"
         "https://developer.dataplatform.knmi.nl/example-scripts"
         "https://dataplatform.knmi.nl/dataset/knmi14-gemiddelde-temperatuur-3-2"
         "https://discuss.streamlit.io/t/how-to-link-a-button-to-a-webpage/1661/7")
