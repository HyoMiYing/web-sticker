# coding=utf-8



class Igra:
    def __init__(self, position = None):
        if not position:
            position = [1, 3, 5, 7]
        self.position = position
        self.player = 'player1'
    
    def move(self, row, num):
        '''Funkcija z validacijskimi metodami preveri pravilnost vnesenih podatkov. Če so podatki pravilni vrne 'Input is valid', sprejme vrstico in število oduzetih palic iz taiste vratice ter nato spremeni pozicijo na plošči. '''

        #Preveri validacijo
        if self.validation_row(row) == 'Row invalid':
            return 'Row invalid'
        elif self.validation_num(row, num) == 'Num invalid':
            return 'Num invalid'
        
        #Spremeni igralca in pozicijo
        self.change_player()

        self.position[int(row) - 1] = int(self.position[int(row) - 1]) - int(num)

        #Preveri ali je igra končana
        if self.end():
            return 'Game over, winner is {}'.format(self.player)
        return 'Input is valid'


    def end(self):
        '''Funkcija se zažene na začetku vsakega kroga kjer preveri ali je na plošča prazna in je torej igra končana. Ča je slednje res vrne True, v nasprotnem primeru pa False.  '''
        stevilo_praznih_vrstic = self.position.count(0)
        
        if stevilo_praznih_vrstic == len(self.position):
            return True
        else:
            return False

    def change_player(self):
        '''Funkcija ničesar ne sprejme ali vrne. Spremeni igralca na vrsti, v kolikor pa ta še ni določen (na začetku igre) ga nastavi na 'player1'.'''
        
        if self.player == 'player1':
            self.player = 'player2'
        elif self.player == 'player2':
            self.player = 'player1'
        elif self.player == None:
            self.player = 'player1'

    # validacijske funkcije

    def validation_row(self, row):
        try:
            float(row)
        except:
            return 'Row invalid'

        row = float(row)

        if row.is_integer():
            if 0 < row and row <= len(self.position) and self.position[int(row) - 1] != 0:
                return 'Row is valid'
            else:
                return 'Row invalid'
        else:
            return 'Row invalid'
    
    def validation_num(self, row, num):
        try:
            float(num)
        except:
            return 'Num invalid'

        num = float(num)
        row = int(row)

        if num.is_integer():
            if num > 0 and num <= self.position[row - 1]:
                return 'Num is valid'
            else:
                return 'Num invalid'
        else:
            return 'Num invalid'

       


class Sticker:
    def __init__(self):
        self.igre = {}

    def add_new_id(self):
        if self.igre == {}:
            return 0
        else:
            return max(self.igre.keys()) + 1
    
    def new_game(self,position = None):
        id_igre = self.add_new_id()
        game = Igra(position)
        
        self.igre[id_igre] = game
        return id_igre

    def remove_id(self, id_igre):
        if id_igre in self.igre.keys():
            self.igre.pop(id_igre)
            return True
        else:
            return False

