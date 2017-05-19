#!/usr/bin/env python
#coding=utf-8 



#  # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # 

import serial
import wxSerialConfigDialog

# import serial.tools.list_ports
# # # # # # # # # # # # # # # # # # # # # 
# SHOW_BAUDRATE = 1 << 0
# SHOW_FORMAT = 1 << 1
# SHOW_FLOW = 1 << 2
# SHOW_TIMEdata, timeout=3.0 = 1 << 3
# SHOW_ALL = SHOW_BAUDRATE | SHOW_FORMAT | SHOW_FLOW | SHOW_TIMEOUT
# # # # # # # # # # # # # # # # # # # # # 
#  # # # # # # # # # # # # # # # # # # # # 

g_ser = serial.Serial()
g_log = None

def init(log):
    global g_ser
    global g_log
    g_log = log
    wxSerialConfigDialog.Get_Selected_SerialNum(g_ser)
    # print g_ser
    g_ser.timeout = 3.0
    g_ser.write('aaaaa')


def send_and_read6(data, timeout=3.0):
	global g_ser
	global g_log
	g_ser.timeout = timeout
	g_ser.write(data); g_ser.flush();
	
	rcv = g_ser.read(6)
	if len(rcv) > 0:
		g_log.WriteText("Received: " + rcv + "\r\n")
	return rcv

def send_and_read8(data, timeout=3.0):
	global g_ser
	global g_log
	g_ser.timeout = timeout
	g_ser.write(data); g_ser.flush();
	rcv = g_ser.read(8)
	if len(rcv) > 0:
		g_log.WriteText("Received: " + rcv + "\r\n")
	return rcv

def send_and_read10(data, timeout=3.0):
	global g_ser
	global g_log
	g_ser.timeout = timeout
	g_ser.write(data); g_ser.flush();
	rcv = g_ser.read(10)
	if len(rcv) > 0:
		g_log.WriteText("Received: " + rcv + "\r\n")
	return rcv


def read_R3_soft_version():
	global g_log
	version = send_and_read6('R03DA5', 0.2)
	if len(version) < 6:
		return None
	return version

def read_R0():
	r0 = send_and_read6('R00DA5', 0.2)
	if len(r0) < 6:
		return None
	return r0
	
def read_R1():
	r1 = send_and_read6('R01DA5', 0.2)
	if len(r1) < 6:
		return None
	return r1

def read_R2():
	r2 = send_and_read6('R02DA5', 0.2)
	if len(r2) < 6:
		return None
	return r2

def _read_RadarData():
	global g_log
	return 0

# 超时后用一下
def clear_read_buf(x, timeout=0.05):
	global g_log
	global g_ser
	g_ser.timeout = timeout
	g_log.WriteText("Received: " + g_ser.read(x) + "   ,but by clear-buf\r\n")

