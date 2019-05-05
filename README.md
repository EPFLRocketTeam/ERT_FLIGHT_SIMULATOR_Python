# ERT_FLIGHT_SIMULATOR

Repository for the EPFL Rocket Team's flight simulator translated to Python.

The aim is to create a GUI from the existing Matlab code, created by Hassan and then imporved by Eric and Emilien.

Initial steps are
1. Create a rocket from objects as below
![Rocket object](Objects/Support/SimERT_Python_Rocket.png)
2. Implement a 1D model
3. Implement a 3D model

**Run the code from /venv/Include**

# Technical information
Nose cone design : https://en.wikipedia.org/wiki/Nose_cone_design

Nose cone software design : https://www.instructables.com/id/Design-a-Rocket-Nose-Cone-with-Software/

Literature and volumes : https://aviation.stackexchange.com/questions/24414/why-when-is-the-blunt-nose-better

Useful notes for OpenRocket : http://openrocket.sourceforge.net/techdoc.pdf

# Tasks
## Jules
- Finish documenting the **_stdAtmosUS.py_** doc.
- Check the drag.py class is implemented
- Check the AB_drag.py class is implemented
- Create the Rocket_Kinematic.py doc
- Create the 1D simulator
- Examiner la formule de l'amortissement
## Paul
- Choisir un moteur qui nous envoie en supersonique
- Faire tourner le simulateur avec le modèle de drag supersonique et subsonique
- Trouver le modèle transonique

