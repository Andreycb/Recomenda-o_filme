import os
import pandas as pd
import numpy as np
import operator
from scipy import spatial


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = (os.path.join(BASE_DIR, 'data'))

filmes = pd.read_csv(os.path.join(DATA_DIR, 'movies.csv'))
notas = pd.read_csv(os.path.join(DATA_DIR, 'ratings.csv'))

#Transformando a coluna de generos em varias colunas
divisao = filmes['genres'].str.split('|')
generos = []
for row in divisao:
    for elem in row:
        generos.append(elem)
generos = set(generos)

for i in generos:
    filmes[i] = 0

counter = 0
for row in divisao:
    for i in row:
        filmes.loc[counter, i] = 1
    counter += 1

#Relacionar filmes similares    
filmesDic = filmes.iloc[:,0:-1].values #movieDic[0]

def ComputeDistance(a, b):
    genresA = a[3:-1]
    genresA = np.array(list(genresA))
    genresB = b[3:-1]
    genresB = np.array(list(genresB))
    genreDistance = spatial.distance.cosine(genresA, genresB)
    return genreDistance

idfilme = filmesDic[0][0]
n = 5

distances = []
cont = 0
while (cont <= 9741):
    c = filmesDic[cont][0]
    d = filmesDic[idfilme][0]
    if(c != d):
        dist = ComputeDistance(filmesDic[idfilme],filmesDic[cont])
        distances.append((filmesDic[cont][1], dist))
    cont += 1
distances.sort(key=operator.itemgetter(1))
neighbors = []
for x in range(n):
    neighbors.append(distances[x][0])

print(filmesDic[0][0])
print(neighbors)