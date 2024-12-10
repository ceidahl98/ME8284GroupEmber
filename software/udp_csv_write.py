import socket
import time
import serial
import queue
import keyboard
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import os

# Configuration
UDP_IP = "localhost"
UDP_PORT = 8284
SERIAL_PORT = "COM3"
BAUD_RATE = 115200
a_buffer = queue.Queue(1024)
b_buffer = queue.Queue(1024)
a_time_buffer = queue.Queue(1024)
b_time_buffer = queue.Queue(1024)

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((UDP_IP, UDP_PORT))
udp_sock.setblocking(False)
variance = 1
base_latency = .05
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0)
ser.flush()


trial_number = 1
def generate_filename(base_latency, variance, trial_number):
    return f"./trials/Metronome_latency_{base_latency}_variance_{variance}_trial_{trial_number}.csv"


def handle_udp_data(data):
    udp_message = data.decode('utf-8').strip()
    parts = udp_message.split()
    forceA = float(parts[0].split(':')[1])
    forceB = float(parts[1].split(':')[1])

    a_buffer.put(forceA)
    b_buffer.put(forceB)
    current_time = time.time()
    a_delay = np.random.normal(base_latency, variance)
    b_delay = np.random.normal(base_latency, variance)
    a_delay = max(a_delay, 1e-3) + current_time
    b_delay = max(b_delay, 1e-3) + current_time

    a_time_buffer.put(a_delay)
    b_time_buffer.put(b_delay)

    if ser.is_open and time.time() >= a_time_buffer.queue[0]:
        forceA = a_buffer.get()
        serial_message = f"A{forceA}\n"
        ser.write(serial_message.encode())
        a_time_buffer.get()

    if ser.is_open and time.time() >= b_time_buffer.queue[0]:
        forceB = b_buffer.get()
        serial_message = f"B{forceB}\n"
        ser.write(serial_message.encode())
        b_time_buffer.get()

    return forceA, forceB


def handle_serial_data(data):
    udp_sock.sendto(data.encode(), (UDP_IP, UDP_PORT))


# Main event loop
print("Starting loop...")
forceA = 0
dataTrackA = []
dataTrackB = []
timeline = []
recording = False

while True:
    # Check for UDP data
    try:
        udp_data, addr = udp_sock.recvfrom(1024)
        forceA, forceB = handle_udp_data(udp_data)

        if keyboard.is_pressed('r'):
            if not recording:
                print("Recording started...")
                recording = True
                start_time = time.time()

            dataTrackA.append(forceA)
            dataTrackB.append(forceB)
            timeline.append(time.time() - start_time)

        elif recording:

            print("Recording stopped. Writing to CSV...")
            recording = False


            filename = generate_filename(base_latency, variance, trial_number)

            data = pd.DataFrame({
                "Time": timeline,
                "ForceA": dataTrackA,
                "ForceB": dataTrackB
            })
            data.to_csv(filename, index=False)
            print(f"Data written to {filename}")


            trial_number += 1

            # Clear tracking data
            dataTrackA=[]
            dataTrackB=[]
            timeline=[]

    except BlockingIOError:
        pass  # No UDP data available

    # Check for Serial data
    if ser.in_waiting > 0:
        serial_data = ser.readline().decode('utf-8').strip()
        if serial_data:
            handle_serial_data(serial_data)
