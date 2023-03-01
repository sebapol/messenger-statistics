lista = ['a','a','a','b','b']
indeksy = []
indeks = 0
for i in range(lista.count('a')):
    indeksy.append(lista[indeks:].index('a'))
    indeks = lista[indeks:].index('a') + 1
print(indeksy)