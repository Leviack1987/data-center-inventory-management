import sqlite3
connection=sqlite3.connect("inventory.db")
cursor=connection.cursor()

def chooseOption():
        while True:
              try:
                    opt=int(input("Choose an option: "))
                    while (opt>4 or opt<1):
                        print("Please choose between 1, 2, 3, and 4")
                        opt=int(input("Choose an option: "))
                    return opt
              except ValueError:
                    print("Please enter one of the possible numbers")

while True:
    print("DATA CENTER INVENTORY MANAGEMENT\n1. View Inventory\n2. Receive Stock\n3. Issue Stock\n4. Exit\n")
    option=chooseOption()

    if(option==1):
                cursor.execute("SELECT component,quantity,location FROM inventory;")
                rows=cursor.fetchall()
                print("\nCOMPONENT      QUANTITY     LOCATION")
                print(rows[0][0]+"       "+str(rows[0][1])+"           "+rows[0][2])
                print(rows[1][0]+"            "+str(rows[1][1])+"           "+rows[1][2])
                print(rows[2][0]+"            "+str(rows[2][1])+"           "+rows[2][2])

    elif(option==2):
          component=input("Which component? ").upper()
          while(component!="DDR5 RAM" and component!="SSD" and component!="CPU"):
                print("Please choose DDR5 RAM, SSD or CPU")
                component=input("Which component? ").upper()
        
          units=int(input("How many units arrived? "))
          while(units<0):
                print("Please answer witha number greater than a negative")
                units=int(input("How many units arrived? "))

          cursor.execute("UPDATE inventory SET quantity = quantity + ? WHERE component = ?;",(units,component))
          connection.commit()
          print("Successfully received "+str(units)+" "+component+" units.")
          
    elif(option==3):
        component=input("Which component? ").upper()
        while(component!="DDR5 RAM" and component!="SSD" and component!="CPU"):
            print("Please choose DDR5 RAM, SSD or CPU")
            component=input("Which component? ").upper()

        units=int(input("How many units were used? "))
        cursor.execute("SELECT quantity FROM inventory WHERE component = ?;",(component,))
        quantity=cursor.fetchone()
        while(units<0 or units>quantity[0]):
            print("Please give a number that does not exceed the stock and it is positive.")
            units=int(input("How many units were used? "))
        
        cursor.execute("UPDATE inventory SET quantity = quantity - ? WHERE component = ?;", (units,component))
        connection.commit()
        print("Successfully issued "+str(units)+" "+component+" units.")

        
    else:
          break


print("Goodbye!")
connection.close()