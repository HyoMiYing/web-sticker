import random

ZGUBLJENE_POZICIJE = [((1, 1),)]
DOBLJENE_POZICIJE = []
ZACETNE_POTEZE = [((3,1),(5, 1), (7,1)), ((1,1),(2,1),(5,1),(7,1)), ((1,1),(3,1),(4,1),(7,1)), ((1,1),(3,1),(5,1),(4,1)), ((1,1),(3,1),(5,1),(4,1)), ((1,1),(3,1),(5,1),(6,1))]




def analiza(position, difficulty):
    
    
    drevesa_moznosti = {}
    drevo_tockovanja1 = {}
    drevo_moznosti1 = {}

    pos_mat = zapis_mat(position)
    pos_nabor = zapis_nabor(position)
    
    #Robni primeri
    if pos_mat == {(1,1)}:
            return ((0,1),)

    
    if difficulty == 'advanced':
        if pos_mat == {(1,1), (3,1), (5,1), (7,1)}:
            return random.choice(ZACETNE_POTEZE)
        elif pos_mat == {(5,1), (7,1), (1,1)}:
            return ((1,1), (5,1),(4,1))

    drevo_moznosti1 = mozne_poteze(pos_nabor)
    drevesa_moznosti[1] = drevo_moznosti1

    drevo_moznosti1 = {}

    #Iskanje v globino

    for nabor_stopnje_1 in drevesa_moznosti[1]:
        if nabor_stopnje_1 in ZGUBLJENE_POZICIJE:
            return nabor_stopnje_1
        elif nabor_stopnje_1 in DOBLJENE_POZICIJE:
            pass
        else:
            drevo_moznosti1[nabor_stopnje_1] = mozne_poteze(nabor_stopnje_1)
    
    
    drevesa_moznosti[2] = drevo_moznosti1
    drevo_moznosti1 = {}
    drevo_moznosti2 = {}


    for nabor_stopnje_1,  seznam_naborov_stopnje_2 in drevesa_moznosti[2].items():
        
        switch = True
        for nabor_stopnje_2 in seznam_naborov_stopnje_2:
            if nabor_stopnje_2 in ZGUBLJENE_POZICIJE:
                switch = False
            else:
                drevo_moznosti2[nabor_stopnje_2] = mozne_poteze(nabor_stopnje_2)
        
        if switch:
            drevo_moznosti1[nabor_stopnje_1] = drevo_moznosti2
        drevo_moznosti2 = {}
    
    if drevo_moznosti1 == {}:
        return random.choice([x for x in drevesa_moznosti[2].keys()])
    else:
        drevesa_moznosti[3] = drevo_moznosti1

    drevo_moznosti1, drevo_moznosti2, drevo_moznosti3 = {}, {}, {}
    
    for nabor_stopnje_1, slovar_naborov_stopnje_2_3 in drevesa_moznosti[3].items():
        count = 0
        for nabor_stopnje_2, seznam_naborov_stopnje_3 in slovar_naborov_stopnje_2_3.items():
            switch = False
            switch2 = False
            for nabor_stopnje_3 in seznam_naborov_stopnje_3:
                if nabor_stopnje_3 in ZGUBLJENE_POZICIJE:
                    switch = True   
                else:
                    drevo_moznosti3[nabor_stopnje_3] = mozne_poteze(nabor_stopnje_3)
            if switch:
                count += 1
            else:
                drevo_moznosti2[nabor_stopnje_2] = drevo_moznosti3
            drevo_moznosti3 = {}
        
        if count == len([x for x in slovar_naborov_stopnje_2_3.keys()]):
            return nabor_stopnje_1
        drevo_moznosti1[nabor_stopnje_1] = drevo_moznosti2
        drevo_moznosti2 = {}

    
    drevesa_moznosti[4] = drevo_moznosti1

    if difficulty == 'biginner':
        return random.choice([x for x in drevesa_moznosti[4].keys()])

    drevo_moznosti1, drevo_moznosti2, drevo_moznosti3, drevo_moznosti4 = {}, {}, {}, {}

    for nabor_stopnje_1, slovar_naborov_stopnje_2_4 in drevesa_moznosti[4].items():
        skip = False
        for nabor_stopnje_2, slovar_naborov_stopnje_3_4 in slovar_naborov_stopnje_2_4.items():
            count = 0
            for nabor_stopnje_3, seznam_naborov_stopnje_4 in slovar_naborov_stopnje_3_4.items():
                switch = False
                for nabor_stopnje_4 in seznam_naborov_stopnje_4:
                    if nabor_stopnje_4  in ZGUBLJENE_POZICIJE:
                        switch = True
                    else:
                        drevo_moznosti4[nabor_stopnje_4] = mozne_poteze(nabor_stopnje_4)
                if switch:
                    count += 1
                else:
                    drevo_moznosti3[nabor_stopnje_3] = drevo_moznosti4
                drevo_moznosti4 = {}
            
            if count == len([x for x in slovar_naborov_stopnje_3_4.keys()]):
                skip = True
            else:
                drevo_moznosti2[nabor_stopnje_2] = drevo_moznosti3
            drevo_moznosti3 = {}
        
        if skip == False:
            drevo_moznosti1[nabor_stopnje_1] = drevo_moznosti2
        drevo_moznosti2 = {}

    if drevo_moznosti1 == {}:
        return random.choice([x for x in drevesa_moznosti[4].keys()])
    else:
        drevesa_moznosti[5] = drevo_moznosti1
    
    drevo_moznosti1, drevo_moznosti2, drevo_moznosti3, drevo_moznosti4, drevo_moznosti5 = {}, {}, {}, {}, {}

    for nabor_stopnje_1 , slovar_naborov_stopnje_2_5 in drevesa_moznosti[5].items():
        for nabor_stopnje_2, slovar_naborov_stopnje_3_5 in slovar_naborov_stopnje_2_5.items():
            skip = False
            for nabor_stopnje_3, slovar_naborov_stopnje_4_5 in slovar_naborov_stopnje_3_5.items():
                count1, count2 = 0, 0
                for nabor_stopnje_4, seznam_naborov_stopnje_5 in slovar_naborov_stopnje_4_5.items():
                    switch = False
                    for nabor_stopnje_5 in seznam_naborov_stopnje_5:
                        if nabor_stopnje_5 in ZGUBLJENE_POZICIJE:
                            switch = True
                        else:
                            drevo_moznosti5[nabor_stopnje_5] = mozne_poteze(nabor_stopnje_5)
                    if switch:
                        count1 += 1
                    count2 += 1
                    drevo_moznosti4[nabor_stopnje_4] = drevo_moznosti5
                    drevo_moznosti5 = {}
                
                if count1 == count2:
                    skip = True
                else:
                    drevo_moznosti3[nabor_stopnje_3] = drevo_moznosti4
                drevo_moznosti4 = {}
            
            if skip:
                pass
            else:
                drevo_moznosti2[nabor_stopnje_2] = drevo_moznosti3
            drevo_moznosti3 = {}
        
        if drevo_moznosti2 == {}:
            return nabor_stopnje_1
        else:
            drevo_moznosti1[nabor_stopnje_1] = drevo_moznosti2
        drevo_moznosti2 = {}
    
    drevesa_moznosti[6] = drevo_moznosti1


    drevo_moznosti1, drevo_moznosti2, drevo_moznosti3, drevo_moznosti4, drevo_moznosti5, drevo_moznosti6 = {}, {}, {}, {}, {}, {}
    
    for nabor_stopnje_1, slovar_naborov_stopnje_2_6 in drevesa_moznosti[6].items():
        skip1 = False
        for nabor_stopnje_2, slovar_naborov_stopnje_3_6 in slovar_naborov_stopnje_2_6.items():
            count3, count4 = 0,0
            for nabor_stopnje_3, slovar_naborov_stopnje_4_6 in slovar_naborov_stopnje_3_6.items():
                skip2 = True
                for nabor_stopnje_4, slovar_naborov_stopnje_5_6 in slovar_naborov_stopnje_4_6.items():
                    count1, count2 = 0, 0
                    for nabor_stopnje_5, seznam_naborov_stopnje_6 in slovar_naborov_stopnje_5_6.items():
                        switch = False
                        for nabor_stopnje_6 in seznam_naborov_stopnje_6:
                            if nabor_stopnje_6 in ZGUBLJENE_POZICIJE:
                                switch = True  
                            else:
                                drevo_moznosti6[nabor_stopnje_6] = mozne_poteze(nabor_stopnje_6)
                        count2 += 1
                        if switch:
                            count1 += 1
                        else:
                            drevo_moznosti5[nabor_stopnje_5] = drevo_moznosti6
                        drevo_moznosti6 = {}
                    if count1 == count2:
                        skip2 = True
                        break
                    else:    
                        drevo_moznosti4[nabor_stopnje_4] = drevo_moznosti5
                    drevo_moznosti5 = {}
                
                if skip2 == True:
                    count3 += 1
                else:
                    drevo_moznosti3[nabor_stopnje_3] = drevo_moznosti4
                drevo_moznosti4 = {}
                count4 += 1
            if count4 == count3:
                skip1 = True
            if drevo_moznosti3 != {}:
                drevo_moznosti2[nabor_stopnje_2] = drevo_moznosti3
            drevo_moznosti3 = {}
        
        if drevo_moznosti2 != {} and skip1 == False:
            drevo_moznosti1[nabor_stopnje_1] = drevo_moznosti2
        drevo_moznosti2 = {}
    if drevo_moznosti1 == {}:
        
  
        return random.choice([x for x in drevesa_moznosti[6].keys()])
    else:
        
        drevesa_moznosti[7] = drevo_moznosti1


    drevo_moznosti1, drevo_moznosti2, drevo_moznosti3, drevo_moznosti4, drevo_moznosti5, drevo_moznosti6, drevo_moznosti7 = {}, {}, {}, {}, {}, {}, {}

    for nabor_stopnje_1, slovar_naborov_stopnje_2_7 in drevesa_moznosti[7].items():
        
        for nabor_stopnje_2, slovar_naborov_stopnje_3_7 in slovar_naborov_stopnje_2_7.items():
            for nabor_stopnje_3, slovar_naborov_stopnje_4_7 in slovar_naborov_stopnje_3_7.items():
                for nabor_stopnje_4, slovar_naborov_stopnje_5_7 in slovar_naborov_stopnje_4_7.items():
                    skip = False
                    for nabor_stopnje_5, slovar_naborov_stopnje_6_7 in slovar_naborov_stopnje_5_7.items():
                        count1, count2 = 0,0
                        for nabor_stopnje_6, seznam_naborov_stopnje_7 in slovar_naborov_stopnje_6_7.items():
                            switch = False
                            for nabor_stopnje_7 in seznam_naborov_stopnje_7:
                                if nabor_stopnje_7 in ZGUBLJENE_POZICIJE:
                                    switch = True
                                else:
                                    drevo_moznosti7[nabor_stopnje_7] = mozne_poteze(nabor_stopnje_7)
                            if switch:
                                count1 += 1
                            else:
                                drevo_moznosti6[nabor_stopnje_6] = drevo_moznosti7
                            drevo_moznosti7 = {}
                            count2 += 1
                        if count1 == count2:
                            skip = True
                            
                        else:
                            drevo_moznosti5[nabor_stopnje_5] = drevo_moznosti6
                        drevo_moznosti6 = {}
                    if skip:
                        pass
                    else:
                        drevo_moznosti4[nabor_stopnje_4] = drevo_moznosti5
                    drevo_moznosti5 = {}
                if drevo_moznosti4 != {}:
                    drevo_moznosti3[nabor_stopnje_3] = drevo_moznosti4
                    
                drevo_moznosti4 = {}
            if drevo_moznosti3 != {}:
                drevo_moznosti2[nabor_stopnje_2] = drevo_moznosti3
            drevo_moznosti3 = {}
        if drevo_moznosti2 != {}:
            drevo_moznosti1[nabor_stopnje_1] = drevo_moznosti2
        else:
            return nabor_stopnje_1
        drevo_moznosti2 = {}
    if drevo_moznosti1 == {}:
        
        return random.choice([x for x in drevesa_moznosti[7].keys()])
    else:
        drevesa_moznosti[8] = drevo_moznosti1


    for x in drevesa_moznosti[8].keys():
        print(x)    

    return random.choice([x for x in drevesa_moznosti[8].keys()])

    

            

# Dodatne funkcije za pomoč pri analiziranju

def mozne_poteze(pos_nabor):
    pridobljene_pozicije = []

    pos_mat = set(pos_nabor)

    if pos_mat == {(1,1)}:
        return []

    
    for nabor1 in pos_mat:
    
        for st_oduzetih in range(1, nabor1[0]):
            zacasni_nabor = tuple([nabor1[0] - st_oduzetih, 1])
            stikalo = False
            for nabor2 in pos_mat:
                if nabor2[0] == zacasni_nabor[0]:
                    stikalo = True
                    if nabor1[1] == 1:
                        pridobljene_pozicije.append(tuple((pos_mat - {nabor1, nabor2}) | {tuple([nabor2[0], nabor2[1] + 1])}))
                    else:
                        pridobljene_pozicije.append(tuple((pos_mat - {nabor1, nabor2}) | {tuple([nabor2[0], nabor2[1] + 1])    } | {tuple([nabor1[0], nabor1[1] - 1])}))
            if stikalo == False:
                if nabor1[1] == 1:
                    pridobljene_pozicije.append(tuple((pos_mat - {nabor1}) | {tuple([zacasni_nabor[0], 1])}))
                else:
                    pridobljene_pozicije.append(tuple((pos_mat - {nabor1}) | {tuple([zacasni_nabor[0], 1])    } | {tuple([nabor1[0], nabor1[1] - 1])}))
        if len(pos_mat) == 1 and nabor1[1] == 1:
            pass
        else:
            if nabor1[1] == 1:
                pridobljene_pozicije.append(tuple(pos_mat - {nabor1}))
            else:
                pridobljene_pozicije.append(tuple((pos_mat - {nabor1}) | {tuple([nabor1[0], nabor1[1] - 1])}))
    
    return pridobljene_pozicije






def zapis_povezav(position):
    pos_povezav = [] 
    for count in range(1, len(position) + 1):
        if position[count - 1] != 0:
            pos_povezav.append((position[count - 1], count))
    
    return sorted(pos_povezav)

def zapis_mat(position):
    zapis = set()
    
    for st_kart in range(1, max(position) + 1):
        if position.count(st_kart) != 0:
            zapis.add((st_kart, position.count(st_kart)))
    
    return zapis


def zapis_nabor(position):
    return tuple(zapis_mat(position))

def zapis_position(pos_mat):
    position = []
    for nabor in pos_mat:
        for count in range(nabor[1]):
            position.append(nabor[0])
    return position


# Glavna funkcija, ki združuje delovanje v celoto.

def maschine(position, difficulty):
    nova_pozicija_nabor = analiza(position, difficulty)

    pozicija_nabor = zapis_nabor(position)
    seznam_povezav = zapis_povezav(position)
    nova_pozicija_mat = set(nova_pozicija_nabor)
    nova_pozicija = zapis_position(nova_pozicija_mat)
    palice_na_koncu = None

    for stevilo_palic in range(1, max(position) + 1):
        if nova_pozicija.count(stevilo_palic) < position.count(stevilo_palic):
            palice_na_zacetku = stevilo_palic
        elif nova_pozicija.count(stevilo_palic) > position.count(stevilo_palic):
            palice_na_koncu = stevilo_palic

    if palice_na_koncu == None:
        palice_na_koncu = 0
    
    
    for povezava in seznam_povezav:
        if povezava[0] == palice_na_zacetku:
            return (povezava[1], palice_na_zacetku - palice_na_koncu)




