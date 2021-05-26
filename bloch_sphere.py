from __future__ import division, print_function
# https://www.glowscript.org/docs/VPythonDocs/index.html
import cmath
from visual import *
from numpy import matrix
import wx

from qc_gate import QuantumGates

DEBUG = False
DEBUGU = True


class Qubit:
    """
    In this class we apply the Quantum Gate Transformation Matrix
    to a qubit.
    """

    def __init__(self, radius): 
        self.r = radius  # radius
        # row-1, col-1 element is theta, row-1, col-2 element is phi
        self.polarCord = matrix([0.0, 0.0])  # polar co-ordinate of qubit
        # row-1, col-1 element is probability |0> state, row-1, col-2 element is the probability of state |1>
        self.qubit = matrix([1 + 0j, 0 + 0j]).T  # Qubit Amplitudes 2*1 matrix

    def setVector(self, theta, phi):
        """
        Sets a qubit to a position
        :param theta: is angle from positive z-axis where 0<= theta <= 180
        :param phi: is angle from positive x-axis where 0<= phi <= 360
        """

        # self.polarCord[0, 0] = theta  # set (0,0) element of the matrix to theta
        # self.polarCord[0, 1] = phi
        self.polarCord = matrix([theta, phi])

        # Calculate Cartesian coordinates from theta and phi
        # will use this co-ordinates to draw the world in 3D sphere.
        x = ((math.cos(phi) * math.sin(theta)))
        y = ((math.sin(phi) * math.sin(theta)))
        z = ((math.cos(theta)))

        # Put world-frame cartesian coordinates back onto bloch sphere frame
        position = vector(x, y, z)
        vpy_point.pos = qubitFrame.world_to_frame(position * self.r)

    def setAmplitudes(self, alpha, beta):
        """
        set a superposition sate of global aubit
        :param alpha: is probability of state |0>
        :param beta: is probability of state |1>
        """
        self.qubit[0] = alpha
        self.qubit[1] = beta

    def applyTransformation(self, U):
        """
        apply transformation to the qubit
        :param U: is the unitary matrix to apply linear transformation to qubit
        """
        self.qubit = U * self.qubit

    def updatePosition(self):
        """
        Updates the all positions (arrow & rings) based upon point position
        """
        pointer.axis = vpy_point.pos

        # Find the point position in world frame
        xPos = qubitFrame.frame_to_world(vpy_point.pos).x
        yPos = qubitFrame.frame_to_world(vpy_point.pos).y
        zPos = qubitFrame.frame_to_world(vpy_point.pos).z

        # Move and scale rings accordingly
        xRing.pos.x = xPos
        yRing.pos.y = yPos
        zRing.pos.z = zPos
        try:
            xRing.radius = math.sqrt(self.r ** 2 - xPos ** 2)
            yRing.radius = math.sqrt(self.r ** 2 - yPos ** 2)
            zRing.radius = math.sqrt(self.r ** 2 - zPos ** 2)
        except:
            a = 1
        # Find polar angles, Get Amplitudes, and update labels
        # theta = math.atan2(xPos, zPos)
        theta = math.atan2(math.sqrt(xPos ** 2 + yPos ** 2), zPos)  # bug fix by @author Hasan Masum
        # phi = ((2 * pi) - math.atan2(yPos, xPos)) % (2 * pi) # clockwise positive
        phi = (math.atan2(yPos, xPos)) % (2 * pi)  # anti clockwise positive

        self.setDataLabels(self.qubit[0], self.qubit[1], theta, phi)
        # setVector(theta,phi)

    def setDataLabels(self, alpha, beta, theta, phi):
        """
        update the labels
        :param alpha: probability of state |0>
        :param beta: probability of state |1>
        :param theta: angle with positive z-axis
        :param phi: angle with positive x-axis
        """
        a = str(round(alpha.real, 3)) + '+' + str(round(alpha.imag, 3)) + 'i'
        b = str(round(beta.real, 3)) + '+' + str(round(beta.imag, 3)) + 'i'
        c = str(round((alpha.real ** 2), 3)) + '+' + str(round((alpha.imag ** 2), 3)) + 'i'
        d = str(round((beta.real ** 2), 3)) + '+' + str(round((beta.imag ** 2), 3)) + 'i'
        label = ('Alpha:   (' + a + ') \nBeta: (' + b + ')')
        dataText1.SetLabel(label)
        label = ('Alpha^2: (' + c + ') \nBeta^2: (' + d + ')')
        dataText1a.SetLabel(label)
        a = str(round(theta.real, 3))
        b = str(round(phi.real, 3))
        c = str(round(theta.real / pi, 3))
        d = str(round(phi.real / pi, 3))
        e = str(round(math.degrees(theta.real), 0))
        f = str(round(math.degrees(phi.real), 0) % 360)

        label = ('Theta: ' + a + '\nTheta/Pi: ' + c + '\nTheta(Deg): ' + e)
        dataText2.SetLabel(label)
        label = ('Phi: ' + b + '\nPhi/Pi: ' + d + '\nPhi(Deg): ' + f)
        dataText2a.SetLabel(label)

class BlochSphereVisualizer:
    TAG = "BlochSphereVisualizer->"

    def __init__(self, qubit, qubitFrame):
        print ("init BlochSphereVisualizer")
        self.qubit = qubit
        self.qubitFrame = qubitFrame

    def setVector(self, theta, phi):
        """
        Sets a qubit to a position
        :param theta: is angle from positive z-axis where 0<= theta <= 180
        :param phi: is angle from positive x-axis where 0<= phi <= 360
        """

        # self.polarCord[0, 0] = theta  # set (0,0) element of the matrix to theta
        # self.polarCord[0, 1] = phi
        self.qubit.polarCord = matrix([theta, phi])

        # Calculate Cartesian coordinates from theta and phi
        # will use this co-ordinates to draw the world in 3D sphere.
        x = ((math.cos(phi) * math.sin(theta)))
        y = ((math.sin(phi) * math.sin(theta)))
        z = ((math.cos(theta)))

        # Put world-frame cartesian coordinates back onto bloch sphere frame
        position = vector(x, y, z)
        vpy_point.pos = qubitFrame.world_to_frame(position * self.qubit.r)

    def animateQubit(self, axis, angle):
        print (BlochSphereVisualizer.TAG, "animateQubit()")
        fps = 128
        for i in range(0, fps):
            rate(fps)  # number of frames or loop iteration per second
            # https://www.glowscript.org/docs/VPythonDocs/rotation.html
            self.qubitFrame.rotate(axis=axis, angle= angle / fps)  # for anti-clockwise rotation w.r.t z-axis
            self.qubit.updatePosition()

    # apply gates with animation ===================================================
    def setHadamard(self, evt):
        print(BlochSphereVisualizer.TAG,'Hadamard')
        self.qubit.applyTransformation(QuantumGates.H)
        self.animateQubit(axis=(1 / math.sqrt(2), 0, 1 / math.sqrt(2)), angle=pi)

    def setPauliX(self, evt):
        print('Pauli X')
        self.qubit.applyTransformation(QuantumGates.X)
        # pi radian rotation w.r.t x-axis
        self.animateQubit(axis=(1, 0, 0), angle=pi ) 
    
    def setPauliY(self, evt):
        print('Pauli Y')
        self.qubit.applyTransformation(QuantumGates.Y)
        # pi radian rotation w.r.t y-axis
        self.animateQubit(axis=(0, 1, 0), angle=(pi) ) 

    def setPauliZ(self, evt):
        print('Pauli Z')
        self.qubit.applyTransformation(QuantumGates.Z)
        # pi radian rotation w.r.t y-axis
        self.animateQubit(axis=(0, 0, 1), angle=(pi) )

    def setPhase(self, evt):
        print('Phase')
        self.qubit.applyTransformation(QuantumGates.S)


        # pi/2 radian clockwise rotation w.r.t z-axis
        # self.animateQubit(axis=(0, 0, 1), angle= -1 *(pi / 2) )

        # pi/2 radian anti-clockwise rotation w.r.t z-axis
        self.animateQubit(axis=(0, 0, 1), angle=(pi / 2) )  

    def setPI8(self, evt):
        print('PI 8')
        self.qubit.applyTransformation(QuantumGates.T)

        # pi/4 radian clockwise rotation w.r.t z-axis
        # self.animateQubit(axis=(0, 0, 1), angle= -1 *(pi / 4) )

        # pi/4 radian anti-clockwise rotation w.r.t z-axis
        self.animateQubit(axis=(0, 0, 1), angle=(pi / 4) )
        
    def setsNot(self, evt):
        print('sqrt Not')
        self.qubit.applyTransformation(QuantumGates.sN)
        for i in range(0, 128):
            rate(128)
            self.qubitFrame.rotate(axis=(0, 1, 0), angle=1 * (pi / 4) / 128)
            self.qubit.updatePosition()


    # set positions without any animation ==========================================
    def setTheta(self, evt):
        thetaValue = thetaSlider.GetValue()
        thetaSliderLab.SetLabel('Theta (Deg): ' + str(thetaValue))
        self.setVector(math.radians(thetaValue), self.polarCord[0, 1])
        self.qubit.setAmplitudes(0, 0)
        self.qubit.updatePosition()

    def setPhi(self, evt):
        phiValue = phiSlider.GetValue()
        phiSliderLab.SetLabel('Phi (Deg): ' + str(phiValue))
        self.setVector(self.polarCord[0, 0], math.radians(phiValue))
        self.qubit.setAmplitudes(0, 0)
        self.qubit.updatePosition()

    def setqZero(self, evt):
        self.setVector(0, 0.0)
        self.qubit.setAmplitudes(1, 0)
        self.qubit.applyTransformation(QuantumGates.I)
        self.qubit.updatePosition()

    def setqOne(self, evt):
        self.setVector(pi, 0)
        self.qubit.setAmplitudes(0, 1)
        self.qubit.applyTransformation(QuantumGates.I)
        self.qubit.updatePosition()

    def setqPos(self, evt):
        self.setqZero(wx.EVT_SHOW)
        self.setHadamard(wx.EVT_SHOW)

    def setqNeg(self, evt):
        self.setqOne(wx.EVT_SHOW)
        self.setHadamard(wx.EVT_SHOW)


# The window=======================================================================================
wWidth = 310
wHeight = 725
M = 720
L = 10
d = 20
r = 100
Top = 40
TopB = 15

# w = window(width=wWidth, height=wHeight,menus=True, title='Bloch Sphere')
# display(window=w, x=d, y=d, width=L-2*d, height=L-2*d, forward=(1,-1,0))
# display(x=1024, y=0, width=M, height=M, forward=(-1,-.5,-.5))

w = window(width=wWidth, height=wHeight, menus=True, title='Bloch Sphere')

# disp = display(window=w,width=2*d, height=2*d, forward=(1,-1,0))
disp = display(window=w, x=d, y=d, width=M, height=M, forward=(-1, -.5, -.5))
disp2 = display(x=300, y=0, width=M, height=M, forward=(-1, -.5, -.5))

# The Qubit frame after creating windows
sceneFrame = frame()
qubitFrame = frame(frame=sceneFrame)

# create a bloch sphere
qubit = Qubit(r)
bsVisualizer = BlochSphereVisualizer(qubit
=qubit,qubitFrame=qubitFrame)


color_temp = vector(1, 1, 1)
local_light(pos=(r * 2, r * 2, 0), color=color_temp)
local_light(pos=(r * -2, r * 2, 0), color=color_temp)
local_light(pos=(r * 2, r * -2, 0), color=color_temp)
local_light(pos=(r * -2, r * -2, 0), color=color_temp)

# Buttons, Text, Window Setup
bSize = 50
p = w.panel
title = wx.StaticText(p, pos=(L * 2, 0), size=(300, 25), label='Qubit Bloch Sphere', style=wx.ALIGN_CENTRE)
title.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.BOLD))

about1 = wx.StaticText(p, pos=(L, wHeight - 150), size=(400, 25), label='Created By: Tyler Dwyer', style=wx.ALIGN_LEFT)
about1.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))

about2 = wx.StaticText(p, pos=(L, wHeight - 130), size=(400, 25), label='Email: tdwyer@sfu.ca', style=wx.ALIGN_LEFT)
about2.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))
about3 = wx.StaticText(p, pos=(L, wHeight - 110), size=(400, 25), label='Web: www.sfu.ca\~tdwyer', style=wx.ALIGN_LEFT)
about3.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))

about3 = wx.StaticText(p, pos=(wWidth / 2 - 110, wHeight - 90), size=(400, 25), label='Simon Fraser University',
                       style=wx.ALIGN_LEFT)
about3.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))

# Row Zero/One
wx.StaticText(p, pos=(L + 0 * bSize, 0 * bSize + Top), label='Base States:', style=wx.ALIGN_LEFT)
qZero = wx.Button(p, label='|0>', pos=(L + 0 * bSize, 1 * bSize + TopB), size=(bSize, bSize))
qOne = wx.Button(p, label='|1>', pos=(L + 1 * bSize, 1 * bSize + TopB), size=(bSize, bSize))

wx.StaticText(p, pos=(L + 3 * bSize, 0 * bSize + Top), label='Superposition:', style=wx.ALIGN_LEFT)
qPos = wx.Button(p, label='|+>', pos=(L + 3 * bSize, 1 * bSize + TopB), size=(bSize, bSize))
qNeg = wx.Button(p, label='|->', pos=(L + 4 * bSize, 1 * bSize + TopB), size=(bSize, bSize))

# Row Two/Three
wx.StaticText(p, pos=(L + 0 * bSize, 2 * bSize + Top), label='Hadamard', style=wx.ALIGN_LEFT)
hadamard = wx.Button(p, label='H', pos=(L + 0 * bSize, 3 * bSize + TopB), size=(bSize, bSize))

wx.StaticText(p, pos=(L + 2 * bSize, 2 * bSize + Top), label='Pauli', style=wx.ALIGN_LEFT)
pauliX = wx.Button(p, label='X', pos=(L + 2 * bSize, 3 * bSize + TopB), size=(bSize, bSize))
pauliY = wx.Button(p, label='Y', pos=(L + 3 * bSize, 3 * bSize + TopB), size=(bSize, bSize))
pauliZ = wx.Button(p, label='Z', pos=(L + 4 * bSize, 3 * bSize + TopB), size=(bSize, bSize))

# Row Four/Five
wx.StaticText(p, pos=(L + 0 * bSize, 4 * bSize + Top), label='Phase', style=wx.ALIGN_LEFT)
phase = wx.Button(p, label='S', pos=(L + 0 * bSize, 5 * bSize + TopB), size=(bSize, bSize))

wx.StaticText(p, pos=(L + 2 * bSize, 4 * bSize + Top), label='Pi/8', style=wx.ALIGN_LEFT)
pi8 = wx.Button(p, label='T', pos=(L + 2 * bSize, 5 * bSize + TopB), size=(bSize, bSize))

wx.StaticText(p, pos=(L + 4 * bSize, 4 * bSize + Top), label='Sqrt(Not)', style=wx.ALIGN_LEFT)
sNot = wx.Button(p, label='sN', pos=(L + 4 * bSize, 5 * bSize + TopB), size=(bSize, bSize))

# Row Six/Seven
thetaSliderLab = wx.StaticText(p, pos=(L + 0 * bSize, 6 * bSize + Top), label='Theta (Deg):', style=wx.ALIGN_LEFT)
thetaSlider = wx.Slider(p, pos=(L + 0 * bSize, 7 * bSize + TopB), size=(5 * bSize, 20), minValue=0, maxValue=179)
thetaSlider.Bind(wx.EVT_SCROLL, bsVisualizer.setTheta)

phiSliderLab = wx.StaticText(p, pos=(L + 0 * bSize, 7 * bSize + Top), label='Phi (Deg):', style=wx.ALIGN_LEFT)
phiSlider = wx.Slider(p, pos=(L + 0 * bSize, 8 * bSize + TopB), size=(5 * bSize, 20), minValue=0, maxValue=359)
phiSlider.Bind(wx.EVT_SCROLL, bsVisualizer.setPhi)

# Row Eight/Nine
dataText1 = wx.StaticText(p, pos=(L, 8 * bSize + Top), label='Loading ...', style=wx.ALIGN_LEFT)
dataText2 = wx.StaticText(p, pos=(L, 9 * bSize + Top), label='Loading ...', style=wx.ALIGN_LEFT)
dataText1a = wx.StaticText(p, pos=(L + 2.75 * bSize, 8 * bSize + Top), label='Loading ...', style=wx.ALIGN_LEFT)
dataText2a = wx.StaticText(p, pos=(L + 2.75 * bSize, 9 * bSize + Top), label='Loading ...', style=wx.ALIGN_LEFT)


# Button Bindings
hadamard.Bind(wx.EVT_BUTTON, bsVisualizer.setHadamard)  # bind with setHadamard() function
pauliX.Bind(wx.EVT_BUTTON, bsVisualizer.setPauliX)
pauliY.Bind(wx.EVT_BUTTON, bsVisualizer.setPauliY)
pauliZ.Bind(wx.EVT_BUTTON, bsVisualizer.setPauliZ)
phase.Bind(wx.EVT_BUTTON, bsVisualizer.setPhase)
pi8.Bind(wx.EVT_BUTTON, bsVisualizer.setPI8)
sNot.Bind(wx.EVT_BUTTON, bsVisualizer.setsNot)
qZero.Bind(wx.EVT_BUTTON, bsVisualizer.setqZero)
qOne.Bind(wx.EVT_BUTTON, bsVisualizer.setqOne)
qPos.Bind(wx.EVT_BUTTON, bsVisualizer.setqPos)
qNeg.Bind(wx.EVT_BUTTON, bsVisualizer.setqNeg)


# floor = box(pos=(0, -r, 0), length=r * 2, height=r / 1000, width=r * 2, color=color.cyan)
# ball = sphere(frame=qubitFrame, pos=(0, 0, 0), radius=r, material=materials.earth, opacity=.5)
ball = sphere(frame=qubitFrame, pos=(0, 0, 0), radius=r, opacity=.3)

pointer = arrow(frame=qubitFrame, pos=(0, 0, 0), axis=(0, 0, r), shaftwidth=r / 25, color=color.red)

# red point on top of arrow which is in sphere surface
vpy_point = sphere(frame=qubitFrame, pos=(0, 0, r), radius=r / 25, color=color.red)
# ring perpendicular to x-axis
xRing = ring(frame=sceneFrame, pos=(1, 0, 0), axis=(1, 0, 0), radius=r, thickness=r / 100, color=color.green)
# ring perpendicular to y-axis
yRing = ring(frame=sceneFrame, pos=(0, 1, 0), axis=(0, 1, 0), radius=r, thickness=r / 100, color=color.blue)
# ring perpendicular to y-axis
zRing = ring(frame=sceneFrame, pos=(0, 0, 1), axis=(0, 0, 1), radius=r, thickness=r / 100, color=color.yellow)
rodx = cylinder(frame=sceneFrame, pos=((r * 2.5) / -2, 0, 0), axis=(r * 2.5, 0, 0), radius=r / 100, color=color.green)
rody = cylinder(frame=sceneFrame, pos=(0, (r * 2.5) / -2, 0), axis=(0, r * 2.5, 0), radius=r / 100, color=color.blue)
rodz = cylinder(frame=sceneFrame, pos=(0, 0, (r * 2.5) / -2), axis=(0, 0, r * 2.5), radius=r / 100, color=color.yellow)
# Labels
zero = text(frame=sceneFrame, text='|0>', pos=(0, 0, r * 1.5), height=r * .25, align='center', depth=r * -0.03,
            color=color.green, axis=(0, 0, 1))
one = text(frame=sceneFrame, text='|1>', pos=(0, 0, r * -1.5), height=r * .25, align='center', depth=r * -0.03,
           color=color.green, axis=(0, 0, 1))

xtext = text(frame=sceneFrame, text='x', pos=(r * .5, 0, 0), height=r * .15, align='center', depth=r * -0.02,
             color=color.green, axis=(0, 0, 1))
ytext = text(frame=sceneFrame, text='y', pos=(0, r * .5, 0), height=r * .15, align='center', depth=r * -0.02,
             color=color.blue, axis=(0, 0, 1))
ztext = text(frame=sceneFrame, text='z', pos=(0, 0, r * .5), height=r * .15, align='center', depth=r * -0.02,
             color=color.yellow, axis=(0, 0, 1))

# Setting up qubit
bsVisualizer.setVector(0, 0.0)

# Initial scene/camera rotations
sceneFrame.rotate(axis=(1, 0, 0), angle=-1 * pi / 2)
zero.rotate(axis=(1, 0, 0), angle=-1 * pi / 2)
one.rotate(axis=(1, 0, 0), angle=-1 * pi / 2)
ball.rotate(axis=(1, 0, 0), angle=1 * pi / 2)
ball.rotate(axis=(0, 0, 1), angle=2 * pi / 2)
ztext.rotate(axis=(1, 0, 0), angle=1 * pi / 2)
ytext.rotate(axis=(1, 0, 0), angle=1 * pi / 2)
xtext.rotate(axis=(1, 0, 0), angle=1 * pi / 2)

bsVisualizer.setqZero(wx.EVT_SHOW)
# setPauliX(wx.EVT_SHOW)
# setHadamard(wx.EVT_SHOW)
# setPauliY(wx.EVT_SHOW)
# setPauliY(wx.EVT_SHOW)
# setPauliZ(wx.EVT_SHOW)
# setPauliZ(wx.EVT_SHOW)
# setHadamard(wx.EVT_SHOW)
# Main running loop
while 1:
    rate(128)
    # Keep things updated
    # updatePosition()
