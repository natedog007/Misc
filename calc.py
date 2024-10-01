# Python Calculator
import tkinter as tk

calculation = "" 

# Adds whatever the user input was onto the GUI in the form of a string 
def add_to_calc(symbol):
    global calculation
    calculation += str(symbol)
    text_result.delete(1.0, "end")
    text_result.insert(1.0, calculation)

# The eval() function is doing most of the heavy lifting on this function
# Sets calculation to a string of a solved version of calculatoion then deletes the calculation 
# and replaces it with the new solved calculation
def evaluate_calc():
    global calculation
    try:
        calculation = str(eval(calculation))
        text_result.delete(1.0,"end")
        text_result.insert(1.0, calculation)  
    except:
        clear_f()
        text_result.insert(1.0, "Error")


# Clears the calculator screen by deleting the string in the textbox
def clear_f():
    global calculation
    calculation = ""
    text_result.delete(1.0,"end")


# Creates GUI with resolution of 300x275 
root = tk.Tk()
root.geometry('300x275')

# Creates a test root and a grid for the text to appear on
text_result = tk.Text(root, height=2, width=16, font=("Arial", 24))
text_result.grid(columnspan=5)

# Buttons(root, what the button is, sending that button's value to calc function, width, font)
# .grid() is for button location on the previously defined grid
btn_1 = tk.Button(root, text="1", command=lambda:add_to_calc(1), width=5 ,font=("Arial", 14))
btn_1.grid(row=2, column=1)

btn_2 = tk.Button(root, text="2", command=lambda:add_to_calc(2), width=5 ,font=("Arial", 14))
btn_2.grid(row=2, column=2)

btn_3 = tk.Button(root, text="3", command=lambda:add_to_calc(3), width=5 ,font=("Arial", 14))
btn_3.grid(row=2, column=3)

btn_4 = tk.Button(root, text="4", command=lambda:add_to_calc(4), width=5 ,font=("Arial", 14))
btn_4.grid(row=3, column=1)

btn_5 = tk.Button(root, text="5", command=lambda:add_to_calc(5), width=5 ,font=("Arial", 14))
btn_5.grid(row=3, column=2)

btn_6 = tk.Button(root, text="6", command=lambda:add_to_calc(6), width=5 ,font=("Arial", 14))
btn_6.grid(row=3, column=3)

btn_7 = tk.Button(root, text="7", command=lambda:add_to_calc(7), width=5 ,font=("Arial", 14))
btn_7.grid(row=4, column=1)

btn_8 = tk.Button(root, text="8", command=lambda:add_to_calc(8), width=5 ,font=("Arial", 14))
btn_8.grid(row=4, column=2)

btn_9 = tk.Button(root, text="9", command=lambda:add_to_calc(9), width=5 ,font=("Arial", 14))
btn_9.grid(row=4, column=3)

btn_0 = tk.Button(root, text="0", command=lambda:add_to_calc(0), width=5 ,font=("Arial", 14))
btn_0.grid(row=5, column=2)

# Sign buttons (pass a string instead of an int)
btn_plus = tk.Button(root, text="+", command=lambda:add_to_calc("+"), width=5 ,font=("Arial", 14))
btn_plus.grid(row=2, column=4)

btn_minus = tk.Button(root, text="-", command=lambda:add_to_calc("-"), width=5 ,font=("Arial", 14))
btn_minus.grid(row=3, column=4)

btn_multi = tk.Button(root, text="*", command=lambda:add_to_calc("*"), width=5 ,font=("Arial", 14))
btn_multi.grid(row=4, column=4)

btn_div = tk.Button(root, text="/", command=lambda:add_to_calc("/"), width=5 ,font=("Arial", 14))
btn_div.grid(row=5, column=4)

# Parentheses
btn_open = tk.Button(root, text="(", command=lambda:add_to_calc("("), width=5 ,font=("Arial", 14))
btn_open.grid(row=5, column=1)

btn_close = tk.Button(root, text=")", command=lambda:add_to_calc(")"), width=5 ,font=("Arial", 14))
btn_close.grid(row=5, column=3)

# Clear and Equals
btn_equal = tk.Button(root, text="=", command= evaluate_calc, width=11 ,font=("Arial", 14))
btn_equal.grid(row=6, column=1, columnspan=2)

btn_close = tk.Button(root, text="C", command=clear_f, width=11 ,font=("Arial", 14))
btn_close.grid(row=6, column=3, columnspan=2)



root.mainloop()

