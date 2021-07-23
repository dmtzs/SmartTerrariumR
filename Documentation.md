# Documentation
Here you can find the explanation of each of the methods that are in the whole program. So you can now the purpose of that methods.
<br>
This is the official documentation of the program.

## Raspberry
Just a quick example for description and next the fragment of code
```
def readData(self):
    with open(os.path.abspath(self.filename), 'r') as jsonFile:
        self.jsonData = json.load(jsonFile)
        jsonFile.close()
```