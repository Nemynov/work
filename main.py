class BoardOutException (Exception):
    def __init__(self, text):
        self.text = text



class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'{self.x , self.y}'


class Ship:
    _lives = None
    def __init__(self, _len, begin_dot , _direction):
        self._len = _len
        self.begin_dot = begin_dot
        self._direction = _direction
        self._lives = self._len

    def dots(self):
        dot_list=[self.begin_dot]
        x = self.begin_dot.x
        y = self.begin_dot.y

        for i in range(self._len-1):
            if self._direction == 'x': x += 1 # расположение корабля по горизонтали
            else: y += 1
            dot_list.append(Dot(x,y))

        return dot_list

BOARD_SIZE = 6 # размер доски

class Board:

    _board = [['' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    _ships = []
    hid = None
    living_ships_count = 7

    def add_ship(self, ship):
        dots = ship.dots()
        for dot in dots:
            x = dot.x
            y = dot.y
            if BOARD_SIZE<x<1 or BOARD_SIZE<y<1: raise BoardOutException('Координаты корабля вне игрового поля')
            if self._board[x-1][y-1]!='': raise BoardOutException('Неверная расстановка')

        self._ships.append(ship)
        for dot in dots:
            self._board[dot.x-1] [dot.y-1] = ''



class Dot:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'{self.x , self.y}'


class Ship:
    _lives = None
    def __init__(self, _len, begin_dot , _direction):
        self._len = _len
        self.begin_dot = begin_dot
        self._direction = _direction
        self._lives = self._len

    def dots(self):
        dot_list=[self.begin_dot]
        x = self.begin_dot.x
        y = self.begin_dot.y

        for i in range(self._len-1):
            if self._direction == 'x': x += 1    # если  корабль расположен  по горизонтали
            else: y += 1
            dot_list.append(Dot(x,y))

        return dot_list

BOARD_SIZE = 6 # размер доски

class Board:



    def __init__(self, hid=False):
        self._board = [['' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.ship_list = []
        self.living_ships_count = 7
        self.hid = hid

    def out(self, dot):
        if dot.x > BOARD_SIZE or dot.x < 1 or dot.y > BOARD_SIZE or dot.y < 1: return True
        else: return False

    def add_ship(self, ship):
        dots = ship.dots()
        for dot in dots:
            x = dot.x
            y = dot.y
            if self.out(dot):  return False
                #raise BoardOutException('Координаты корабля вне игрового поля')

            if self._board[y-1][x-1] != '':  return False
                #raise BoardOutException('Неверная расстановка')

        self.ship_list.append(ship)                # добавление корабля к списку кораблей
        for dot in dots:                        # постановка корабля на доску
            self._board[dot.y-1] [dot.x-1] = '■'

        return True

    def contour(self, ship, mark = ' '):
        for dot in ship.dots():
            for y in [dot.y-2,dot.y-1,dot.y]:
                for x in [dot.x-2,dot.x-1,dot.x]:
                    if   0 <= x < BOARD_SIZE and  0 <= y < BOARD_SIZE and self._board[y][x] in ['' , ' ']:
                        self._board[y][x] = mark

    def show_board(self):   # вывод доски на консоль
        print('  |', end='')
        for i in range(BOARD_SIZE):
            print(f' {i+1} ', end='|')
        print()
        for i in range(BOARD_SIZE):
            print(f'{i+1} ', end='|')
            for j in range(BOARD_SIZE):
                c = self._board[i][j]
                if self.hid and c == '■':   c = '' # скрываем корабли неа доске противника
                print(c.center(3,' '), end='|')
            print()

    def shot(self, dot):
        if self.out(dot): raise BoardOutException('Неверный ход')
        elif self._board[dot.y-1][dot.x-1] in ['*', 'X']:
            raise BoardOutException('Такой ход уже был')

        if self._board[dot.y-1][dot.x-1] == '■':    # если есть попадание
            self._board[dot.y - 1][dot.x - 1] = 'X'
            for ship in self.ship_list:
                for d in ship.dots():
                    if d == dot:
                        ship._lives -= 1    # уменьшаем число жизней корабля
                        if  ship._lives == 0:
                            self.living_ships_count -= 1    # уменьшаем число кораблей в списке, если число жизней корабля равно 0
                            self.contour(ship,'  ')
                            self.ship_list.remove(ship)
                            return 'корабль убит'
                        return 'корабль ранен'
        else:
            self._board[dot.y - 1][dot.x - 1] = '*'
            return  'промах'


class Player:
    def __init__(self, my_board, opponent_board):
        self.my_board = my_board
        self.opponent_board = opponent_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                dot = self.ask()
                shot_result = self.opponent_board.shot(dot)
                print(f'{dot} {shot_result}')

                if shot_result == 'промах':
                    return False
                else:
                    return True

            except BoardOutException as er:
                print(er)
            except ValueError:
                print('Ошибка ввода')


class User(Player):
    def ask(self):
        xy = input('Сделайте ход. Укажите координаты х и y через пробел: ').split()
        if len(xy) != 2:    raise ValueError()
        return Dot(xy[0], xy[1])


import random, time

class Ai(Player):
    def ask(self):
        print('Ход компьютера ...')

        while True:
            x = random.randint(1,BOARD_SIZE)
            y = random.randint(1, BOARD_SIZE)
            c = self.opponent_board._board[y-1][x-1]
            if c != '*' and c != 'X' and c != '  ':
                return Dot(x,y)


class Game:
    def random_board(self, hid = False):
        while True:
            b = Board(hid)

            for ship_len in [3,2,2,1,1,1,1]:
                for i in range(2000):
                    x = random.randint(1,BOARD_SIZE)
                    y = random.randint(1,BOARD_SIZE)
                    xy = random.choice(['x','y'])
                    sh = Ship(ship_len ,Dot(x,y),xy)
                    add_success = b.add_ship(sh)
                    if add_success:             # если кораблю нашли место на доске, то обводим контур и переходим к следующему кораблю
                        b.contour(sh)
                        break
                if not add_success: break       # если не нашли место кораблю, то делаем новую доску

            if add_success: break
        return b

    def greet(self):
        print('ИГРА "Морской бой"')
        print('Игра проиходит в поле 6х6')
        print('Вы играете против компьютера')
        print('Расстановка кораблей происходит случайным образом')
        print('_________________________________________________')

    def __init__(self):
        self.user_board = self.random_board()
        self.ai_board = self.random_board(True)

        self.user = User(self.user_board, self.ai_board)
        self.ai = Ai(self.ai_board, self.user_board)

    def loop(self):
        num = 0
        while True:
            if num % 2 == 0:
                print("-" * 20)
                print("Доска пользователя:")
                self.user_board.show_board()
                print('Осталось кораблей: ', self.user_board.living_ships_count)
                print("-" * 20)
                print("Доска компьютера:")
                self.ai_board.show_board()
                print('Осталось кораблей: ', self.ai_board.living_ships_count)
                print("-" * 20)

                repeat = self.user.move()
                time.sleep(2)
            else:
                repeat = self.ai.move()
                time.sleep(2)
            if repeat:
                num -= 1

            if self.ai_board.living_ships_count == 0:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.user_board.living_ships_count == 0:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1


    def start(self):
        self.greet()
        self.loop()




g=Game()
g.start()
