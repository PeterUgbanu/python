from itertools import combinations
from typing import Literal
from PIL import Image, ImageDraw, ImageFont
    
def listValues(iteratable):
    """iteratable must be a list or tuple"""
    return "".join([str(el) for el in iteratable])


class Transaction:
    def __init__(self, items: list) -> None:
        self.items = items

class Apriori:
    def __init__(self, transactions: list) -> None:
        self.transactions = transactions
        # self.counts = []
        self.combos = [self.__level(num) for num in range(1,len(self.transactions))]
        self.probabilities = self.__loop()
        self.nodes = self.__createNodes()
        self.nodeValues = list(map(lambda x: listValues(x), self.nodes))


    def __combo(self):
        itemlist = []
        for transaction in self.transactions:
            for item in transaction.items:
                itemlist.append(item)
        return set(itemlist)

    def __level(self, num):
        combo = self.__combo()
        return list(combinations(combo, num))

    def __loop(self):
        probabilities = {}
        for items in self.combos:
            for values in items:
                (prob, count) = self.__probability(values)
                value = round(prob, 2)
                probabilities[f"{values}"] = (value, count)
        return probabilities

    def __probability(self, items):
        count = 0
        for transaction in self.transactions:
            if self.__every(set(items), set(transaction.items)):
                count += 1
        # self.counts.append((count / len(self.transactions), count))
        return (count / len(self.transactions), count)
    
    def __every(self, l1: set, l2: set):
        a, x = 0, 0
        while x < len(l1):
            if l1.issubset(l2):
                a += 1
            x += 1
        if a == len(l1):
            return True
        return False

    def __createNodes(self):
        nodes = []
        for itemSet in self.combos:
            for item in itemSet:
                nodes.append(item)
        return nodes

class Lattice:
    def __init__(self, limit: float, apriori: Apriori):
        
        self.limit = limit

        self.apriori = apriori
        self.longest_dim = len(max(self.apriori.combos)[0])-1

        self.height = 1000
        self.width = self.longest_dim * 750

        self.image = Image.new('RGB', (self.width, self.height), (128, 128, 128))
        self.draw = ImageDraw.Draw(self.image)
        # self.font = ImageFont.truetype(size=16)

    def __start_drawing(self):
        self.draw.ellipse(
            (self.width/2+10, 50, self.width/2+70, 100), 
            fill=(255, 255, 255), 
            outline=(0, 0, 0), width=2
        )
        self.draw.text(((self.width/2)+25, 70,), text="Start", fill=(0,0,0), spacing=1)

        for i, combo in enumerate(self.apriori.combos):
            y = 200 + (150 * i)
            for index, item in enumerate(combo):
                x_divisor = len(combo) 
                x_ = self.width / x_divisor
                value = listValues(item)
                support = self.apriori.probabilities[f"{item}"][0]
                x = (x_ *(index+1))-((x_ / 2)+(x_/4)) #if i != self.longest_dim else (x_ *(index+1))-(x_ / 2)
                self.__draw_circles(x, y, support, value, self.apriori.probabilities[f"{item}"][1])

                #  draw lines
                if i == 0:
                    self.__draw_lines(0, self.width/2+40, 100, "start")
                if i < self.longest_dim:
                    self.__draw_lines(i+1, x+30, y+50, value)

    def show(self):
        self.__start_drawing()
        self.image.show()

    def save(self, filename):
        self.__start_drawing()
        self.image.save(filename)

    def __draw_circles(self, x, y, support: float, value: str, count: int):
        self.draw.ellipse(
            (x, y, x+70, y+70), 
            fill=(255, 255, 255) if support >= self.limit else (50, 50, 50), 
            outline=(0, 255, 0)if support >= self.limit else (255, 0, 0), width=2
        )
        self.draw.text((12+x+(50/len(value))if len(value) > 2 else x+30, y+15,), text=value,
                        fill=(0,0,0) if support >= self.limit else (255, 255, 255), spacing=1, 
                    )
        self.draw.text((x+25, y+30), text=str(support), 
                       fill=(0,0,0) if support >= self.limit else (255, 255, 255), spacing=1, 
                    )
        self.draw.text((x+30, y+50), text=str(count), 
                       fill=(0,0,0) if support >= self.limit else (255, 255, 255), spacing=1, 
                    )
        
    def __draw_lines(self, index, x, y, value):
        for i, item in enumerate(self.apriori.combos[index]):
            x_divisor = len(self.apriori.combos[index]) 
            x_ = self.width / x_divisor
            x1 = (x_*(i+1)) -((x_ / 2)+(x_/4)) #if index != self.longest_dim else x_ / 2
            if set(value).issubset(set(listValues(item))):
                self.draw.line((x,y+20, x1+35, y+100), fill=(0, 0, 0), width=2, joint='curve')
            elif value == "start":
                self.draw.line((x,y, x1+35, y+100), fill=(0, 0, 0), width=2, joint='curve')

if __name__ == "__main__":
    t1 = Transaction([1,3,4])
    t2 = Transaction([1,2,4,6])
    t3 = Transaction([3,4,5,6])
    t4 = Transaction([1,2,3,4, 6])
    t5 = Transaction([3,5,6])

    ap = Apriori((t1, t2, t3, t4, t5))
    # print(ap.probabilities)
    # print(ap.counts)
    # for key in list(ap.probabilities.keys()):
    #     if ap.probabilities[key] > 0.6:
    #         print(key)
    lat = Lattice(0.6, ap)
    lat.save("assignment-lattice.png")
      
