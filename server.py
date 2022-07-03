import socket      
import sys
import os
import signal

WIN_COMBINATIONS = [(0, 1, 2),(3, 4, 5),(6, 7, 8),(0, 3, 6),(1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6)]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #create socket


s.bind(('192.168.50.164', 12345))     
next = None #players move  
init = True #detects if it the first round so it won't repeat
places = "---------"
print ("Game active at 12345")

s.listen(5)    
print ("Listening for clients")
c, addr = s.accept()

def win(places):
    for placeA, placeB, placeC in WIN_COMBINATIONS: #this is the win combination placements
        if places[placeA] == places[placeB] == places[placeC] and (places[placeA] != '-' and places[placeB] != '-' and places[placeC] != '-'):
            c.send("WIN".encode()) # if the player wins then this message prompt appear
            return True

    return False

def game(places):
    #  the game board
    print( places[0] + " | " + places[1] + " | " + places[2])
    print( places[3] + " | " + places[4] + " | " + places[5])
    print( places[6] + " | " + places[7] + " | " + places[8])

while True:
    if (init):
        c.send(places.encode())#send placements made from the player to the other
        init = False

   
    while next == None:
        places = c.recv(1024).decode()# receive the placements from the other player
            
        if places == "WIN":
            print("Player 1 win! Game ending")
            s.close()
            raise  SystemExit
        else:
            places = places[:9]
                
        print("Received response from Player 1")
        game(places)

        break

    while True:
        next = int(input("Where do you want to place an X? (1,2,3,4,5,6,7,8,9)")) - 1
        placeslist = list(places)
        if (placeslist[next] == '-'):#this is for the programming to detect if the spot is empty or not
            placeslist[next] = 'X'
            places = ''.join(placeslist)
            break
        else:
            print("This placement is filled already")#to tell the players when someone put the thing inside the space
            continue

    os.system("clear")#clear the plane so it's easier to see

    if (win(places)):
        game(places)
        print("You win! Game ending")
        s.close()
        raise  SystemExit

    c.send(places.encode())
    next = None

    # c.close()
