# ressources
# https://fr.acervolima.com/comment-integrer-des-graphiques-matplotlib-dans-linterface-graphique-de-tkinter/

from numpy import *   # full import pour taper les noms de fonctions, e et pi direct
import tkinter 
from tkinter.ttk import Combobox
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.interpolate import approximate_taylor_polynomial
from scipy.interpolate import pade

sympy_install = False
try :
    from sympy import symbols, sympify, lambdify, factorial
    from sympy.functions.elementary.trigonometric import *
    from sympy.functions.elementary.exponential import * 
    sympy_install = True
    def sympy_taylor(fonction, ordre, x_0=0):
        x = symbols('x')
        fonc_formel = sympify(fonction)
        poly_taylor = poly1d([(fonc_formel.diff(x, i)/factorial(i)).subs(x, x_0).evalf()  for i in range(ordre, -1, -1)])
        return poly_taylor
except Exception as excep :
    print(excep)


# defaults
x_min = -3
x_max = 3
ordres = [3,5,7]
x_0 = 0
fonction = "sin(x)"

# Horreur : différents noms de fonctions selon numpy et sympy ! => 2 dict
fonctions_exemples = {}

# sans sympy, avec numpy seul :
fonctions_exemples[False] = {
                                "1/(1+x)"    : "1/(1+x)",
                                "(1+x)^5"    : "(1+x)**5", 
                                "exp x"      : "exp(x)",
                                "ln(1+x)"    : "log(1+x)",
                                "log_10(1+x)": "log10(1+x)",
                                "cos x"      : "cos(x)",
                                "sin x"      : "sin(x)",
                                "tan x"      : "tan(x)",
                                "ch x"       : "cosh(x)",
                                "sh x"       : "sinh(x)",
                                "th x"       : "tanh(x)",
                                "arccos x"   : "arccos(x)",
                                "arcsin x"   : "arcsin(x)",
                                "arctan x"   : "arctan(x)",
                                "argch x"    : "arccosh(x)",
                                "argsh x"    : "arcsinh(x)",
                                "argth x"    : "arctanh(x)",   
                                }

# avec sympy :
fonctions_exemples[True] = {
                                "1/(1+x)"    : "1/(1+x)",
                                "(1+x)^5"    : "(1+x)**5", 
                                "exp x"      : "exp(x)",  # ?
                                "ln(1+x)"    : "log(1+x)",
                                "log_10(1+x)": "log(1+x)/log(10)",
                                "cos x"      : "cos(x)",
                                "sin x"      : "sin(x)",
                                "tan x"      : "tan(x)",
                                "ch x"       : "cosh(x)",
                                "sh x"       : "sinh(x)",
                                "th x"       : "tanh(x)",
                                "arccos x"   : "acos(x)",
                                "arcsin x"   : "asin(x)",
                                "arctan x"   : "atan(x)",
                                "argch x"    : "acosh(x)",
                                "argsh x"    : "asinh(x)",
                                "argth x"    : "atanh(x)",   
                                }

def plot():
    try :
        xmin = float(eval(sv_xmin.get()))   # les eval : pour entrer e, pi ou pi/4 sans pb
        xmax = float(eval(sv_xmax.get()))
        if sv_ordre.get() :
            ordres = [int(el) for el in sv_ordre.get().split(',')]
        else :
            ordres = []
        x_0 = float(eval(sv_x_0.get()))
        fonction = sv_fonction.get()
        print(f"fonction {fonction} à développer en {x_0} aux ordres {ordres}\n")
    except Exception as excep :
        print(excep)
    axe_x = linspace(xmin, xmax, 100)
    if sympy_install :
        x = symbols('x')
        fonc = lambdify(x, sympify(fonction), "numpy")
    else :
        fonc = lambda x : eval(fonction)
    devs = {}
    pades = {}
    for ordre in ordres :
        if sympy_install :
            devs[ordre] = sympy_taylor(fonction, ordre, x_0)
        else : 
            devs[ordre] = approximate_taylor_polynomial(fonc, x_0, ordre, 1)
        var_subs = {1 : f"(x-{x_0})", 0 : "x", -1 : f"(x+{-x_0})"}
        print(f"développement d'ordre {ordre} en {x_0} :\n{poly1d(devs[ordre], variable=var_subs[int(sign(x_0))])}\n")
    #pade_ok = True
    #if pade_ok : 
    #    pades[ordres[-1]] = pade(devs[ordres[-1]], 2)
    #    print(f"développement de Padé d'ordre {ordre//2}, en {x_0} :\np=\n{poly1d(pades[ordre][0], variable=var_subs[int(sign(x_0))])}\nq=\n{poly1d(pades[ordre][1], variable=var_subs[int(sign(x_0))])}\n")
    fig = Figure(figsize=(8, 8), dpi=100) 
    plt = fig.add_subplot(111)
    plt.grid(color='grey', linestyle='-', linewidth=1)
    plt.axhline(y=0, color='black', linewidth=1)
    plt.axvline(x=0, color='black', linewidth=1)
    decalage = lambda x : x-x_0   # les approximations sont calculées en x=x_0, mais ramenées en x=0.
    couleur = lambda i : {"color" : "blue"} if i==0 else {}   # couleurs imposées
    for i, ordre in enumerate(ordres) :
        plt.plot(axe_x, devs[ordre](decalage(axe_x)), label=f"{poly1d(devs[ordre], variable=var_subs[int(sign(x_0))])}", **couleur(i))
    plt.plot(axe_x, fonc(axe_x), label=f"{fonction}", color="red", linewidth=3)
    plt.legend(shadow=True, prop={'family':'monospace', 'size':8})
    if window.ls_canvas_toolbar :
        window.ls_canvas_toolbar[-1][0].get_tk_widget().destroy()
        window.ls_canvas_toolbar[-1][1].destroy()
    canvas = FigureCanvasTkAgg(fig, master=display)   
    toolbar = NavigationToolbar2Tk(canvas, display) 
    toolbar.update()
    canvas.draw()
    canvas.get_tk_widget().pack()
    window.ls_canvas_toolbar.append((canvas, toolbar))
  
window = tkinter.Tk() 
window.title('Developpements limités') 
window.geometry("1400x700")
window.focus_set()
window.ls_canvas_toolbar = []

settings = tkinter.Frame(window)
settings.pack()

label_xmin = tkinter.Label(master=settings, text="xmin")
label_xmin.grid(row=0, column=0)
sv_xmin = tkinter.StringVar(value=str(x_min))
entry_xmin = tkinter.Entry(master=settings, textvariable=sv_xmin)
entry_xmin.grid(row=1, column=0)
 
label_xmax = tkinter.Label(master=settings, text="xmax")
label_xmax.grid(row=0, column=1)
sv_xmax = tkinter.StringVar(value=str(x_max)) 
entry_xmax = tkinter.Entry(master=settings, textvariable=sv_xmax) 
entry_xmax.grid(row=1, column=1)

label_ordre = tkinter.Label(master=settings, text="ordres des DL\n(séparés par ',')")
label_ordre.grid(row=0, column=2)
sv_ordre = tkinter.StringVar(value=', '.join(str(el) for el in ordres))
entry_ordre = tkinter.Entry(master=settings, textvariable=sv_ordre) 
entry_ordre.grid(row=1, column=2)

label_ordre = tkinter.Label(master=settings, text="en x_0 =")
label_ordre.grid(row=0, column=3)
sv_x_0 = tkinter.StringVar(value=str(x_0))
entry_ordre = tkinter.Entry(master=settings, textvariable=sv_x_0) 
entry_ordre.grid(row=1, column=3)

label_fonction = tkinter.Label(master=settings, text=f"fonction à entrer\n(nom {'sympy' if sympy_install else 'numpy'})")
label_fonction.grid(row=0, column=4)
sv_fonction = tkinter.StringVar(value=str(fonction))
entry_fonction = tkinter.Entry(master=settings, textvariable=sv_fonction)
entry_fonction.grid(row=1, column=4)

label_combo_fonction = tkinter.Label(settings, text="ou choisir")
label_combo_fonction.grid(row=0, column=5)
sv_choix = tkinter.StringVar()
combo_fonction = Combobox(settings, values=list(fonctions_exemples[sympy_install].keys()), textvariable=sv_choix)
combo_fonction.grid(row=1, column=5)
combo_fonction.bind('<<ComboboxSelected>>', lambda event: sv_fonction.set(sv_fonction.get()+fonctions_exemples[sympy_install][sv_choix.get()]))
combo_fonction.current(6)

plot_button = tkinter.Button(master=settings, command=plot, height=2, width=10, text="plot this !") 
plot_button.grid(row=1, column=6)

display = tkinter.Frame(window)
display.pack()



window.mainloop() 