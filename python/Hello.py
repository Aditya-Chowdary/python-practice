# # import cowsay

# # print(cowsay.cow("Hello, World!"))
# # print(cowsay.trex("Hello, World!"))
# #this is a single line comment
# '''this is a multi-line comment'''

# def hello(to):
#     print("Hello,",to)
    
# #Ask user for their name
# Name = input("What is your name?\n").strip().title()
# hello(Name) #Call the hello function with the user's name

# # Name = Name.strip() #Remove leading and trailing spaces
# # Name = Name.capitalize() #Capitalize the first letter of the name
# # Name = Name.lower() #Convert the name to lowercase
# # Name = Name.upper() #Convert the name to uppercase
# # Name = Name.title() #Convert the name to title case

# print("Oh, cool! I like name", Name)
# print("Oh, cool! I like name " + Name)
# print("Oh, cool! I like name ",Name,sep='..')
# print("Oh, cool! I like name ",end='')
# print(Name)
# print(f"Oh, cool! I like name {Name}")

# print(2+3) #Addition
# print(2-3) #Subtraction
# print("2+3 = ", 2+3) 

class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def speak(self):
            print("Dog barks")


d = Dog()
d.speak()  # Output: Dog barks



