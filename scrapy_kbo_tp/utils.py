import csv
import os
 
def lire_numero_entreprises():
    path = os.path.join(os.path.dirname(__file__), 'enterprise.csv') 
    path = os.path.abspath(path)  
    print("Lecture CSV depuis :", path)
 
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row['EnterpriseNumber'].strip().replace('.', '') for row in reader]