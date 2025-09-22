import string
import os
import random

class plainText:

    def __init__(self, data, table, key): #Create object properties 
        self.data = data
        self.table = table
        self.key = key
        random.seed(self.key)

    def getRayTable(self):

        rayKey = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=100)) #Using master key as seed, generate rayKey
        random.seed(rayKey) #Set rayKey as seed
        random.shuffle(self.table[0]) #Shuffle element of table
        
        row = [] #Init row
        rayTable = [] #Init rayTable
        row.extend(self.table[0]) # Add first row to rayTable

        for i in table: #Create the rest of the table
            rayTable.append(row.copy())
            row.extend(row[0])
            row.pop(0)

        random.seed(self.key) #Set seed back to master key
        self.table = rayTable
        return rayTable

    def encrypt(self):

        for i in self.data:
            pass

        return ciphText



if __name__ == "__main__":

    def get_Elements(upCharQuery = True, lowCharQuery = True, symQuery = True, whispaQuery = True, numQuery = True):
        cipherElements = []
        alphUp = list(string.ascii_uppercase)
        alphLow = list(string.ascii_lowercase)
        numbers = list(string.digits)
        whitespace = list(string.whitespace)
        symbols = list(string.punctuation)

        if (upCharQuery):
            cipherElements.extend(alphUp)
        if (lowCharQuery):
            cipherElements.extend(alphLow)
        if (symQuery):
            cipherElements.extend(symbols)
        if (whispaQuery):
            cipherElements.extend(whitespace)
        if (numQuery):
            cipherElements.extend(numbers)

        return cipherElements

    def get_Table(elements):
        table = []
        row = []
        row.extend(elements)

        for i in range(len(elements)):
            table.append(row.copy())
            row.extend(row[0])
            row.pop(0)

        return table

    table = get_Table(get_Elements(True, True, True, False, True))
    text = plainText("hello", table, "123")

    text.getRayTable()
    print(text.table)
    input()

