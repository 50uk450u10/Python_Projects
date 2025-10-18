# Losing Battle Quiz
# Defeat the dreaded infinite loop
health = 10
trolls = 0
damage = 3

print("Your lone hero is surrounded by a massive army of trolls.\nYour hero unsheathes his sword for the last fight of his life.\n")

while health > 0:
    trolls += 1
    health -= damage
    print(f"Your hero swings and defeats an evil troll, but takes {damage} damage points.\n")
    
print(f"Your hero fought valiantly and defeated {trolls} trolls.\nBut alas, your hero is no more.")
input("\n\nPress the enter key to exit.")