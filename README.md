# libMetrology
Library for mechanical metrology frame analysis , based on Homogenous Transformation Theorem

# Analysis 
* __orthogonal vector constrain and generating__
* laser frame calibration flow and model


# Preparation
1. forward/inverse-kinematic model for pod
* given X,Y,Z,U,V,W , output Transformation matrix 
* given Transformation matrix , solve X,Y,Z,U,V,W 
2. orthogonal vector/points commands to Pod , for calibration of C1
3. orthogonal vector/points commands to Pod , for calibration of C2
4. orthogonal vector/points commands to Pod , for calibration of C3

# Functions

# Simulation (Using the real kinematic parameters)
## Workpiece Chain
1. given known R-C1 Error , extract it along Camera Calibration Flow, evaluating calculation error
2. given known R-C2 Error , extract it using Camera Calibration Flow, evaluating calculation error
3. given known R-C3 Error , extract it using Camera Calibration Flow, evaluating calculation error
4. given known End Effctor Position/Posture Error , extract it by C1/C2/C3 reading , evaluating calculation error 
## Board Chain
