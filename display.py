import tkinter as tk
import json

with open("food.txt", "r") as readableFile:
    file = readableFile.read()
    if len(file) > 0:
        foods = json.loads(file)
    else:
        foods = {
            "Bread": ["Egg", "Flour", "Milk", "Honey", "Yeast"]
        }

class TitleFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.createWidgets()
        
    def createWidgets(self):
        tk.Label(
            self, text="Food Ingredients Reminder App", pady=10,
        ).grid(column=0, row=0,)
        tk.Button(
            self, text="Add Food", command=lambda: PopUpWindow(self.master.master)
        ).grid(column=1, row=0)

class BodyFrame(tk.Frame):
    def __init__(self, master, foods):
        super().__init__(master)
        self.foods = foods
        self.selectedFood = list(self.foods.keys())[0]
        self.ingredients = list(foods.values())[0]

        self.foodLabelFrame = tk.LabelFrame(self, text="Food List")
        for index, food in enumerate(self.foods.keys()):
            self.createFood(self.foodLabelFrame, food, index + 1)
        
        self.foodLabelFrame.grid(column=0, row=0, padx=10, sticky=tk.NW)
        self.ingredientFrame()
        
    def ingredientFrame(self):
        self.ingredientLabelFrame = tk.LabelFrame(self, text=self.selectedFood+" Ingredients",)
        for index, ingredient in enumerate(self.ingredients):
            tk.Label(self.ingredientLabelFrame, text=f"{index + 1} -> {ingredient.capitalize()}").pack(anchor=tk.W)

        tk.Button(self.ingredientLabelFrame, text="Update", command=lambda: print("update food")).pack(anchor=tk.SE)
        self.ingredientLabelFrame.grid(column=1, row=0, padx=10, sticky=tk.NW)

    def createFood(self, container, foodName: str, index):
        tk.Button(
            container, text=f"{index} -> {foodName.capitalize()}",
            command= lambda: self.selectFood(foodName)
        ).pack(anchor=tk.W, fill=tk.X)
        

    def selectFood(self, foodName):
        self.ingredients = self.foods.get(foodName)
        self.selectedFood = foodName
        self.ingredientLabelFrame.destroy()
        self.ingredientFrame()

class MainFrame(tk.Frame):
    def __init__(self, master, foods):
        super().__init__(master)
        self.foods = foods
        self.pack()

        self.title = TitleFrame(self)
        self.title.pack(pady=5, padx=10)

        self.body = BodyFrame(self, self.foods)
        self.body.pack(pady=10, padx=5)

class PopUpWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master=master)

        self.ingredients = []
        self.foodName = ""

        self.mainFrame = tk.LabelFrame(self, text="Food Addition Form")

        # Form for adding food and ingredients
        self.formFrame = tk.LabelFrame(self.mainFrame, text="Add Food")
        tk.Label(self.formFrame, text="Enter Food Name").pack(anchor=tk.W)
        self.foodEntry = tk.Entry(self.formFrame, background="grey", relief=tk.SUNKEN)
        self.foodEntry.pack()
        tk.Button(self.formFrame, text="Add Food Name", command= lambda: self.enterFood()).pack(anchor=tk.W)
        tk.Label(self.formFrame, text="Enter Ingredients").pack(anchor=tk.W)
        self.ingredientEntry = tk.Entry(self.formFrame, background="grey", relief=tk.SUNKEN)
        self.ingredientEntry.pack()
        tk.Button(self.formFrame, text="Add Ingredient", command= lambda: self.addIngredient()).pack(anchor=tk.W)
        self.buildDetails()
        #placing on the screen
        self.formFrame.grid(row=0, column=0, padx=5, pady=10, sticky=tk.NW)
        self.mainFrame.pack(padx=20, pady=5)

        tk.Button(self, text="Add Food", command=lambda: self.addFood()).pack(pady=20)

    def buildDetails(self):
        """frame for displaying details of added food and ingredient"""
        self.detailFrame = tk.LabelFrame(self.mainFrame, text="Food Details")
        self.foodTitle = tk.Label(self.detailFrame, text="Food Name: "+self.foodName,)
        self.foodTitle.pack(anchor=tk.W)
        if len(self.ingredients) > 0:
            for index, ingredient in enumerate(self.ingredients):
                tk.Label(self.detailFrame, text=f"{index+1} -> {ingredient}").pack(anchor=tk.W)

        self.detailFrame.grid(row=0, column=1, sticky=tk.NW, padx=5, pady=10)

    def addIngredient(self):
        if len(self.foodEntry.get()) < 1:
            alertDialog(self, "Please enter food name before ingredients")
        else:
            if len(self.ingredientEntry.get()) < 1:
                alertDialog(self, "Please enter Ingredient name")
            else:
                self.ingredients.append(self.ingredientEntry.get().capitalize())
                self.detailFrame.destroy()
                self.buildDetails()

        self.ingredientEntry.delete(0, tk.END)

    def addFood(self):
        foods.update({self.foodName: self.ingredients})
        writeableFile = open('food.txt', 'w')
        writeableFile.write(json.dumps(foods))
        writeableFile.close()
        self.destroy()
        self.master.destroy()
        Application().run()

    def enterFood(self):
        value = self.foodEntry.get()
        if len(value) < 1:
            alertDialog(self, "Please enter food name")
        else:
            self.foodName += value.capitalize()
            self.foodEntry.config(state="disabled")
            self.detailFrame.destroy()
            self.buildDetails()

def alertDialog(master, text):
    alert = tk.Toplevel(master)
    tk.Label(alert, text=text, foreground="red").pack(padx=10, pady=10)


class Application:
    def __init__(self):
        self.master = tk.Tk()
        self.frame = None

    def run(self):
        self.frame = MainFrame(self.master, foods)
        self.frame.mainloop()

Application().run()