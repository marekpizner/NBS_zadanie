import requests
import json
import dateutil.parser as p

uctovne_jednotky_url = 'http://www.registeruz.sk/cruz-public/api/uctovne-jednotky'
uctovna_jednotka_url = 'http://www.registeruz.sk/cruz-public/api/uctovna-jednotka'
uctovna_zavierka_url = 'http://www.registeruz.sk/cruz-public/api/uctovna-zavierka'

uctovne_vykazy_url = 'http://www.registeruz.sk/cruz-public/api/uctovne-vykazy'
uctovny_vykaz_url = 'http://www.registeruz.sk/cruz-public/api/uctovny-vykaz'


def rest_request(url, params):
    response = requests.get(url, params=params)
    if (response.ok):
        json_response = json.loads(response.content)
    else:
        json_response = 0;
    return json_response


def uloha1():
    parm = {'ico': input("Enter ICO:")}
    parm = {'zmenene-od': '2000-01-01'}

    data = rest_request(uctovne_jednotky_url, parm)

    output_str = []
    output = False

    for key in data['id']:
        # print(str(key))
        parm2 = {'id': str(key)}
        data2 = rest_request(uctovna_jednotka_url, parm2)
        if 'idUctovnychZavierok' in data2:
            for key2 in data2['idUctovnychZavierok']:
                # print(str(key2))
                parm3 = {'id': str(key2)}
                data3 = rest_request(uctovna_zavierka_url, parm3)
                # print(data3['datumZostaveniaK'], len(data3['idUctovnychVykazov']))
                output_str.append([data3['datumZostaveniaK'], len(data3['idUctovnychVykazov'])])
                output = True

    if output == False:
        print("prazdny vystup")
    else:
        sorted(output_str, key=lambda d: p.parse(d[0]))
        for out in output_str:
            print(str(out[0]) + "\t" + str(out[1]))


def uloha2():
    parm = {'zmenene-od': input("Enter date:")}
    data = rest_request(uctovne_vykazy_url, parm)

    for key in data['id']:
        print(str(key))
        parm = {'id': str(key)}
        data2 = rest_request(uctovny_vykaz_url, parm)


uloha1()
# uloha2()
