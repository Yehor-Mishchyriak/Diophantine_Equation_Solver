# Imports
from math import gcd, floor, ceil
import tkinter as tk

# General configuration
# Creation of the window
win = tk.Tk()
win.title('Diophantine equation solver')
win.geometry('315x500+640+150')
win.resizable(False, False)

# Creation of frame(s)
main_frame = tk.Frame(win, width=315, height=500, bg='#153d4a')

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
        return ' - ' + str(abs(coeff))


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


def does_it_satisfy_x(value, b, x0):
    if -b * value + x0 > 0:
        return True
    else:
        return False


def does_it_satisfy_y(value, a, y0):
    if a * value + y0 > 0:
        return True
    else:
        return False


# Functions TIED with the GUI
def solve():
    users_output['state'] = 'normal'                                                # DATA TYPE - TUPLE
    users_output.delete(1.0, tk.END)                                                    # INDEXES:
    entered_equation = users_input.get()                   #                   0       1         2       3         4               5
    coefficients_vars = gather_coefficients(entered_equation)  # <<=== <A-COEFFICIENT, X, B-COEFFICIENT, Y, C-COEFFICIENT, INITIAL_EQUATION>
    users_output.insert(1.0, '\n' * 1000)
    data_positioning = 1.2
    if coefficients_vars == '<ERROR>' or coefficients_vars[1] == coefficients_vars[3]:
        users_output.insert(data_positioning, 'Unfortunately, I solve equations only of this type - \"ax+by=c\" :(')
        return None
    gcd_of_a_b = gcd(coefficients_vars[0], coefficients_vars[2])
    users_output.insert(1.2, coefficients_vars[5])
    if not check_int(coefficients_vars[4] / gcd_of_a_b):
        data_positioning += 2
        users_output.insert(data_positioning, 'The equation ' + coefficients_vars[5] + ' cannot be solved in whole numbers.')
        return None
    # Reducing the coefficients dividing by gcd(a,b,c) if possible
    if coefficients_vars[0] != coefficients_vars[0] / gcd_of_a_b:
        i = 0
        for coefficient in coefficients_vars[::2]:
            coefficients_vars[i] = int(coefficient / gcd_of_a_b)
            i += 2
        data_positioning += 2
        users_output.insert(data_positioning, 'Let\'s reduce the coefficients of the equation by ' + str(gcd_of_a_b) + ' times:')
        data_positioning += 2
        users_output.insert(data_positioning, beginning_mystr(coefficients_vars[0]) + coefficients_vars[1] + middle_mystr(coefficients_vars[2]) + coefficients_vars[3] + ' = ' + str(coefficients_vars[4]))
    # Now we're getting two values for 'x' and 'y' which will satisfy the equation 'ax + by = c'
    satisfying_values = get_the_values_xy(coefficients_vars[0], coefficients_vars[2], coefficients_vars[4])
    data_positioning += 2
    users_output.insert(data_positioning, 'A couple of values satisfying the equation: ')
    data_positioning += 2
    users_output.insert(data_positioning, coefficients_vars[1] + '₀ = ' + str(satisfying_values[0]) + '; ' + coefficients_vars[3] + '₀ = ' + str(satisfying_values[1]))
    data_positioning += 2
    users_output.insert(data_positioning, 'Formulas: ')
    data_positioning += 2
    users_output.insert(data_positioning, 'x = -bn + x₀')
    data_positioning += 2
    users_output.insert(data_positioning, 'y = an + y₀')
    data_positioning += 2
    users_output.insert(data_positioning, 'Let\'s substitute the values: ')

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

    data_positioning += 2
    users_output.insert(data_positioning, 'An array of the "n" values which turn the formulas in positive solutions: ')
    data_positioning += 2

    # This is for y
    # ==================================================================================================================
    if coefficients_vars[0] < 0:    # a < 0
        yvalue = satisfying_values[1] / coefficients_vars[0]
        if check_int(yvalue):
            yvalue = int(yvalue)
            if does_it_satisfy_y(yvalue, coefficients_vars[0], satisfying_values[1]):
                yinequality_sign = ' ≤ '
            else:
                yinequality_sign = ' < '
        else:
            yvalue = floor(yvalue)
            if does_it_satisfy_y(yvalue, coefficients_vars[0], satisfying_values[1]):
                yinequality_sign = ' ≤ '
            else:
                yinequality_sign = ' < '
    else:   # a > 0
        yvalue = -satisfying_values[1] / coefficients_vars[0]
        if check_int(yvalue):
            yvalue = int(yvalue)
            if does_it_satisfy_y(yvalue, coefficients_vars[0], satisfying_values[1]):
                yinequality_sign = ' ≥ '
            else:
                yinequality_sign = ' > '
        else:
            yvalue = ceil(yvalue)
            if does_it_satisfy_y(yvalue, coefficients_vars[0], satisfying_values[1]):
                yinequality_sign = ' ≥ '
            else:
                yinequality_sign = ' > '
    # ==================================================================================================================

    # This is for x
    # ==================================================================================================================
    if coefficients_vars[2] < 0:    # b < 0
        xvalue = -satisfying_values[0] / -coefficients_vars[2]
        if check_int(xvalue):
            xvalue = int(xvalue)
            if does_it_satisfy_x(xvalue, coefficients_vars[2], satisfying_values[0]):
                xinequality_sign = ' ≥ '
            else:
                xinequality_sign = ' > '
        else:
            xvalue = ceil(xvalue)
            if does_it_satisfy_x(xvalue, coefficients_vars[2], satisfying_values[0]):
                xinequality_sign = ' ≥ '
            else:
                xinequality_sign = ' > '
    else:   # b > 0
        xvalue = satisfying_values[0] / coefficients_vars[2]
        if check_int(xvalue):
            xvalue = int(xvalue)
            if does_it_satisfy_x(xvalue, coefficients_vars[2], satisfying_values[0]):
                xinequality_sign = ' ≤ '
            else:
                xinequality_sign = ' < '
        else:
            xvalue = floor(xvalue)
            if does_it_satisfy_x(xvalue, coefficients_vars[2], satisfying_values[0]):
                xinequality_sign = ' ≤ '
            else:
                xinequality_sign = ' < '

    # ==================================================================================================================

    users_output.insert(data_positioning, 'Г n' + xinequality_sign + str(xvalue) + ';')
    data_positioning += 1
    users_output.insert(data_positioning, '|  ')
    data_positioning += 1
    users_output.insert(data_positioning, 'L n' + yinequality_sign + str(yvalue) + '.')

    # /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-

    temporary_sign_x = xinequality_sign
    temporary_sign_y = yinequality_sign

    if temporary_sign_x != ' < ' and temporary_sign_x != ' > ':
        if temporary_sign_x == ' ≤ ':
            temporary_sign_x = ' < '
        else:
            temporary_sign_x = ' > '

    if temporary_sign_y != ' < ' and temporary_sign_y != ' > ':
        if temporary_sign_y == ' ≤ ':
            temporary_sign_y = ' < '
        else:
            temporary_sign_y = ' > '

    # /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-

    if temporary_sign_x == temporary_sign_y == ' > ':
        if xvalue > yvalue or xvalue == yvalue:
            data_positioning += 2
            if xinequality_sign == ' ≥ ' and does_it_satisfy_y(xvalue, coefficients_vars[0], satisfying_values[1]):
                users_output.insert(data_positioning, 'n Є [ ' + str(xvalue) + ' ; +∞ )')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: ∞')
            else:
                users_output.insert(data_positioning, 'n Є ( ' + str(xvalue) + ' ; +∞ )')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: ∞')
        else:
            data_positioning += 2
            if yinequality_sign == ' ≥ ' and does_it_satisfy_x(yvalue, coefficients_vars[2], satisfying_values[0]):
                users_output.insert(data_positioning, 'n Є [ ' + str(yvalue) + ' ; +∞ )')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: ∞')
            else:
                users_output.insert(data_positioning, 'n Є ( ' + str(yvalue) + ' ; +∞ )')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: ∞')
    elif temporary_sign_x == temporary_sign_y == ' < ':
        if xvalue < yvalue or xvalue == yvalue:
            data_positioning += 2
            if xinequality_sign == ' ≤ ' and does_it_satisfy_y(xvalue, coefficients_vars[0], satisfying_values[1]):
                users_output.insert(data_positioning, 'n Є ( -∞ ; ' + str(xvalue) + ' ]')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: ∞')
            else:
                users_output.insert(data_positioning, 'n Є ( -∞ ; ' + str(xvalue) + ' )')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: ∞')
        else:
            data_positioning += 2
            if yinequality_sign == ' ≤ ' and does_it_satisfy_x(yvalue, coefficients_vars[2], satisfying_values[0]):
                users_output.insert(data_positioning, 'n Є ( -∞ ; ' + str(yvalue) + ' ]')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: ∞')
            else:
                users_output.insert(data_positioning, 'n Є ( -∞ ; ' + str(yvalue) + ' )')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: ∞')
    else:
        if xvalue == yvalue:
            if xinequality_sign == ' ≥ ' or xinequality_sign == ' ≤ ':
                if yinequality_sign == ' ≥ ' or yinequality_sign == ' ≤ ':
                    data_positioning += 2
                    users_output.insert(data_positioning, 'n Є { ' + str(xvalue) + ' }')
                    data_positioning += 2
                    users_output.insert(data_positioning, 'The number of the positive solutions: 1')
                else:
                    data_positioning += 2
                    users_output.insert(data_positioning, 'n Є {}')
                    data_positioning += 2
                    users_output.insert(data_positioning, 'The number of the positive solutions: 0')
            else:
                data_positioning += 2
                users_output.insert(data_positioning, 'n Є {}')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: 0')

        elif temporary_sign_x == ' > ':
            if xvalue > yvalue:
                data_positioning += 2
                users_output.insert(data_positioning, 'n Є {}')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: 0')
            else:
                data_positioning += 2
                if xinequality_sign == ' ≥ ' and does_it_satisfy_y(xvalue, coefficients_vars[0], satisfying_values[1]):
                    left_bracket = '[ '
                else:
                    left_bracket = '( '

                if yinequality_sign == ' ≤ ' and does_it_satisfy_x(yvalue, coefficients_vars[2], satisfying_values[0]):
                    right_bracket = ' ]'
                else:
                    right_bracket = ' )'
                users_output.insert(data_positioning,
                                    'n Є ' + left_bracket + str(xvalue) + ' ; ' + str(yvalue) + right_bracket)
                data_positioning += 2
                if left_bracket == '[ ':
                    xvalue -= 1
                if right_bracket == ' ]':
                    yvalue += 1
                users_output.insert(data_positioning,
                                    'The number of the positive solutions: ' + str(yvalue - 1 - xvalue))
        else:

            if yvalue > xvalue:
                data_positioning += 2
                users_output.insert(data_positioning, 'n Є {}')
                data_positioning += 2
                users_output.insert(data_positioning, 'The number of the positive solutions: 0')
            else:
                data_positioning += 2
                if yinequality_sign == ' ≥ ' and does_it_satisfy_x(yvalue, coefficients_vars[2], satisfying_values[0]):
                    left_bracket = '[ '
                else:
                    left_bracket = '( '

                if xinequality_sign == ' ≤ ' and does_it_satisfy_y(xvalue, coefficients_vars[0], satisfying_values[1]):
                    right_bracket = ' ]'
                else:
                    right_bracket = ' )'
                users_output.insert(data_positioning,
                                    'n Є ' + left_bracket + str(yvalue) + ' ; ' + str(xvalue) + right_bracket)
                data_positioning += 2
                if left_bracket == '[ ':
                    yvalue -= 1
                if right_bracket == ' ]':
                    xvalue += 1
                users_output.insert(data_positioning,
                                    'The number of the positive solutions: ' + str(xvalue - 1 - yvalue))

    users_output['state'] = 'disabled'


def delete():
    users_output['state'] = 'normal'
    users_input.delete(0, tk.END)
    users_output.delete(1.0, tk.END)
    users_output['state'] = 'disabled'


# Creation of widgets
users_input = tk.Entry(main_frame, width=32, bg='#f1f1f2', bd=3, font=16, selectbackground='#217ca3',
                       selectforeground='#0f1b07')

language_label = tk.Label(main_frame, fg='#ffffff', font=('Arial Black', 16), text='Enter an equation: ', bg='#174b5c')

solve_button = tk.Button(main_frame, fg='#ffffff', bg='#174b5c',
                         activebackground='#09232b', activeforeground='#ffffff', font=('Arial Black', 14),
                         cursor='hand2', text='Solve', bd=4, relief='ridge', height=1, width=10, command=solve)

delete_button = tk.Button(main_frame, fg='White', bg='#174b5c',
                          activebackground='#09232b', activeforeground='#ffffff', font=('Arial Black', 14),
                          cursor='hand2', text='Delete', bd=4, relief='ridge', height=1, width=10, command=delete)

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
