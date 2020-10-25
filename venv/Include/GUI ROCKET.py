# GUI
# Author : Henri Faure
# Last update : 21 May 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import string
from Simulator1D import Simulator1D
from Functions.stdAtmosUS import stdAtmosUS
from Rocket.Body import Body
from Rocket.Rocket import Rocket
from Rocket.Stage import Stage
import os


# Ouvre une fenetre with title and icon
fenetre = Tk()
fenetre.geometry("1280x980")
fenetre.grid()
fenetre.title('Simulator EPFL Rocket')
fenetre.call('wm', 'iconphoto', fenetre._w, PhotoImage(file="Parameters/ERT_logo.png"))
fenetre.configure(bg="light goldenrod yellow")

fenetre.rowconfigure(0, weight=1)  # first row is used to module the rocket, saving chosen parameters
fenetre.rowconfigure(1, weight=3)  # give a weight 3 times more important to the second row, used to draw rocket
fenetre.columnconfigure(0, weight=1)
# Add scrollbar to frame
def Add_Scrollbar(frameL, canvas, vbar, frameN):
    frameL.grid()
    frameL.rowconfigure(0, weight=1)
    frameL.columnconfigure(0, weight=1)
    frameL.grid_propagate('False')
    canvas.configure(bg='gray85', highlightthickness=0, bd=0, relief='flat')
    vbar.configure(orient='vertical', command=canvas.yview)
    vbar.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vbar.set)
    canvas.grid(row=0, column=0, sticky='nswe')
    canvas.columnconfigure(0, weight=1)
    canvas.create_window((0, 0), window=frameN, anchor='nw')
    frameL.grid_remove()


# Configure scrollregion of canvas
def ScrollReg(canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))


# TODO: Change scale (current scale is 1mm ~ 3 pixels)
def UpdateScale():
    return


# TODO: Modify the tree's branch selected to change parameters
def change():
    selected = tree.focus()
    stage = get_stage()
    substage = get_substage()

    #case ogive selected
    if selected[1] == "t":
        if selected[2] == 'n':
            NoseCone = open('Parameters/param_rocket/NoseCone.txt', 'r')  # Read text file
            NoseCone1 = NoseCone.readlines()
            VAL_N = []
            for line in NoseCone1:  # taking each line
                VAL_N.append(float(line))
            OpenNoseParams(fenetre, VAL_N, disp=0)

        # case tube selected
        elif selected[2] == 't':
            Tube = open('Parameters/param_rocket/Tube.txt', 'r')  # Read text file
            Tube1 = Tube.readlines()
            VAL_N = []
            for line in Tube1:  # taking each line
                VAL_N.append(float(line))
            OpenTubeParams(fenetre, VAL_N, disp=0)

        # case fins selected
        elif selected[2] == 'f':
            Fins = open('Parameters/param_rocket/Fins.txt', 'r')  # Read text file
            Fins1 = Fins.readlines()
            VAL_N = []
            for line in Fins1:  # taking each line
                VAL_N.append(float(line))
            OpenFinsParams(fenetre, VAL_N, disp=0)

        # case BT selected
        elif selected[2] == 'b':
            BT = open('Parameters/param_rocket/BoatTail.txt', 'r')  # Read text file
            BT1 = BT.readlines()
            VAL_N = []
            for line in BT1:  # taking each line
                VAL_N.append(float(line))
            OpenBoatTailParams(fenetre, VAL_N, disp=0)

    elif selected[1] == "s":
        piece = bodyParts[stage][substage][0]
        if piece == 'n':
            p = 'Nose'
        elif piece == 't':
            p = 'Tube'
        elif piece == 'f':
            p = 'Fins'
        elif piece == 'b':
            p = 'BT'

        if selected[2] == 'p':
            Parachute = open('Parameters/param_rocket/Parachute'+p+'.txt', 'r')  # Read text file
            Parachute1 = Parachute.readlines()
            VAL_P = []
            for line in Parachute1:  # taking each line
                VAL_P.append(float(line))
            OpenParachuteParams(fenetre, VAL_P, disp=0)

        elif selected[2] == 'w':
            Weight = open('Parameters/param_rocket/Weight'+p+'.txt', 'r')  # Read text file
            Weight1 = Weight.readlines()
            VAL_W = []
            for line in Weight1:  # taking each line
                VAL_W.append(float(line))
            OpenWeightParams(fenetre, VAL_W, disp=0)

        elif selected[2] == 'c':
            InnerTube = open('Parameters/param_rocket/InnerTube'+p+'.txt', 'r')  # Read text file
            InnerTube1 = InnerTube.readlines()
            VAL_IT = []
            for line in InnerTube1:  # taking each line
                VAL_IT.append(float(line))
            OpenInnerTubeParams(fenetre, VAL_IT, disp=0)

## Add a stage
# Make an array of Frame Geometry to memorize each stage's frame
FrameGeometry = []
item = -1

# Make an array of Canvas Geometry to memorize each substage's canvas
CanvasGeometry = []

# Vector which retains position of frame in FrameGeometry
PosF = []
incF = -1

# Array of items B
ITEMB=[]

bodyParts=[]

# MATRIX of position canvas
PosC = []
IncC = []

# Alphabet
alpha0 = list(string.ascii_lowercase)
inc0 = -1

# Colors
colors = ["blue", "red", "green", "black", "yellow"]

# Add a stage to the tree view
def Add_Stage():
    # Insert tree's branch to the rocket
    # Create a frame by stage in which canvas are then created for different rocket's parts
    def addstage():
        global item, ITEMB, FrameGeometry, PosF, incF, PosCN, IncC, alpha0, inc0  # global allows to update variables out of the function
        incF += 1
        posF = incF
        PosF.append(posF)

        PosCN = []
        PosC.append(PosCN)
        incCN = -1
        IncC.append(incCN)

        itemBN = -1
        ITEMB.append(itemBN)

        bodyParts.append([])

        inc0 += 1

        item += 1

        # Create frame and attribute to the n-ième frame, name 'frame02n'
        frame02idx = Frame(frame02, name='frame02%s%d' % (alpha0[inc0], item), bg='white',
                           highlightthickness=0, bd=0, relief='flat')
        FrameGeometry.append(frame02idx)
        FrameStage(frame02idx)


    def FrameStage(frame02idx):
        global item, FrameGeometry, alpha0, inc0
        branch = tree.insert(NameRocket, 'end', 'id%s%d' % (alpha0[inc0], item), text='%s' % (StageName.get()))
        tree.focus(branch)
        tree.selection_set(branch)
        tree.see(branch)
        UpdateButtonState()
        elem = tree.focus()
        if elem[1] == 'd' or elem[1] == 't':
            stage = elem[-1]
        UpdateBodyPartState(int(stage))
        StageName.destroy()
        Save.destroy()

        frame02idx.grid(row=0, column=item)
        frame02idx.rowconfigure(0, weight=1)

    def UpdateSaveButton(entry):
        if entry.get():
            addstage()

    def enter(b):
        Save.invoke()

    StageName = Entry(frameAAAB, validate='key')  # Enter the name of the new stage
    StageName.grid(row=1, column=0, sticky='nswe')
    StageName.focus()
    StageName.bind('<Return>', enter)
    Save = Button(frameAAAB, text='Save', command=lambda: UpdateSaveButton(StageName))  # Button 'Save' launches addstage()
    Save.grid(row=1, column=1, sticky='nswe')

    CanvasGeometry.append([])


# Get the tree's item selected (used to attach part rocket the selected stage)
def Selected_Stage():
    StageItem = tree.selection()
    return StageItem


## Add a substage
# Alphabet
alpha = list(string.ascii_lowercase)
inc = -1

# Add a subbranch in treeview
def Add_Substage(StageSelected, subpart, canvasN, Stg, frame_idx, name):
    # Add a canvasN (N as Number) to draw Nosecone for N=1, Tube N=2, Fins N=3, Boat-Tail N=4
    def CanvasSubstage(canvasN, Stg, frame_idx):
        global CanvasGeometry, inc, ITEMB
        # Create canvas, named canvas-N-itemA-Stg
        # N design type rocket's part, itemA numbers canvas, Stg references it to his frame parent
        canvasidx = Canvas(frame_idx, name='%s%s%d%d' % (canvasN, alpha[inc], ITEMB[Stg], Stg))
        CanvasGeometry[Stg].append(canvasidx)


    global ITEMB, alpha, inc, PosC, IncC
    IncC[Stg] += 1
    posC = IncC[Stg]
    PosC[Stg].append(posC)
    ITEMB[Stg] += 1
    bodyParts[tree.index(tree.focus())].append([name])
    print(bodyParts)
    inc += 1
    br = tree.insert(StageSelected, 'end', 'it%s%s%d%d' % (name, alpha[inc], ITEMB[Stg], Stg), text=subpart)
    tree.see(br)


    CanvasSubstage(canvasN, Stg, frame_idx)
    print(CanvasGeometry)
    UpdateBodyPartState(get_stage())

# Add a subbranch in treeview
def Add_SubSubstage(StageSelected, subpart, canvasN, Stg, frame_idx, name, pos):


    global ITEMB, alpha, inc, PosC, IncC

    bodyParts[tree.index(tree.parent(tree.focus()))][pos].append(name)
    l = tree.focus()[2]
    print(bodyParts)
    inc += 1
    br = tree.insert(StageSelected, 'end', 'is%s%s%d%d' % (name, alpha[inc], ITEMB[Stg], Stg), text=subpart)
    tree.see(br)
    tree.selection_set(br)
    tree.focus(br)
    UpdateBodyPartState(get_stage())

## Remodulate treeview and rocket (remove, move up, move down, change)
# Remove the tree's branch
def do_remove():
    global FrameGeometry, CanvasGeometry, ITEMB, PosF, incF, PosC, IncC, item
    sel = tree.focus()
    part = sel[2]
    place = int(tree.index(sel))
    stage = get_stage()
    substage = get_substage()

    if sel:
        parent_id = tree.parent(sel)
        tree.delete(sel)
        tree.selection_set(parent_id)
        tree.focus(parent_id)



    value1 = int(sel[-1])  # Stage number
    prefix1 = sel[1] # 'd' -> frame / 't' -> canvas
    prefix3 = sel[-2]  # letter which makes each frame unique

    # if prefix1 == 'd' indicates that the selected tree's item is a stage
    if prefix1 == 'd':
        del bodyParts[stage]
        item -= 1
        for i, frame in enumerate(FrameGeometry):
            Val2 = []
            for val2 in str(frame):
                Val2.append(val2)
            value2 = int(Val2[-1])
            letter2 = str(Val2[-2])

            if (value2 == value1) and (letter2 == prefix3):
                incF -= 1
                IncC[value1] = -1
                ITEMB[value1] = -1

                FrameGeometry[value1].destroy()


                pos1 = PosF[value1]
                for f, posf in enumerate(PosF):
                    PosF[value2] = -1
                    if posf > pos1:
                        PosF[f] -= 1
                        #FrameGeometry[f].grid(row=0, column=PosF[f])

                for c, posc in enumerate(PosC[value1]):
                    PosC[value1][c] = -1



    # if prefix1 == 't' indicates that the selected tree's item is a substage
    if prefix1 == 't':
        del bodyParts[stage][place]

        if part == 'n':
            num = '1'
        elif part == 't':
            num = '2'
        elif part == 'f':
            num = '3'
        elif part == 'b':
            num = '4'

        for j, canvas in enumerate(CanvasGeometry[value1]):
            Val3 = []
            for val3 in str(canvas):
                Val3.append(val3)
            if Val3[-4] == num:
                can = j

        CanvasGeometry[value1][can].destroy()
        del CanvasGeometry[value1][can]
        ITEMB[value1] -= 1

        for i in range(len(CanvasGeometry[value1])):
            tmp2 = []
            for l in str(CanvasGeometry[value1][i]):
                tmp2.append(l)
            piece = tmp2[-4]
            if piece == str(1):
                letter = 'n'
            elif piece == str(2):
                letter = 't'
            elif piece == str(3):
                letter = 'f'
            elif piece == str(4):
                letter = 'b'

            idx = 0
            for k, part in enumerate(bodyParts[stage]):
                if part[0] == letter:
                    idx = k

            CanvasGeometry[value1][i].grid(row=0, column=idx)

    if prefix1 == 's':
        del bodyParts[stage][substage][place+1]
        DrawFullPiece()
        #TODO: Remove subsub parts from canvas

    UpdateBodyPartState(stage)
    UpdateButtonState()


# Move the tree's branch up
def do_move_up():
    global FrameGeometry, CanvasGeometry, ITEMB, PosF, incF, PosC, IncC
    sel = tree.selection()
    stage = get_stage()
    if sel:
        for s in sel:
            idx = tree.index(s)
            if idx != 0:
                tree.move(s, tree.parent(s), idx-1)

    id = str(sel[0])
    Val1 = []
    for val1 in id:
        Val1.append(val1)
    value1 = int(Val1[-1])  # Stage number
    prefix1 = str(Val1[1])  # 'd' -> frame / 't' -> canvas
    prefix3 = str(Val1[-2])  # letter which makes each frame unique
    prefix4 = str(Val1[-3])  # letter which makes each canvas unique

    if idx != 0:
        if prefix1 == 'd':
            bodyParts[tree.index(sel)], bodyParts[tree.index(sel)+1] = bodyParts[tree.index(sel)+1], bodyParts[tree.index(sel)]
            for i, frame in enumerate(FrameGeometry):
                Val2 = []
                for val2 in str(frame):
                    Val2.append(val2)
                value2 = int(Val2[-1])
                letter2 = str(Val2[-2])

                if (value2 == value1) and (letter2 == prefix3):
                    FrameGeometry[value1].grid(row=0, column=PosF[value1]-1)
                    FrameGeometry[np.where(np.array(PosF) == PosF[value1]-1)[0][0]].grid(row=0, column=PosF[value1])

                    PosF[np.where(np.array(PosF) == PosF[value1]-1)[0][0]] += 1
                    PosF[value1] -= 1

        elif prefix1 == 't':
            for j, canvas in enumerate(CanvasGeometry[value1]):
                Val3 = []
                for val3 in str(canvas):
                    Val3.append(val3)

                value2 = int(Val3[-1]) # stage num
                value3 = int(Val3[-2]) # itemB
                letter3 = str(Val3[-3])

                if (value2 == value1) and (letter3 == prefix4):
                    #CanvasGeometry[value1][tree.index(sel)].grid(row=0, column=PosC[value1][value3]-1)
                    #CanvasGeometry[value1][np.where(np.array(PosC[value1]) == PosC[value1][value3] - 1)[0][0]].grid(row=0, column=PosC[value1][value3])
                    #CanvasGeometry[value1][tree.index(sel)-1].grid(row=0, column=PosC[value1][tree.index(sel)])


                    tmp = bodyParts[stage][tree.index(sel)+1]
                    bodyParts[stage][tree.index(sel)+1] = bodyParts[stage][tree.index(sel)]
                    bodyParts[stage][tree.index(sel)] = tmp

                    for i in range(len(CanvasGeometry[value1])):
                        tmp2 = []
                        for l in str(CanvasGeometry[value1][i]):
                            tmp2.append(l)

                        letter = ''
                        piece = tmp2[-4]
                        if piece == str(1):
                            letter = 'n'
                        elif piece == str(2):
                            letter = 't'
                        elif piece == str(3):
                            letter = 'f'
                        elif piece == str(4):
                            letter = 'b'
                        else:
                            continue

                        idx = 0
                        for k, part in enumerate(bodyParts[stage]):
                            if part[0] == letter:
                                idx = k

                        CanvasGeometry[value1][i].grid(row=0, column=idx)

                    PosC[value1][value3-1] += 1
                    #PosC[value1][np.where(np.array(PosC[value1]) == PosC[value1][value3] - 1)[0][0]] += 1
                    PosC[value1][value3] -= 1
        UpdateBodyPartState(stage)
        UpdateButtonState()

# Move the tree's branch down
# Move the tree's branch up; refer to do_move_dow() (very similar)
def do_move_down():
    global FrameGeometry, CanvasGeometry, ITEMB, PosF, incF, PosC, IncC
    sel = tree.selection()
    stage = get_stage()
    if tree.next(sel):
        if sel:
            for s in sel:
                idx = tree.index(s)
                tree.move(s, tree.parent(s), idx+1)

        id = str(sel[0])
        Val1 = []
        for val1 in id:
            Val1.append(val1)
        value1 = int(Val1[-1])  # Stage number
        prefix1 = str(Val1[1])  # 'd' -> frame
        prefix3 = str(Val1[-2])  # letter which makes each frame unique
        prefix4 = str(Val1[-3])  # letter which makes each canvas unique

        if prefix1 == 'd':
            for i, frame in enumerate(FrameGeometry):
                Val2 = []
                for val2 in str(frame):
                    Val2.append(val2)
                value2 = int(Val2[-1])
                letter2 = str(Val2[-2])

                if (value2 == value1) and (letter2 == prefix3):
                    FrameGeometry[value1].grid(row=0, column=PosF[value1]+1)
                    FrameGeometry[np.where(np.array(PosF) == PosF[value1]+1)[0][0]].grid(row=0, column=PosF[value1])

                    PosF[np.where(np.array(PosF) == PosF[value2]+1)[0][0]] -= 1
                    PosF[value1] += 1

        elif prefix1 == 't':
            for j, canvas in enumerate(CanvasGeometry[value1]):
                Val3 = []
                for val3 in str(canvas):
                    Val3.append(val3)
                value2 = int(Val3[-1])
                value3 = int(Val3[-2])
                letter3 = str(Val3[-3])

                if (value2 == value1) and (letter3 == prefix4):

                    tmp = bodyParts[stage][tree.index(sel)]
                    bodyParts[stage][tree.index(sel)] = bodyParts[stage][tree.index(sel)-1]
                    bodyParts[stage][tree.index(sel)-1] = tmp

                    for i in range(len(bodyParts[stage])):
                        tmp2 = []
                        for l in str(CanvasGeometry[value1][i]):
                            tmp2.append(l)

                        letter = ''
                        piece = tmp2[-4]
                        if piece == str(1):
                            letter = 'n'
                        elif piece == str(2):
                            letter = 't'
                        elif piece == str(3):
                            letter = 'f'
                        elif piece == str(4):
                            letter = 'b'
                        else:
                            continue

                        idx = 0
                        for k, part in enumerate(bodyParts[stage]):
                            if str(part[0]) == letter:
                                idx = k

                        CanvasGeometry[value1][i].grid(row=0, column=idx)

                    PosC[value1][value3 - 1] += 1
                    # PosC[value1][np.where(np.array(PosC[value1]) == PosC[value1][value3] - 1)[0][0]] += 1
                    PosC[value1][value3] -= 1
        UpdateBodyPartState(stage)
        UpdateButtonState()

# Function which permits to entry rocket's parameters manually
def EntryButton(frameACN, name, rnum, cnum, entries, val=0):
    # Check all values are mathematical values
    def TestFunction(value):
        if value in '0123456789-+*/.()':
            return True
        else:
            return False


    Label(frameACN, text='%s' % name, bg='gray85', anchor=NW).grid(row=rnum, column=cnum, padx=10, pady=2)
    entry = Entry(frameACN, validate='key', validatecommand=(frameACN.register(TestFunction), '%S'))
    entry.insert(0, 0)
    entry.grid(row=rnum + 1, column=cnum, padx=10, pady=10)
    entries.append(entry)

def get_stage():
    selected = tree.focus()
    if selected[1] == 'd':
        stage = tree.index(tree.focus())
        return stage
    elif selected[1] == 't':
        parent = tree.parent(selected)
        if parent[1] == 'd':
            stage = tree.index(parent)
            return stage
    elif selected[1] == 's':
        parent=tree.parent(tree.parent(selected))
        stage = tree.index(parent)
        return stage

def get_substage():
    selected = tree.focus()
    print(selected)
    if selected[1] == 'd':
        stage = len(tree.get_children(selected))-1
        return stage
    elif selected[1] == 't':
        stage = tree.index(selected)
        return stage
    elif selected[1] == 's':
        parent=tree.parent(selected)
        stage = tree.index(parent)
        return stage


# Function wich get values from entries (entries references all rocket part parameters)
def hallo(entries):
    Array_Value = []
    for entry in entries:
        Array_Value = np.append(Array_Value, eval(entry.get()))
    return Array_Value


# Display geometrical nosecone in drawing
LENGTH = [0, 0, 0, 0, 0, 0, 0]
DIAMETER = [0, 0, 0, 0, 0, 0, 0]

# Display geometrical Eiger nosecone in drawing
def EigerNoseCone():
    frameACA.grid_remove()

    # a file EigerNose.txt is already created with parameters pre-selected
    EP = open('Parameters/param_rocket/EigerNose.txt', 'r')
    EP1 = EP.readlines()
    VALUES_N = []
    for line in EP1:  # taking each line
        conv_float = float(line)
        VALUES_N.append(conv_float)
    DrawNose(VALUES_N, display=1)

# Display geometrical Eiger tube in drawing
def EigerTube():
    EP = open('Parameters/param_rocket/EigerTube.txt', 'r')
    EP1 = EP.readlines()
    VALUES_T = []
    for line in EP1:  # taking each line
        conv_float = float(line)
        VALUES_T.append(conv_float)
    DrawTube(VALUES_T, display=1)

# Display geometrical Eiger fins in drawing
def EigerFins():
    EP = open('Parameters/param_rocket/EigerFins.txt', 'r')
    EP1 = EP.readlines()
    VALUES_F = []
    for i, line in enumerate(EP1):  # taking each line
        if i == 0:
            conv_int = int(line)
            VALUES_F.append(conv_int)
        else:
            conv_float = float(line)
            VALUES_F.append(conv_float)

    DrawFins(VALUES_F, display=1)

# Display geometrical Eiger nosecone in drawing
def EigerBoatTail():
    EP = open('Parameters/param_rocket/EigerBoatTail.txt', 'r')
    EP1 = EP.readlines()
    VALUES_BT = []
    for line in EP1:  # taking each line
        conv_float = float(line)
        VALUES_BT.append(conv_float)
    DrawBoatTail(VALUES_BT, display=1)

## MOTOR
# Get motor type
def AT_L850():
    AT_L850_Text = open("Parameters/param_motor/Motor.txt", "w")
    AT_L850_Text.write("AT_L850")
    AT_L850_Text.close()


def Cesaroni_M1800():
    Cesaroni_M1800_Text = open("Parameters/param_motor/Motor.txt", "w")
    Cesaroni_M1800_Text.write("Cesaroni_M1800")
    Cesaroni_M1800_Text.close()


# Get values from entries then run GetEnvironment()
def MexicoEnv():
    EP = open('Parameters/param_env/Mexico.txt', 'r')
    EP1 = EP.readlines()
    VALUES_E = []
    for line in EP1:  # taking each line
        conv_float = float(line)
        VALUES_E.append(conv_float)
    GetEnvironment(VALUES_E)

# Get values from entries then execute GetEnvironment()
def SaveEnvironment(entries):
    VALUES_E = hallo(entries)
    GetEnvironment(VALUES_E)


# Save environment parameters
def GetEnvironment(VALUES_E):
    DispData()
    Env_Text = open("Parameters/param_env/Env.txt", "w")
    for i in range(len(VALUES_E)):
        Env_Text.write("%s\n" % (VALUES_E[i]))
    Env_Text.close()


## DATAs
# Displays Data
def DispData():
    # Name, Mass, Length, Max Diameter
    Name = 'Eiger'
    Mass = 8796
    Length = sum(LENGTH)
    Max_Diameter = max(DIAMETER)

    canvas6.delete('all')
    canvas6.configure(width=250, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvas6.create_text(125, 20, text='%s \nLength %.2f mm, max.diameter %.2f mm \nMass with motors %.2f g' % (Name,
                                                                                                               Length,
                                                                                                               Max_Diameter,
                                                                                                               Mass),
                        fill='black', font='Arial 8 italic', justify='left')
    canvas6.pack(side='left', anchor='nw')

    # Stability, Centre de masse, Centre de pression, nombre de Mach
    Stability = 2.28
    CG = 1927
    CP = 2300
    Mach = 0.30

    canvas7.delete('all')
    canvas7.configure(width=100, height=50, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvas7.create_text(50, 25, text='Stability : %s cal \nCG : %d cm \nCP %d cm \nat M=%d' % (Stability, CG, CP, Mach),
                        fill='black', font='Arial 8 italic', justify='left')
    canvas7.pack(side='right', anchor='ne')

    # Apogee, Max velocity, Max acceleration, Nombre de Mach
    Apogee = 3048
    max_v = 207
    max_a = 89.8
    Mach_v = 0.82

    canvas8.delete('all')
    canvas8.configure(width=200, height=40, bg='white', highlightthickness=0, bd=0, relief='ridge')
    canvas8.create_text(100, 20,
                        text='Apogee : %d m \nMax. velocity : %d m.s-1   (Mach %d) \nMax. acceleration : %d m.s-2'
                             % (Apogee, max_v, Mach_v, max_a), font='Arial 8 italic', fill='blue', justify='left')
    canvas8.pack(side='left', anchor='sw')


## Launch Simulator1D.py
def Launch_Simulator1D():
    if __name__ == '__main__':
        NoseCone = open('Parameters/param_rocket/NoseCone.txt', 'r')  # Read text file
        NoseCone1 = NoseCone.readlines()
        VAL_N = []
        for line in NoseCone1:  # taking each line
            conv_float = float(line)
            VAL_N.append(conv_float)

        Tube = open('Parameters/param_rocket/Tube.txt', 'r')
        Tube1 = Tube.readlines()
        VAL_T = []
        for line in Tube1:  # taking each line
            conv_float = float(line)
            VAL_T.append(conv_float)

        Fins = open('Parameters/param_rocket/Fins.txt', 'r')
        Fins1 = Fins.readlines()
        VAL_F = []
        for i, line in enumerate(Fins1):  # taking each line
            if i == 0:
                conv_int = int(float(line))
                VAL_F.append(conv_int)
            else:
                conv_float = float(line)
                VAL_F.append(conv_float)

        BoatTail = open('Parameters/param_rocket/BoatTail.txt', 'r')
        BoatTail1 = BoatTail.readlines()
        VAL_BT = []
        for line in BoatTail1:  # taking each line
            conv_float = float(line)
            VAL_BT.append(conv_float)

        Motor = open('Parameters/param_motor/Motor.txt', 'r')
        Motor1 = Motor.readlines()

        Env = open('Parameters/param_env/Env.txt', 'r')
        Env1 = Env.readlines()
        VAL_E = []
        for line in Env1:  # taking each line
            conv_float = float(line)
            VAL_E.append(conv_float)

        # Rocket definition
        gland = Body('tangent ogive', [0, VAL_N[1] * 10 ** (-3)], [0, (VAL_N[0]) * 10 ** (-3)])

        tubes_francais = Body("cylinder", [VAL_N[1] * 10 ** (-3), VAL_BT[1] * 10 ** (-3), VAL_BT[2] * 10 ** (-3)],
                              [0, (VAL_T[0] + VAL_F[9]) * 10 ** (-3), (VAL_T[0] + VAL_F[9] + VAL_BT[0]) * 10 ** (-3)])

        M3_cone = Stage('Matterhorn III nosecone', gland, 1.26, 0.338, np.array([[VAL_N[2], VAL_N[3], VAL_N[4]],
                                                                                 [VAL_N[5], VAL_N[6], VAL_N[7]],
                                                                                 [VAL_N[8], VAL_N[9], VAL_N[10]]]))

        M3_body = Stage('Matterhorn III body', tubes_francais, 9.6, 0.930, np.array([[VAL_T[2], VAL_T[3], VAL_T[4]],
                                                                                     [VAL_T[5], VAL_T[6], VAL_T[7]],
                                                                                     [VAL_T[8], VAL_T[9], VAL_T[10]]]))

        finDefData = {'number': VAL_F[0],
                      'root_chord': VAL_F[1] * 10 ** (-3),
                      'tip_chord': VAL_F[2] * 10 ** (-3),
                      'span': VAL_F[3] * 10 ** (-3),
                      'sweep': VAL_F[4] * 10 ** (-3),
                      'thickness': VAL_F[5] * 10 ** (-3),
                      'phase': VAL_F[6],
                      'body_top_offset': (VAL_T[0] + VAL_F[7]) * 10 ** (-3),
                      'total_mass': VAL_F[8] * 10 ** (-3)}

        M3_body.add_fins(finDefData)

        M3_body.add_motor('Motors/%s.eng' % (Motor1[0]))

        Matterhorn_III = Rocket()

        Matterhorn_III.add_stage(M3_cone)
        Matterhorn_III.add_stage(M3_body)

        # Bla
        US_Atmos = stdAtmosUS(VAL_E[0], VAL_E[1], VAL_E[2], VAL_E[3])

        # Sim
        Simulator1D(Matterhorn_III, US_Atmos).get_integration(101, 30)

        # DispData()

    # Current simulation yields an apogee of 2031.86 m whereas Matlab 1D yields 2022.99 m
    return

def DrawN(VALUES_N, canvas):
    print(VALUES_N[2])
    canvas.configure(width=VALUES_N[0] / 3, height=VALUES_N[1] / 3, bg='white', highlightthickness=0, bd=0,
                      relief='ridge')  # 300 mm + 350 mm
    canvas.create_arc(2 / 3 * (1 - VALUES_N[1] / 3), 3.3 * VALUES_N[1] / 3, 4.1 * VALUES_N[1] / 3, -1, width=1,
                       outline=colors[int(VALUES_N[2])], style=ARC, start=90, extent=90)
    canvas.create_arc(2 / 3 * (1 - VALUES_N[1] / 3), VALUES_N[1] / 3, 4.1 * VALUES_N[1] / 3 + 3,
                       -2.3 * VALUES_N[1] / 3, width=1, outline=colors[int(VALUES_N[2])], style=ARC, start=-90, extent=-90)
    canvas.create_line(7 / 5 * VALUES_N[1] / 3, 0, VALUES_N[0] / 3 - 1, 0, width=1, fill=colors[int(VALUES_N[2])])
    canvas.create_line(7 / 5 * VALUES_N[1] / 3, VALUES_N[1] / 3 - 1, VALUES_N[0] / 3 - 1, VALUES_N[1] / 3 - 1, width=1,
                        fill=colors[int(VALUES_N[2])])
    canvas.create_line(VALUES_N[0] / 3 - 1, 0, VALUES_N[0] / 3 - 1, VALUES_N[1] / 3 - 1, width=1, fill=colors[int(VALUES_N[2])])


def DrawNose(VALUES_N, display=0):
    # Get the index 'stg' of stage : example, first stage has an index stg = 0
    Stg = int(tree.focus()[-1])
    stage = get_stage()

    if display:
        # Get frame parent of canvas
        frame02idx = FrameGeometry[Stg]

        # Get Canvas in frame02idx
        Add_Substage(tree.selection(), 'Ogive', 'canvas1', Stg, frame02idx, 'n')

    # Write folder Parameters a file NoseCone.txt which parameters selected by the user
    NoseCone_Text = open('Parameters/param_rocket/NoseCone.txt', "w")
    for i in range(len(VALUES_N)):
        NoseCone_Text.write("%s\n" % (VALUES_N[i]))
    NoseCone_Text.close()

    idx = 0
    for i in range(len(bodyParts[stage])):
        tmp2 = []
        for l in str(CanvasGeometry[Stg][i]):
            tmp2.append(l)
        if int(tmp2[-4]) == 1:
            idx = i


    LENGTH[0] = VALUES_N[0]
    DIAMETER[0] = VALUES_N[1]
    DispData()

    canvas1 = CanvasGeometry[Stg][idx]

    DrawFullPiece()

    for i, substage in enumerate(bodyParts[stage]):
        if substage[0] == 'n':
            tmp = i
            break

    canvas1.grid(row=0, column=tmp)


def OpenNoseParams(fenetre, values=[600, 155,0,0,0,0,0,0,0,0,0,0], disp=1):

    noseParam = Toplevel(fenetre)
    noseParam.title("NoseCone Parameters")
    noseParam.geometry("400x200")
    Title = Label(noseParam, text = "Change params")
    Title.pack()

    notebook = ttk.Notebook(noseParam)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Dimensions")
    notebook.pack(expand=1, fill="both")

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Inertia")
    notebook.pack(expand=1, fill="both")

    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Personalize")
    notebook.pack(expand=1, fill="both")

    color=values[2]

    def slide(var):
        lengthEntry.delete(0, "end")
        lengthEntry.insert(0,str(lengthScale.get()))
        DrawNose([lengthScale.get(), DiaScale.get(), color,inertia1.get(),inertia2.get(),inertia3.get(),inertia4.get(),
                 inertia5.get(),inertia6.get(),inertia7.get(),inertia8.get(),inertia9.get()])

    def insertVal(var):
        lengthScale.set(lengthEntry.get())

    def slide1(var):
        DiaEntry.delete(0, "end")
        DiaEntry.insert(0,str(DiaScale.get()))
        DrawNose([lengthScale.get(), DiaScale.get(), color,inertia1.get(),inertia2.get(),inertia3.get(),inertia4.get(),
                 inertia5.get(),inertia6.get(),inertia7.get(),inertia8.get(),inertia9.get()])

    def insertVal1(var):
        DiaScale.set(DiaEntry.get())

    def Ok():
        color = colors.index(clicked.get())
        DrawNose([lengthScale.get(), DiaScale.get(), color, inertia1.get(),inertia2.get(),inertia3.get(),inertia4.get(),
                 inertia5.get(),inertia6.get(),inertia7.get(),inertia8.get(),inertia9.get()])

    lengthLabel = Label(tab1, text="Length: ")
    lengthLabel.grid(row=1, column=0)
    lengthEntry = Entry(tab1)
    lengthEntry.grid(row=1, column=1, pady=5)
    lengthEntry.insert(0, values[0])
    lengthEntry.bind("<Return>", insertVal)
    lengthScale = Scale(tab1, from_=0, to=1000, orient=HORIZONTAL, command=slide, showvalue=0)
    lengthScale.grid(row=1, column=2)
    lengthScale.set(values[0])

    DiaLabel = Label(tab1, text="Diameter: ")
    DiaLabel.grid(row=2, column=0)
    DiaEntry = Entry(tab1)
    DiaEntry.grid(row=2, column=1, pady=10)
    DiaEntry.insert(0, values[1])
    DiaEntry.bind("<Return>", insertVal1)
    DiaScale = Scale(tab1, from_=0, to=300, orient=HORIZONTAL, command=slide1, showvalue=0)
    DiaScale.grid(row=2, column=2)
    DiaScale.set(values[1])

    inertia0 = Label(tab2, text="Inertial Matrix: ")
    inertia0.grid(row=1, column=0)
    print(values)

    inertia1 = Entry(tab2, width=4, justify=CENTER); inertia1.grid(row=0, column=1, pady = 2, padx=2); inertia1.insert(0,values[3])
    inertia2 = Entry(tab2, width=4, justify=CENTER); inertia2.grid(row=0, column=2, pady = 2, padx=2); inertia2.insert(0,values[4])
    inertia3 = Entry(tab2, width=4, justify=CENTER); inertia3.grid(row=0, column=3, pady = 2, padx=2); inertia3.insert(0,values[5])
    inertia4 = Entry(tab2, width=4, justify=CENTER); inertia4.grid(row=1, column=1, pady = 2, padx=2); inertia4.insert(0,values[6])
    inertia5 = Entry(tab2, width=4, justify=CENTER); inertia5.grid(row=1, column=2, pady = 2, padx=2); inertia5.insert(0,values[7])
    inertia6 = Entry(tab2, width=4, justify=CENTER); inertia6.grid(row=1, column=3, pady = 2, padx=2); inertia6.insert(0,values[8])
    inertia7 = Entry(tab2, width=4, justify=CENTER); inertia7.grid(row=2, column=1, pady = 2, padx=2); inertia7.insert(0,values[9])
    inertia8 = Entry(tab2, width=4, justify=CENTER); inertia8.grid(row=2, column=2, pady = 2, padx=2); inertia8.insert(0,values[10])
    inertia9 = Entry(tab2, width=4, justify=CENTER); inertia9.grid(row=2, column=3, pady = 2, padx=2); inertia9.insert(0,values[11])

    ColorLabel = Label(tab3, text="Color: ")
    ColorLabel.grid(row=0, column=0)
    clicked = StringVar()
    clicked.set(colors[int(color)])
    ColorMenu = OptionMenu(tab3, clicked,"blue", "red", "green", "black", "yellow")
    ColorMenu.grid(row=0, column=1)
    Button(tab3, text="Ok", command=Ok).grid(row=0, column=2)

    if disp:
        DrawNose([lengthScale.get(), DiaScale.get(), color,inertia1.get(),inertia2.get(),inertia3.get(),inertia4.get(),
                 inertia5.get(),inertia6.get(),inertia7.get(),inertia8.get(),inertia9.get()], display=1)

    def validCB():
        DrawNose([lengthScale.get(), DiaScale.get(), colors.index(clicked.get()), inertia1.get(), inertia2.get(), inertia3.get(), inertia4.get(),
             inertia5.get(), inertia6.get(), inertia7.get(), inertia8.get(), inertia9.get()])
        noseParam.destroy()
        noseParam.update()

    validateButton = Button(noseParam, text="OK", command=validCB)
    validateButton.pack(anchor="e", padx=10, pady=5)
    #validateButton.grid(row=3, column=2)
    noseParam.mainloop()

def DrawT(VALUES_T, canvas):
    canvas.configure(width=VALUES_T[0] / 3, height=VALUES_T[1] / 3, bg='white', highlightthickness=0, bd=0,
                      relief='ridge')  # 2010 mm

    canvas.create_rectangle(1, 0, VALUES_T[0] / 3 - 1, VALUES_T[1] / 3 - 1, width=1, outline=colors[int(VALUES_T[2])])



# Display geometrical tube in drawing
def DrawTube(VALUES_T, display=0):
    # Get the index 'stg' of stage : example, first stage has an index stg = 0
    Stg = int(tree.focus()[-1])
    stage = get_stage()

    if display:
        frame02idx = FrameGeometry[Stg]

        # Get Canvas in frame02idx
        Add_Substage(tree.selection(), 'Tube', 'canvas2', Stg, frame02idx, 't')

    Tube_Text = open("Parameters/param_rocket/Tube.txt", "w")
    for i in range(len(VALUES_T)):
        Tube_Text.write("%s\n" % (VALUES_T[i]))
    Tube_Text.close()

    idx = 0
    for i in range(len(CanvasGeometry[Stg])):
        tmp2 = []
        for l in str(CanvasGeometry[Stg][i]):
            tmp2.append(l)
        if int(tmp2[-4]) == 2:
            idx = i

    canvas2 = CanvasGeometry[Stg][idx]

    Len_Tube = VALUES_T[0]
    LENGTH[1] = Len_Tube
    Dia_Tube = VALUES_T[1]
    DIAMETER[1] = Dia_Tube
    DispData()

    DrawFullPiece()

    for i, substage in enumerate(bodyParts[stage]):
        if substage[0] == 't':
            tmp = i
            break

    canvas2.grid(row=0, column=tmp)

def OpenTubeParams(fenetre, values=[2038, 155, 0, 0,0,0,0,0,0,0,0,0], disp=1):

    tubeParam = Toplevel(fenetre)
    tubeParam.title("Tube Parameters")
    tubeParam.geometry("400x200")
    Title = Label(tubeParam, text = "Change tube params")
    Title.pack()

    notebook = ttk.Notebook(tubeParam)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Dimensions")
    notebook.pack(expand=1, fill="both")

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Inertia")
    notebook.pack(expand=1, fill="both")

    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Personalize")
    notebook.pack(expand=1, fill="both")

    color = values[2]


    def slide(var):
        lengthEntry.delete(0, "end")
        lengthEntry.insert(0,str(lengthScale.get()))
        DrawTube([lengthScale.get(), DiaScale.get(), colors.index(clicked.get()), inertia1.get(), inertia2.get(),
                  inertia3.get(), inertia4.get()
                     , inertia5.get(), inertia6.get(), inertia7.get(), inertia8.get(), inertia9.get()])

    def insertVal(var):
        lengthScale.set(lengthEntry.get())

    def slide1(var):
        DiaEntry.delete(0, "end")
        DiaEntry.insert(0,str(DiaScale.get()))
        DrawTube([lengthScale.get(), DiaScale.get(), colors.index(clicked.get()), inertia1.get(), inertia2.get(),
                  inertia3.get(), inertia4.get()
                     , inertia5.get(), inertia6.get(), inertia7.get(), inertia8.get(), inertia9.get()])

    def insertVal1(var):
        DiaScale.set(DiaEntry.get())

    def Ok():
        color = colors.index(clicked.get())
        DrawTube([lengthScale.get(), DiaScale.get(), color, inertia1.get(),inertia2.get(),inertia3.get(),inertia4.get(),
                 inertia5.get(),inertia6.get(),inertia7.get(),inertia8.get(),inertia9.get()])


    lengthLabel = Label(tab1, text="Length: ")
    lengthLabel.grid(row=1, column=0)
    lengthEntry = Entry(tab1)
    lengthEntry.grid(row=1, column=1)
    lengthEntry.insert(0, values[0])
    lengthEntry.bind("<Return>", insertVal)
    lengthScale = Scale(tab1, from_=0, to=3000, orient=HORIZONTAL, command=slide)
    lengthScale.grid(row=1, column=2)
    lengthScale.set(values[0])

    DiaLabel = Label(tab1, text="Diameter: ")
    DiaLabel.grid(row=2, column=0)
    DiaEntry = Entry(tab1)
    DiaEntry.grid(row=2, column=1)
    DiaEntry.insert(0, values[1])
    DiaEntry.bind("<Return>", insertVal1)
    DiaScale = Scale(tab1, from_=0, to=300, orient=HORIZONTAL, command=slide1)
    DiaScale.grid(row=2, column=2)
    DiaScale.set(values[1])

    inertia1 = Entry(tab2, width=4, justify=CENTER);inertia1.grid(row=0, column=1, pady=2, padx=2)
    inertia1.insert(0, values[3])
    inertia2 = Entry(tab2, width=4, justify=CENTER);inertia2.grid(row=0, column=2, pady=2, padx=2)
    inertia2.insert(0, values[4])
    inertia3 = Entry(tab2, width=4, justify=CENTER);inertia3.grid(row=0, column=3, pady=2, padx=2)
    inertia3.insert(0, values[5])
    inertia4 = Entry(tab2, width=4, justify=CENTER);inertia4.grid(row=1, column=1, pady=2, padx=2)
    inertia4.insert(0, values[6])
    inertia5 = Entry(tab2, width=4, justify=CENTER);inertia5.grid(row=1, column=2, pady=2, padx=2)
    inertia5.insert(0, values[7])
    inertia6 = Entry(tab2, width=4, justify=CENTER);inertia6.grid(row=1, column=3, pady=2, padx=2)
    inertia6.insert(0, values[8])
    inertia7 = Entry(tab2, width=4, justify=CENTER);inertia7.grid(row=2, column=1, pady=2, padx=2)
    inertia7.insert(0, values[9])
    inertia8 = Entry(tab2, width=4, justify=CENTER);inertia8.grid(row=2, column=2, pady=2, padx=2)
    inertia8.insert(0, values[10])
    inertia9 = Entry(tab2, width=4, justify=CENTER);inertia9.grid(row=2, column=3, pady=2, padx=2)
    inertia9.insert(0, values[11])

    ColorLabel = Label(tab3, text="Color: ")
    ColorLabel.grid(row=0, column=0)
    clicked = StringVar()
    clicked.set(colors[int(color)])
    ColorMenu = OptionMenu(tab3, clicked, "blue", "red", "green", "black", "yellow")
    ColorMenu.grid(row=0, column=1)
    Button(tab3, text="Ok", command=Ok).grid(row=0, column=2)

    if disp:
        DrawTube([lengthScale.get(), DiaScale.get(), colors.index(clicked.get()), inertia1.get(), inertia2.get(), inertia3.get(), inertia4.get()
                        , inertia5.get(), inertia6.get(), inertia7.get(), inertia8.get(), inertia9.get()], display=1)

    def validCB():
        color = colors.index(clicked.get())
        DrawTube(
            [lengthScale.get(), DiaScale.get(), color, inertia1.get(), inertia2.get(), inertia3.get(), inertia4.get(),
             inertia5.get(), inertia6.get(), inertia7.get(), inertia8.get(), inertia9.get()])
        tubeParam.destroy()
        tubeParam.update()

    validateButton = Button(tubeParam, text="OK", command=validCB)
    validateButton.pack(anchor="e", padx=10, pady=5)
    tubeParam.mainloop()

def DrawF(VALUES_F, canvas):
    color = colors[int(VALUES_F[11])]
    if VALUES_F[0] == 3:
        canvas.configure(width=VALUES_F[9] / 3, height=VALUES_F[10] / 3 + 2 * VALUES_F[3] / 3, bg='white',
                          highlightthickness=0, bd=0, relief='ridge')  # 350 mm
        canvas.create_rectangle(1, VALUES_F[3] / 3, VALUES_F[9] / 3 - 1, VALUES_F[3] / 3 + VALUES_F[10] / 3 - 1,
                                 width=1, outline=color)
        canvas.create_polygon(VALUES_F[7] / 3, VALUES_F[3] / 3 + 2 / 3 * VALUES_F[10] / 3,
                               VALUES_F[1] / 3 + VALUES_F[7] / 3 - 1, VALUES_F[3] / 3 + 2 / 3 * VALUES_F[10] / 3,
                               VALUES_F[2] / 3 + VALUES_F[4] / 3 + VALUES_F[7] / 3,
                               2 / 3 * VALUES_F[10] / 3 + 5 / 3 * VALUES_F[3] / 3 - 1,
                               VALUES_F[4] / 3 + VALUES_F[7] / 3,
                               2 / 3 * VALUES_F[10] / 3 + 5 / 3 * VALUES_F[3] / 3 - 1, width=1, outline=color, fill='')
        canvas.create_polygon(VALUES_F[7] / 3, VALUES_F[3] / 3 - 3, VALUES_F[1] / 3 + VALUES_F[7] / 3 - 1,
                               VALUES_F[3] / 3 - 3, VALUES_F[2] / 3 + VALUES_F[4] / 3 + VALUES_F[7] / 3, 0,
                               VALUES_F[4] / 3 + VALUES_F[7] / 3, 0, width=1, outline=color, fill='')


# Display geometrical fins in drawing
def DrawFins(VALUES_F, display=0):
    # Get the index 'stg' of stage : example, first stage has an index stg = 0
    Stg = int(tree.focus()[-1])
    stage = get_stage()

    if display:
        frame02idx = FrameGeometry[Stg]

        # Get Canvas in frame02idx
        Add_Substage(tree.selection(), 'Fins', 'canvas3', Stg, frame02idx, 'f')

    Fins_Text = open("Parameters/param_rocket/Fins.txt", "w")
    for i in range(len(VALUES_F)):
        Fins_Text.write("%s\n" % (VALUES_F[i]))
    Fins_Text.close()

    idx = 0
    for i in range(len(bodyParts[stage])):
        tmp2 = []
        for l in str(CanvasGeometry[Stg][i]):
            tmp2.append(l)
        if int(tmp2[-4]) == 3:
            idx = i

    canvas3 = CanvasGeometry[Stg][idx]

    LENGTH[2] = VALUES_F[9]
    DIAMETER[2] = VALUES_F[10]
    DispData()

    DrawFullPiece()

    for i, substage in enumerate(bodyParts[stage]):
        if substage[0] == 'f':
            tmp = i
            break
    canvas3.grid(row=0, column=tmp)

def OpenFinsParams(fenetre, values=[3, 282, 123, 216, 115, 30, 0, 40, 300, 350, 155, 0], disp=1):

    FinParam = Toplevel(fenetre)
    FinParam.title("Fin Parameters")
    FinParam.geometry("400x600")
    Label(FinParam, text = "Change Fin params").pack()

    notebook = ttk.Notebook(FinParam)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Dimensions")
    notebook.pack(expand=1, fill="both")

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Personalize")
    notebook.pack(expand=1, fill="both")

    color = values[11]

    def slideLength(var):
        lengthEntry.delete(0, "end")
        lengthEntry.insert(0,str(lengthScale.get()))
        DrawFins([nbScale.get(),rcScale.get(),tcScale.get(),spanScale.get(),sweepScale.get(),ThScale.get(),
                 PhScale.get(),BTOScale.get(),MassScale.get(),lengthScale.get(),DiaScale.get(), color])

    def insertValLength(var):
        lengthScale.set(lengthEntry.get())

    def slideDia(var):
        DiaEntry.delete(0, "end")
        DiaEntry.insert(0,str(DiaScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValDia(var):
        DiaScale.set(DiaEntry.get())

    def slideNum(var):
        nbEntry.delete(0, "end")
        nbEntry.insert(0,str(nbScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValNum(var):
        nbScale.set(nbEntry.get())

    def slideRC(var):
        rcEntry.delete(0, "end")
        rcEntry.insert(0, str(rcScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValRC(var):
        rcScale.set(rcEntry.get())

    def slideTC(var):
        tcEntry.delete(0, "end")
        tcEntry.insert(0,str(tcScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValTC(var):
        tcScale.set(tcEntry.get())

    def slideSpan(var):
        spanEntry.delete(0, "end")
        spanEntry.insert(0,str(spanScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValSpan(var):
        spanScale.set(spanEntry.get())

    def slideSwp(var):
        sweepEntry.delete(0, "end")
        sweepEntry.insert(0,str(sweepScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValSwp(var):
        sweepScale.set(sweepEntry.get())

    def slideTh(var):
        ThEntry.delete(0, "end")
        ThEntry.insert(0,str(ThScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValTh(var):
        ThScale.set(ThEntry.get())

    def slideMass(var):
        MassEntry.delete(0, "end")
        MassEntry.insert(0,str(MassScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValMass(var):
        MassScale.set(MassEntry.get())

    def slideBTO(var):
        BTOEntry.delete(0, "end")
        BTOEntry.insert(0,str(BTOScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValBTO(var):
        BTOScale.set(BTOEntry.get())

    def slidePh(var):
        PhEntry.delete(0, "end")
        PhEntry.insert(0,str(PhScale.get()))
        DrawFins([nbScale.get(), rcScale.get(), tcScale.get(), spanScale.get(), sweepScale.get(), ThScale.get(),
                  PhScale.get(), BTOScale.get(), MassScale.get(), lengthScale.get(), DiaScale.get(), color])

    def insertValPh(var):
        PhScale.set(PhEntry.get())

    def Ok():
        color = colors.index(clicked.get())
        DrawFins([nbScale.get(),rcScale.get(),tcScale.get(),spanScale.get(),sweepScale.get(),ThScale.get(),
                 PhScale.get(),BTOScale.get(),MassScale.get(),lengthScale.get(),DiaScale.get(), color])

    nbLabel = Label(tab1, text="Num: ")
    nbLabel.grid(row=1, column=0)
    nbEntry = Entry(tab1)
    nbEntry.grid(row=1, column=1)
    nbEntry.insert(0, values[0])
    nbEntry.bind("<Return>", insertValNum)
    nbScale = Scale(tab1, from_=0, to=10, orient=HORIZONTAL, command=slideNum)
    nbScale.grid(row=1, column=2)
    nbScale.set(values[0])

    rcLabel = Label(tab1, text="Root coord: ")
    rcLabel.grid(row=2, column=0)
    rcEntry = Entry(tab1)
    rcEntry.grid(row=2, column=1)
    rcEntry.insert(0, values[1])
    rcEntry.bind("<Return>", insertValRC)
    rcScale = Scale(tab1, from_=0, to=500, orient=HORIZONTAL, command=slideRC)
    rcScale.grid(row=2, column=2)
    rcScale.set(values[1])

    tcLabel = Label(tab1, text="Tip coord: ")
    tcLabel.grid(row=3, column=0)
    tcEntry = Entry(tab1)
    tcEntry.grid(row=3, column=1)
    tcEntry.insert(0, values[2])
    tcEntry.bind("<Return>", insertValTC)
    tcScale = Scale(tab1, from_=0, to=300, orient=HORIZONTAL, command=slideTC)
    tcScale.grid(row=3, column=2)
    tcScale.set(values[2])

    spanLabel = Label(tab1, text="Span: ")
    spanLabel.grid(row=4, column=0)
    spanEntry = Entry(tab1)
    spanEntry.grid(row=4, column=1)
    spanEntry.insert(0, values[3])
    spanEntry.bind("<Return>", insertValSpan)
    spanScale = Scale(tab1, from_=0, to=500, orient=HORIZONTAL, command=slideSpan)
    spanScale.grid(row=4, column=2)
    spanScale.set(values[3])

    sweepLabel = Label(tab1, text="Sweep: ")
    sweepLabel.grid(row=5, column=0)
    sweepEntry = Entry(tab1)
    sweepEntry.grid(row=5, column=1)
    sweepEntry.insert(0, values[4])
    sweepEntry.bind("<Return>", insertValSwp)
    sweepScale = Scale(tab1, from_=0, to=300, orient=HORIZONTAL, command=slideSwp)
    sweepScale.grid(row=5, column=2)
    sweepScale.set(values[4])

    ThLabel = Label(tab1, text="Thickness: ")
    ThLabel.grid(row=6, column=0)
    ThEntry = Entry(tab1)
    ThEntry.grid(row=6, column=1)
    ThEntry.insert(0, values[5])
    ThEntry.bind("<Return>", insertValTh)
    ThScale = Scale(tab1, from_=0, to=50, orient=HORIZONTAL, command=slideTh)
    ThScale.grid(row=6, column=2)
    ThScale.set(values[5])

    PhLabel = Label(tab1, text="Phase: ")
    PhLabel.grid(row=7, column=0)
    PhEntry = Entry(tab1)
    PhEntry.grid(row=7, column=1)
    PhEntry.insert(0, values[6])
    PhEntry.bind("<Return>", insertValPh)
    PhScale = Scale(tab1, from_=0, to=360, orient=HORIZONTAL, command=slidePh)
    PhScale.grid(row=7, column=2)
    PhScale.set(values[6])

    BTOLabel = Label(tab1, text="Body Top Offset: ")
    BTOLabel.grid(row=8, column=0)
    BTOEntry = Entry(tab1)
    BTOEntry.grid(row=8, column=1)
    BTOEntry.insert(0, values[7])
    BTOEntry.bind("<Return>", insertValBTO)
    BTOScale = Scale(tab1, from_=0, to=200, orient=HORIZONTAL, command=slideBTO)
    BTOScale.grid(row=8, column=2)
    BTOScale.set(values[7])

    MassLabel = Label(tab1, text="Mass: ")
    MassLabel.grid(row=9, column=0)
    MassEntry = Entry(tab1)
    MassEntry.grid(row=9, column=1)
    MassEntry.insert(0, values[8])
    MassEntry.bind("<Return>", insertValMass)
    MassScale = Scale(tab1, from_=0, to=1000, orient=HORIZONTAL, command=slideMass)
    MassScale.grid(row=9, column=2)
    MassScale.set(values[8])

    lengthLabel = Label(tab1, text="Length: ")
    lengthLabel.grid(row=10, column=0)
    lengthEntry = Entry(tab1)
    lengthEntry.grid(row=10, column=1)
    lengthEntry.insert(0, values[9])
    lengthEntry.bind("<Return>", insertValLength)
    lengthScale = Scale(tab1, from_=0, to=1000, orient=HORIZONTAL, command=slideLength)
    lengthScale.grid(row=10, column=2)
    lengthScale.set(values[9])

    DiaLabel = Label(tab1, text="Diameter: ")
    DiaLabel.grid(row=11, column=0)
    DiaEntry = Entry(tab1)
    DiaEntry.grid(row=11, column=1)
    DiaEntry.insert(0, values[10])
    DiaEntry.bind("<Return>", insertValDia)
    DiaScale = Scale(tab1, from_=0, to=300, orient=HORIZONTAL, command=slideDia)
    DiaScale.grid(row=11, column=2)
    DiaScale.set(values[10])

    ColorLabel = Label(tab2, text="Color: ")
    ColorLabel.grid(row=0, column=0)
    clicked = StringVar()
    clicked.set(colors[int(color)])
    ColorMenu = OptionMenu(tab2, clicked, "blue", "red", "green", "black", "yellow")
    ColorMenu.grid(row=0, column=1)
    Button(tab2, text="Ok", command=Ok).grid(row=0, column=2)

    if disp:
        DrawFins([nbScale.get(),rcScale.get(),tcScale.get(),spanScale.get(),sweepScale.get(),ThScale.get(),
                 PhScale.get(),BTOScale.get(),MassScale.get(),lengthScale.get(),DiaScale.get(), color], display=1)

    def validCB():
        color = colors.index(clicked.get())
        DrawFins([nbScale.get(),rcScale.get(),tcScale.get(),spanScale.get(),sweepScale.get(),ThScale.get(),
                 PhScale.get(),BTOScale.get(),MassScale.get(),lengthScale.get(),DiaScale.get(), color])
        FinParam.destroy()
        FinParam.update()

    validateButton = Button(FinParam, text="OK", command=validCB)
    validateButton.pack(anchor="e", padx=10, pady=5)
    FinParam.mainloop()

def DrawBT(VALUES_BT, canvas):
    color = colors[int(VALUES_BT[-1])]
    canvas.configure(width=VALUES_BT[0] / 3, height=max(VALUES_BT[1], VALUES_BT[2]) / 3, bg='white',
                      highlightthickness=0, bd=0, relief='ridge')  # 50 mm
    if VALUES_BT[1] > VALUES_BT[2]:
        canvas.create_polygon(1, 0, VALUES_BT[0] / 3 - 1, (VALUES_BT[1] / 3 - VALUES_BT[2] / 3) / 2,
                               VALUES_BT[0] / 3 - 1, (VALUES_BT[1] / 3 + VALUES_BT[2] / 3) / 2 - 1, 1,
                               VALUES_BT[1] / 3 - 1, width=1, outline=color, fill='')
    else:
        canvas.create_polygon(1, (VALUES_BT[2] / 3 - VALUES_BT[1] / 3) / 2, VALUES_BT[0] / 3 - 1, 0,
                               VALUES_BT[0] / 3 - 1, VALUES_BT[2] / 3 - 1, 1,
                               (VALUES_BT[2] / 3 + VALUES_BT[1] / 3) / 2 - 1, width=1, outline=color, fill='')


# Display geometrical tube in drawing
def DrawBoatTail(VALUES_BT, display=0):

    Stg = int(tree.focus()[-1])
    stage = get_stage()

    if display:
        frame02idx = FrameGeometry[Stg]

        # Get Canvas in frame02idx
        Add_Substage(tree.selection(), 'Boat-Tail', 'canvas4', Stg, frame02idx, 'b')

    BoatTail_Text = open("Parameters/param_rocket/BoatTail.txt", "w")
    for i in range(len(VALUES_BT)):
        BoatTail_Text.write("%s\n" % (VALUES_BT[i]))
    BoatTail_Text.close()

    idx = 0
    for i in range(len(bodyParts[stage])):
        tmp2 = []
        for l in str(CanvasGeometry[Stg][i]):
            tmp2.append(l)
        if int(tmp2[-4]) == 4:
            idx = i

    canvas4 = CanvasGeometry[Stg][idx]

    LENGTH[3] = VALUES_BT[0]
    Dia_BoatTail = max(VALUES_BT[1], VALUES_BT[2])
    DIAMETER[3] = Dia_BoatTail
    DispData()

    DrawFullPiece()

    for i, substage in enumerate(bodyParts[stage]):
        if substage[0] == 'b':
            tmp = i
            break
    canvas4.grid(row=0, column=tmp)

def OpenBoatTailParams(fenetre, values=[41, 155, 133, 0], disp=1):

    BoatTailParam = Toplevel(fenetre)
    BoatTailParam.title("Boat Tail Parameters")
    BoatTailParam.geometry("400x200")
    Title = Label(BoatTailParam, text = "Change boat tail params")
    Title.pack()

    notebook = ttk.Notebook(BoatTailParam)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Dimensions")
    notebook.pack(expand=1, fill="both")

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Personalize")
    notebook.pack(expand=1, fill="both")

    color = values[-1]

    def slide(var):
        lengthEntry.delete(0, "end")
        lengthEntry.insert(0,str(lengthScale.get()))
        DrawBoatTail([lengthScale.get(), Dia1Scale.get(), Dia2Scale.get(), color])

    def insertVal(var):
        lengthScale.set(lengthEntry.get())

    def slide1(var):
        Dia1Entry.delete(0, "end")
        Dia1Entry.insert(0,str(Dia1Scale.get()))
        DrawBoatTail([lengthScale.get(), Dia1Scale.get(), Dia2Scale.get(), color])

    def insertVal1(var):
        Dia1Scale.set(Dia1Entry.get())

    def slide2(var):
        Dia2Entry.delete(0, "end")
        Dia2Entry.insert(0, str(Dia2Scale.get()))
        DrawBoatTail([lengthScale.get(), Dia1Scale.get(), Dia2Scale.get(), color])

    def insertVal2(var):
        Dia2Scale.set(Dia2Entry.get())

    def Ok():
        color = colors.index(clicked.get())
        DrawBoatTail([lengthScale.get(), Dia1Scale.get(), Dia2Scale.get(), color])


    lengthLabel = Label(tab1, text="Length: ")
    lengthLabel.grid(row=1, column=0)
    lengthEntry = Entry(tab1)
    lengthEntry.grid(row=1, column=1)
    lengthEntry.insert(0, values[0])
    lengthEntry.bind("<Return>", insertVal)
    lengthScale = Scale(tab1, from_=0, to=100, orient=HORIZONTAL, command=slide)
    lengthScale.grid(row=1, column=2)
    lengthScale.set(values[0])

    Dia1Label = Label(tab1, text="1st Diameter: ")
    Dia1Label.grid(row=2, column=0)
    Dia1Entry = Entry(tab1)
    Dia1Entry.grid(row=2, column=1)
    Dia1Entry.insert(0, values[1])
    Dia1Entry.bind("<Return>", insertVal1)
    Dia1Scale = Scale(tab1, from_=0, to=300, orient=HORIZONTAL, command=slide1)
    Dia1Scale.grid(row=2, column=2)
    Dia1Scale.set(values[1])

    Dia2Label = Label(tab1, text="2nd Diameter: ")
    Dia2Label.grid(row=3, column=0)
    Dia2Entry = Entry(tab1)
    Dia2Entry.grid(row=3, column=1)
    Dia2Entry.insert(0, values[2])
    Dia2Entry.bind("<Return>", insertVal2)
    Dia2Scale = Scale(tab1, from_=0, to=300, orient=HORIZONTAL, command=slide2)
    Dia2Scale.grid(row=3, column=2)
    Dia2Scale.set(values[2])

    ColorLabel = Label(tab2, text="Color: ")
    ColorLabel.grid(row=0, column=0)
    clicked = StringVar()
    clicked.set(colors[int(color)])
    ColorMenu = OptionMenu(tab2, clicked, "blue", "red", "green", "black", "yellow")
    ColorMenu.grid(row=0, column=1)
    Button(tab2, text="Ok", command=Ok).grid(row=0, column=2)

    if disp:
        DrawBoatTail([lengthScale.get(), Dia1Scale.get(), Dia1Scale.get(), color], display=1)

    def validCB():
        color = colors.index(clicked.get())
        DrawBoatTail([lengthScale.get(), Dia1Scale.get(), Dia2Scale.get(), color])
        BoatTailParam.destroy()
        BoatTailParam.update()

    validateButton = Button(BoatTailParam, text="OK", command=validCB)
    validateButton.pack(anchor="e", padx=10, pady=5)
    BoatTailParam.mainloop()

def OpenMotorParams():
    MotorParams = Toplevel(fenetre)
    MotorParams.title("Create Custom Motor")
    MotorParams.geometry("450x450")
    Title = Label(MotorParams, text="Change Motor params")
    Title.pack()

    notebook = ttk.Notebook(MotorParams)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Details")
    notebook.pack(expand=1, fill="both")

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Values")
    notebook.pack(expand=1, fill="both")

    label1 = Label(tab1, text="Name", bg='gray85', anchor=NW).grid(row=0, column=0, padx=10, pady=2)
    entry1 = Entry(tab1)
    entry1.grid(row=1, column=0, padx=10, pady=10)
    entry1.insert(0,"Name : ")

    label2 = Label(tab1, text="Diameter", bg='gray85', anchor=NW).grid(row=0, column=1, padx=10, pady=2)
    entry2 = Entry(tab1)
    entry2.grid(row=1, column=1, padx=10, pady=10)
    entry2.insert(0, 0)

    label3 = Label(tab1, text="Length", bg='gray85', anchor=NW).grid(row=0, column=2, padx=10, pady=2)
    entry3 = Entry(tab1)
    entry3.grid(row=1, column=2, padx=10, pady=10)
    entry3.insert(0, 0)

    label4 = Label(tab1, text="Delay", bg='gray85', anchor=NW).grid(row=2, column=0, padx=10, pady=2)
    entry4 = Entry(tab1)
    entry4.grid(row=3, column=0, padx=10, pady=10)
    entry4.insert(0, 0)

    label5 = Label(tab1, text="Weight Full [kg]", bg='gray85', anchor=NW).grid(row=2, column=1, padx=10, pady=2)
    entry5 = Entry(tab1)
    entry5.grid(row=3, column=1, padx=10, pady=10)
    entry5.insert(0, 0)

    label6 = Label(tab1, text="Weight Empty [kg]", bg='gray85', anchor=NW).grid(row=2, column=2, padx=10, pady=2)
    entry6 = Entry(tab1)
    entry6.grid(row=3, column=2, padx=10, pady=10)
    entry6.insert(0, 0)

    label7 = Label(tab1, text="Length [mm]", bg='gray85', anchor=NW).grid(row=4, column=0, padx=10, pady=2)
    entry7 = Entry(tab1)
    entry7.grid(row=5, column=0, padx=10, pady=10)
    entry7.insert(0, 0)

    label8 = Label(tab1, text="Name 2", bg='gray85', anchor=NW).grid(row=4, column=1, padx=10, pady=2)
    entry8 = Entry(tab1)
    entry8.grid(row=5, column=1, padx=10, pady=10)
    entry8.insert(0, "Name 2: ")

    label9 = Label(tab2, text="Time: ", bg='gray85', anchor=NW).grid(row=0, column=1, padx=10, pady=2)
    entry9 = Entry(tab2)
    entry9.grid(row=1, column=1, padx=10, pady=10)
    entry9.insert(0, 0)

    label10 = Label(tab2, text="Thrust", bg='gray85', anchor=NW).grid(row=0, column=2, padx=10, pady=2)
    entry10 = Entry(tab2)
    entry10.grid(row=1, column=2, padx=10, pady=10)
    entry10.insert(0, 0)

    couples = []
    def addCouple():
        couples.append([entry9.get(), entry10.get()])
        Label(tab2, text="%s" % (entry9.get())).grid(row=2, column=1)
        Label(tab2, text="%s" % (entry10.get())).grid(row=2, column=2)
        entry9.delete(0, END); entry10.delete(0,END)
        entry9.insert(0, 0)
        entry10.insert(0, 0)


    button1 = Button(tab2, text="Add Couple", command=addCouple).grid(row=1, column=3, padx=10, pady=2)

    def validCB():
        BT_Text = open('Parameters/param_motor/Custom_Motor.txt', "w")
        vals = [entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get(), entry7.get(),
                entry8.get()]
        for val in vals:
            BT_Text.write("%s " % (val))
        BT_Text.write("\n")
        for couple in couples:
            BT_Text.write("   "+couple[0]+" "+couple[1]+"\n")

        BT_Text.close()



    def quitPage():
        MotorParams.destroy()
        MotorParams.update()

    applyButton = Button(MotorParams, text="Apply", command=validCB)
    applyButton.pack(anchor="w", padx=10, pady=5)
    quitButton = Button(MotorParams, text="Ok", command=quitPage)
    quitButton.pack(anchor="e", padx=10, pady=5)
    MotorParams.mainloop()

def OpenEnvParams():
    EnvParams = Toplevel(fenetre)
    EnvParams.title("Create Custom Environment")
    EnvParams.geometry("450x450")
    Title = Label(EnvParams, text="Change Motor params")
    Title.pack()

    notebook = ttk.Notebook(EnvParams)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Details")
    notebook.pack(expand=1, fill="both")

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Values")
    notebook.pack(expand=1, fill="both")

    entries5 = []
    EntryButton(tab1, 'Altitude [m]', 0, 0, entries5)
    EntryButton(tab1, 'Temperature [K]', 0, 1, entries5)
    EntryButton(tab1, 'Pressure [Pa]', 0, 2, entries5)
    EntryButton(tab1, 'Humidity [%]', 2, 0, entries5)

    DispE = Button(tab1, text='Save', command=lambda: SaveEnvironment(entries5))
    DispE.grid(row=4, column=2, sticky='se', padx=10, pady=10)

    def quitPage():
        EnvParams.destroy()
        EnvParams.update()

    quitButton = Button(EnvParams, text="Ok", command=quitPage)
    quitButton.pack(anchor="e", padx=10, pady=5)
    EnvParams.mainloop()

def DrawP(VALUES_P, canvas):
    midh = canvas.winfo_height() / 2
    midw = canvas.winfo_width() / 2

    parachute = canvas.create_oval(midw - VALUES_P[0] / 2, midh - VALUES_P[0] / 2, midw + VALUES_P[0] / 2,
                                    midh + VALUES_P[0] / 2,
                                    width=1, outline='red', fill='', dash='1')

    text = canvas.create_text(midw, midh, text="P", fill='red')

    canvas.move(parachute, VALUES_P[2], 0)
    canvas.move(text, VALUES_P[2], 0)


def DrawParachute(VALUES_P, display=0):
    # Get the index 'stg' of stage : example, first stage has an index stg = 0
    Stg = int(tree.focus()[-1])
    stage = get_stage()
    substage = get_substage()

    if display:
        frame02idx = FrameGeometry[Stg]
        idx = tree.index(tree.focus())

        # Get Canvas in frame02idx
        Add_SubSubstage(tree.selection(), 'Parachute', 'canvas5', Stg, frame02idx, 'p', idx)

    piece = bodyParts[stage][substage][0]
    if piece == 'n':
        p = "Nose"
    elif piece == 't':
        p = "Tube"
    elif piece == 'f':
        p = "Fins"
    elif piece == 'b':
        p = "BT"

    Para_Text = open("Parameters/param_rocket/Parachute"+p+".txt", "w")
    for i in range(len(VALUES_P)):
        Para_Text.write("%s\n" % (VALUES_P[i]))
    Para_Text.close()

    DrawFullPiece()



def OpenParachuteParams(fenetre, values=[20, 20, 0], disp=1):
    ParachuteParams = Toplevel(fenetre)
    ParachuteParams.title("Create Custom Parachute")
    ParachuteParams.geometry("450x450")
    Title = Label(ParachuteParams, text="Change Parachute params")
    Title.pack()

    notebook = ttk.Notebook(ParachuteParams)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Details")
    notebook.pack(expand=1, fill="both")

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Values")
    notebook.pack(expand=1, fill="both")

    canvas = GetCanvas()
    len = canvas.winfo_width()/2

    def slide(var):
        DiaEntry.delete(0, "end")
        DiaEntry.insert(0,str(DiaScale.get()))
        DrawParachute([DiaScale.get(), CoefEntry.get(), PosScale.get()])

    def insertVal(var):
        DiaScale.set(DiaEntry.get())

    def slide1(var):
        PosEntry.delete(0, "end")
        PosEntry.insert(0,str(PosScale.get()))
        DrawParachute([DiaScale.get(), CoefEntry.get(), PosScale.get()])

    def insertVal1(var):
        PosScale.set(PosEntry.get())

    DiaLabel = Label(tab1, text="Diameter: ")
    DiaLabel.grid(row=1, column=0)
    DiaEntry = Entry(tab1)
    DiaEntry.grid(row=1, column=1)
    DiaEntry.insert(0, values[0])
    DiaEntry.bind("<Return>", insertVal)
    DiaScale = Scale(tab1, from_=0, to=100, orient=HORIZONTAL, command=slide)
    DiaScale.grid(row=1, column=2)
    DiaScale.set(values[0])

    PosLabel = Label(tab1, text="Position relative au centre de la piece: ")
    PosLabel.grid(row=3, column=0)
    PosEntry = Entry(tab1)
    PosEntry.grid(row=3, column=1)
    PosEntry.insert(0, values[2])
    PosEntry.bind("<Return>", insertVal1)
    PosScale = Scale(tab1, from_=-len, to=len, orient=HORIZONTAL, command=slide1)
    PosScale.grid(row=3, column=2)
    PosScale.set(values[2])

    CoefLabel = Label(tab1, text="Coefficient de trainée: ")
    CoefLabel.grid(row=2, column=0)
    CoefEntry = Entry(tab1)
    CoefEntry.grid(row=2, column=1)
    CoefEntry.insert(0, values[1])

    if disp:
        DrawParachute([DiaScale.get(), CoefEntry.get(), PosScale.get()], display=1)

    def quitPage():
        ParachuteParams.destroy()
        ParachuteParams.update()

    quitButton = Button(ParachuteParams, text="Ok", command=quitPage)
    quitButton.pack(anchor="e", padx=10, pady=5)
    ParachuteParams.mainloop()

def DrawIT(VALUES_IT, canvas):
    length = canvas.winfo_width()
    height = canvas.winfo_height()

    inner_tube1 = canvas.create_rectangle(length-(VALUES_IT[0])/3, height/2-(VALUES_IT[1]/2)/3, length, height/2+(VALUES_IT[1]/2)/3, width=1, outline='green')
    inner_tube2 = canvas.create_rectangle(length - (VALUES_IT[0])/3, height / 2 - (VALUES_IT[2] / 2)/3, length,
                                          height / 2 + (VALUES_IT[2] / 2)/3, width=1, outline='green', dash='1')

    canvas.move(inner_tube1, -VALUES_IT[4], 0)
    canvas.move(inner_tube2, -VALUES_IT[4], 0)


def DrawInnerTube(VALUES_IT, display=0):

    # Get the index 'stg' of stage : example, first stage has an index stg = 0
    Stg = int(tree.focus()[-1])
    stage = get_stage()
    substage = get_substage()

    if display:
        frame02idx = FrameGeometry[Stg]
        idx = tree.index(tree.focus())

        # Get Canvas in frame02idx
        Add_SubSubstage(tree.selection(), 'InnerTube', 'canvas5', Stg, frame02idx, 'c', idx)

    piece = bodyParts[stage][substage][0]
    if piece == 'n':
        p = "Nose"
    elif piece == 't':
        p = "Tube"
    elif piece == 'f':
        p = "Fins"
    elif piece == 'b':
        p = "BT"

    IT_Text = open("Parameters/param_rocket/InnerTube"+p+".txt", "w")
    for i in range(len(VALUES_IT)):
        IT_Text.write("%s\n" % (VALUES_IT[i]))
    IT_Text.close()

    DrawFullPiece()



def OpenInnerTubeParams(fenetre, values=[600, 150, 140, 5, 0], disp=1):
    tubeParam = Toplevel(fenetre)
    tubeParam.title("Inner Tube Parameters")
    tubeParam.geometry("500x500")
    Title = Label(tubeParam, text="Change inner tube params")
    Title.pack()

    notebook = ttk.Notebook(tubeParam)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Dimensions")
    notebook.pack(expand=1, fill="both")

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Inertia")
    notebook.pack(expand=1, fill="both")

    canvas = GetCanvas()
    len = canvas.winfo_width()
    print(len)

    def slide(var):
        lengthEntry.delete(0, "end")
        lengthEntry.insert(0, str(lengthScale.get()))
        PosScale.config(to=len-lengthScale.get()/3)
        DrawInnerTube([lengthScale.get(), DiaExtScale.get(), DiaInnScale.get(), ThScale.get(), PosScale.get()])

    def insertVal(var):
        lengthScale.set(lengthEntry.get())

    def slide1(var):
        DiaExtEntry.delete(0, "end")
        DiaExtEntry.insert(0, str(DiaExtScale.get()))
        DiaInnScale.config(to=DiaExtScale.get())
        ThScale.config(to=DiaExtScale.get() / 2)
        DrawInnerTube([lengthScale.get(), DiaExtScale.get(), DiaInnScale.get(), ThScale.get(), PosScale.get()])

    def insertVal1(var):
        DiaExtScale.set(DiaExtEntry.get())

    def slide2(var):
        DiaInnEntry.delete(0, "end")
        DiaInnEntry.insert(0, str(DiaInnScale.get()))
        ThEntry.delete(0, "end")
        ThEntry.insert(0, (DiaExtScale.get() - DiaInnScale.get())/2)
        ThScale.set(ThEntry.get())
        DrawInnerTube([lengthScale.get(), DiaExtScale.get(), DiaInnScale.get(), ThScale.get(), PosScale.get()])

    def insertVal2(var):
        DiaInnScale.set(DiaInnEntry.get())

    def slide3(var):
        ThEntry.delete(0, "end")
        ThEntry.insert(0, str(ThScale.get()))
        DiaInnEntry.delete(0, "end")
        DiaInnEntry.insert(0, DiaExtScale.get()-2*ThScale.get())
        DiaInnScale.set(DiaInnEntry.get())
        DrawInnerTube([lengthScale.get(), DiaExtScale.get(), DiaInnScale.get(), ThScale.get(), PosScale.get()])

    def insertVal3(var):
        ThScale.set(ThEntry.get())

    def slide4(var):
        PosEntry.delete(0, "end")
        PosEntry.insert(0, str(PosScale.get()))
        DrawInnerTube([lengthScale.get(), DiaExtScale.get(), DiaInnScale.get(), ThScale.get(), PosScale.get()])

    def insertVal4(var):
        PosScale.set(PosEntry.get())

    lengthLabel = Label(tab1, text="Length: ")
    lengthLabel.grid(row=1, column=0)
    lengthEntry = Entry(tab1)
    lengthEntry.grid(row=1, column=1)
    lengthEntry.insert(0, values[0])
    lengthEntry.bind("<Return>", insertVal)
    lengthScale = Scale(tab1, from_=0, to=400, orient=HORIZONTAL, command=slide)
    lengthScale.grid(row=1, column=2)
    lengthScale.set(values[0])

    DiaExtLabel = Label(tab1, text="Ext. Diameter: ")
    DiaExtLabel.grid(row=2, column=0)
    DiaExtEntry = Entry(tab1)
    DiaExtEntry.grid(row=2, column=1)
    DiaExtEntry.insert(0, values[1])
    DiaExtEntry.bind("<Return>", insertVal1)
    DiaExtScale = Scale(tab1, from_=0, to=300, orient=HORIZONTAL, command=slide1)
    DiaExtScale.grid(row=2, column=2)
    DiaExtScale.set(values[1])

    DiaInnLabel = Label(tab1, text="Inner Diameter: ")
    DiaInnLabel.grid(row=3, column=0)
    DiaInnEntry = Entry(tab1)
    DiaInnEntry.grid(row=3, column=1)
    DiaInnEntry.insert(0, values[2])
    DiaInnEntry.bind("<Return>", insertVal2)
    DiaInnScale = Scale(tab1, from_=0, to=DiaExtScale.get(), orient=HORIZONTAL, command=slide2)
    DiaInnScale.grid(row=3, column=2)
    DiaInnScale.set(values[2])

    ThLabel = Label(tab1, text="Tube Thickness: ")
    ThLabel.grid(row=4, column=0)
    ThEntry = Entry(tab1)
    ThEntry.grid(row=4, column=1)
    ThEntry.insert(0, values[3])
    ThEntry.bind("<Return>", insertVal3)
    ThScale = Scale(tab1, from_=0, to=DiaExtScale.get()/2, orient=HORIZONTAL, command=slide3)
    ThScale.grid(row=4, column=2)
    ThScale.set(values[3])

    PosLabel = Label(tab1, text="Position relative au bout de la piece: ")
    PosLabel.grid(row=5, column=0)
    PosEntry = Entry(tab1)
    PosEntry.grid(row=5, column=1)
    PosEntry.insert(0, values[4])
    PosEntry.bind("<Return>", insertVal4)
    PosScale = Scale(tab1, from_=0, to=len, orient=HORIZONTAL, command=slide4)
    PosScale.grid(row=5, column=2)
    PosScale.set(values[4])

    if disp:
        DrawInnerTube([lengthScale.get(), DiaExtScale.get(), DiaInnScale.get(), ThScale.get(), PosScale.get()], display=1)

    def validCB():
        tubeParam.destroy()
        tubeParam.update()

    validateButton = Button(tubeParam, text="OK", command=validCB)
    validateButton.pack(anchor="e", padx=10, pady=5)
    tubeParam.mainloop()

def OpenBanderolleParams(fenetre, values=[20, 20], disp=1):
    return
def OpenDamperParams(fenetre, values=[20, 20], disp=1):
    return




def DrawW(VALUES_W, canvas):
    midh = canvas.winfo_height() / 2
    midw = canvas.winfo_width() / 2

    weight = canvas.create_oval(midw - VALUES_W[0] / 2, midh - VALUES_W[0] / 2, midw + VALUES_W[0] / 2,
                                 midh + VALUES_W[0] / 2,
                                 width=1.5, outline='black', fill='')

    text = canvas.create_text(midw, midh, text="W", fill='black')

    canvas.move(weight, VALUES_W[1], 0)
    canvas.move(text, VALUES_W[1], 0)


def DrawWeight(VALUES_W, display = 0):
    # Get the index 'stg' of stage : example, first stage has an index stg = 0
    Stg = int(tree.focus()[-1])
    stage = get_stage()
    substage = get_substage()

    if display:
        frame02idx = FrameGeometry[Stg]
        idx = tree.index(tree.focus())

        # Get Canvas in frame02idx
        Add_SubSubstage(tree.selection(), 'Weight', 'canvas5', Stg, frame02idx, 'w', idx)

    piece = bodyParts[stage][substage][0]
    if piece == 'n':
        p = "Nose"
    elif piece == 't':
        p = "Tube"
    elif piece == 'f':
        p = "Fins"
    elif piece == 'b':
        p = "BT"

    Weight_Text = open("Parameters/param_rocket/Weight"+p+".txt", "w")
    for i in range(len(VALUES_W)):
        Weight_Text.write("%s\n" % (VALUES_W[i]))
    Weight_Text.close()

    DrawFullPiece()


def OpenWeightParams(fenetre, values=[20, 0], disp=1):
    WeightParams = Toplevel(fenetre)
    WeightParams.title("Add Weight")
    WeightParams.geometry("450x450")
    Title = Label(WeightParams, text="Change Weight params")
    Title.pack()

    notebook = ttk.Notebook(WeightParams)
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Details")
    notebook.pack(expand=1, fill="both")

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="...")
    notebook.pack(expand=1, fill="both")

    def slide(var):
        WeightEntry.delete(0, "end")
        WeightEntry.insert(0, str(WeightScale.get()))
        DrawWeight([WeightScale.get(), PosScale.get()])

    def insertVal(var):
        WeightScale.set(WeightEntry.get())

    def slide2(var):
        PosEntry.delete(0, "end")
        PosEntry.insert(0, str(PosScale.get()))
        DrawWeight([WeightScale.get(), PosScale.get()])

    def insertVal2(var):
        PosScale.set(PosEntry.get())

    canvas = GetCanvas()
    len = canvas.winfo_width()/2

    WeightLabel = Label(tab1, text="Weight: ")
    WeightLabel.grid(row=1, column=0)
    WeightEntry = Entry(tab1)
    WeightEntry.grid(row=1, column=1)
    WeightEntry.insert(0, values[0])
    WeightEntry.bind("<Return>", insertVal)
    WeightScale = Scale(tab1, from_=0, to=100, orient=HORIZONTAL, command=slide)
    WeightScale.grid(row=1, column=2)
    WeightScale.set(values[0])

    PosLabel = Label(tab1, text="Position relative au centre de la piece: ")
    PosLabel.grid(row=3, column=0)
    PosEntry = Entry(tab1)
    PosEntry.grid(row=3, column=1)
    PosEntry.insert(0, values[1])
    PosEntry.bind("<Return>", insertVal2)
    PosScale = Scale(tab1, from_=-len, to=len, orient=HORIZONTAL, command=slide2)
    PosScale.grid(row=3, column=2)
    PosScale.set(values[1])


    if disp:
        DrawWeight([WeightScale.get(), PosScale.get()], display=1)

    def quitPage():
        WeightParams.destroy()
        WeightParams.update()

    quitButton = Button(WeightParams, text="Ok", command=quitPage)
    quitButton.pack(anchor="e", padx=10, pady=5)
    WeightParams.mainloop()

def GetCanvas():
    stage = get_stage()
    selected = tree.focus()
    if selected[1] == 'd':
        place = len(tree.get_children(selected))-1
    elif selected[1] == 't':
        place = tree.index(tree.focus())
    else:
        place = tree.index(tree.parent(tree.focus()))

    piece = bodyParts[stage][place][0]

    if piece == 'n':
        num = 1
    elif piece == 't':
        num = 2
    elif piece == 'f':
        num = 3
    elif piece == 'b':
        num = 4

    for i in range(len(CanvasGeometry[int(selected[-1])])):
        tmp = []
        for l in str(CanvasGeometry[int(selected[-1])][i]):
            tmp.append(l)

        if tmp[-4] == str(num):
            return CanvasGeometry[int(selected[-1])][i]

def DrawFullPiece():

    stage = get_stage()
    substage = get_substage()
    canvas = GetCanvas()
    canvas.delete("all")
    list = bodyParts[stage][substage]

    accessoryList = ['p', 'w', 'c']

    VALUES = []
    if list[0] == 'n':
        p = 'Nose'
        NoseCone = open('Parameters/param_rocket/NoseCone.txt', 'r')  # Read text file
        NoseCone1 = NoseCone.readlines()
        for line in NoseCone1:  # taking each line
            VALUES.append(float(line))
        DrawN(VALUES, canvas)
    elif list[0] == 't':
        p = 'Tube'
        Tube = open('Parameters/param_rocket/Tube.txt', 'r')  # Read text file
        Tube1 = Tube.readlines()
        for line in Tube1:  # taking each line
            VALUES.append(float(line))
        DrawT(VALUES, canvas)
    elif list[0] == 'f':
        p = 'Fins'
        Fins = open('Parameters/param_rocket/Fins.txt', 'r')  # Read text file
        Fins1 = Fins.readlines()
        for line in Fins1:  # taking each line
            VALUES.append(float(line))
        DrawF(VALUES, canvas)
    elif list[0] == 'b':
        p = 'BT'
        BoatTail = open('Parameters/param_rocket/BoatTail.txt', 'r')  # Read text file
        BoatTail1 = BoatTail.readlines()
        for line in BoatTail1:  # taking each line
            VALUES.append(float(line))
        DrawBT(VALUES, canvas)

    for item in accessoryList:
        VALUES1 = []
        if item in list:
            if item == 'p':
                Parachute = open('Parameters/param_rocket/Parachute'+p+'.txt', 'r')  # Read text file
                Parachute1 = Parachute.readlines()
                for line in Parachute1:  # taking each line
                    VALUES1.append(float(line))
                DrawP(VALUES1, canvas)
            elif item == 'w':
                Weight = open('Parameters/param_rocket/Weight'+p+'.txt', 'r')  # Read text file
                Weight1 = Weight.readlines()
                for line in Weight1:  # taking each line
                    VALUES1.append(float(line))
                DrawW(VALUES1, canvas)
            elif item == 'c':
                InnerTube = open('Parameters/param_rocket/InnerTube'+p+'.txt', 'r')  # Read text file
                InnerTube1 = InnerTube.readlines()
                for line in InnerTube1:  # taking each line
                    VALUES1.append(float(line))
                DrawIT(VALUES1, canvas)


def SearchMotorInFolder():
    fenetre.filemotor = filedialog.askopenfilename(initialdir=os.getcwd()+"/Motors", title="Select a File", filetypes=[("Motor Files", ".eng"), ("All Files", ".*")])
    count = -5
    while 1:
        if fenetre.filemotor[count] == "/":
            count += 1
            break
        if fenetre.filemotor[count] == "\\":
            count += 1
            break
        count -= 1

    name = fenetre.filemotor[count:-4]
    Text = open("Parameters/param_motor/Motor.txt", "w")
    Text.write(name)
    Text.close()

def SearchEnvInFolder():
    fenetre.fileEnv = filedialog.askopenfilename(initialdir=os.getcwd()+"/Parameters/param_env", title="Select a File", filetypes=[("Txt Files", ".txt"), ("All Files", ".*")])
    if fenetre.fileEnv:
        count = -5
        while 1:
            if fenetre.fileEnv[count] == "/":
                count += 1
                break
            if fenetre.fileEnv[count] == "\\":
                count += 1
                break
            count -= 1

        name = fenetre.fileEnv[count:-4]

        EP = open('Parameters/param_env/'+name+'.txt', 'r')
        EP1 = EP.readlines()
        VALUES_E = []
        for line in EP1:  # taking each line
            conv_float = float(line)
            VALUES_E.append(conv_float)
        GetEnvironment(VALUES_E)
    return

def UpdateButtonState():
    selection = tree.focus()
    if selection[1] == 'd':
        MoveUp.config(fg="black", state=NORMAL)
        MoveDown.config(fg="black", state=NORMAL)
        Change.config(fg="grey", state=DISABLED)
        Remove.config(fg="black", state=NORMAL)
        New_Stage.config(fg="grey", state=DISABLED)
        frameAB.grid(row=0, column=1, sticky='nswe')


    elif selection[1] == 't' or selection[1] == 's':
        MoveUp.config(fg="black", state=NORMAL)
        MoveDown.config(fg="black", state=NORMAL)
        Change.config(fg="black", state=NORMAL)
        Remove.config(fg="black", state=NORMAL)
        New_Stage.config(fg="grey", state=DISABLED)
        frameAB.grid(row=0, column=1, sticky='nswe')


    elif int(selection[1]) == 0:
        New_Stage.config(fg="black", state=NORMAL)
        MoveUp.config(fg="grey", state=DISABLED)
        MoveDown.config(fg="grey", state=DISABLED)
        Change.config(fg="grey", state=DISABLED)
        Remove.config(fg="grey", state=DISABLED)
        frameAB.grid_remove()


def UpdateBodyPartState(stage):
    selection = tree.focus()

    NoseCone_choice.config(fg="black", state=NORMAL)
    Tube_choice.config(fg="black", state=NORMAL)
    Fins_choice.config(fg="black", state=NORMAL)
    BoatTail_choice.config(fg="black", state=NORMAL)
    Parachute_choice.config(fg="black", state=NORMAL)
    Band_choice.config(fg="black", state=NORMAL)
    Damper_choice.config(fg="black", state=NORMAL)
    Weight_choice.config(fg="black", state=NORMAL)
    IT_choice.config(fg="black", state=NORMAL)

    for parts in bodyParts[stage]:
        if 'n' in parts:
            NoseCone_choice.config(fg="grey", state=DISABLED)

        if 't' in parts:
            Tube_choice.config(fg="grey", state=DISABLED)

        if 'f' in parts:
            Fins_choice.config(fg="grey", state=DISABLED)

        if 'b' in parts:
            BoatTail_choice.config(fg="grey", state=DISABLED)


    if selection[1] == 't':
        NoseCone_choice.config(fg="grey", state=DISABLED)
        Tube_choice.config(fg="grey", state=DISABLED)
        Fins_choice.config(fg="grey", state=DISABLED)
        BoatTail_choice.config(fg="grey", state=DISABLED)
        for subpart in bodyParts[stage][tree.index(selection)]:
            if 'p' in subpart:
                Parachute_choice.config(fg="grey", state=DISABLED)
            if 's' in subpart:
                Band_choice.config(fg="grey", state=DISABLED)
            if 'd' in subpart:
                Damper_choice.config(fg="grey", state=DISABLED)
            if 'w' in subpart:
                Weight_choice.config(fg="grey", state=DISABLED)
            if 'c' in subpart:
                IT_choice.config(fg="grey", state=DISABLED)

    if selection[1] == 's':
        Parachute_choice.config(fg="grey", state=DISABLED)
        Band_choice.config(fg="grey", state=DISABLED)
        Damper_choice.config(fg="grey", state=DISABLED)
        Weight_choice.config(fg="grey", state=DISABLED)
        IT_choice.config(fg="grey", state=DISABLED)

    DispOtherPieces()

def DispOtherPieces():
    elem = tree.focus()
    if elem[1] == 't' or elem[1] == 's':
        frameAC1.bind("<Configure>", ScrollReg(canvasACA))
        frameACA.grid(row=0, column=0, sticky='nswe')
    else:
        frameACA.grid_remove()


# Menu
# TODO: Assign command to menu
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

### First row in window
frameA = Frame(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
frameA.grid(row=0, column=0, sticky='nswe')
frameA.rowconfigure(0, weight=1)
frameA.columnconfigure(0, weight=9)
frameA.columnconfigure(1, weight=9)
frameA.columnconfigure(2, weight=13)
frameA.columnconfigure(3, weight=4)
frameA.grid_propagate('False')

## Arborescence, Left part of first row
frameAA = Frame(frameA, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
frameAA.grid(row=0, column=0, sticky='nswe')
frameAA.rowconfigure(0, weight=1)
frameAA.columnconfigure(0, weight=3)
frameAA.columnconfigure(1, weight=1)
frameAA.grid_propagate('False')

# Frame with treeview
frameAAA = Frame(frameAA, bg='white', highlightthickness=1, bd=1, relief='groove')
frameAAA.grid(row=0, column=0, padx=3, pady=3, sticky='nswe')
frameAAA.rowconfigure(0, weight=4)
frameAAA.rowconfigure(1, weight=1)
frameAAA.columnconfigure(0, weight=1)
frameAAA.grid_propagate('False')

frameAAAA = Frame(frameAAA, bg='white', highlightthickness=1, bd=1, relief='flat')
frameAAAA.grid(row=0, column=0, sticky='nswe')
frameAAAA.rowconfigure(0, weight=1)
frameAAAA.grid_propagate('False')
tree = ttk.Treeview(frameAAAA)
tree['show'] = 'tree'
NameRocket = tree.insert("", 0, text="Rocket")
tree.grid(row=0, column=0, sticky='nswe')
vbarTree = ttk.Scrollbar(frameAAAA, orient="vertical", command=tree.yview)
vbarTree.grid(row=0, column=1, sticky='ns')
tree.configure(yscrollcommand=vbarTree.set)
tree.focus(NameRocket)
tree.selection_set(NameRocket)

frameAAAB = Frame(frameAAA, bg='white', highlightthickness=1, bd=1, relief='groove')
frameAAAB.grid(row=1, column=0, sticky='nswe')
frameAAAB.rowconfigure(0, weight=1)
frameAAAB.columnconfigure(0, weight=1)
frameAAAB.grid_propagate('False')

# Frame with buttons 'change', 'new stage' and 'delete'
frameAAB = Frame(frameAA, bg='gray85', highlightthickness=0, bd=0, relief='flat')
frameAAB.grid(row=0, column=1, padx=3, pady=3, sticky='nswe')
frameAAB.columnconfigure(0, weight=1)
frameAAB.rowconfigure(0, weight=1)
frameAAB.rowconfigure(1, weight=1)
frameAAB.rowconfigure(2, weight=1)
frameAAB.rowconfigure(3, weight=1)
frameAAB.rowconfigure(4, weight=1)
frameAAB.grid_propagate('False')

# Button Move up
MoveUp = Button(frameAAB, text='Move up', bg='gray80', fg='grey', cursor='hand2', relief=RAISED, state=DISABLED,
                command=lambda: do_move_up())
MoveUp.grid(row=0, column=0, padx=3, pady=1, sticky='we')

# Button Move down
MoveDown = Button(frameAAB, text='Move down', bg='gray80', fg='grey', cursor='hand2', relief=RAISED, state=DISABLED,
                  command=lambda: do_move_down())
MoveDown.grid(row=1, column=0, padx=3, pady=1, sticky='we')
Change = Button(frameAAB, text='Change', bg='gray80', fg='grey', cursor='hand2', relief=RAISED, state=DISABLED,
                command=lambda: change())
Change.grid(row=2, column=0, padx=3, pady=1, sticky='we')

# Button New Stage
New_Stage = Button(frameAAB, text='New Stage', bg='gray80', fg='black', cursor='hand2', relief=RAISED, state=NORMAL,
                   command=lambda: Add_Stage())
New_Stage.grid(row=3, column=0, padx=3, pady=1, sticky='we')

# Button Remove
Remove = Button(frameAAB, text="Remove", bg='gray80', fg='grey', cursor='hand2', relief=RAISED, state=DISABLED,
                command=lambda: do_remove())
Remove.grid(row=4, column=0, padx=3, pady=1, sticky='we')

## Add new part, Center part of first row
frameAB = Frame(frameA, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
frameAB.grid(row=0, column=1, sticky='nswe')
frameAB.rowconfigure(0, weight=1)
frameAB.columnconfigure(0, weight=1)
frameAB.grid_propagate('False')
canvasAB = Canvas(frameAB, bg='gray85', highlightthickness=0, bd=0, relief='flat')
vbarAB = Scrollbar(frameAB, orient='vertical', command=canvasAB.yview)
vbarAB.pack(side="right", fill="y")
canvasAB.configure(yscrollcommand=vbarAB.set)
canvasAB.grid(row=0, column=0, sticky='nswe')
canvasAB.columnconfigure(0, weight=1)
frameAB.grid_remove()

# Frame with buttons Nosecone, Tube, Fins, Boat-Tail, Motor and Environment
frameAB1 = Frame(canvasAB, bg='gray85', highlightthickness=0, bd=0, relief='flat')
canvasAB.create_window((0, 0), window=frameAB1, anchor='nw')
frameAB1.bind("<Configure>", ScrollReg(canvasAB))

## Entries to select parameters, Right part of first row
frameAC = Frame(frameA, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
frameAC.grid(row=0, column=2, sticky='nswe')
frameAC.rowconfigure(0, weight=1)
frameAC.columnconfigure(0, weight=1)
frameAC.grid_propagate('False')

# Nosecone parameters
frameACA = Frame(frameAC, bg='gray85', highlightthickness=0, bd=0, relief='flat')
canvasACA = Canvas(frameACA)
vbarACA = Scrollbar(frameACA)
frameAC1 = Frame(canvasACA, bg='gray85', highlightthickness=0, bd=0, relief='flat')
Add_Scrollbar(frameACA, canvasACA, vbarACA, frameAC1)

#Accessories
Label(frameAC1, text="Accessories: ", bg="grey85", anchor="w").grid(row=0, column=0)
Label(frameAC1, text="InnerPieces: ", bg="grey85", anchor="w").grid(row=2, column=0)

#Parachute Button
Parachute_choice = Button(frameAC1, text='Parachute', bg='white', fg='black', cursor='hand2', relief=RAISED,
                          command=lambda: OpenParachuteParams(fenetre))
Parachute_choice.grid(row=1, column=0, padx=10, pady=10, ipadx=20, ipady=10, sticky='nswe')

#Banderolle Button
Band_choice = Button(frameAC1, text='Banderolle', bg='white', fg='grey', cursor='hand2', relief=RAISED, state=DISABLED,
                          command=lambda: OpenBanderolleParams(fenetre))
#Band_choice.grid(row=0, column=1, padx=10, pady=10, ipadx=20, ipady=10, sticky='nswe')

#Cordon Amortisseur Button
Damper_choice = Button(frameAC1, text='Damper', bg='white', fg='grey', cursor='hand2', relief=RAISED, state=DISABLED,
                          command=lambda: OpenDamperParams(fenetre))
#Damper_choice.grid(row=0, column=2, padx=10, pady=10, ipadx=20, ipady=10, sticky='nswe')

#Weight Button
Weight_choice = Button(frameAC1, text='Weight', bg='white', fg='black', cursor='hand2', relief=RAISED, state=NORMAL,
                          command=lambda: OpenWeightParams(fenetre))
Weight_choice.grid(row=1, column=1, padx=10, pady=10, ipadx=20, ipady=10, sticky='nswe')

#Inner Tube Button
IT_choice = Button(frameAC1, text='Inner Tube', bg='white', fg='black', cursor='hand2', relief=RAISED, state=NORMAL,
                          command=lambda: OpenInnerTubeParams(fenetre))
IT_choice.grid(row=3, column=0, padx=10, pady=10, ipadx=20, ipady=10, sticky='nswe')

# Button 'Nosecone' allows to select Eiger NoseCone or to enter specific parameters
NoseCone_choice = Menubutton(frameAB1, text='Nosecone', bg='white', fg='black', cursor='hand2', relief=RAISED)
NoseCone_choice.grid()
NoseCone_choice.menu = Menu(NoseCone_choice, tearoff=0)
NoseCone_choice["menu"] = NoseCone_choice.menu

nose = StringVar()
NoseCone_choice.menu.add_radiobutton(label='Eiger', variable=nose, value='Eiger NoseCone',
                                     command=lambda: EigerNoseCone())
NoseCone_choice.menu.add_separator()
NoseCone_choice.menu.add_radiobutton(label='Personalize', variable=nose, command=lambda: OpenNoseParams(fenetre))
NoseCone_choice.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky='nswe')

Tube_choice = Menubutton(frameAB1, text='Tube', bg='white', fg='black', cursor='hand2', relief=RAISED)
Tube_choice.grid()
Tube_choice.menu = Menu(Tube_choice, tearoff=0)
Tube_choice["menu"] = Tube_choice.menu

tube = StringVar()
Tube_choice.menu.add_radiobutton(label='Eiger', variable=tube, value='Eiger Tube',
                                 command=lambda: EigerTube())
Tube_choice.menu.add_separator()
Tube_choice.menu.add_radiobutton(label='Personalize', variable=tube, command=lambda: OpenTubeParams(fenetre))
Tube_choice.grid(row=0, column=1, padx=10, pady=10, ipadx=25, ipady=10, sticky='nswe')

Fins_choice = Menubutton(frameAB1, text='Fins', bg='white', fg='black', cursor='hand2', relief=RAISED)
Fins_choice.grid()
Fins_choice.menu = Menu(Fins_choice, tearoff=0)
Fins_choice["menu"] = Fins_choice.menu

fins = StringVar()
Fins_choice.menu.add_radiobutton(label='Eiger', variable=fins, value='Eiger Fins',
                                 command=lambda: EigerFins())
Fins_choice.menu.add_separator()
Fins_choice.menu.add_radiobutton(label='Personalize', variable=fins, command=lambda: OpenFinsParams(fenetre))
Fins_choice.grid(row=0, column=2, padx=10, pady=10, ipadx=27, ipady=10, sticky='nswe')

BoatTail_choice = Menubutton(frameAB1, text='Boat-Tail', bg='white', fg='black', cursor='hand2', relief=RAISED)
BoatTail_choice.grid()
BoatTail_choice.menu = Menu(BoatTail_choice, tearoff=0)
BoatTail_choice["menu"] = BoatTail_choice.menu

bt = StringVar()
BoatTail_choice.menu.add_radiobutton(label='Eiger', variable=bt, value='Eiger BoatTail',
                                     command=lambda: EigerBoatTail())
BoatTail_choice.menu.add_separator()
BoatTail_choice.menu.add_radiobutton(label='Personalize', variable=bt, command=lambda: OpenBoatTailParams(fenetre))
BoatTail_choice.grid(row=1, column=0, padx=10, pady=10, ipadx=15, ipady=10, sticky='nswe')

# Choose motor
motor_choice = Menubutton(frameAB1, text='Motor', bg='white', fg='black', cursor='hand2', relief=RAISED)
motor_choice.grid()
motor_choice.menu = Menu(motor_choice, tearoff=0)
motor_choice["menu"] = motor_choice.menu

mtr = StringVar()
motor_choice.menu.add_radiobutton(label='AT_L850', value='AT_L850', variable=mtr, command=lambda: AT_L850())
motor_choice.menu.add_radiobutton(label='Cesaroni_M1800', value='Cesaroni_M1800', variable=mtr, command=lambda:
Cesaroni_M1800())
motor_choice.menu.add_separator()
motor_choice.menu.add_radiobutton(label='Search in folder', variable=bt, command=lambda: SearchMotorInFolder())
motor_choice.menu.add_separator()
motor_choice.menu.add_radiobutton(label='Personalize', variable=bt, command=lambda: OpenMotorParams())

motor_choice.grid(row=1, column=1, padx=10, pady=10, ipadx=20, ipady=10, sticky='nswe')

# Choose Environment
env_choice = Menubutton(frameAB1, text="Environment", bg='white', fg='black', cursor='hand2', relief='raised')
env_choice.grid()
env_choice.menu = Menu(env_choice, tearoff=0)
env_choice["menu"] = env_choice.menu

env = StringVar()
env_choice.menu.add_radiobutton(label='Mexico', variable=env, value='Mexico environment',
                                command=lambda: MexicoEnv())

env_choice.menu.add_separator()
env_choice.menu.add_radiobutton(label='Search in folder', variable=env, command=lambda: SearchEnvInFolder())
env_choice.grid(row=1, column=2, padx=10, pady=10, ipadx=2, ipady=10, sticky='nswe')

env_choice.menu.add_separator()
env_choice.menu.add_radiobutton(label='Personalize', variable=env, command=lambda: OpenEnvParams())
env_choice.grid(row=1, column=2, padx=10, pady=10, ipadx=2, ipady=10, sticky='nswe')


### Launch Simulation, Update datas (Right of first row)
frameAD = Frame(frameA, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
frameAD.grid(row=0, column=3, sticky='nswe')
frameAD.grid_propagate('False')

# Design rocket, Second row of window
# scale : 1 pixel <-> 3 millimeters
frameB = Frame(fenetre, bg='gray85', highlightthickness=3, bd=1, relief='sunken')
frameB.grid(row=1, column=0, sticky='nswe')
frameB.rowconfigure(0, weight=1)
frameB.columnconfigure(0, weight=1)
frameB.grid_propagate('False')

# Frame for the geometry of the rocket
frame0 = Frame(frameB, bg='white')
frame0.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
frame0.rowconfigure(0, weight=1)
frame0.rowconfigure(1, weight=3)
frame0.rowconfigure(2, weight=1)
frame0.columnconfigure(0, weight=1)
frame0.grid_propagate('False')
frame01 = Frame(frame0, bg='white', highlightthickness=0, bd=0, relief='flat')
frame01.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
frame02 = Frame(frame0, bg='white', highlightthickness=0, bd=0, relief='flat')
frame02.grid(row=1, column=0)
frame02.rowconfigure(0, weight=1)
frame03 = Frame(frame0, bg='white', highlightthickness=0, bd=0, relief='flat')
frame03.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

# Update data
canvas6 = Canvas(frame01)
canvas7 = Canvas(frame01)
canvas8 = Canvas(frame03)
canvas9 = Canvas(frame03)  # change scale

# Launch simulation
simu_button = Button(frameAD, text='Launch simulation', bg='red', fg='white', cursor='hand2',
                     relief=RAISED, command=lambda: Launch_Simulator1D())
simu_button.grid(row=0, column=0, padx=10, pady=10, sticky='nswe')

# Bouton de sortie
# stop = Button(fenetre, text="x", bg='RED', fg='white', command=fenetre.quit)
# stop.grid(row=1, column=1, sticky='nswe', in_=canvasB)



#Double click binding for tree
def bindingDoubleClick(b):
    change()
tree.bind("<Double-1>", bindingDoubleClick)

def bindingSingleClick(b):
    UpdateButtonState()
    elem = tree.focus()
    if elem[1] == 'd':
        stage = tree.index(elem)
        UpdateBodyPartState(int(stage))
    elif elem[1] == 't':
        prnt=tree.parent(tree.focus())
        stage = tree.index(prnt)
        UpdateBodyPartState(int(stage))
    elif elem[1] == 's':
        prnt = tree.parent(tree.parent(elem))
        stage = tree.index(prnt)

        UpdateBodyPartState(int(stage))


tree.bind("<ButtonRelease-1>", bindingSingleClick)

# Disp window
fenetre.mainloop()
