import json

persons = {"Name":"Aditya","age":25,"city":"BCM","Relationship":"Single"}

personsJSON = json.dumps(persons, indent=4)
print(personsJSON)

with open('person.json', 'w') as file:
    json.dump(persons,file,indent=4)

    print(json.loads(personsJSON))