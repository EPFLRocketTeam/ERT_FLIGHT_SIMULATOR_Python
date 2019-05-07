# GUI
# Author : Henri Faure
# Last update : 6 May 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from tkinter import *
import numpy as np
from Simulator1D import Simulator1D
from Functions.stdAtmosUS import stdAtmosUS
from Rocket.Body import Body
from Rocket.Rocket import Rocket
from Rocket.Stage import Stage

# Displays in a label the selected rocket part
def TextLabel(type1, type2):
    label = Label(fenetre, text='The %s %s is selected' %(type2, type1), bg='DarkOrange1')
    label.grid(row=3, column=0, columnspan=3, in_=canvasAB)
    label.after(4000, lambda: label.destroy())

# Function which permits entry value manually
def EntryButton(canvasACN, name, rnum, cnum, entries):

    # Check all values are mathematical values
    def TestFunction(value):
        if value in '0123456789-+*/.':
            return True
        else:
            return False

    Label(fenetre, text='%s' % name, bg='gray85', anchor=NW).grid(row=rnum, column=cnum, padx=10, pady=2, in_=canvasACN)
    entry = Entry(fenetre, validate='key', validatecommand=(fenetre.register(TestFunction), '%S'))
    entry.insert(0, 0)
    entry.grid(row=rnum+1, column=cnum, padx=10, pady=10, in_=canvasACN)
    entries.append(entry)

# Function wich geta values from entries
def hallo(entries):
    Array_Value = []
    for entry in entries:
        Array_Value = np.append(Array_Value, eval(entry.get()))
    return Array_Value

# Displays canvas in which are the nosecone's parameters
def DispNoseCone():
    NoseCone_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC2.grid_remove()
    canvasAC3.grid_remove()
    canvasAC4.grid_remove()
    canvasAC5.grid_remove()
    canvasAC1.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical Eiger nosecone in drawing
def EigerNoseCone():
    EP = open('Parameters\\param_rocket\\EigerNose.txt', 'r')
    EP1=EP.readlines()
    VALUES_N = []
    for line in EP1:  # taking each line
        conv_int = float(line)
        VALUES_N.append(conv_int)
    DisplayNose(VALUES_N)

# Get values from entries then execute DisplayNose()
def SaveNose():
    VALUES_N = hallo(entries1)
    DisplayNose(VALUES_N)

# Display geometrical nosecone in drawing
LENGTH = [0, 0, 0, 0, 0, 0, 0]
DIAMETER = [0, 0, 0, 0, 0, 0, 0]
def DisplayNose(VALUES_N):
    canvas1.delete('all')

    NoseCone_Text = open('Parameters\\param_rocket\\NoseCone.txt', "w")
    for i in range(len(VALUES_N)):
        NoseCone_Text.write("%2.f\n" % (VALUES_N[i]))
    NoseCone_Text.close()

    Len_Nose = VALUES_N[0]
    LENGTH[0] = Len_Nose
    Dia_Nose = VALUES_N[1]
    DIAMETER[0] = Dia_Nose
    DispData()

    canvas1.configure(width=VALUES_N[0]/3, height=VALUES_N[1]/3, bg='white', highlightthickness=0, bd=0,
                     relief='ridge')  # 300 mm + 350 mm
    canvas1.create_arc(2/3*(1-VALUES_N[1]/3), 3.3*VALUES_N[1]/3, 4.1*VALUES_N[1]/3, -1, width=1, outline='blue', style=ARC,
                       start=90, extent=90)
    canvas1.create_arc(2/3*(1-VALUES_N[1]/3), VALUES_N[1]/3, 4.1*VALUES_N[1]/3+3, -2.3*VALUES_N[1]/3, width=1,
                       outline='blue', style=ARC, start=-90, extent=-90)
    canvas1.create_line(7/5*VALUES_N[1]/3, 0, VALUES_N[0]/3-1, 0, width=1, fill='blue')
    canvas1.create_line(7/5*VALUES_N[1]/3, VALUES_N[1]/3-1, VALUES_N[0]/3-1, VALUES_N[1]/3-1, width=1, fill='blue')
    canvas1.create_line(VALUES_N[0]/3-1, 0, VALUES_N[0]/3-1, VALUES_N[1]/3-1, width=1, fill='blue')
    canvas1.grid(row=3, column=1, in_=canvas0)

# Displays canvas in which are the tube's parameters
def DispTube():
    Tube_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC1.grid_remove()
    canvasAC3.grid_remove()
    canvasAC4.grid_remove()
    canvasAC5.grid_remove()
    canvasAC2.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical Eiger tube in drawing
def EigerTube():
    EP = open('Parameters\\param_rocket\\EigerTube.txt', 'r')
    EP1=EP.readlines()
    VALUES_T = []
    for line in EP1:  # taking each line
        conv_int = float(line)
        VALUES_T.append(conv_int)
    DisplayTube(VALUES_T)

# Get values from entries then execute DisplayTube()
def SaveTube():
    VALUES_T = hallo(entries2)
    DisplayTube(VALUES_T)

# Display geometrical tube in drawing
def DisplayTube(VALUES_T):
    canvas2.delete('all')

    Tube_Text = open("Parameters\\param_rocket\\Tube.txt", "w")
    for i in range(len(VALUES_T)):
        Tube_Text.write("%2.f\n" % (VALUES_T[i]))
    Tube_Text.close()

    Len_Tube = VALUES_T[0]
    LENGTH[1] = Len_Tube
    Dia_Tube = VALUES_T[1]
    DIAMETER[1] = Dia_Tube
    DispData()

    canvas2.configure(width=VALUES_T[0]/3, height=VALUES_T[1]/3, bg='white', highlightthickness=0, bd=0, relief='ridge')  # 2010 mm
    canvas2.create_rectangle(1, 0, VALUES_T[0]/3-1, VALUES_T[1]/3-1, width=1, outline='blue')
    canvas2.grid(row=3, column=2, in_=canvas0)

# Displays canvas in which are the fins's parameters
def DispFins():
    Fins_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC1.grid_remove()
    canvasAC2.grid_remove()
    canvasAC4.grid_remove()
    canvasAC5.grid_remove()
    canvasAC3.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical Eiger fins in drawing
def EigerFins():
    EP = open('Parameters\\param_rocket\\EigerFins.txt', 'r')
    EP1=EP.readlines()
    VALUES_F = []
    for line in EP1:  # taking each line
        conv_int = float(line)
        VALUES_F.append(conv_int)
    DisplayFins(VALUES_F)

# Get values from entries then execute DisplayFins()
def SaveFins():
    VALUES_F = hallo(entries3)
    DisplayFins(VALUES_F)

# Display geometrical fins in drawing
def DisplayFins(VALUES_F):
    canvas3.delete('all')

    Fins_Text = open("Parameters\\param_rocket\\Fins.txt", "w")
    for i in range(len(VALUES_F)):
        Fins_Text.write("%2.f\n" % (VALUES_F[i]))
    Fins_Text.close()

    Len_Fins = VALUES_F[9]
    LENGTH[2] = Len_Fins
    Dia_Fins = VALUES_F[10]
    DIAMETER[2] = Dia_Fins
    DispData()

    if VALUES_F[0] == 3:
        canvas3.configure(width=VALUES_F[9]/3, height=VALUES_F[10]/3+2*VALUES_F[3]/3, bg='white', highlightthickness=0,
                           bd=0, relief='ridge')  # 350 mm
        canvas3.create_rectangle(1, VALUES_F[3]/3, VALUES_F[9]/3-1, VALUES_F[3]/3+VALUES_F[10]/3-1, width=1, outline='blue')
        canvas3.create_polygon(VALUES_F[7]/3, VALUES_F[3]/3+2/3*VALUES_F[10]/3, VALUES_F[1]/3+VALUES_F[7]/3-1,
                               VALUES_F[3]/3+2/3*VALUES_F[10]/3, VALUES_F[2]/3+VALUES_F[4]/3+VALUES_F[7]/3, 2/3*VALUES_F[10]/3+5/3*VALUES_F[3]/3-1,
                               VALUES_F[4]/3+VALUES_F[7]/3, 2/3*VALUES_F[10]/3+5/3*VALUES_F[3]/3-1, width=1, outline='blue', fill='')
        canvas3.create_polygon(VALUES_F[7]/3, VALUES_F[3]/3-3, VALUES_F[1]/3+VALUES_F[7]/3-1, VALUES_F[3]/3-3,
                               VALUES_F[2]/3+VALUES_F[4]/3+VALUES_F[7]/3, 0, VALUES_F[4]/3+VALUES_F[7]/3, 0, width=1, outline='blue', fill='')
        canvas3.grid(row=3, column=4, in_=canvas0)

# Displays canvas in which are the boat-tail's parameters
def DispBoatTail():
    BoatTail_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC1.grid_remove()
    canvasAC2.grid_remove()
    canvasAC3.grid_remove()
    canvasAC5.grid_remove()
    canvasAC4.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Display geometrical Eiger nosecone in drawing
def EigerBoatTail():
    EP = open('Parameters\\param_rocket\\EigerBoatTail.txt', 'r')
    EP1=EP.readlines()
    VALUES_BT = []
    for line in EP1:  # taking each line
        conv_int = float(line)
        VALUES_BT.append(conv_int)
    DisplayBoatTail(VALUES_BT)

# Get values from entries then execute DisplayBoatTail()
def SaveBoatTail():
    VALUES_BT = hallo(entries4)
    DisplayBoatTail(VALUES_BT)

# Display geometrical boat-tail in drawing
def DisplayBoatTail(VALUES_BT):
    canvas4.delete('all')

    BoatTail_Text = open("Parameters\\param_rocket\\BoatTail.txt", "w")
    for i in range(len(VALUES_BT)):
        BoatTail_Text.write("%2.f\n" % (VALUES_BT[i]))
    BoatTail_Text.close()

    Len_BoatTail = VALUES_BT[0]
    LENGTH[3] = Len_BoatTail
    Dia_BoatTail = VALUES_BT[1]
    DIAMETER[3] = Dia_BoatTail
    DispData()

    canvas4.configure(width=VALUES_BT[0]/3, height=VALUES_BT[1]/3, bg='white', highlightthickness=0, bd=0,
                       relief='ridge')  # 50 mm
    canvas4.create_polygon(1, 1, VALUES_BT[0]/3 - 1, (VALUES_BT[1]/3-VALUES_BT[2]/3)/2, VALUES_BT[0]/3 - 1,
                            (VALUES_BT[1]/3+VALUES_BT[2]/3)/2, 1, VALUES_BT[1]/3 - 1, width=1, outline='blue', fill='')
    canvas4.grid(row=3, column=8, ipadx=70, in_=canvas0)

# Get motor type
def AT_L850():
    AT_L850_Text = open("param_motor\\Motor.txt", "w")
    AT_L850_Text.write("AT_L850")
    AT_L850_Text.close()

def Cesaroni_M1800():
    Cesaroni_M1800_Text = open("param_motor\\Motor.txt", "w")
    Cesaroni_M1800_Text.write("Cesaroni_M1800")
    Cesaroni_M1800_Text.close()

# Displays canvas in which are the environment's parameters
def DispEnvironment():
    env_choice.configure(state=ACTIVE, activebackground='dodgerblue')
    canvasAC1.grid_remove()
    canvasAC2.grid_remove()
    canvasAC3.grid_remove()
    canvasAC4.grid_remove()
    canvasAC5.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAC)

# Get values from entries then run GetEnvironment()
def CernierEnv():
    EP = open('Parameters\\param_env\\Cernier.txt', 'r')
    EP1=EP.readlines()
    VALUES_E = []
    for line in EP1:  # taking each line
        conv_int = float(line)
        VALUES_E.append(conv_int)
    GetEnvironment(VALUES_E)

# Get values from entries then execute GetEnvironment()
def SaveEnvironment():
    VALUES_E = hallo(entries5)
    GetEnvironment(VALUES_E)

# Save environment parameters
def GetEnvironment(VALUES_E):
    DispData()
    Env_Text = open("Parameters\\param_env\\Env.txt", "w")
    for i in range(len(VALUES_E)):
        Env_Text.write("%2.f\n" % (VALUES_E[i]))
    Env_Text.close()

# Displays Data
def DispData():

    # Name, Mass, Length, Max Diameter
    Name = 'Eiger'
    Mass = 3832
    Length = sum(LENGTH)
    Max_Diameter = max(DIAMETER)

    canvas6.delete('all')
    canvas6.configure(width=250, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvas6.create_text(125, 20, text='%s \nLength %.2f mm, max.diameter %.2f mm \nMass with motors %.2f g' % (Name,
                             Length, Max_Diameter, Mass), fill='black', font='Arial 8 italic', justify='left')
    canvas6.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky='nw', in_=canvas0)

    # Stability, Centre de masse, Centre de pression, nombre de Mach
    Stability = 2.28
    CG = 114
    CP = 137
    Mach = 0.30

    canvas7.delete('all')
    canvas7.configure(width=100, height=50, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvas7.create_text(50, 25, text='Stability : %s cal \nCG : %d cm \nCP %d cm \nat M=%d' % (Stability, CG, CP, Mach),
                        fill='black', font='Arial 8 italic', justify='left')
    canvas7.grid(row=0, column=6, columnspan=3, padx=10, pady=10, sticky='ne', in_=canvas0)

    # Apogee, Max velocity, Max acceleration, Nombre de Mach
    Apogee = 3040
    max_v = 107
    max_a = 49.8
    Mach_v = 0.32

    canvas8.delete('all')
    canvas8.configure(width=200, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvas8.create_text(100, 20, text='Apogee : %d m \nMax. velocity : %d m.s-1   (Mach %d) \nMax. acceleration : %d m.s-2'
                                      % (Apogee, max_v, Mach_v, max_a), font='Arial 8 italic', fill='blue', justify='left')
    canvas8.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky='nw', in_=canvas0)

def Launch_Simulator1D():
    if __name__ == '__main__':
        NoseCone = open('Parameters\\param_rocket\\NoseCone.txt', 'r')
        NoseCone1 = NoseCone.readlines()
        VAL_N = []
        for line in NoseCone1:  # taking each line
            conv_int = int(line)
            VAL_N.append(conv_int)

        Tube = open('Parameters\\param_rocket\\Tube.txt', 'r')
        Tube1 = Tube.readlines()
        VAL_T = []
        for line in Tube1:  # taking each line
            conv_int = int(line)
            VAL_T.append(conv_int)

        Fins = open('Parameters\\param_rocket\\Fins.txt', 'r')
        Fins1 = Fins.readlines()
        VAL_F = []
        for line in Fins1:  # taking each line
            conv_int = int(line)
            VAL_F.append(conv_int)

        BoatTail = open('Parameters\\param_rocket\\BoatTail.txt', 'r')
        BoatTail1 = BoatTail.readlines()
        VAL_BT = []
        for line in BoatTail1:  # taking each line
            conv_int = float(line)
            VAL_BT.append(conv_int)

        Motor = open('Parameters\\param_motor\\Motor.txt', 'r')
        Motor1 = Motor.readlines()

        Env = open('Parameters\\param_env\\Env.txt', 'r')
        Env1 = Env.readlines()
        VAL_E = []
        for line in Env1:  # taking each line
            conv_int = float(line)
            VAL_E.append(conv_int)

        # Rocket definition
        gland = Body('tangent ogive', [0, VAL_N[1]*10**(-3)], [0, (VAL_N[0])*10**(-3)])

        tubes_francais = Body("cylinder", [VAL_N[1]*10**(-3), VAL_BT[1]*10**(-3), VAL_BT[2]*10**(-3)],
                                          [0, (VAL_T[0]+VAL_F[9])*10**(-3), (VAL_T[0]+VAL_F[9]+VAL_BT[0])*10**(-3)])

        M3_cone = Stage('Matterhorn III nosecone', gland, 1.26, 0.338, np.array([[VAL_N[2], VAL_N[3], VAL_N[4]],
                                                                                 [VAL_N[5], VAL_N[6], VAL_N[7]],
                                                                                 [VAL_N[8], VAL_N[9], VAL_N[10]]]))

        M3_body = Stage('Matterhorn III body', tubes_francais, 9.6, 0.930, np.array([[VAL_T[2], VAL_T[3], VAL_T[4]],
                                                                                     [VAL_T[5], VAL_T[6], VAL_T[7]],
                                                                                     [VAL_T[8], VAL_T[9], VAL_T[10]]]))

        finDefData = {'number': VAL_F[0],
                      'root_chord': VAL_F[1]*10**(-3),
                      'tip_chord': VAL_F[2]*10**(-3),
                      'span': VAL_F[3]*10**(-3),
                      'sweep': VAL_F[4]*10**(-3),
                      'thickness': VAL_F[5]*10**(-3),
                      'phase': VAL_F[6],
                      'body_top_offset': (VAL_T[0]+VAL_F[7])*10**(-3),
                      'total_mass': VAL_F[8]*10**(-3)}

        M3_body.add_fins(finDefData)

        M3_body.add_motor('Motors/%s.eng' % (Motor1[0]))

        Matterhorn_III = Rocket()

        Matterhorn_III.add_stage(M3_cone)
        Matterhorn_III.add_stage(M3_body)

        # Bla
        US_Atmos = stdAtmosUS(VAL_E[0], VAL_E[1], VAL_E[2], VAL_E[3])
        print(VAL_E[0], VAL_E[1], VAL_E[2], VAL_E[3])

        # Sim
        Simulator1D(Matterhorn_III, US_Atmos).get_integration(101, 30)

    # Current simulation yields an apogee of 2031.86 m whereas Matlab 1D yields 2022.99 m
    return


# Ouvre une fenetre with title and icon
fenetre = Tk()
fenetre.geometry("640x480")
fenetre.grid()
fenetre.title('Simulator EPFL_Rocket')
fenetre.call('wm', 'iconphoto', fenetre._w, PhotoImage(file='Parameters\ERT_logo.png'))
fenetre.configure(bg="light goldenrod yellow")

fenetre.rowconfigure(0, weight=1)
fenetre.rowconfigure(1, weight=50)  #give a weight more important to the second row
fenetre.columnconfigure(0, weight=1)

# Menu
menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Create", command=fenetre)
menu1.add_command(label="Edit")
menu1.add_separator()
menu1.add_command(label="Quit", command=fenetre.quit)
menubar.add_cascade(label="File", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Cut")
menu2.add_command(label="Copy")
menu2.add_command(label="Paste")
menubar.add_cascade(label="Edit", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Launch")
menubar.add_cascade(label="Analyse", menu=menu3)

menu4 = Menu(menubar, tearoff=0)
menu4.add_command(label="Launch")
menubar.add_cascade(label="Help", menu=menu4)

fenetre.config(menu=menubar)

# First row in window
canvasA = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
#canvasA.grid_propagate('False')
canvasA.grid(row=0, column=0, sticky='nswe')

# Arborescence, Left part of first row
canvasAA = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
canvasAA.grid(row=0, column=0, sticky='nswe', in_=canvasA)

# Add new part, Center part of first row
canvasAB = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
canvasAB.grid(row=0, column=1, sticky='nswe', in_=canvasA)

# Parameters, Right part of first row
canvasAC = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
canvasAC.grid(row=0, column=2, sticky='nswe', in_=canvasA)

# Fins parameters
canvasAC1 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')

# Nosecone parameters
canvasAC2 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')
# vbar2 = Scrollbar(canvasAC2, orient=VERTICAL)
# vbar2.grid(row=0, column=3, rowspan=10, sticky='ns', in_=canvasAC2)
# vbar2.config(command=canvasAC2.yview)
# canvasAC.configure(yscrollcommand=vbar2.set)

# Tube parameters
canvasAC3 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')
# vbar3 = Scrollbar(canvasAC3, orient=VERTICAL)
# vbar3.grid(row=0, column=3, rowspan=10, sticky='ns', in_=canvasAC3)
# vbar3.config(command=canvasAC3.yview)
# canvasAC.configure(yscrollcommand=vbar3.set)

# Boat-Tail parameters
canvasAC4 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')

# Environment parameters
canvasAC5 = Canvas(fenetre, bg='gray85', highlightthickness=0, bd=0, relief='flat')

# Choose NoseCone
Inertia=Label(canvasAC1, text='Inertia Matrix of Nosecone', bg='gray85', fg='blue')
Inertia.grid(row=0, column=0, columnspan=3, padx=10, pady=2, in_=canvasAC1)

Len_Nose = 0
entries1 = []
EntryButton(canvasAC1, 'Length', 7, 0, entries1)
EntryButton(canvasAC1, 'Diameter', 7, 1, entries1)
EntryButton(canvasAC1, '1', 1, 0, entries1)
EntryButton(canvasAC1, '2', 1, 1, entries1)
EntryButton(canvasAC1, '3', 1, 2, entries1)
EntryButton(canvasAC1, '4', 3, 0, entries1)
EntryButton(canvasAC1, '5', 3, 1, entries1)
EntryButton(canvasAC1, '6', 3, 2, entries1)
EntryButton(canvasAC1, '7', 5, 0, entries1)
EntryButton(canvasAC1, '8', 5, 1, entries1)
EntryButton(canvasAC1, '9', 5, 2, entries1)

DispN = Button(fenetre, text='Displays', command=lambda: SaveNose())
DispN.grid(row=9, column=2, sticky='se', padx=10, pady=10, in_=canvasAC1)

NoseCone_choice = Menubutton(fenetre, text='Nosecone', bg='white', fg='black', cursor='hand2', relief=RAISED)
NoseCone_choice.grid()
NoseCone_choice.menu = Menu(NoseCone_choice, tearoff=0)
NoseCone_choice["menu"] = NoseCone_choice.menu

nose = StringVar()
NoseCone_choice.menu.add_radiobutton(label='Eiger', variable=nose, value='Eiger NoseCone',
                                command=lambda: EigerNoseCone())
NoseCone_choice.menu.add_separator()
NoseCone_choice.menu.add_radiobutton(label='Personalize', variable=nose, command=lambda: DispNoseCone())
NoseCone_choice.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky='nswe', in_=canvasAB)

# Choose Tube
InertiaTube=Label(canvasAC2, text='Inertia Matrix of Tube', bg='gray85', fg='blue')
InertiaTube.grid(row=0, column=0, columnspan=3, padx=10, pady=2, in_=canvasAC2)

entries2 = []
EntryButton(canvasAC2, 'Length', 7, 0, entries2)
EntryButton(canvasAC2, 'Diameter', 7, 1, entries2)
EntryButton(canvasAC2, '1', 1, 0, entries2)
EntryButton(canvasAC2, '2', 1, 1, entries2)
EntryButton(canvasAC2, '3', 1, 2, entries2)
EntryButton(canvasAC2, '4', 3, 0, entries2)
EntryButton(canvasAC2, '5', 3, 1, entries2)
EntryButton(canvasAC2, '6', 3, 2, entries2)
EntryButton(canvasAC2, '7', 5, 0, entries2)
EntryButton(canvasAC2, '8', 5, 1, entries2)
EntryButton(canvasAC2, '9', 5, 2, entries2)

DispT = Button(fenetre, text='Displays', command=lambda: SaveTube())
DispT.grid(row=9, column=2, sticky='se', padx=10, pady=10, in_=canvasAC2)

Tube_choice = Menubutton(fenetre, text='Tube', bg='white', fg='black', cursor='hand2', relief=RAISED)
Tube_choice.grid()
Tube_choice.menu = Menu(Tube_choice, tearoff=0)
Tube_choice["menu"] = Tube_choice.menu

tube = StringVar()
Tube_choice.menu.add_radiobutton(label='Eiger', variable=tube, value='Eiger Tube',
                                command=lambda: EigerTube())
Tube_choice.menu.add_separator()
Tube_choice.menu.add_radiobutton(label='Personalize', variable=tube, command=lambda: DispTube())
Tube_choice.grid(row=0, column=1, padx=10, pady=10, ipadx=25, ipady=10, sticky='nswe', in_=canvasAB)

# Choose Fins
entries3 = []
EntryButton(canvasAC3, 'Number', 0, 0, entries3)
EntryButton(canvasAC3, 'Root chord', 0, 1, entries3)
EntryButton(canvasAC3, 'Tip chord', 0, 2, entries3)
EntryButton(canvasAC3, 'Span', 2, 0, entries3)
EntryButton(canvasAC3, 'Sweep', 2, 1, entries3)
EntryButton(canvasAC3, 'Thickness', 2, 2, entries3)
EntryButton(canvasAC3, 'Phase', 4, 0, entries3)
EntryButton(canvasAC3, 'Body top offset', 4, 1, entries3)
EntryButton(canvasAC3, 'Total mass', 4, 2, entries3)
EntryButton(canvasAC3, 'Lengtgh', 6, 0, entries3)
EntryButton(canvasAC3, 'Diameter', 6, 1, entries3)

DispF = Button(fenetre, text='Displays', command=lambda: SaveFins())
DispF.grid(row=8, column=2, sticky='se', padx=10, pady=10, in_=canvasAC3)

Fins_choice = Menubutton(fenetre, text='Fins', bg='white', fg='black', cursor='hand2', relief=RAISED)
Fins_choice.grid()
Fins_choice.menu = Menu(Fins_choice, tearoff=0)
Fins_choice["menu"] = Fins_choice.menu

fins = StringVar()
Fins_choice.menu.add_radiobutton(label='Eiger', variable=fins, value='Eiger Fins',
                                command=lambda: EigerFins())
Fins_choice.menu.add_separator()
Fins_choice.menu.add_radiobutton(label='Personalize', variable=fins, command=lambda: DispFins())
Fins_choice.grid(row=0, column=2, padx=10, pady=10, ipadx=27, ipady=10, sticky='nswe', in_=canvasAB)

# Choose BoatTail
entries4 = []
EntryButton(canvasAC4, 'Length', 0, 0, entries4)
EntryButton(canvasAC4, 'First Diameter', 0, 1, entries4)
EntryButton(canvasAC4, 'Second Diameter', 0, 2, entries4)

DispBT = Button(fenetre, text='Displays', command=lambda: SaveBoatTail())
DispBT.grid(row=2, column=2, sticky='se', padx=10, pady=10, in_=canvasAC4)

BoatTail_choice = Menubutton(fenetre, text='Boat-Tail', bg='white', fg='black', cursor='hand2', relief=RAISED)
BoatTail_choice.grid()
BoatTail_choice.menu = Menu(BoatTail_choice, tearoff=0)
BoatTail_choice["menu"] = BoatTail_choice.menu

bt = StringVar()
BoatTail_choice.menu.add_radiobutton(label='Eiger', variable=bt, value='Eiger BoatTail',
                                command=lambda: EigerBoatTail())
BoatTail_choice.menu.add_separator()
BoatTail_choice.menu.add_radiobutton(label='Personalize', variable=bt, command=lambda: DispBoatTail())
BoatTail_choice.grid(row=1, column=0, padx=10, pady=10, ipadx=15, ipady=10, sticky='nswe', in_=canvasAB)

# Choose motor
motor_choice = Menubutton(fenetre, text='Motor', bg='white', fg='black', cursor='hand2', relief=RAISED)
motor_choice.grid()
motor_choice.menu = Menu(motor_choice, tearoff=0)
motor_choice["menu"] = motor_choice.menu

mtr = StringVar()
motor_choice.menu.add_radiobutton(label='AT_L850', value='AT_L850', variable=mtr, command=lambda: AT_L850())
motor_choice.menu.add_radiobutton(label='Cesaroni_M1800', value='Cesaroni_M1800', variable=mtr, command=lambda:
    Cesaroni_M1800())

motor_choice.grid(row=1, column=1, padx=10, pady=10, ipadx=20, ipady=10, sticky='nswe', in_=canvasAB)

# Choose Environment
env_choice = Menubutton(fenetre, text="Environment", bg='white', fg='black', cursor='hand2', relief='raised')
env_choice.grid()
env_choice.menu = Menu(env_choice, tearoff=0)
env_choice["menu"] = env_choice.menu

env = StringVar()
env_choice.menu.add_radiobutton(label='Cernier', variable=env, value='Cernier environment',
                                command=lambda: CernierEnv())
# env_choice.menu.add_radiobutton(label='Zurich', variable=env, value='Zurich environment',
#                                 command=lambda: TextLabel('environment ', 'Zurich '))
# env_choice.menu.add_radiobutton(label='Mexico', variable=env, value='Mexico environment',
#                                 command=lambda: TextLabel('environment ', 'Mexico '))
env_choice.menu.add_separator()
env_choice.menu.add_radiobutton(label='Personalize', variable=env, command=lambda: DispEnvironment())
env_choice.grid(row=1, column=2, padx=10, pady=10, ipadx=2, ipady=10, sticky='nswe', in_=canvasAB)

entries5 = []
EntryButton(canvasAC5, 'Altitude', 0, 0, entries5)
EntryButton(canvasAC5, 'Temperature', 0, 1, entries5)
EntryButton(canvasAC5, 'Pressure', 0, 2, entries5)
EntryButton(canvasAC5, 'Humidity', 2, 0, entries5)

DispE = Button(fenetre, text='Save', command=lambda: SaveEnvironment())
DispE.grid(row=4, column=2, sticky='se', padx=10, pady=10, in_=canvasAC5)

# Design rocket, Second row of window
# scale : 1 pixel <-> 3 millimeters
# length : 3010 mm
# diameter : 155.6 mm
canvasB = Canvas(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
canvasB.grid(row=1, column=0, sticky='nswe')
canvasB.rowconfigure(0, weight=1)
canvasB.columnconfigure(0, weight=1)

# Quite superficial
canvas0 = Canvas(fenetre, bg='white')
canvas0.grid(row=0, column=0, sticky='nsew', padx=10, pady=10, in_=canvasB)
canvas0.rowconfigure(0, weight=1)
canvas0.rowconfigure(1, weight=5)
canvas0.rowconfigure(2, weight=1)
canvas0.rowconfigure(3, weight=5)
canvas0.rowconfigure(4, weight=1)

# Scrollbar
hbar=Scrollbar(canvasB, orient=HORIZONTAL)
hbar.grid(row=1, column=0, sticky='ew', in_=canvasB)
hbar.config(command=canvas0.xview)
vbar=Scrollbar(canvasB, orient=VERTICAL)
vbar.grid(row=0, column=1, sticky='ns', in_=canvasB)
vbar.config(command=canvas0.yview)
canvas0.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

# Draw rocket
canvas1 = Canvas(fenetre)
canvas2 = Canvas(fenetre)
canvas3 = Canvas(fenetre)
canvas4 = Canvas(fenetre)

# Update data
canvas6 = Canvas(fenetre)
canvas7 = Canvas(fenetre)
canvas8 = Canvas(fenetre)
canvasX = Canvas(fenetre)
# canvasY = Canvas(fenetre, width=830, height=20, bg='white', highlightthickness=0, bd=0, relief='ridge')
# canvasY.grid(row=0, column=1, columnspan=3, sticky='nsew', in_=canvas0)

# Launch simulation
simu_button = Button(fenetre, text='Launch simulation', bg='red', fg='white', cursor='hand2', relief=RAISED, command=lambda: Launch_Simulator1D())
simu_button.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', in_=canvasAA)

# Bouton de sortie
# stop = Button(fenetre, text="x", bg='RED', fg='white', command=fenetre.quit)
# stop.grid(row=1, column=1, sticky='nswe', in_=canvasB)

# Disp window
fenetre.mainloop()