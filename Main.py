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

def boxplot(data_clean):
    fig = px.box(data_frame=data_clean,
                 x='Gemiddelde',
                 hover_data=[data_clean.index.date, data_clean['Standaarddeviatie']],
                 labels={'Gemiddelde': 'Gemiddelde temperatuur in °C', 'hover_data_0': 'Datum'},
                 orientation='h',
                 height=300,
                 color_discrete_sequence=px.colors.qualitative.Dark2)

    fig.update_layout(title="Boxplot gemiddelde temperatuur van weerstations in Nederland 1981-2010", title_x=0.5)

    # fig.show()
    return fig

def boxplot2(data_clean):
    fig = px.box(data_frame=data_clean,
                 x='Standaarddeviatie',
                 hover_data=[data_clean.index.date, data_clean['Gemiddelde']],
                 labels={'Standaarddeviatie': 'Standaarddeviatie gemiddelde temperatuur in °C',
                         'hover_data_0': 'Datum'},
                 orientation='h',
                 height=300,
                 color_discrete_sequence=px.colors.qualitative.Bold)

    fig.update_layout(title="Boxplot standaarddeviatie gemiddelde temperatuur van weerstations in Nederland 1981-2010",
                      title_x=0.5)

    # fig.show()
    return fig

def scatter(data_clean):
    # We kunnen ook de gemiddelde temperatuur per maand berekenen en daar een plot van maken

    gem_temp = pd.DataFrame(columns=['Gemiddelde'], index=range(0, 360))

    k = 0
    for i in range(1981, 2011):
        for j in range(1, 13):
            gem_temp.iloc[k, 0] = (
                round(data_clean[(data_clean.index.month == j) & (data_clean.index.year == i)]['Gemiddelde'].mean(), 1))
            k += 1

    # Dit zorgt voor de juiste getallen bij de x-as

    k = 0
    for i in range(1981, 2011):
        for j in range(0, 12):
            gem_temp.loc[k, 'Tijd'] = i + j / 12
            k += 1

    # Jaartal om te laten zien bij het hoveren

    k = 0
    for i in range(1981, 2011):
        for j in range(0, 12):
            gem_temp.loc[k, 'Jaartal'] = i
            k += 1

    # Maand om te laten zien bij het hoveren

    lijst_maanden = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli',
                     'augustus', 'september', 'oktober', 'november', 'december']

    j = 0
    for i in range(0, 360):
        gem_temp.loc[i, 'Maand'] = lijst_maanden[j]
        j += 1
        if j == 12:
            j = 0

    fig = px.scatter(data_frame=gem_temp,
                     x=gem_temp['Tijd'],
                     y=gem_temp['Gemiddelde'],
                     trendline='ols',
                     height=550,
                     width=750,
                     title='Spreidingsdiagram gemiddelde temperatuur per maand in Nederland 1981-2010',
                     trendline_color_override='black',
                     labels={'Gemiddelde': 'Gemiddelde temperatuur in °C', 'Tijd': 'Jaartal'},
                     hover_data=['Jaartal', 'Maand'],
                     color=gem_temp['Maand'],
                     trendline_scope='overall',
                     color_discrete_sequence=px.colors.qualitative.Light24)
    
    annotation1 = {'x':1997,
    'y':0.5,
    'showarrow':True,
    'arrowhead':5,
    'text':"Laatste elfstedentocht",
    'font':{'size': 11}}

    annotation2 = {'x':1986,
    'y':-1.2,
    'showarrow':True,
    'arrowhead':5,
    'text':"Elfstedentocht 1986",
    'font':{'size': 11}}

    annotation3 = {'x':1982,
    'y':-1.5,
    'showarrow':False,
    'arrowhead':5,
    'text':"Elfstedentocht 1985",
    'font':{'size': 11}}

    fig.update_layout({'annotations': [annotation1, annotation2, annotation3]})
    
    # fig.show()
    return fig

def scatter2(data_clean):
    data_clean['Tijd in jaren'] = range(0, len(data_clean))
    data_clean['Tijd in jaren'] = data_clean['Tijd in jaren'] / 365.25 + 1981
    data_clean['Gemiddelde temp.'] = data_clean['Gemiddelde']

    fig = px.scatter(data_frame=data_clean,
                     x=data_clean['Tijd in jaren'],
                     y=data_clean['Gemiddelde temp.'],
                     trendline='ols',
                     height=550,
                     width=750,
                     title='Trendlijn gemiddelde temperatuur in Nederland 1981-2010',
                     trendline_color_override='red',
                     labels={'Gemiddelde temp.': 'Gemiddelde temperatuur in °C'},
                     trendline_scope='overall',
                     range_y=[9, 13],
                     range_x=[1980, 2012])

    fig.update_traces(visible=False, selector=dict(mode="markers"))

    # fig.show()
    return fig

def tabel(data_clean):
    regressie = pd.DataFrame(columns=['De Bilt', 'Rotterdam', 'Maastricht', 'Vlissingen', 'Leeuwarden',
                                      'Lente', 'Zomer', 'Herfst', 'Winter', 'Totaal'],
                             index=['Opwarming per 10 jaar', 'lege rij', 'Ondergrens: 0.025', 'Bovengrens: 0.975'])

    # regressie['De Bilt'] = voorspel_stations['De Bilt UT']
    # regressie['Rotterdam'] = voorspel_stations['Rotterdam ZH']
    # regressie['Maastricht'] = voorspel_stations['Maastricht LI']
    # regressie['Vlissingen'] = voorspel_stations['Vlissingen ZE']
    # regressie['Leeuwarden'] = voorspel_stations['Leeuwarden FR']
    #
    # regressie['Lente'] = voorspel_seizoenen['lente']
    # regressie['Zomer'] = voorspel_seizoenen['zomer']
    # regressie['Herfst'] = voorspel_seizoenen['herfst']
    # regressie['Winter'] = voorspel_seizoenen['winter']
    #
    # regressie['Totaal'] = voorspel_stations['Gemiddelde']

    regressie2 = regressie.drop(index='lege rij')
    regressie2.index = ['Geschatte opwarming per 10 jaar', 'Ondergrens schatting', 'Bovengrens schatting']
    return regressie2

def koudste_warmste(data_clean):
    # Top 10 koudste en warmste dagen
    # Leuk feitje: 4 januari 1997 was de laatste Elfstedentocht en ook in 1985 op 21 februari werd hij gereden

    top_10_koud = pd.DataFrame(data_clean.sort_values(by='Gemiddelde')['Gemiddelde'].head(10))
    top_10_warm = pd.DataFrame(data_clean.sort_values(by='Gemiddelde', ascending=False)['Gemiddelde'].head(10))

    top_10_koud2 = top_10_koud.reset_index()
    top_10_warm2 = top_10_warm.reset_index()

    top_10 = pd.DataFrame(columns=['Datum van laagste', 'Laagste temperatuur', 'Datum van hoogste', 'Hoogste temperatuur'],
                          index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


    top_10['Datum van laagste'] = top_10_koud2['Datum']
    top_10['Laagste temperatuur'] = top_10_koud2['Gemiddelde']
    top_10['Datum van hoogste'] = top_10_warm2['Datum']
    top_10['Hoogste temperatuur'] = top_10_warm2['Gemiddelde']



    top_10.index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    return top_10

# Eerst maar is de data downloaden van de KNMI website




st.image(
    "https://i.ibb.co/R79T9ct/Naamloos.png",
    # Manually Adjust the width of the image as per requirement
)
st.title('Analyse temperatuur KNMI 1981-2010')



checkbox = st.checkbox('Selecteer deze checkbox om de blog te lezen')
try:
    data = download_data()
except:
    st.error("We hebben wel een internet verbinding nodig.")

if checkbox:

    st.title('Inhoudsopgave')
    st.write('  - Inleiding\n'
             '  - API ophalen van KNMI\n'
             '  - Data bewerken\n'
             '  - Visualisatie\n'
             '  - Voorspelling\n'
             '  - Literatuurlijst\n'
             '  - Gemaakt door')


    st.title('Inleiding')
    # st.write('Wij hebben een API opgehaald van de KNMI website. Deze data hebben we eerst opgeschoond en gegevens toegevoegd zoals het gemiddelde en standaard deviatie. We hebben vervolgens een globale weergave gemaakt en zijn opzoek gegaan naar een gemiddelde temperatuur stijging, ......')
    st.write('Deze blog is gemaakt door studenten van de minor Data Science aan de Hogeschool van Amsterdam. Zij kregen de opdracht om een data-analyse te maken waarbij de data en het onderwerp zelf mochten worden gekozen. \n\nHet klimaatprobleem is één van de grootste uitdagingen van onze tijd en daarom hebben wij ervoor gekozen om onderzoek te doen naar de temperatuur in Nederland. Via een API van het KNMI hebben we data ingeladen: de gemiddelde temperatuur per dag voor 14 weerstations in Nederland voor de periode 1981 t/m 2010.\n\nMet behulp van de data proberen we antwoord te geven op de volgende vraag: wordt het warmer in Nederland? En zo ja: hoe snel gaat dat? We hebben eerst de data schoongemaakt zodat deze gebruiksklaar was en vervolgens hebben we verschillende analyses uitgevoerd en visualisaties gemaakt. Hierbij hebben we gebruik gemaakt van de programmeertaal Python en Jupyter Notebook. Veel leesplezier!')

    st.title('Data ophalen via een API van het KNMI')
    st.write('KNMI staat voor Koninklijk Nederlands Meteorologisch Instituut. Het KNMI heeft een website en deze is van de overheid. Op de website staan openbare API’s (Application Programming Interface) waarvan wij er één hebben gebruikt. Deze website legt volledig uit hoe je met een API data kan inladen. We hebben het stappenplan volledig gevolgd en uiteindelijk data ingeladen in Jupyter Notebook. We gebruiken Jupyter Notebook om met Python te werken. Hieronder zie je een schematische weergave van de data-tabel die we hebben ingeladen.')


    st.write(data.head(7))

    link = '[KNMI API example](https://developer.dataplatform.knmi.nl/example-scripts)'
    st.markdown(link, unsafe_allow_html=True)


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

    st.title('Data schoonmaken & bewerken')
    st.write('Voordat we echt aan de slag kunnen met onze data moeten we de data opschonen. Dit hebben we gedaan door eerst de kolommen een naam te geven. Dit konden we afleiden van de KNMI-website. Hier is bijvoorbeeld nummer 240 de locatie op Schiphol. Hieronder zie je een afbeelding waar zo makkelijk te herleiden is welk nummer bij welk station hoort. Na het toevoegen van de kolommen kwamen we erachter dat we nog een aantal rijen moesten laten vallen, want die behoorden niet tot de relevante data. We hebben ook een controle gedaan of er missende gegevens waren, maar gelukkig waren die er niet. We hebben de kolom met getallen die de datum moeten voorstellen omgezet in werkelijke tijdsdata (een zogenaamde timeseries). Dit was noodzakelijk om te kunnen filteren op bijvoorbeeld een specifiek jaar. Vervolgens hebben we nog een kolom met de gemiddelde temperatuur van alle weerstations toegevoegd en een kolom met de standaardafwijking daarvan.')

    # Afbeelding toevoegen: KNMI_meetpunten.png
    st.image(
        "https://i.ibb.co/2cVCFHZ/Microsoft-Teams-image.png",
          # Manually Adjust the width of the image as per requirement
    )

    st.write('Na het toevoegen van de kolommen kwamen we erachter dat we nog een aantal rijen moesten laten vallen, want die behoorde niet tot de dataset. We hebben ook een controlle gedaan of er missende gegevens zijn, maar gelukkig waren er geen missende gegevens. ')

    st.write(data2.head())

    st.write('We hebben de dataset gekoppieerd waarbij een dataset de datum als een index is en een dataset waarbij de datum een kolom is. Dit hebben we gedaan voor enkele visualisaties die je later in deze blog gaat zien. Na deze aanpassingen hebben we een gemiddelde en een standaard deviatie toegevoegd aan de datasets')



    st.write(data_clean.head())


    st.title('Visualisaties')
    st.header('Temperatuur in Nederland, 1981 - 2010')

    stations = st.multiselect(
            "Kies meet station", list(data_clean.columns), ["Valkenburg ZH", "Schiphol NH"]
        )


    if not stations:
        st.error("Please select at least one station.")
    else:
        data_search = data_clean.loc[:, stations]
        # st.write("Geselecteerde data", data_search.sort_index())
        # st.line_chart(data_search)

        fig = px.line(data_search)
        # fig = make_subplots(specs=[[{"secondary_y": True}]])
        # fig.add_trace(go.Scatter(data_search))

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
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            title_text="Temperatuur over de tijd van alle meetpunten en het gemiddelde"
        )

        fig.update_xaxes(title_text="Tijd in dagen/maanden/jaar (met scrollbar)")

        fig.update_yaxes(title_text="Temperatuur in graden Culsius (°C)",
                         secondary_y=False)
        st.plotly_chart(fig)

    st.write('Deze interactieve lijngrafiek gebruikt alle data van de dataset. Op de verticale as is de temperatuur te lezen en op de horizontale as de tijd. Elke meetpunt kan worden geselecteerd en de periode kan je zelf ook aangeven door te selecteren. Dit is een duidelijke globale weergave van de dataset. Om een nog beter beeld te krijgen van de data hebben we de volgende visualisaties gemaakt:\n'
             '- Boxplot gemiddelde temperatuur, 1981-2010\n'
             '- Boxplot standaarddeviatie, 1981-2010\n'
             '- Gemiddelde temperatuur per maand, 1981 - 2010?\n'
             '- Opwarming van Nederland\n'
             '- Extreme waardes')






    # fig = line_chart(data2)
    # fig.update_layout(height=500, width=1000)
    #
    # st.plotly_chart(fig)

    st.header('Boxplot gemiddelde temperatuur')



    fig = boxplot(data_clean)
    st.plotly_chart(fig)



    st.write('We hadden twee kolommen toegevoegd aan de dataset, namelijk de gemiddelde temperatuur van alle weerstations en de standaarddeviatie daarvan. Een boxplot zet al die waardes op een rijtje van klein naar groot en pakt vervolgens de mediaan, het getal wat in het midden ligt. Dat is de verticale groene streep in het midden van de grafiek. De waarde hiervan is 11,1 °C. Vervolgens pakt hij de waardes die op 1/4 en op 3/4 van de getallenreeks staan. In dit geval 6,6 °C en 16 °C. Dit maakt samen de box en 50% van alle waarnemingen liggen hierin. De twee lijnen die uitsteken aan de box bevatten de meeste overige waardes, de onderste en bovenste 25%. Echter, je ziet nog enkele punten aan de linker kant. Dit zijn uitbijters, extreme waarden. De boxplot geeft dus inzicht in de verdeling van de gemiddelde temperatuur.')

    st.header('Boxplot standaarddeviatie')

    fig = boxplot2(data_clean)
    st.plotly_chart(fig)

    st.write('De standaarddeviatie van de gemiddelde temperatuur van alle meetstations is een maat voor de spreiding van de temperatuur over verschillende locaties in Nederland. Hoe groter de standaarddeviatie, hoe meer temperatuurverschil tussen de locaties. We zien dat stations gemiddelde zo’n 0,7 graden van elkaar verschillen. Bijna altijd is de standaardafwijking kleiner dan 1,5 graden. Er zijn wel enkele opvallende uitschieters aan de rechterkant te zien.')


















    st.header('Gemiddelde temperatuur per maand')
    st.write("F1: 0.0447443 * Tijd (jaren) + -78.2203")
    fig = scatter(data_clean)
    st.plotly_chart(fig)

    st.write('Deze spreidingsdiagram geeft een globale weergave aan van temperatuurstijging in Nederland. We moeten er meteen bijzeggen dat dit te weinig data hebben waardoor er toevalligheid kan zijn. En we hebben het gemiddelde genomen van elke maand, dus dat veranderd de trendlijn ook een beetje. (Daarvoor hebben we een tweede grafiek gemaakt waar wel alle data is gebruikt en waar de trendline nauwkeuriger is.) We hebben het gemiddelde van elke maand een apparte kleur gegeven zodat je duidelijk kan aflezen wat voornamelijkst de warmste maanden zijn en wat de koudste maanden.')

    
    
    
    
    st.header('Opwarming van Nederland')

    st.write("F2: 0.000120045 * Tijd (dagen) + 10.4651")

    fig = scatter2(data_clean)
    st.plotly_chart(fig)

    st.write('Deze grafiek is bijna hetzelfde als de gemiddelde temperatuur per maand, alleen is hier ingezoomd om de trendlijn en zijn alle data gebruikt en geen gemiddelde. Bij beide grafieken staan twee formules omschreven, F1 en F2. F1 heeft een stijging van 0.0447443 per jaar. F2 heeft een stijging van 0.0438164 per jaar. Het verschil door het gemiddelde hebben we eruit gehaald, waardoor F2 veel nauwkeuriger is.')







    st.header('Extreme waardes')

    extreme = koudste_warmste(data_clean)
    st.write(extreme)

    st.write('Hierboven zie je een tabel van de top 10 koudste en warmste dagen van de periode 1981 - 2010. Je moet nagaan dat dit de gemiddelde temperatuur is van de hele dag. Dus er is om de zoveel tijd weer nieuwe meting gedaan en daarvan is het gemiddelde gedaan. Dus dat wil zeggen dat 27,9 °C niet de maximale temperatuur is, maar het gemiddelde. "Juli 2006 warmste maand in zeker 300 jaar" zegt het KNMI. Aan de hand van deze gegevens gaan we een voorspelling doen.')



    st.title('Voorspelling')

    st.write('Wij gaan een voorspelling uitvoeren wat de temperatuur is in het jaar 2030, 2050 en 2100. We gebruiken voor deze voorspelling formule: F2. We moeten er wel bij zeggen dat deze voorspelling niet volledig correct kan zijn, omdat we te weinig tijd hadden om een goede analyse te maken en omdat we te weinig data hebben.')


    st.write('We voorspellen dat de gemiddelde temperatuur voor: \n'
             '- 2030: 12.61 °C\n' 
             '- 2050: 13.49 °C\n' 
             '- 2100: 15.68 °C')




    st.title("Literatuurlijst")
    st.write("https://docs.streamlit.io/en/stable/getting_started.html#add-text-and-data"
             "https://docs.streamlit.io/en/stable/api.html#magic-commands"
             "https://www.clo.nl/indicatoren/nl022613-temperatuur-mondiaal-en-in-nederland"
             "https://developer.dataplatform.knmi.nl/example-scripts"
             "https://dataplatform.knmi.nl/dataset/knmi14-gemiddelde-temperatuur-3-2"
             "https://discuss.streamlit.io/t/how-to-link-a-button-to-a-webpage/1661/7")


    st.title('Gemaakt door')
    st.write(' 	- Marcel Zwagerman	500889946\n'
             '  - Sjoerd Fijne		500828895\n'
             '  - Mirko Bosch		500888784\n'
             '  - Martijn Draper	500888847')
