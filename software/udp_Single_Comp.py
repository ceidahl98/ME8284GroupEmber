import socket
import time
import serial
import queue
import keyboard
import matplotlib.pyplot as plt
import numpy as np
import csv


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
variance = .200
base_latency = .050
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0)
ser.flush()


def handle_udp_data(data):

    udp_message = data.decode('utf-8').strip()
    #print(f"Received UDP: {udp_message}")

    parts = udp_message.split()
    forceA = float(parts[0].split(':')[1])

    forceB = float(parts[1].split(':')[1])
    a_buffer.put(forceA)
    b_buffer.put(forceB)
    current_time = time.time()
    a_delay = np.random.normal(base_latency,variance)
    b_delay = np.random.normal(base_latency,variance)
    if a_delay < 0:
        a_delay=1e-3

    if b_delay <0:
        b_delay= 1e-3

    a_delay = current_time + a_delay
    b_delay = current_time + b_delay
    a_time_buffer.put(a_delay)
    b_time_buffer.put(b_delay)
    # Forward command to serial
    if ser.is_open and time.time()>=a_time_buffer.queue[0]:

        forceA = a_buffer.get()
        serial_message = f"A{forceA}\n"
        ser.write(serial_message.encode())
        a_time_buffer.get()
        #print(f"Sent to Serial: {serial_message}")

    if ser.is_open and time.time() >=b_time_buffer.queue[0]:
        forceB = b_buffer.get()
        serial_message = f"B{forceB}\n"
        print("ForceB",forceB)
        ser.write(serial_message.encode())
        b_time_buffer.get()
    return forceA, forceB

# Function to process Serial data
def handle_serial_data(data):
    #print(f"Serial Data: {data.strip()}")

    # Forward Serial data to UDP
    udp_sock.sendto(data.encode(), (UDP_IP, UDP_PORT))
    #print(f"Sent to UDP: {data.strip()}")

# Main event loop
print("Starting loop...")
forceA=0
dataTrackA = []
dataTrackB = []
timeline = []
i = 0
start_flag = False
while True:

    # Check for UDP data
    try:
        udp_data, addr = udp_sock.recvfrom(1024)  # Non-blocking
        forceA, forceB = handle_udp_data(udp_data)
        if keyboard.is_pressed('r'):

            if start_flag == False:
                start_flag = True
                start = time.time()

            dataTrackA.append(forceA)
            dataTrackB.append(forceB)
            timeline.append(time.time() - start)


    except BlockingIOError:
        pass  # No UDP data available

    # Check for Serial data
    if ser.in_waiting > 0:
        serial_data = ser.readline().decode('utf-8').strip()
        if serial_data:
            handle_serial_data(serial_data)


    if keyboard.is_pressed('a'):
        length = len(dataTrackA)
        #timeline = np.arange(0,length/1000,1/(length/1000))

        plt.plot(timeline,dataTrackA)
        plt.ylabel('Force A')
        plt.show()

        start_flag = False

    if keyboard.is_pressed('b'):
        length = len(dataTrackB)
        #timeline = np.arange(0,length/1000,1/(length/1000))

        plt.plot(timeline,dataTrackB)
        plt.ylabel("Force B")
        plt.show()

        start_flag = False


    i+=1
    # Add a small delay to prevent 100% CPU usage
    #time.sleep(0.01)
    #print(time.time()-start)
