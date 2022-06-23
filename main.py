matr=[['-' for j in range(3)] for i in range(3)]

def print_matr(m):
    print('  0 1 2')
    for i in range(3):
        print(i,*m[i])

def is_win(m):
    for i in range(3):
        if m[i][0]==m[i][1]==m[i][2] and m[i][0]!='-': return True
        if m[0][i]==m[1][i]==m[2][i] and m[0][i]!='-': return True
    if m[0][0]==m[1][1]==m[2][2] and m[0][0]!='-': return True
    if m[2][0]==m[1][1]==m[0][2] and m[2][0]!='-': return True
    return False

def  player_move(m, symbol):
    while True:
        coord= (input(f' Игрок [{symbol}]: введите номер строки и солбца через пробел  {symbol}= '))
        coord=list(map(int,coord.split()))
        if m[coord[0]][coord[1]]!='-':
            print('Ячейка занята. Повторите ввод')
        else:
            m[coord[0]][coord[1]]=symbol
            print_matr(m)
            return m


print('Игра крестики-нолики')
print_matr(matr)

i=1
winner=''
while True:
    print('\nШаг ',i)
    matr=player_move(matr, 'x')
    winner=is_win(matr)
    if winner:
        print ('\nПобедил [x]!')
        break

    i += 1
    if i == 10:
        print('\nНичья!')
        break

    print('\nШаг ',i)
    matr=player_move(matr, 'o')
    winner=is_win(matr)
    if winner:
        print ('\nПобедил [o]!')
        break
    i += 1

