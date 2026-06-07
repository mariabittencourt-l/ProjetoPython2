import json 
import time
import os

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data_dict = {item["name"]: item for item in data}
    return data_dict

def show_description(data, location):
    print("\n" + data[location]["description"] + "\n")

def travel(data, location):
    exits = data[location]["exits"]
    
    if not exits:
        print('''
===============================
No available paths from here.
''')
        return location
        
    print('''
===============================
Available ways:''')
    for index, exit_name in enumerate(exits, 1): 
        print(f"{index} - {exit_name}")
    print("0 - Cancel travel\n")
        
    while True:
        try:
            choice = int(input('''
===============================
Choose the new location: '''))
            
            if choice == 0:
                return location
            elif 1 <= choice <= len(exits):
                return exits[choice - 1]
            else:
                print("Error: Choose a valid number from the list.")
                
        except ValueError:
            print("Error: Please enter only integer numbers.")

def talk_to_npc(data,location,inventory,current_keyword):
    npc = data[location]["npc"]
    print(f'''
===============================
{npc['name']}:''')
    print(npc[ 'dialogue'])

    #first NPC (no answer)
    if "answer" not in npc:

        if npc['item'] not in inventory:
            inventory.append(npc['item'])
            current_keyword = npc['keyword']

            print(f'''
===============================
You received: {npc['item']}''')
            print(f'New keyword learned: {npc['keyword']}')
        else: 
            print('''
===============================
You have already talked to this NPC''')

        return current_keyword
    #last NPC
    if npc['name'] == 'Seal Guardian':
        
        answer = input('''
===============================
Your answer: ''').upper()

        if answer != npc['answer']:
            print('''
===============================
Wrong answer.''')
            return current_keyword
        
        missing = [
            item for item in npc['required_items']
            if item not in inventory
        ]

        if missing:
            print('''
===============================
You don't have all relices yet''')
            return current_keyword
        
        print( '\n', npc['ending'])
        exit()
    
    #normal NPC
    answer = input('''
    ===============================
    Your answer: ''').upper()

    if answer == npc['answer']:
        if npc['item'] not in inventory:
            inventory.append(npc['item'])
            current_keyword = npc['keyword']

            print(f'''
===============================
You received: {npc['item']}
''')
            print(f"New keyword learned: {npc['keyword']}")

        else: 
            print('\nYou already have this relic.')
    
    else:
        print('''
===============================
Wrong answer.''')
    return current_keyword

def check_combat(data, location, inventory):
    if "enemy" not in data[location]:
        return True

    else:
        enemy = data[location]["enemy"]
        if enemy['reward_item'] in inventory:
            print(f"\nThe corpse of {enemy['name']} lies on the ground. The area is safe.")
            return True

        else:
            print(f'''
===============================
ENEMY BLOCKING THE PATH: {enemy['name']}
===============================
{enemy['dialogue']}
''')

            if enemy['item_needed'] not in inventory:
                print(f"You don't have the [{enemy['item_needed']}] to face this danger!")  
                print("You are forced to retreat to Dirtmouth for safety!")
                return False 

            else:
                print("1 - Attack with your Nail")
                print("2 - Retreat")
                
                choice = input("\nChoose your action: ")
                
                if choice == "1":
                    print(f"\nYou brandish your nail and strike the {enemy['name']} with bravery!")
                    print(f"Victory! You defeated the {enemy['name']} and obtained: {enemy['reward_item']}!")
                    inventory.append(enemy['reward_item'])
                    return True

                else:
                    print("\nYou decided to take a step back and retreat.")
                    return False

def gameplay(data, first_loc):
    location = first_loc
    inventory=[]
    current_keyword= None

    show_description(data, location)


    while(True):
        print(f'''
===============================
Actual location: {location}
===============================''')
        print("1 - Show actual location description")
        print("2 - Travel")
        print("3 - Talk to NPC")
        print("4 - Show inventory")
        print("q - Quit the game\n")

        user_input = input("Choose your option: ")
        if user_input == "1": 
            print('===============================')
            print('''
Description: ''')
            show_description(data, location)
            print('===============================')

        elif user_input == "2": 
            old_location = location
            location = travel(data, location)
            if not check_combat(data, location, inventory):
                location = old_location
                
            show_description(data, location)

        elif user_input == '3':
            current_keyword = talk_to_npc(
                data,
                location,
                inventory,
                current_keyword
            )
        
        elif user_input == '4':
            print('''
===============================
Inventory:''')
            
            if inventory:
                for item in inventory:
                    print(f"- {item}")
            else: 
                print("Empty")

            print()


        elif user_input == "q": return 
        else: 
            print('''===============================
Please input a valid option''', flush=True)
            time.sleep(2)

data = load_json("game.json")

gameplay(data, "Dirtmouth")

#teste