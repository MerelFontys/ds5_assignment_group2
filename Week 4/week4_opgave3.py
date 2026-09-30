# door merel 

import random

# vraag de grootte
grootte = 0
while grootte < 2 or grootte > 20:
    try:
        grootte = int(input("Hoe groot wil je dat je speelveld is? (NxN, 2 t/m 20): "))
    except ValueError:
        print("Gebruik alleen een geheel getal.")

aantal_mijnen = max(1, grootte * grootte // 6)


def print_bord(bord):
    print("   ", end="")
    for c in range(grootte):
        print(f"{c + 1:2}", end=" ")
    print()
    for r in range(grootte):
        print(f"{r + 1:2} ", end="")
        for c in range(grootte):
            print(f" {bord[r][c]}", end=" ")
        print()


def mijnen_maken():
    # 1 = mijn, 0 = geen mijn
    mijnen = [[0] * grootte for i in range(grootte)]
    geplaatst = 0
    while geplaatst < aantal_mijnen:
        r = random.randint(0, grootte - 1)
        c = random.randint(0, grootte - 1)
        if mijnen[r][c] == 0:
            mijnen[r][c] = 1
            geplaatst = geplaatst + 1
    return mijnen


def tel_buren(mijnen, r, c):
    # telt de mijnen in de 8 vakjes om (r, c) heen
    aantal = 0
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            nr = r + dr
            nc = c + dc
            if 0 <= nr < grootte and 0 <= nc < grootte:
                aantal = aantal + mijnen[nr][nc]
    return aantal


def open_vak(mijnen, zichtbaar, r, c):
    if zichtbaar[r][c] != ".":
        return
    aantal = tel_buren(mijnen, r, c)
    if aantal == 0:
        zichtbaar[r][c] = " "
        # geen mijnen in de buurt? laat dan alle vakjes in de buurt zien
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr = r + dr
                nc = c + dc
                if 0 <= nr < grootte and 0 <= nc < grootte:
                    open_vak(mijnen, zichtbaar, nr, nc)
    else:
        zichtbaar[r][c] = str(aantal)


def toon_mijnen(mijnen, zichtbaar):
    # kopie van het bord waarop alle mijnen als * staan
    bord = [row[:] for row in zichtbaar]
    for r in range(grootte):
        for c in range(grootte):
            if mijnen[r][c] == 1:
                bord[r][c] = "*"
    return bord


def nog_vakjes_over(mijnen, zichtbaar):
    # True zolang er een vakje zonder mijn nog dicht is
    for r in range(grootte):
        for c in range(grootte):
            if mijnen[r][c] == 0 and (zichtbaar[r][c] == "." or zichtbaar[r][c] == "F"):
                return True
    return False


def spelen():
    mijnen = mijnen_maken()
    zichtbaar = [["."] * grootte for i in range(grootte)]
    print(f"Er zitten {aantal_mijnen} mijnen op het veld.")

    while True:
        print()
        print_bord(zichtbaar)

        if not nog_vakjes_over(mijnen, zichtbaar):
            print("Hij is opgelost!")
            break

        tekst = input("Rij, kolom en 0 (open vakje) of 1 (zet/haal vlag weg), bijvoorbeeld '2 4 0'. Of 'oplossen' / 'stoppen': ")
        if tekst == "stoppen":
            break
        if tekst == "oplossen":
            print_bord(toon_mijnen(mijnen, zichtbaar))
            break

        onderdelen = tekst.split()
        if len(onderdelen) != 3:
            print("Typ precies drie getallen met een spatie ertussen.")
            continue
        try:
            r = int(onderdelen[0]) - 1
            c = int(onderdelen[1]) - 1
            keuze = int(onderdelen[2])
        except ValueError:
            print("Gebruik alleen gehele getallen.")
            continue

        if r < 0 or r >= grootte or c < 0 or c >= grootte or keuze < 0 or keuze > 1:
            print(f"Rij en kolom moeten 1 t/m {grootte} zijn en het laatste getal 0 of 1.")
            continue

        if keuze == 1:
            if zichtbaar[r][c] == ".":
                zichtbaar[r][c] = "F"
            elif zichtbaar[r][c] == "F":
                zichtbaar[r][c] = "."
            else:
                print("Dit vakje is al open.")
        else:
            if zichtbaar[r][c] == "F":
                print("Haal eerst de vlag weg (laatste getal 1).")
            elif zichtbaar[r][c] != ".":
                print("Dit vakje is al open.")
            elif mijnen[r][c] == 1:
                print("Je hebt een mijn geraakt...")
                print_bord(toon_mijnen(mijnen, zichtbaar))
                break
            else:
                open_vak(mijnen, zichtbaar, r, c)


spelen()