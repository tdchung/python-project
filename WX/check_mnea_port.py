import os
import time
import datetime
import serial
import serial.tools.list_ports

list_baudrate = [9600, 14400, 19200, 38400, 57600, 115200, 128000]
# list_baudrate = [9600, 115200]


##############################################################################
# Log file
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, 'Check_nmea_{}.txt'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))

def create_log_file():
    return os.path.join(LOG_DIR, 'Check_nmea_{}.txt'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))
# log
def log(data, log_file=None):
    with open(LOG_FILE if not log_file else log_file, 'a+') as f:
        f.write(str(data))


##############################################################################
def get_list_comports():
    return [comport.device for comport in serial.tools.list_ports.comports()]


def is_nmea_port(ser):
    ser.reset_input_buffer()
    data = ser.read(500)

    # print(f'RAW: {data}')
    list_nmea = []
    buff_str = None
    try:
        buff_str = data.decode("utf-8")
        # print(f'Str: {buff_str}')
    except Exception as e:
        print("decode excetption: ", str(e))
    
    if not buff_str:
        # raw data is not correct
        return False, list_nmea
    
    list_msg = buff_str.split('\n')
    for msg in list_msg[1:-1]:
        if msg[0] != '$':
            print(f'Not NMEA message: {msg}')
            return False, list_nmea
        list_nmea.append(msg.split(',')[0][1:])
    return True, list(dict.fromkeys(list_nmea))


def save_nmea_log(ser, log_file):
    ser.reset_input_buffer()

    for _ in range(100):
        data = ser.readline()
        buff_str = None
        try:
            buff_str = data.decode("utf-8")
            # print(f'Str: {buff_str}')
        except Exception as e:
            print("decode excetption: ", str(e))
        print(f'Str: {buff_str}')
        log(buff_str, log_file)
    

    pass


if __name__ == '__main__':
    list_ports = get_list_comports()

    for port in list_ports:
        # if port == '/dev/ttyUSB0':
            for baudrate in list_baudrate:
                lfile = create_log_file()
                print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Start checking in port {port} - {baudrate}')

                ser = serial
                try:
                    ser = serial.Serial(port, baudrate, timeout=15)
                    if ser.isOpen():
                        ser.close()
                    ser.open()
                    ser.isOpen()
                    # print ("port is opened!")
                except Exception as e:
                    print("Serial excetption: ", str(e))
                    ser = None
                
                if ser:
                    res, list_nmea = is_nmea_port(ser)
                    if res:
                        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Port {port} - {baudrate} is GPS NMEA data')
                        print(list_nmea)
                        log(f'GPS NMEA port found: {port} {baudrate}\r\n', lfile)
                        log(f'List NMEA: {list_nmea}\r\n', lfile)
                    
                        save_nmea_log(ser, lfile)
                    else:
                        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Port {port} - {baudrate} is NOT NMEA port')
