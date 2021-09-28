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