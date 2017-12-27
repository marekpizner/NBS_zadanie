import requests
import json
import os

uctovne_jednotky_url = 'http://www.registeruz.sk/cruz-public/api/uctovne-jednotky'
uctovna_jednotka_url = 'http://www.registeruz.sk/cruz-public/api/uctovna-jednotka'
uctovna_zavierka_url = 'http://www.registeruz.sk/cruz-public/api/uctovna-zavierka'

uctovne_vykazy_url = 'http://www.registeruz.sk/cruz-public/api/uctovne-vykazy'
uctovny_vykaz_url = 'http://www.registeruz.sk/cruz-public/api/uctovny-vykaz'


def rest_request(url, params):
    """
    Nacita url a vykona get request na danej url
    :param url: cielova url
    :param params: parametre dopytu
    :return: vystup z requestu v jsone
    """
    response = requests.get(url, params=params)
    if (response.ok):
        json_response = json.loads(response.content)
    else:
        json_response = 0;
    return json_response


def uloha1():
    """
    Uloha 1
    :return:
    """
    #Nacitam ICO z klavesnice
    parm = {'zmenene-od': '2000-01-01', 'ico': input("Enter ICO:")}
    #REST dopyt
    data = rest_request(uctovne_jednotky_url, parm)

    output_str = {}

    #Cylkicky prechadzam jednotilve id-cka a vukonavam dopyty na zaklade ziskanych dat
    for key in data['id']:
        parm2 = {'id': str(key)}
        data2 = rest_request(uctovna_jednotka_url, parm2)
        if 'idUctovnychZavierok' in data2:
            for key2 in data2['idUctovnychZavierok']:
                parm3 = {'id': str(key2)}
                data3 = rest_request(uctovna_zavierka_url, parm3)

                if data3['datumZostaveniaK'] in output_str:
                    output_str[data3['datumZostaveniaK']] += (len(data3['idUctovnychVykazov']))
                else:
                    output_str[data3['datumZostaveniaK']] = (len(data3['idUctovnychVykazov']))
                output = True

    #Vystup na konzolu
    if len(output_str) == 0:
        print("prazdny vystup")
    else:
        for out in output_str:
            print(str(out) + "\t" + str(output_str[str(out)]))


def uloha2_one_page(data):
    """
    Funkcia ktora pre kazde id z listu \"uctovne-jednotky\" vyhlada ICO a datum
    :param data: zoznam id-ciek
    :return:
    """
    if 'id' in data:
        for key in data['id']:

            parm = {'id': str(key)}
            data2 = rest_request(uctovny_vykaz_url, parm)

            if 'idUctovnejZavierky' not in data2:
                continue

            parm2 = {'id': data2['idUctovnejZavierky']}
            data3 = rest_request(uctovna_zavierka_url, parm2)

            date = data3['datumZostaveniaK']
            if 'ico' in data3:
                print(str(key) + "\t" + str(data3['ico']) + "\t" + str(date))
            else:
                parm3 = {'id': data3['idUJ']}
                data4 = rest_request(uctovna_jednotka_url, parm3)
                if 'ico' in data4:
                    print(str(key) + "\t" + str(data4['ico']) + "\t" + str(date))


def uloha2():
    """
    Uloha 2
    :return:
    """
    #Nacitam vstup z klavesnice
    input_str = input("Enter date:")
    parm = {'max-zaznamov': '1000', 'zmenene-od': input_str}
    #Ziskam 1. stranu id-ciek
    data = rest_request(uctovne_vykazy_url, parm)
    #Zavolam funkciu na hladanie ICO a datmu
    uloha2_one_page(data)

    #Cyklus v kt. sa riesi strankovanie
    while 'pocetZostavajucichId' in data:
        length = len(data['id']) - 1
        last = data['id'][length]
        parm = {'max-zaznamov': '1000', 'pokracovat-za-id': last, 'zmenene-od': input_str}
        #Po zisteni posledneho id a zmeneni parametrov \"parm\" zavolam REST dopyt
        data = rest_request(uctovne_vykazy_url, parm)
        uloha2_one_page(data)
        #Kontrola posledneho dopytu, ak pocetZostavajucichId == 0, typ padom koncim cyklus
        if data['pocetZostavajucichId'] == 0:
            break;


if __name__ == "__main__":
    #Nacitanie enviroment variables, na zaklade kt. sa rozhodne aka uloha sa spusti
    if os.environ.get('ULOHA') is not None:
        if os.environ['ULOHA'] == '1':
            uloha1()
        elif os.environ['ULOHA'] == '2':
            uloha2()
    else:
        #Ak nie su enviroment variables tak sa spustia obe
        uloha1()
        uloha2()
