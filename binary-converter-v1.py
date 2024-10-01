# My attempt at a binary converter in Python 
# Start Date 9/19/24
# End Date 9/20/24
import tkinter as tk


def binary_to_decimal_converter(ui):
    print(int(ui,2))

def decimal_to_binary_converter(ui):
    if ui >= 1:
        decimal_to_binary_converter(ui // 2)
    print(ui % 2, end = '')

if __name__=="__main__":
    
    
    # Creates GUI with resolution of 300x275 
    root = tk.Tk()
    root.geometry('400x100')

    # Creates a test root and a grid for the text to appear on
    text_result = tk.Text(root, height=2, width=16, font=("Arial", 24))
    text_result.grid(columnspan=5)
    
    n = 0
    while (n != 1):
        choice = str(input("Type 'd' for decimal to binary and 'e' for the opposite: "))
        
        if choice == 'd': 
            user_input = int(input("Enter Decimal number: "))
            decimal_to_binary_converter(user_input)
        elif choice == 'e':
            user_input = input("Enter Binary number: ")
            binary_to_decimal_converter(user_input)
        else:
            print("invalid")
        
        n = int(input("Would you like to convert again? 0 for yes and 1 for no: "))
        