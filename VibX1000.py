##||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||##
##.....................VIBX1000 Vibration Monitor ..........................##
##....................Machine Vibration Monitoring @ 3 - 1000 Hz............##
##......................Written by Simon Maselli............................##
##......................www.minnovation.com.au..............................##
##......................January 27,2018.....................................##
##..................... Copyright 2018 - M innovation.......................##
##||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||##

import time, math, machine, gc

Freq = 1000
Delay = 1/Freq/2

NZEROS = 2
NPOLES = 2


def data(P1,P2):

  AcX = 0
  AmX = 0
  BmX = 0
  OmX = 0
  LSmX = 0
  OOmX = 0

  x = 0
  xv = [0,0,0]
  yv = [0,0,0]

  adc = machine.ADC(bits=12)
  apin = adc.channel(pin=P2, attn=3)

  for i in range(Freq*2):

      x = (apin()-1820)/(4096/3300)/310

      OallGAIN = 1.006278364e+00
      xv[0] = xv[1]
      xv[1] = xv[2]
      xv[2] = x / OallGAIN;
      yv[0] = yv[1]
      yv[1] = yv[2];
      yv[2] = (xv[2] - xv[0]) + (0.9875119299 * yv[0]) + ( -0.0062440659 * yv[1]);
      xO = yv[2];

      AcX = AcX + math.pow(yv[2],2)
      AmX = AmX + math.pow(MechVib(x),2)
      BmX = BmX + math.pow(BPVib(x),2)
      OmX = OmX + math.pow(OneX(x),2)
      LSmX = LSmX + math.pow(LSVib(x),2)
      OOmX = OOmX + math.pow(OOVib(x),2)

      time.sleep(Delay)

  #string = "X:"+str(round(math.sqrt(AcX/Freq)*9.81),3)+" mm/s"
  print("{\"value\":"+str(round(math.sqrt(AcX/Freq)*9.81,3))+",\"Overall\":"+str(round(math.sqrt(OOmX/Freq)*9.81,3))+",\"300Hz\":"+str(round(math.sqrt(AmX/Freq)*9.81,3))+",\"1x\":"+str(round(math.sqrt(OmX/Freq)*9.81,3))+",\"LS\":"+str(round(math.sqrt(LSmX/Freq)*9.81,3))+",\"BP\":"+str(round(math.sqrt(BmX/Freq)*9.81,3))+"}")

  #return("{\"value\":"+str(round(math.sqrt(AcX/Freq)*9.81,3)))+"}"
  ## CLEAN READY FOR NEXT SAMPLE ##

def OOVib(x):
    OOxv = [0,0,0]
    OOyv = [0,0,0]
    OOGAIN = 1.006278364e+00
    OOxv[0] = OOxv[1]
    OOxv[1] = OOxv[2]
    OOxv[2] = x / OOGAIN
    OOyv[0] = OOyv[1]
    OOyv[1] = OOyv[2]
    OOyv[2] = (OOxv[2] - OOxv[0]) + (0.9875119299 * OOyv[0]) + ( -0.0062440659 * OOyv[1])
    return(OOyv[2])

def MechVib(x):
    MechGAIN = 2.962610505e+00
    Mxv = [0,0]
    Myv = [0,0]
    Mxv[0] = Mxv[1]
    Mxv[1] = x / MechGAIN
    Myv[0] = Myv[1]
    Myv[1] = (Mxv[0] + Mxv[1]) + ( 0.3249196962 * Myv[0])
    return(Myv[1])

def BPVib(x):
    BPGAIN = 3.275925737e+01
    BPxv = [0,0,0]
    BPyv = [0,0,0]
    BPxv[0] = BPxv[1]
    BPxv[1] = BPxv[2]
    BPxv[2] = x / BPGAIN
    BPyv[0] = BPyv[1]
    BPyv[1] = BPyv[2]
    BPyv[2] = (BPxv[2] - BPxv[0]) + (-0.9390625058 * BPyv[0]) + ( 1.8790704994 * BPyv[1])
    return(BPyv[2])

def LSVib(x):
    LSGAIN = 1.259314862e+01
    LSxv = [0,0,0]
    LSyv = [0,0,0]
    LSxv[0] = LSxv[1]
    LSxv[1] = LSxv[2]
    LSxv[2] = x / LSGAIN
    LSyv[0] = LSyv[1]
    LSyv[1] = LSyv[2]
    LSyv[2] = (LSxv[2] - LSxv[0]) + (-0.8568009569 * LSyv[0]) + ( 1.8563419216 * LSyv[1])
    return(LSyv[2])

def OneX(x):
    OneXGAIN = 1.689454484e+01
    OneXxv = [0,0]
    OneXyv = [0,0]
    OneXxv[0] = OneXxv[1]
    OneXxv[1] = x / OneXGAIN
    OneXyv[0] = OneXyv[1]
    OneXyv[1] = (OneXxv[0] + OneXxv[1]) + (  0.8816185924 * OneXyv[0])
    return(OneXyv[1])

while True:
    data('P13','P14')
