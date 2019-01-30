import haravasto as h
import random as r
import time as t
tila = {
    "nakyva": None,
    "eriavat": None
}
HIIRI = {
    "HIIRI_VASEN": "vasen",
    "HIIRI_OIKEA": "oikea",
    "HIIRI_KESKI": "keski"
    }
alku = {
    "leveys": None,
    "korkeus": None,
    "miinat": None
}
tulokset = {
    "aika": t.strftime("%Y-%m-%d %H:%M:%S", t.localtime()),
    "kesto": None,
    "aloitus": None,
    "lopetus": None,
    "tulos": "Voitto",
    "vuorot": 0,
    "nimi": None,
    "min": 0,
    "sec": 0
}
#funktioiden järjestys:
#main
#piirra_kentta
#miinoita
#laske_ninjat
#laske_keski
#kasittele_hiiri
#tulvataytto
#tallenna_kokoelma
#lataa_tiedosto
#pyyda_syote
#pelin_aloitus
#lopetus
    
def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """

    h.lataa_kuvat("spritet")
    h.luo_ikkuna(alku["korkeus"] * 40, alku["leveys"] * 40)
    h.aseta_piirto_kasittelija(piirra_kentta)
    h.aseta_hiiri_kasittelija(kasittele_hiiri)
    tulokset["aloitus"] = t.time()
    h.aloita()
    
def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    h.tyhjaa_ikkuna ()
    h.piirra_tausta ()
    h.aloita_ruutujen_piirto ()
    for i, rivi in enumerate(tila["nakyva"]):
        for j, sarake in enumerate(rivi):
            h.lisaa_piirrettava_ruutu(sarake, j * 40, i * 40)
    h.piirra_ruudut ()
    
def miinoita(kentta, jaljella, miinat):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """
    for miina in range(miinat):
        a, b = r.choice(jaljella)
        kentta[a - 1][b - 1] = "x"
        jaljella.remove((a, b))
        
def laske_ninjat(x, y, huone):
    """
    Käy vierekkäiset ruudut läpi ja palauttaa niissä olevien miinojen määrän.
    """
    ninjat = 0
    korkeus = len(huone) - 1
    leveys = len(huone[0]) - 1
    if x == 0:
        xalku = x
        xloppu = x + 1
    elif x == leveys:
        xloppu = x
        xalku = x - 1
    else:
        xalku = x - 1
        xloppu = x + 1 
    if y == 0:
        yalku = y
        yloppu = y + 1
    elif y == korkeus:
        yalku = y - 1
        yloppu = y
    else:
        yalku = y - 1
        yloppu = y + 1
    for x in range(xalku, xloppu + 1):
        for y in range(yalku, yloppu + 1):
            if huone[y][x] == "x":
                ninjat += 1
    return ninjat
    
def laske_keski(x, y, huone):
    """
    Käy vierekkäiset ruudut läpi ja avaa tyhjät ruudut
    """
    korkeus = len(huone) - 1
    leveys = len(huone[0]) - 1
    if x == 0:
        xalku = x
        xloppu = x + 1
    elif x == leveys:
        xloppu = x
        xalku = x - 1
    else:
        xalku = x - 1
        xloppu = x + 1 
    if y == 0:
        yalku = y
        yloppu = y + 1
    elif y == korkeus:
        yalku = y - 1
        yloppu = y
    else:
        yalku = y - 1
        yloppu = y + 1
    for x in range(xalku, xloppu + 1):
        for y in range(yalku, yloppu + 1):
            if huone[y][x] == " ":
                huone[y][x] = piilo[y][x]
                if huone[y][x] == "x":
                    havio()
                if piilo[y][x] == "0":
                    tulvataytto(tila["nakyva"], x, y, piilo)

def kasittele_hiiri(i, j, painike, muokkauspainike):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    """
    if painike == 1:
        painike = HIIRI["HIIRI_VASEN"]
    if painike == 2:
        painike = HIIRI["HIIRI_KESKI"]
    if painike == 4:
        painike = HIIRI["HIIRI_OIKEA"]
    i = i // 40
    j = j // 40
    tila["eriavat"] = 0
    if painike == "oikea": #lipun lisäys
        if tila["nakyva"][j][i] == " ":
            tila["nakyva"][j][i] = "f"
        elif tila["nakyva"][j][i] == "f":
            tila["nakyva"][j][i] = " "
    elif painike == "keski": #keskinapin toiminta
        if tila["nakyva"][j][i] in "12345678":
           laske_keski(i, j, tila["nakyva"])
    else:
        tila["nakyva"][j][i] = piilo[j][i] #näyttää ruudun
    tulokset["vuorot"] += 1
    if tila["nakyva"][j][i] == "x": # miinaan osuminen
        havio()
    if tila["nakyva"][j][i] == "0":     #tulvatäyttö
        tulvataytto(tila["nakyva"], i, j, piilo)
    for b, ruudut in enumerate(tila["nakyva"]): # Voiton määritys
        for a, ruutu in enumerate(ruudut):
            if tila["nakyva"][b][a] == piilo[b][a]:
                pass
            else:
                tila["eriavat"] += 1
    if tila["eriavat"] == alku["miinat"]: # Voiton tarkistus
        voitto()

def tulvataytto(planeetta, aloitus_x, aloitus_y, planeetta_piilo):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    lista = [(aloitus_x, aloitus_y)]
    while True:
        piste = lista.pop()
        planeetta[piste[1]][piste[0]] = "0"
        korkeus = len(planeetta) - 1
        leveys = len(planeetta[0]) - 1
        x = piste[0]
        y = piste[1]
        if x == 0:
            xalku = x
            xloppu = x + 1
        elif x == leveys:
            xloppu = x
            xalku = x - 1
        else:
            xalku = x - 1
            xloppu = x + 1        
        if y == 0:
            yalku = y
            yloppu = y + 1
        elif y == korkeus:
            yalku = y - 1
            yloppu = y
        else:
            yalku = y - 1
            yloppu = y + 1
        for x in range(xalku, xloppu + 1):
            for y in range(yalku, yloppu + 1):
                if planeetta[y][x] == planeetta[piste[1]][piste[0]]:
                    pass
                else:
                    if planeetta_piilo[y][x] == "0":
                        lista.append((x, y))
                    if planeetta_piilo[y][x] in "12345678":
                        planeetta[y][x] = planeetta_piilo[y][x]

        if lista == []:
            break

def tallenna_kokoelma(tiedosto):
    try:
        with open(tiedosto, "a") as kohde:
                kohde.write("{aika}, {min}min{sec}sec, {tulos}, vuorot:{vuorot}, nick:{nimi}, {leveys}x{korkeus}, miinat:{miinat}\n".format(
                    aika = tulokset["aika"],
                    min = int(tulokset["min"]),
                    sec = int(tulokset["sec"]),
                    tulos = tulokset["tulos"],
                    vuorot = tulokset["vuorot"],
                    nimi = tulokset["nimi"],
                    leveys = alku["leveys"],
                    korkeus = alku["korkeus"],
                    miinat = alku["miinat"]
                ))
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tallennus epäonnistui")

def lataa_tiedosto(tiedosto):
    try:
        with open(tiedosto) as lahde:
            for rivi in lahde.readlines():
                print(rivi)
    except IOError:
        print("Tiedoston avaaminen ei onnistunut.")

def pyyda_syote(pyynto, virheviesti, minimi, maksimi):
    """
    Kysyy käyttäjältä kokonaislukua käyttäen kysymyksenä parametrina annettua
    merkkijonoa. Virheellisen syötteen kohdalla käyttäjälle näytetään toisena
    parametrina annettu virheilmoitus. Käyttäjän antama kelvollinen syöte
    palautetaan kokonaislukuna.
    """
    while True:
        try:
            kokonaisluku = int(input(pyynto))
        
        except ValueError:
            print(virheviesti)
            
        else:
            if kokonaisluku < minimi:
                print(virheviesti)
            elif kokonaisluku > maksimi:
                print(virheviesti)
            else:
                return kokonaisluku

def pelin_aloitus():
        alku["leveys"] = pyyda_syote("Anna kentän korkeus(2-20):","lue ohje uudestaan", 2, 20)
        alku["korkeus"] = pyyda_syote("Anna kentän leveys (2-30):", "lue ohje uudestaan", 2, 30)
        alku["miinat"] = pyyda_syote("Anna miinojen määrä (1-(leveys x korkeus-1)):", "lue ohje uudestaan", 1, alku["leveys"] * alku["korkeus"] - 1)
        return alku["leveys"], alku["korkeus"], alku["miinat"]

def voitto():
    h.lopeta()
    tulokset["lopetus"] = t.time()
    tulokset["min"], tulokset["sec"] = divmod((tulokset["lopetus"] - tulokset["aloitus"]), 60)
    print("Voitit pelin!")
    print("")
    tulokset["nimi"] = input("Annahan nimi nii laitetaan tulokset talteen:")
    tallenna_kokoelma("tulokset.txt")
    print("")
    
def havio():
    h.lopeta()
    tulokset["lopetus"] = t.time()
    tulokset["min"], tulokset["sec"] = divmod((tulokset["lopetus"] - tulokset["aloitus"]), 60)
    print("Siinä oli miina, hävisit pelin")
    print("")
    tulokset["tulos"] = "Hävio"
    tulokset["nimi"] = input("Annahan nimi nii laitetaan tulokset talteen:")
    tallenna_kokoelma("tulokset.txt")
    print("")


while True:
    tulokset["vuorot"] = 0
    print("Aloita peli: 1")
    print("Tulosta highscoret: 2")
    print("Lopeta: 3")
    if alku["leveys"] != None:
        print("Pelaa uudelleen edellinen kenttä: 4")
        arvo = pyyda_syote("Anna syöte:", "Ootko tosissas?", 1, 4)
    else:
        arvo = pyyda_syote("Anna syöte:", "Ootko tosissas?", 1, 3)
    if arvo == 1:
        pelin_aloitus()
    elif arvo == 2: 
        print("")
        lataa_tiedosto("tulokset.txt")    #tulosta highscoret
        print("Aloita peli: 1")
        print("Lopeta: 2")
        if alku["leveys"] != None:
            print("Pelaa uudelleen edellinen kenttä: 3")
            arvo = pyyda_syote("Anna syöte:", "Ootko tosissas?", 1, 3)
        else:
            arvo = pyyda_syote("Anna syöte:", "Ootko tosissas?", 1, 2)
        if arvo == 1:
            pelin_aloitus()
        elif arvo == 2:
            break
        elif arvo == 3:
            pass
    elif arvo == 3:
        break
    elif arvo == 4 and alku["leveys"] != None:
        pass
    print("")
    nakyva = [] # luodaan ruudukko joka näkyy pelaajalle
    for rivi in range(alku["leveys"]):
        nakyva.append([])
        for sarake in range(alku["korkeus"]):
            nakyva[-1].append(" ")
    tila["nakyva"] = nakyva
    piilo = [] # luodaan ruudukko, joka ei näy. Tähän laitetaan miinat ja numerot
    for rivit in range(alku["leveys"]):
        piilo.append([])
        for sarakkeet in range(alku["korkeus"]):
            piilo[-1].append(" ")
    jaljella = [] #miinoita funktiolle lista josta napataan miinat
    for i in range(alku["leveys"]):
        for j in range(alku["korkeus"]):
            jaljella.append((i, j))
    miinoita(piilo, jaljella, alku["miinat"])
    for j, ruutu in enumerate(piilo):
        for i, joku in enumerate(ruutu):
            if piilo[j][i] == "x":
                pass
            else:
                numero = laske_ninjat(i, j, piilo) #lisätään numerot piilo listaan
                piilo[j][i] = str(numero)
    main()