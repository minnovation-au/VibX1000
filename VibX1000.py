##||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||##
##.....................VIBX1000 Vibration Monitor ..........................##
##....................Machine Vibration Monitoring @ 3 - 1000 Hz............##
##......................Written by Simon Maselli............................##
##......................www.minnovation.com.au..............................##
##......................January 27,2018.....................................##
##..................... Copyright 2018 - M innovation.......................##
##||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||##

import machine, gc, utime, math, ustruct

Freq = 800
Delay = (1/Freq/2)*1000

NZEROS = 2
NPOLES = 2
avg = 0

def data(P1,P2):

  AcX = 0
  AmX = 0
  BmX = 0
  OmX = 0
  LSmX = 0
  OOmX = 0
  avg = 0
  meas=0

  x = 0
  xv = [0,0,0]
  yv = [0,0,0]
  BPxv = [0,0,0]
  BPyv = [0,0,0]
  LSxv = [0,0,0]
  LSyv = [0,0,0]
  Mxv = [0,0]
  Myv = [0,0]
  OneXxv = [0,0]
  OneXyv = [0,0]

  adc = machine.ADC(bits=12)
  apin = adc.channel(pin=P2, attn=3)

  for i in range(Freq*2):

      ## SET FREQUENCY IN MICROSECONDS
      now = utime.ticks_us()
      ## TAKE SAMPLE AND RANGE TO G-s
      x = (apin()*(3300/4096)-1500)/300

      OallGAIN = 1.003927011e+00
      xv[0] = xv[1]
      xv[1] = xv[2]
      xv[2] = x / OallGAIN;
      yv[0] = yv[1]
      yv[1] = yv[2];
      yv[2] = (xv[2] - xv[0]) + (0.9921767002 * yv[0]) + ( -0.0000000000 * yv[1]);

      BPGAIN = 3.275925737e+01
      BPxv[0] = BPxv[1]
      BPxv[1] = BPxv[2]
      BPxv[2] = x / BPGAIN
      BPyv[0] = BPyv[1]
      BPyv[1] = BPyv[2]
      BPyv[2] = (BPxv[2] - BPxv[0]) + (-0.9390625058 * BPyv[0]) + ( 1.8790704994 * BPyv[1])

      MechGAIN = 2.962610505e+00
      Mxv[0] = Mxv[1]
      Mxv[1] = x / MechGAIN
      Myv[0] = Myv[1]
      Myv[1] = (Mxv[0] + Mxv[1]) + ( 0.3249196962 * Myv[0])

      OneXGAIN = 1.689454484e+01
      OneXxv[0] = OneXxv[1]
      OneXxv[1] = x / OneXGAIN
      OneXyv[0] = OneXyv[1]
      OneXyv[1] = (OneXxv[0] + OneXxv[1]) + (  0.8816185924 * OneXyv[0])

      LSGAIN = 1.259314862e+01
      LSxv[0] = LSxv[1]
      LSxv[1] = LSxv[2]
      LSxv[2] = x / LSGAIN
      LSyv[0] = LSyv[1]
      LSyv[1] = LSyv[2]
      LSyv[2] = (LSxv[2] - LSxv[0]) + (-0.8568009569 * LSyv[0]) + ( 1.8563419216 * LSyv[1])

      AcX = AcX + math.pow(yv[2]*9.81*1000,2)
      BmX = BmX + math.pow(BPyv[2]*9.81*1000,2)
      AmX = AmX + math.pow(Myv[1]*9.81*1000,2)
      OmX = OmX + math.pow(OneXyv[1]*9.81*1000,2)
      LSmX = LSmX + math.pow(LSxv[2]*9.81*1000,2)

      meas = meas+1

      ## PAUSE FOR FREQUENCY
      while utime.ticks_us() < now+Delay:
          pass

  print(meas)

  overall = int(round((math.sqrt(AcX/Freq)/(2*3.142*Freq)),3)*1000)
  bearings = int(round((math.sqrt(BmX/Freq)/(2*3.142*200)),3)*1000)
  gearmesh = int(round((math.sqrt(AmX/Freq)/(2*3.142*1000)),3)*1000)
  alignment = int(round((math.sqrt(OmX/Freq)/(2*3.142*1000)),3)*1000)
  process = int(round((math.sqrt(LSmX/Freq)/(2*3.142*100)),3)*1000)

  print(ustruct.pack('hhhhhh',ch,overall,bearings,alignment,process,gearmesh))
  gc.collect()
  ## CLEAN READY FOR NEXT SAMPLE ##

## LOOP FOR TESTING - UNHASH BELOW TO TEST ##
#while True:
    #data('P13','P14')
