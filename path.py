import requests as api
from time import sleep

hitCount = 0

def search_elm(arr, num):
    elm = []
    for i in range(6):
        for j in range(6):
            if arr[i][j] == num:
                elm = [i, j]
                return elm
    return "not found"


# represent the map in a matrix to find direction to follow after a junction
nodes = [
       ['1',  'x', '2',  '3', '4', '5'],
       ['x',  'x', 'x',  '7', '8', '9'],
       ['x',  '6', '6',  '6', 'x', 'x'],
       ['10', '11','12', '13','x', '14'],
       ['15', '16','x',  '17','18','19'],
       ['0',  'x', 'x',  '50','21','22']
    ] 


# given the index of the current junction, find direction to the next one
# aside from node '6' next node will always be either same column or same row
# return 'right', 'left', or 'straight'
def normalize_path(path):
    orientation = 0 # initially facing north
    directions = []
    prev = [5, 0] # index of starting node
    for i in range(len(path)):
        if i == 0: continue
        index = search_elm(nodes, path[i]);

        if index[0] == prev[0]: # same row
            if orientation == 0:
                if index[1] > prev[1]: 
                    directions.append('right')
                    orientation += 1
                else: 
                    directions.append('left')
                    orientation -= 1
            elif orientation == 1 or orientation == 3:
                directions.append('straight')
            elif orientation == 2:
                if index[1] > prev[1]: 
                    directions.append('left')
                    orientation -= 1
                else: 
                    directions.append('right')
                    orientation += 1

        elif index[1] == prev[1]: # same column
            if orientation == 0 or orientation == 2:
                directions.append('straight')
            elif orientation == 1:
                if index[0] > prev[0]:
                    directions.append('right')
                    orientation += 1
                else: 
                    directions.append('left')
                    orientation -= 1
            elif orientaion == 3:
                if index[0] > prev[0]:
                    directions.append('left')
                    orientation -= 1
                else: 
                    directions.append('right')
                    orientation += 1

        # handle node 6
        if  path[i] == '6':
            if path[i-1] == '11': # coming to 6 from 11
                directions.append('right')
            elif path[i-1] == '13': # coming to 6 from 13
                directions.append('left')

        if orientation > 3: orientation = 0 # reset when overflow
        prev = index

    return directions

def get_path():
    # blocking code, execution stops until response is received or timeout
    response = api.get('https://intense-gorge-00247.herokuapp.com/api/nav')
    json = response.json()
    while json['hits'] == hitCount:
        print('waiting for new requests')
        sleep(20)
        response = api.get('https://intense-gorge-00247.herokuapp.com/api/nav')

    return json['path']
