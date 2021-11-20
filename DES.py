# Imports
from math import gcd
import tkinter as tk

# General configuration
# Creation of the window
win = tk.Tk()
win.title('Diophantine equation solver')
win.geometry('315x500+640+150')
win.resizable(False, False)

# Creation of frame(s)
main_frame = tk.Frame(win, width=315, height=500, bg='#153d4a')

# Importing PNG(s)
icon_pic = tk.PhotoImage(file='Diophantine equation solver.png')
win.iconphoto(True, icon_pic)

# Creation of functions


# Functions UNTIED with the GUI
def check_int(expression):
    if len(str(expression)[str(expression).index('.')::]) == 2 and str(expression)[str(expression).index('.') + 1] == '0':
        return True
    else:
        return False


# This function turns coefficient whose type is float to str,
# BUT it is used to write coefficients in between other symbols.
# Moreover, instead of writing "...+1x" it'll write "...+x", thereby making it somewhat prettier.
# The idea is that it also adds "+" to the coeff, not "-", as "-" is automatically written in front of negative numbers.
def middle_mystr(coeff):
    if coeff == -1.0:
        return ' - '
    elif coeff == 1.0:
        return ' + '
    elif coeff >= 0:
        return ' + ' + str(coeff)
    else:
        return str(coeff)


# This function turns coefficient whose type is float to str,
# BUT it is used to write coefficients at the beginning of an equation.
def beginning_mystr(coeff):
    if coeff == -1.0:
        return '-'
    elif coeff == 1.0:
        return ''
    else:
        return str(coeff)


def gather_coefficients(equation):
    # default vars
    b_coefficient = []
    c_coefficient = []
    # Data input
    diophantine_equation = equation
    # Data preparation
    diophantine_equation = diophantine_equation.lower()
    split_equation = list(diophantine_equation)
    while ' ' in split_equation:
        split_equation.remove(' ')

    try:
        # Here comes the actual process of getting the coefficients:
        counter = split_equation.index('=')

        # B coefficient
        # =============================================================================================================
        # EXTRACTING THE DATA:
        for char in split_equation[split_equation.index('=')-1:0:-1]:
            if char == '+' or char == '-':
                b_coefficient.append(char)
                counter -= 1
                break
            b_coefficient.append(char)
            counter -= 1
        del split_equation[counter:split_equation.index('=')]
        b_coefficient.reverse()
        # POST-PROCESSING:
        yariable = b_coefficient[-1]
        del b_coefficient[-1]
        if not any(map(str.isdigit, b_coefficient)):
            if b_coefficient[0] == '+':
                b_coefficient = 1
            else:
                b_coefficient = -1
        else:
            if b_coefficient[0] == '+':
                b_coefficient = int(''.join(b_coefficient[1::]))
            else:
                b_coefficient = -int(''.join(b_coefficient[1::]))
        # =============================================================================================================

        counter = split_equation.index('=')

        # С coefficient
        # =============================================================================================================
        # EXTRACTING THE DATA:
        for char in split_equation[split_equation.index('='):len(split_equation)+1]:
            c_coefficient.append(char)
            counter += 1
        del split_equation[split_equation.index('='):counter]
        del c_coefficient[0]
        # POST-PROCESSING:
        c_coefficient = int(''.join(c_coefficient))
        # =============================================================================================================

        # A coefficient
        # =============================================================================================================
        if not any(map(str.isdigit, split_equation)):
            if '-' in split_equation:
                xariable = split_equation[-1]
                a_coefficient = -1
            else:
                xariable = split_equation[0]
                a_coefficient = 1
        else:
            xariable = split_equation[-1]
            del split_equation[-1]
            a_coefficient = int(''.join(split_equation))

        # =============================================================================================================
        return [a_coefficient, xariable, b_coefficient, yariable, c_coefficient, diophantine_equation]
    except:
        return '<ERROR>'


def get_the_values_xy(a, b, c):
    var = 0
    if abs(a) < abs(b):    # Then let's write 'x' through 'y' < ax = c - by >
        while True:
            if check_int((c - b * var) / a):
                return [int((c - b*var) / a), var]   # /// x, y
            var += 1
    else:   # Then let's write 'y' through 'x' < by = c - ax >
        while True:
            if check_int((c - a * var) / b):
                return [var, int((c - a * var) / b)]   # /// x, y
            var += 1


# Functions TIED with the GUI
def solve():
    users_output['state'] = 'normal'                                                # DATA TYPE - TUPLE
    users_output.delete(1.0, tk.END)                                                    # INDEXES:
    entered_equation = users_input.get()                   #                   0       1         2       3         4               5
    coefficients_vars = gather_coefficients(entered_equation)  # <<=== <A-COEFFICIENT, X, B-COEFFICIENT, Y, C-COEFFICIENT, INITIAL_EQUATION>
    users_output.insert(1.0, '\n' * 1000)
    data_positioning = 1.2
    if coefficients_vars == '<ERROR>' or coefficients_vars[1] == coefficients_vars[3]:
        users_output.insert(data_positioning, 'К сожалению, я решаю только уравнения вида \"ax+by=c\" :(')
        return None
    gcd_of_a_b = gcd(coefficients_vars[0], coefficients_vars[2])
    users_output.insert(1.2, coefficients_vars[5])
    if not check_int(coefficients_vars[4] / gcd_of_a_b):
        data_positioning += 2
        users_output.insert(data_positioning, 'Уравнение ' + coefficients_vars[5] + ' решить в целых числах невозможно.')
        return None
    # Reducing the coefficients dividing by gcd(a,b,c) if possible
    if coefficients_vars[0] != coefficients_vars[0] / gcd_of_a_b:
        i = 0
        for coefficient in coefficients_vars[::2]:
            coefficients_vars[i] = int(coefficient / gcd_of_a_b)
            i += 2
        data_positioning += 2
        users_output.insert(data_positioning, 'Сократим коэф. на ' + str(gcd_of_a_b) + ':')
        data_positioning += 2
        users_output.insert(data_positioning, beginning_mystr(coefficients_vars[0]) + coefficients_vars[1] + middle_mystr(coefficients_vars[2]) + coefficients_vars[3] + ' = ' + str(coefficients_vars[4]))
    # Now we're getting two values for 'x' and 'y' which will satisfy the equation 'ax + by = c'
    satisfying_values = get_the_values_xy(coefficients_vars[0], coefficients_vars[2], coefficients_vars[4])
    data_positioning += 2
    users_output.insert(data_positioning, 'Пара значений удовлетворяющих равенство: ')
    data_positioning += 2
    users_output.insert(data_positioning, coefficients_vars[1] + '₀ = ' + str(satisfying_values[0]) + '; ' + coefficients_vars[3] + '₀ = ' + str(satisfying_values[1]))
    data_positioning += 2
    users_output.insert(data_positioning, 'Формулы: ')
    data_positioning += 2
    users_output.insert(data_positioning, 'x = -bn + x₀')
    data_positioning += 2
    users_output.insert(data_positioning, 'y = an + y₀')
    data_positioning += 2
    users_output.insert(data_positioning, 'Подставим значения: ')
    if satisfying_values[0] >= 0:
        data_positioning += 2
        users_output.insert(data_positioning, coefficients_vars[1] + ' = ' + beginning_mystr(-coefficients_vars[2]) + 'n + ' + str(abs(satisfying_values[0])))
    else:
        data_positioning += 2
        users_output.insert(data_positioning, coefficients_vars[1] + ' = ' + beginning_mystr(-coefficients_vars[2]) + 'n - ' + str(abs(satisfying_values[0])))
    if satisfying_values[1] >= 0:
        data_positioning += 2
        users_output.insert(data_positioning, coefficients_vars[3] + ' = ' + beginning_mystr(coefficients_vars[0]) + 'n + ' + str(abs(satisfying_values[1])))
    else:
        data_positioning += 2
        users_output.insert(data_positioning, coefficients_vars[3] + ' = ' + beginning_mystr(coefficients_vars[0]) + 'n - ' + str(abs(satisfying_values[1])))

    data_positioning += 2
    users_output.insert(data_positioning, 'Ответ: ')

    # X
    if satisfying_values[0] == 0:
        data_positioning += 2
        users_output.insert(data_positioning, coefficients_vars[1] + ' = ' + beginning_mystr(-coefficients_vars[2]) + 'n')
    else:
        if satisfying_values[0] > 0:
            data_positioning += 2
            users_output.insert(data_positioning, coefficients_vars[1] + ' = ' + beginning_mystr(-coefficients_vars[2]) + 'n + ' + str(abs(satisfying_values[0])))
        else:
            data_positioning += 2
            users_output.insert(data_positioning, coefficients_vars[1] + ' = ' + beginning_mystr(-coefficients_vars[2]) + 'n - ' + str(abs(satisfying_values[0])))

    # Y
    if satisfying_values[1] == 0:
        data_positioning += 2
        users_output.insert(data_positioning, coefficients_vars[3] + ' = ' + beginning_mystr(coefficients_vars[0]) + 'n')
    else:
        if satisfying_values[1] > 0:
            data_positioning += 2
            users_output.insert(data_positioning, coefficients_vars[3] + ' = ' + beginning_mystr(coefficients_vars[0]) + 'n + ' + str(abs(satisfying_values[1])))
        else:
            data_positioning += 2
            users_output.insert(data_positioning, coefficients_vars[3] + ' = ' + beginning_mystr(coefficients_vars[0]) + 'n - ' + str(abs(satisfying_values[1])))

    users_output['state'] = 'disabled'


def delete():
    users_output['state'] = 'normal'
    users_input.delete(0, tk.END)
    users_output.delete(1.0, tk.END)
    users_output['state'] = 'disabled'


# Creation of widgets
users_input = tk.Entry(main_frame, width=32, bg='#f1f1f2', bd=3, font=16, selectbackground='#217ca3',
                       selectforeground='#0f1b07')

language_label = tk.Label(main_frame, fg='#ffffff', font=('Arial Black', 16), text='Введите уравнение: ', bg='#174b5c')

solve_button = tk.Button(main_frame, fg='#ffffff', bg='#174b5c',
                         activebackground='#09232b', activeforeground='#ffffff', font=('Arial Black', 14),
                         cursor='hand2', text='Решить', bd=4, relief='ridge', height=1, width=10, command=solve)

delete_button = tk.Button(main_frame, fg='White', bg='#174b5c',
                          activebackground='#09232b', activeforeground='#ffffff', font=('Arial Black', 14),
                          cursor='hand2', text='Удалить', bd=4, relief='ridge', height=1, width=10, command=delete)

users_output = tk.Text(main_frame, width=29, height=15, bg='#f1f1f2', bd=3, font=('Consolas', 14),
                       selectbackground='#217ca3',
                       selectforeground='#0f1b07', state='disabled', wrap='word')

# Placing the widgets
main_frame.pack()
users_input.place(x=10, y=50)
language_label.place(x=10, y=10)
solve_button.place(x=10, y=85)
delete_button.place(x=163, y=85)
users_output.place(x=10, y=145)

# Starting program
win.mainloop()
