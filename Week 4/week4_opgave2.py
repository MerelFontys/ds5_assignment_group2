import random

def print_bord(bord):
    for r in range(9):
        if r == 3 or r == 6:
            print("------+-------+------")
        for c in range(9):
            if c == 3 or c == 6:
                print("|", end=" ")
            if bord[r][c] == 0:
                print(".", end=" ")
            else:
                print(bord[r][c], end=" ")
        print()
'''
maakt een raster aan van 9x9
als er geen getal op een plek staat (=0), dan een "." voor overzicht
'''

def is_mogelijk(bord, r, c, num):
    # is er een waarde gelijk aan het nummer in de rij of de kolom?
    for i in range(9):
        if bord[r][i] == num:
            return False
        if bord[i][c] == num:
            return False
    # is er een waarde gelijk aan het nummer in het 3x3 vakje?
    start_r = (r // 3) * 3 # door middel van floordivision bepaalt dit in welk 3x3 blok je moet kijken
    start_c = (c // 3) * 3
    for i in range(start_r, start_r + 3):
        for j in range(start_c, start_c + 3):
            if bord[i][j] == num:
                return False
    return True
'''
checkt of de mogelijke waarde in die rij, die kolom en dat vakje past
ja? --> True
nee? --> False
'''

def oplossen(bord, mix=False):
    # zoek de eerstvolgende lege plek en probeer 1 t/m 9
    for r in range(9):
        for c in range(9):
            if bord[r][c] == 0:
                getallen = [1, 2, 3, 4, 5, 6, 7, 8, 9] # ga alle mogelijkheden af van 1 t/m 9 totdat je een mogelijkheid vindt
                if mix:
                    random.shuffle(getallen) # geen enkel getal kan meer? Mix = True en shuffle de getallen naar een nieuwe volgorde
                for getal in getallen:
                    if is_mogelijk(bord, r, c, getal):
                        bord[r][c] = getal
                        if oplossen(bord, mix):
                            return True
                        bord[r][c] = 0
                return False
    return True
'''
lost het bord op
'''

def puzzel_maken(remove=40):
    bord = [[0] * 9 for i in range(9)]
    oplossen(bord, True)
    count = 0
    while count < remove:
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        if bord[r][c] != 0:
            bord[r][c] = 0
            count = count + 1
    return bord
'''
maakt een bestaand bord en verwijdert 40 getallen van de 81 zodat je kunt puzzelen
'''

def nog_lege_vakjes(bord):
    for r in range(9):
        for c in range(9):
            if bord[r][c] == 0:
                return True
    return False
'''
controleert of er nog 'lege vakjes' zijn door te checken of er nog een waarde is die gelijk is aan 0
returned true(er zijn geen lege vakken meer) of false(er is nog een waarde gelijk aan 0)
'''

def spelen():
    start = puzzel_maken()
    bord = [row[:] for row in start] # maak een kopie van het bord zodat je tijdens het invullen geen dingen overschrijft

    while True:
        print('\n', end=''); print_bord(bord); print('\n', end='') # print het bord opnieuw voor elke stap

        if not nog_lege_vakjes(bord): # als er geen lege vakjes meer zijn --> klaar
            print("De sudoku is opgelost")
            break

        tekst = input(f"Geef een rij, kolom en getal --- Bijvoorbeeld '2 4 6' \n Wil je een getal wissen? Geef de locatie en waarde 0 \n Andere opties: 'oplossen' of 'stoppen'")
        if tekst == "stoppen":
            break
        if tekst == "oplossen":
            bord = [row[:] for row in start]
            oplossen(bord)
            print_bord(bord)
            break

        onderdelen = tekst.split()
        if len(onderdelen) != 3:
            print("Typ precies drie getallen met alleen een spatie er tussen")
            continue
        try: # stop niet als dit niet lukt
            r = int(onderdelen[0]) - 1
            c = int(onderdelen[1]) - 1
            num = int(onderdelen[2])
        except ValueError: # als deze error komt, vraag om 3 integers
            print("Gebruik alleen gehele getallen en geen letters of leestekens.")
            continue

        if r < 0 or r > 8 or c < 0 or c > 8 or num < 0 or num > 9:
            print("Rij en kolom moeten 1-9 zijn en het getal 0-9.")
            continue
        if start[r][c] != 0:
            print("Dit vakje is onderdeel van het startbord, kies een ander vakje.")
            continue

        oud = bord[r][c] # onthoud het oude nummer voordat je een aanpassing maakt
        bord[r][c] = 0 # maak het vakje tijdelijk leeg zodat je kunt checken op dubbele getallen
        if num != 0 and not is_mogelijk(bord, r, c, num):
            print("Dat getal mag hier niet (staat al in rij, kolom of 3x3 vak).")
            bord[r][c] = oud
        else:
            bord[r][c] = num

spelen()