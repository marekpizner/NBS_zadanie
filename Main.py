import requests
import json

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
    parm = {'zmenene-od': '2000-01-01','ico': input("Enter ICO:")}

    data = rest_request(uctovne_jednotky_url, parm)

    output_str = {}
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
                if data3['datumZostaveniaK'] in output_str:
                    output_str[data3['datumZostaveniaK']] += (len(data3['idUctovnychVykazov']))
                else:
                    output_str[data3['datumZostaveniaK']] = (len(data3['idUctovnychVykazov']))
                output = True


    if output == False:
        print("prazdny vystup")
    else:
        for out in output_str:
            print(str(out) + "\t" + str(output_str[str(out)]))


def uloha2_one_page(data):
    if 'id' in data:
        for key in data['id']:
            #print(str(key))

            parm = {'id': str(key)}
            data2 = rest_request(uctovny_vykaz_url, parm)

            if 'idUctovnejZavierky' not in data2:
                continue

            parm2 = {'id':data2['idUctovnejZavierky']}
            data3 = rest_request(uctovna_zavierka_url, parm2)

            date = data3['datumZostaveniaK']
            if 'ico' in data3:
                print(str(key) + "\t" + str(data3['ico'])+ "\t" + str(date))
            else:
                parm3 = {'id': data3['idUJ']}
                data4 = rest_request(uctovna_jednotka_url,parm3)
                if 'ico' in data4:
                    print(str(key) + "\t" + str(data4['ico']) + "\t" + str(date))



def uloha2():
    input_str = input("Enter date:")
    parm = {'max-zaznamov': '1000', 'zmenene-od': input_str }
    data = rest_request(uctovne_vykazy_url, parm)
    uloha2_one_page(data)

    while 'pocetZostavajucichId' in data:
        #count = data['pocetZostavajucichId']
        l = len(data['id'])-1
        last = data['id'][l]
        parm = {'max-zaznamov': '1000', 'pokracovat-za-id': last, 'zmenene-od': input_str}
        data = rest_request(uctovne_vykazy_url,parm)
        uloha2_one_page(data)


#uloha1()
uloha2()

if __name__ == "__main__":
    uloha1()