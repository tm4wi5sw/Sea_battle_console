# «Морской бой» в консоли
# python 3.8.1
# всё не по заданию
import random as rnd
from log import log


def clear():
    print ("\n"*100)

class Ship:
    def __init__(self): # сюда по заданию должны приходить коодинаты
        pass
        

class Board:
    def __init__(self): # where ships
        self.sea = " ~ "
        self.miss = " * "
        self.ship = " ■ "
        self.wreck = " # "
        self.near = " : " # вблизи корабля, хз какой символ выбрать
        self.shipSet = [3,2,2,1,1,1,1]
        # этот класс двуличен, и изначально не правильно задуман
        self.nps = [[self.sea for x in range(6)] for y in range(6)] # нальём воды на доску
        self.usr = [[self.sea for x in range(6)] for y in range(6)] # -//-
        self.hideNpsShips = True # флаг сокрытия кораблей нпс (в финале рисуем корабли)
        self.generateNpsShip() # разбросать по морю корабли
        self.generateUsrShip() # -//-

    def generateUsrShip(self): # где-то здесь есть ошибка в алгоритме
        def check( x, y, count):
            correct = False
            seaset = set([self.sea])
            checklist = set([])
            if y-1 >= 1:
                checklist.update(self.usr[y-1][x : x + count])
            checklist.update(self.usr[y][x-1 : x + count+1])
            if y+1 <= 5:
                checklist.update(self.usr[y+1][x : x + count])
            if (checklist == seaset):
                correct = True
            return correct
    
        for i in self.shipSet:
            ok = False
            while not ok: # проверить на возможность размещения на доске
                y = rnd.randrange(0, 6)
                x = rnd.randrange(0, 7 - i) # отступ от правого края доски
                ok =  check(x, y, i)
            for ship in range(i):
                self.usr[y][x+ship] = self.ship

    def generateNpsShip(self): # это так быть не должно
        def check( x, y, count):
            correct = False
            seaset = set([self.sea])
            checklist = set([])
            if y-1 >= 1:
                checklist.update(self.nps[y-1][x : x + count])
            checklist.update(self.nps[y][x-1 : x + count+1])
            if y+1 <= 5:
                checklist.update(self.nps[y+1][x : x + count])
            if (checklist == seaset):
                correct = True
            return correct
    
        for i in self.shipSet:
            ok = False
            while not ok: # проверить на возможность размещения на доске
                y = rnd.randrange(0, 6)
                x = rnd.randrange(0, 7 - i) # отступ от правого края доски
                ok =  check(x, y, i)
            for ship in range(i):
                self.nps[y][x+ship] = self.ship

    def hideNpsShip(self, x):
        if x == self.ship:
            return self.sea
        else:
            return x

    def setToNpsBoard(self, x, y):
        if self.nps[x][y] == self.sea:
            self.nps[x][y] = self.miss
        elif self.nps[x][y] == self.ship:
            self.nps[x][y] = self.wreck

    def setToUsrBoard(self, x, y):
        if self.usr[x][y] == self.sea:
            self.usr[x][y] = self.miss
        elif self.usr[x][y] == self.ship:
            self.usr[x][y] = self.wreck

    def cheatNpsAI(self):
        for j in range(6):
            for i in range(6):
                if self.usr[j][i] == self.ship:
                    return j, i

    def checkNpsCorrect(self, x, y):
        if self.nps[x][y] == self.sea or self.nps[x][y] == self.ship:
            return True
        else:
            return False

    def checkUsrCorrect(self, x, y):
        if self.usr[x][y] == self.sea or self.usr[x][y] == self.ship:
            return True
        else:
            return False

    def checkShips(self):
        countNpsShips = 0
        countUsrShips = 0
        for line in self.nps:
            countNpsShips += line.count(self.ship)
        for line in self.usr:
            countUsrShips += line.count(self.ship)

        if countUsrShips == 0:
            self.hideNpsShips = False # включаем отображение вражеских кораблей
            self.draw()
            print("Победа нпс!")
            return False
        if countNpsShips:
            return True
        else:
            self.hideNpsShips = False # включаем отображение вражеских кораблей
            self.draw()
            print("Победа игрока!")
            return False


    def draw(self):
        print(" " * 10 + "NPS SHIPS" + " " * 22 + "YOUR SHIPS")
        lineNum = "  "
        for num in range(1, 7):
            lineNum += "| " + str(num) + " "
        print(lineNum + "|    " + lineNum + "|")
        for i in range(6):
            numLine = str(i + 1) + " |"
            if self.hideNpsShips:
                boardNPS = numLine + "|".join([self.hideNpsShip(cell) for cell in self.nps[i]]) + "|" # заменяем на нпс доске кораблики на море
            else:
                boardNPS = numLine + "|".join(self.nps[i]) + "|" # рисуем нпс доску
            boardUSR = numLine + "|".join(self.usr[i]) + "|" # рисуем юзер доску
            print (boardNPS + "    " + boardUSR)
            # тихий ужас эти пробелы
    
    def update(self):
        # нанести на карту запретную область для выстрелов вокруг обломков
        for y in range(5):
            for x in range(6):
                if self.nps[y][x] == self.wreck:
                    self.nps[y+1][x] = self.near
        for y in range(5,0,-1):
            for x in range(5,0,-1):
                if self.nps[y][x] == self.wreck:
                    self.nps[y-1][x] = self.near
        for y in range(5):
            for x in range(6):
                if self.usr[y][x] == self.wreck:
                    self.usr[y+1][x] = self.near
        for y in range(5,0,-1):
            for x in range(5,0,-1):
                if self.usr[y][x] == self.wreck:
                    self.usr[y-1][x] = self.near

class Game:
    def __init__(self):
        self.board = Board()

    def inputCoord(self):
        try:
            x = int(input("Капитан введите долготу(по вертикали) для выстрела:"))
            y = int(input("Капитан введите широту(по горизонтали) для выстрела:"))
            # проверить правильность координат
            # также проверить на повторное попадание
            if x not in range(1, 7) or y not in range(1, 7) or not self.board.checkNpsCorrect(x-1, y-1):
                raise ValueError
        except ValueError: # все ошибки сводятся к одному сообщению
            clear()
            print("ошибка в данных! повторите ввод")
            correct = False
        else:
            clear()
            print("залп в квадрат[" + str(x) + ":" + str(y) + "]")
            # выполнить залп по карте нпс
            self.board.setToNpsBoard(x-1, y-1)
            correct = True
        return correct
    
    def stepNps(self):
        x = rnd.randrange(0, 6)
        y = rnd.randrange(0, 6)
        # чит затопления кораблей юзера
        #x, y = self.board.cheatNpsAI() # раскомментировать чтоб всегда побеждал нпс

        # проверить на повторное попадание
        if self.board.checkUsrCorrect(x, y):
            # выполнить залп по карте игрока
            self.board.setToUsrBoard(x, y)
            print("нпс выполнил залп в квадрат[" + str(x+1) + ":" + str(y+1) + "]")
            return True
        else:
            return False

    def fight(self):
        victory = False
        while not victory:
            
            # ход игрока
            stepUsrOk = False
            while not stepUsrOk:
                self.board.draw()
                stepUsrOk = self.inputCoord()
            # проверить наличие кораблей у игроков
            victory = not self.board.checkShips()

            # ход нпс
            stepNpsOk = False
            while not stepNpsOk:
                stepNpsOk = self.stepNps()
            self.board.update()
            # проверить наличие кораблей у игроков
            victory = not self.board.checkShips()


seaBattle = Game()
seaBattle.fight()
