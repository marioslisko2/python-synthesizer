#!/usr/bin/env python3

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plot
import time
import sys

def noteToFreq(note):
    f = 440
    return (f/32)*(2**((note - 9)/12))

def envelope(a, d, s, r):
    env = [np.linspace(0, 1, a), np.linspace(1, 0.7, d), np.linspace(0.7, 0.7, s), np.linspace(0.7, 0, r)]
    return env

def sinteza(freq_hz, sps, atten, each_sample_number, env, n, odabir, note):

    waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / sps)
    waveform2 = waveform * 0

    if(odabir == 'p'):
        plot.title('Parne sekundarne frekvencije note %d'% note)
        for i in range (2, n+1, 2):
            waveform = np.sin(2 * np.pi * each_sample_number * (freq_hz * i) / sps) * (1/i)
            plot.plot(waveform, '-')
            waveform2 += waveform

    elif(odabir == 'n'):
        plot.title('Neparne sekundarne frekvencije note %d'% note)
        for i in range (1, n+1, 2):
            waveform = np.sin(2 * np.pi * each_sample_number * (freq_hz * i) / sps) * (1/i)
            plot.plot(waveform, '-')
            waveform2 += waveform
    
    elif(odabir == 's'):
        plot.title('Sve sekundarne frekvencije note %d'% note)
        for i in range (1, n+1):
            waveform = np.sin(2 * np.pi * each_sample_number * (freq_hz * i) / sps) * (1/i)
            plot.plot(waveform, '-')
            waveform2 += waveform
    
    waveform2 *= atten
    
    plot.plot(waveform2, '-')

    plot.xlabel('Vrijeme (1s = 44100)')
    plot.ylabel('Vrijednosti amplituda')

    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')

    plot.xlim([-1000, max(duration_s) * sps + 1000])
    plot.ylim([-1.1, 1.1])
    plot.show()

    waveform_final = []

    for i in range (0, len(env[0])):
        waveform_final.append(env[0][i] * waveform2[i])

    for i in range (0, len(env[1])):
        waveform_final.append(env[1][i] * waveform2[i+a])

    for i in range (0, len(env[2])):
        waveform_final.append(env[2][i] * waveform2[i+a+d])

    for i in range (0, len(env[3])):
        waveform_final.append(env[3][i] * waveform2[i+a+d+s])

    return waveform_final


note = []
atten = []
duration_s = []
odabir = []

zelja = 'd'
brojac = 0
#"""
while(zelja == 'd'):
    print('Unos zeljene note:')
    note.append(int(input()))

    print('Unos glasnoce note:')
    atten.append(float(input()))

    print('Unos trajanja note (u sekundama):')
    duration_s.append(int(input()))

    print('Unesite koje sekundarne frekvencije želite (p-parne, n-neparne, s-sve):')
    odabir.append(input())

    if(not (odabir[brojac]=='p' or odabir[brojac]=='n' or odabir[brojac]=='s')):
        print("Krivi odabir frekvencija.")
        sys.exit()

    brojac+=1

    print('Zelite li unijeti jos nota? (d-da, sve ostalo-ne)')
    zelja = input()
#"""
#"""
# Ovo smo dodali kao primjer gotove pjesmice da skratimo vrijeme unošenja kod testiranja. Maknuti ovaj komentar i zakomentirati petlju while(zelja == 'd').
note = [30, 32, 34, 20, 36, 38, 40, 24] # Broj kodirane note.
atten = [0.5, 0.6, 0.7, 1.0, 0.5, 0.6, 0.7, 1.0] # Glasnoca noti raste.
duration_s = [0.5, 0.5, 0.5, 2.0, 0.5, 0.5, 0.5, 2.0] # Trajanje noti.
odabir = ['p', 'p', 'p', 'p', 'n', 'n', 'n', 'n'] # Prve 4 note parne frekvencije, druge 4 neparne.

# Zakomentirati red 'odabir' iznad te odkomentirati zeljeni red ispod za usporedbu zbrajanja samo parnih ili neparnih frekvencija,  ili svih
#odabir = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
#odabir = ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']
#odabir = ['s', 's', 's', 's', 's', 's', 's', 's']
#"""

sps = 44100 #samples per second
n_note = len(note) #broj nota
n = 20 #broj sekundarnih frekvencija

freq_p = []
wave_p = []
env = []
x1 = []
x2 = []
x3 = []

for z in range (0, n_note):

    a = int(sps*duration_s[z]*(1/12))
    d = int(sps*duration_s[z]*(5/12))
    s = int(sps*duration_s[z]*(1/12))
    r = int(sps*duration_s[z]*(5/12))

    each_sample_number = np.arange(duration_s[z] * sps)
    env.append(envelope(a, d, s, r))

    freq_p.append(noteToFreq(note[z] + 20))
    print("Frekvencija %d. note: %.2f" % (z+1, freq_p[z]))

    wave_p.append(sinteza(freq_p[z], sps, atten[z], each_sample_number, env[z], n, odabir[z], note[z]))

    print("A = %.2fs\nD = %.2fs\nS = %.2fs\nR = %.2fs" % (a/sps, d/sps, s/sps, r/sps))
    print("Trajanje note je %.2f sekundi.\n"% duration_s[z])

    x1.append(np.linspace(a, a+d, d))
    x2.append(np.linspace(a+d, a+d+s, s))
    x3.append(np.linspace(a+d+s, a+d+s+r, r))

for z in range (0, n_note):
    plot.plot(wave_p[z], '-')
    plot.plot(env[z][0], '.')
    plot.plot(x1[z], env[z][1], '.')
    plot.plot(x2[z], env[z][2], '.')
    plot.plot(x3[z], env[z][3], '.')

plot.title('Usporedba valova nota')
plot.xlabel('Vrijeme (1s = 44100)')
plot.ylabel('Vrijednosti amplituda')

plot.xlim([-1000, max(duration_s) * sps + 1000])
plot.ylim([-1.1, 1.1])

plot.grid(True, which='both')
plot.axhline(y=0, color='k')

plot.show()

for i in range(0, n_note):
    sd.play(wave_p[i], sps)
    time.sleep(duration_s[i])
sd.stop()