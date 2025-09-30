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

        yunKey = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=100)) #Using master key as seed, generate rayKey
        print(yunKey)
        ciphText = '' # Initialize ciphertext variable
        random.seed(yunKey) # Set yunkey

        for i in range(len(self.data)):
            rowId = self.table[0].index(yunKey[i % len(yunKey)]) # Get row index 
            columnId = self.table[0].index(self.data[i]) # Get column index
            ciphText += self.table[rowId][columnId] # Add the correct character to the ciphertext string

        random.seed(self.key)
        self.data = ciphText
        return ciphText

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

if __name__ == "__main__":

    table = get_Table(get_Elements(True, True, True, False, True))
    text = plainText("hello", table, "123")

    text.getRayTable()
    print(text.table)
    text.encrypt()
    print(text.data)
    input()