import tkinter as tk
from tkinter import filedialog
import os
import shutil
import xml.etree.ElementTree as et
import csv
running = True
foundxml = False
while running == True:
    os.system('cls')
    print("Welcome to bricklink xml editor!\n")
    print("Would you like to:\nChange the qunatity of all items(1)?\nMerge two files together(2)?\nChange all items to a colour(3)?\nAdd XML files(4)?\nFix Indentation(5)?\nExit(6)?")
    choice = input("Enter your choice(1/2/3/4/5): ")
    if choice == "1":
        os.system('cls')
        # List all .xml files in the working directory
        xml_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.xml')]

        # Print the list of files and ask the user to select one
        print("Select an XML file:")
        for i, file in enumerate(xml_files):
            print(f"{i+1}. {file}")
        file_num = int(input()) - 1
        selected_file = xml_files[file_num]

        # Ask the user to select a number
        print("Enter a number to multiply by:")
        multiplier = int(input())

        # Parse the XML file and multiply the number in each <MINQTY> tag by the selected number
        tree = et.parse(selected_file)
        root = tree.getroot()
        for elem in root.iter('MINQTY'):
            elem.text = str(int(elem.text) * multiplier)

        # Write the modified XML file
        modified_file = f"multiplied_{selected_file}"
        tree.write(modified_file)

        print(f"Modified file saved as {modified_file}")
        input("Press enter to continue...")

    elif choice == "2":
        os.system('cls')
        # get the names of the two XML files to merge from the user
        xml_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.xml')]

        # Print the list of files and ask the user to select one
        print("Select two XML files:")
        for i, file in enumerate(xml_files):
            print(f"{i+1}. {file}")
        file_num = int(input("Enter first file: ")) - 1
        file1 = xml_files[file_num]

        os.system('cls')
        xml_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.xml')]
        xml_files.pop(file_num)
        # Print the list of files and ask the user to select one
        print("Select two XML files:")
        for i, file in enumerate(xml_files):
            print(f"{i+1}. {file}")
        file_num = int(input("Enter second file: ")) - 1
        file2 = xml_files[file_num]
        

        # parse the XML files
        tree1 = et.parse(file1)
        root1 = tree1.getroot()
        tree2 = et.parse(file2)
        root2 = tree2.getroot()

        # merge the items from the second file into the first file
        for item2 in root2.iter("ITEM"):
            item_num2 = item2.find("ITEMID").text
            color2 = item2.find("COLOR").text
            qty2 = int(item2.find("MINQTY").text)
            found_match = False
            
            for item1 in root1.iter("ITEM"):
                item_num1 = item1.find("ITEMID").text
                color1 = item1.find("COLOR").text
                qty1 = int(item1.find("MINQTY").text)
                if item_num1 == item_num2 and color1 == color2:
                    found_match = True
                    item1.find("MINQTY").text = str(qty1 + qty2)
                    break
            
            if not found_match:
                root1.append(item2)

        # write the merged file to disk
        merged_file = os.path.splitext(file1)[0] + "_merged.xml"
        tree1.write(merged_file)

        print(f"Successfully merged {file1} and {file2} into {merged_file}")
        input("Press enter to continue...")

    elif choice == "3":
        os.system('cls')

        #List all XML files in the current working directory and ask the user to select one
        xml_files = [f for f in os.listdir('.') if f.endswith('.xml')]
        print("Select an XML file to modify:")
        for i, f in enumerate(xml_files):
            print(f"{i + 1}. {f}")

        while True:
            try:
                choice = int(input("Enter your choice (1 - {0}): ".format(len(xml_files))))
                xml_file = xml_files[choice - 1]
                break
            except (ValueError, IndexError):
                print("Invalid choice. Please try again.")

        #Ask the user to input a BrickLink color name or number, or an RGB value
        color_input = input("Enter a BrickLink color name or number, or an RGB value (e.g. '128,0,0'): ")
        try:
            color = int(color_input)  # Check if the input is already a color number
        except ValueError:
            # If the input is a color name or RGB value, convert it to a color number using a CSV file
            with open('colors.csv', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                found = False
                for row in reader:
                    if row[1] == color_input:
                        color = int(row[0])
                        found = True
                        break
                    elif row[2] == color_input:
                        color = int(row[0])
                        found = True
                        break
                if not found:
                    try:
                        # If the input is an RGB value, convert it to a color number using the same CSV file
                        r, g, b = [int(x) for x in color_input.split(',')]
                        for row in reader:
                            if (int(row[2][0:2], 16), int(row[2][2:4], 16), int(row[2][4:6], 16)) == (r, g, b):
                                color = int(row[0])
                                found = True
                                break
                        if not found:
                            print("Invalid color name, number, or RGB value. Please try again.")
                            exit()
                    except ValueError:
                        print("Invalid color name, number, or RGB value. Please try again.")
                        exit()

        #Change all item colors in the selected BrickLink XML file to the user's selected color
        tree = et.parse(xml_file)
        root = tree.getroot()

        for item in root.findall('.//ITEM'):
            item_color = item.find('COLOR')
            if item_color is not None:
                item_color.text = str(color)
        tree.write(xml_file)
        print(f"Color of all items in {xml_file} changed to {color}.")
        input("Press enter to continue...")

    elif choice == "4":
        root = tk.Tk()

        # open file dialog box and allow user to select XML files
        file_path = filedialog.askopenfilenames(filetypes=[("XML files", "*.xml")])
        root.withdraw()
        # move selected files to current working directory
        for file in file_path:
            shutil.move(file, os.getcwd())
        print("File Import Complete!")
        input("Press enter to continue...")
    
    elif choice == "5":

        # Get list of XML files in current directory
        xml_files = [f for f in os.listdir('.') if f.endswith('.xml')]

        # Print list of XML files
        print("Available XML files:")
        for i, xml_file in enumerate(xml_files):
            print(f"{i+1}. {xml_file}")

        # Ask user to select an XML file
        selection = int(input("Select an XML file (enter number): "))

        # Load selected XML file
        xml_file = xml_files[selection-1]
        tree = et.parse(xml_file)
        root = tree.getroot()


        # Fix indentation
        et.indent(root)
        tree.write(xml_file)
        print("Indentation fixed.")
        input("Press enter to continue...")

    elif choice == "6":
        os.system('cls')
        print("Bye!")
        running = False
    else:
        input("Invalid choice.\nPress enter to continue...")