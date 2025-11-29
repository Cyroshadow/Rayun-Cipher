import string
import random

class data:

    def __init__(self, data, table, key, yunKey = ""): #Create object properties 
        self.data = data
        self.table = table
        self.key = key
        self.yunKey = yunKey
        random.seed(self.key)

        keyElements = ''.join(random.choices(string.ascii_letters 
                                             + string.digits + 
                                             string.punctuation, k=100)) #Using master key as seed, generate rayKey
        self.yunKey = list(keyElements)
        random.shuffle(self.yunKey)

    def getRayTable(self):

        rayKey = ''.join(random.choices(string.ascii_letters
                                        + string.digits
                                        + string.punctuation, k=100)) #Using master key as seed, generate rayKey
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
        ciphText = '' # Initialize ciphertext variable

        for i in range(len(self.data)):
            rowId = self.table[0].index(self.yunKey[i % len(self.yunKey)]) # Get row index 
            columnId = self.table[0].index(self.data[i]) # Get column index
            ciphText += self.table[rowId][columnId] # Add the correct character to the ciphertext string

        self.data = ciphText
        return ciphText
    
    def decrypt(self):
        plainText = '' # Initialize ciphertext variable

        for i in range(len(self.data)):
            rowId = self.table[0].index(self.yunKey[i % len(self.yunKey)]) # Get row index 
            columnId = self.table[rowId].index(self.data[i]) # Get column index
            plainText += self.table[0][columnId]

        self.data = plainText
        return plainText

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

    table = get_Table(get_Elements(True, True, True, True, True))
    text = data("", table, "g00d_P@ssw0rD")

    text.getRayTable()
    text.encrypt()
    print(text.data)
    text.decrypt()
    print(text.data)