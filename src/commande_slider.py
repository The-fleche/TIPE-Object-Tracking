from serial import *
import serial.tools.list_ports
import time

def swrite(ser, msg: str):
    # facilite l'écriture au slider
    ser.write("{}".format(msg).encode())


def sread(ser, n):
    # simplification de la lecture des réponses du slider
    return ser.read(n).decode("utf-8")


def rotation(ser, rot, angle):
    # simplification des commandes de rotation au slider
    # rot en rad/s
    swrite(ser, f"T{rot}/{angle}#")


def translation(ser, v, dist):
    # simplification des commandes de translation au slider
    # v en m/s
    swrite(ser, f"T{v}/{dist}#")
    
def pos_metre(ser):
    swrite(ser, "P#")
    posm = sread(ser, 5)
    return posm

def pos_angle(ser):
    swrite(ser, "G#")
    posa = sread(ser, 5)
    return posa


def find_Slider():
    comms = serial.tools.list_ports.comports()
    for i in range(len(comms)):
        comms[i] = str(comms[i])
    for i in comms:
        if "USB" in i:
            comm = i.split("-")[0].strip()
            return True, comm 
    return False, None

def origine(ser):
    swrite(ser, "O#")
    sread(ser, 2) # "retourne 'OK' "
    