import socket            
import os
import signal

WIN_COMBINATIONS = [(0, 1, 2),(3, 4, 5),(6, 7, 8),(0, 3, 6),(1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6)]

s = socket.socket()        
 

s.connect(('192.168.50.164', 12345))
next = None


def win(places):
    if (places != "---------"):
        for placeA, placeB, placeC in WIN_COMBINATIONS:
            if places[placeA] == places[placeB] == places[placeC] and (places[placeA] != '-' and places[placeB] != '-' and places[placeC] != '-'):
                s.send("WIN".encode())
                return True

    return False

def game(places):
    # the game board
    print( places[0] + " | " + places[1] + " | " + places[2])
    print( places[3] + " | " + places[4] + " | " + places[5])
    print( places[6] + " | " + places[7] + " | " + places[8])

 
while True:
    while next == None:
        places = s.recv(1024).decode()

        if places == "WIN":
            print("Player 2 win! Game ending")
            s.close()
            quit()
        else:
            places = places[:9]

        print("Received response from Player 2")
        game(places)

        break
    
    while True:
        next = int(input("Where do you want to place an O? (1,2,3,4,5,6,7,8,9)")) - 1
        placeslist = list(places)
        if (placeslist[next] == '-'):
            placeslist[next] = 'O'
            places = ''.join(placeslist)
            break
        else:
            print("this placement is filled already")
            continue

    os.system("clear")

    if (win(places)):
        game(places)
        print("You win! Game ending")
        s.close()
        quit()

    s.send(places.encode())
    next = None

    # s.close() 
