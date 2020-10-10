import urllib
from lxml import html
import requests
from tabulate import tabulate
import pathlib
import base64

# de eerste def creërt een file en zorgt ervoor dat u uw key encoded in een file wordt gezet en in dezelfde directory
def keyfilecreater(padnaarfile):
    file1 = open("{}/Key.txt".format(padnaarfile), "w")
    key1 = str(input("Uw goodreadskey hier intypen a.u.b.: "))
    key1_bytes = key1.encode("utf-8")
    key1_bytes = base64.b64encode(key1_bytes)
    key1_messa = key1_bytes.decode("utf-8")
    key_enc = str(key1_messa)
    file1.write(key_enc)

# De tweede def leest de aangmaakte file en decode de encoded key en returnt deze
def keyfilereader(padnaarfile):
    file2 = open("{}/Key.txt".format(padnaarfile), "r")
    key2 = file2.read()
    key2_bytes = key2.encode("utf-8")
    key2_bytes = base64.b64decode(key2_bytes)
    key2_messa = key2_bytes.decode("utf-8")
    key_dec = str(key2_messa)
    return key_dec


# Vind het path waar deze file wordt gezet zodat de def een file daar creëren
path = pathlib.Path(__file__).parent.absolute()

# Trigger voor de while functie
trigger_while = True

# Input van goodreadskey
vraag = str(input("Heeft u al een goodreadskey ingegeven? (Ja/Nee)"))
if vraag.lower() == "nee":
    keyfilecreater(path)

# While functie om een loop te maken als de input verkeerd is
while trigger_while:
    # Key van Goodreads
    key = str(keyfilereader(path))

    # De user zijn input word encoded om direct als URL weer te geven en zal direct een request sturen naar goodreads
    user_input = input("Geef een titel of auteur: ")
    user_input_en =urllib.parse.quote(user_input)

    # Na de request zal de pagina content opgeslagen worden als HTML in de code als tree en zo verder gebruikt te worden
    tree = html.fromstring(requests.get("https://www.goodreads.com/search.xml?key=" + key + "&q=" + user_input_en).content)

    # Hier wordt alles uit de tree gehaald wat nuttig is voor de user, deze worden opgeslagen in lists
    invalid = tree.xpath('//text()')
    titles = tree.xpath('//title/text()')
    auteur = tree.xpath('//author/name/text()')
    rating = tree.xpath('//average_rating/text()')
    jaar = []
    id_nummer = tree.xpath('//work/id/text()')

    # For loop zorgt ervoor dat al de datums in de list jaar komt en zorgt er ook voor dat wanneer een boek geen datum heeft dit ook zo toont
    for x in tree.xpath('//original_publication_year'):
        if x.text: 
            jaar.append(x.text)
        else:
            jaar.append("Geen datum")

    # Kijkt na of dat de API key juist is ingegeven
    if invalid[0].lower() == "invalid api key.\n":
        print("Uw key is niet in orde. ---->", key)
        print("Typ uw key terug opnieuw in.")
        keyfilecreater(path)
    else:
        # De i is voor de while loop te starten en stoppen deze kijkt of dat al de titels zijn afgegaan
        i = 0
        # De if functie staat hier voor als de user een typfout hebt gemaakt bij de input, de else functie print alles af en zorgt ervoor dat het programme stopt
        if 0 == len(titles):
            print("Heeft u dit wel juist getypt?", user_input)
            print("Probeer het opnieuw.")
        else:
            # De while loop zorgt ervoor dat al de data in de lists wordt weergegeven
            print("**"*20)
            print("Hier zijn uw gevraagde boeken:")
            print("**"*20)
            while i < len(titles):
                print(tabulate([["BoekID","Titel","Auteur","Rating","Jaargang"],[id_nummer[i],titles[i],auteur[i],rating[i],jaar[i]]],headers="firstrow",tablefmt="fancy_grid"))
                i += 1
                if i == len(titles):
                    # Vraagt voor een tweede boek te vinden of te stoppen
                    search = str(input("Wilt u nog een boek zoeken? (Ja/Nee): "))
                    if search.lower() == "nee":
                        trigger_while = False