import argparse
import socket
import multiprocessing
import time
from random import randrange

#Arguments Validation
def check_threads(n):
    number_t = int(n)
    if not 1 < number_t < 1025:
        raise argparse.ArgumentTypeError("{} is an invalid value must be between 1 and 1024".format(number_t))
    return number_t
#Arguments
parser = argparse.ArgumentParser()
parser.add_argument('hostname', type=str,help='Please insert the hostname to scan')
parser.add_argument('-t','--threads',type=check_threads,help='Number of threads to use , default 5 max 1024')
parser.add_argument('-f',action='store_const',const=True,help='Sleeps the threads for some random time (from 0 to 6 seconds)')

#Parse arguments and variables
args = parser.parse_args()
hostname = args.hostname
n_threads = args.threads if args.threads else 5
firewall_timer = True if args.f else False
http_ports = [80,443,8080,8443]

def split(lst, n):
    for i in range(0, n):
        yield lst[i::n]

def scan_ip(host,port_list,sleep_time):
    #Getting the IP from the hostname
    ip_address  = socket.gethostbyname(host)
    http_req_msg = "GET / HTTP/1.1\r\nHost: {}\r\nAccept: text/html\r\n\r\n".format(host)
    for port in port_list:
        time.sleep(sleep_time)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((ip_address, port))
            if result == 0:
                port_msg = "{} open ".format(str(port))
                if port in http_ports:
                    sock.sendall(http_req_msg.encode('UTF-8'))
                    if 'HTTP/1.1' in str(sock.recv(4096), 'utf-8'):
                        port_msg+='(http)'
                print(port_msg)
            sock.close()
        except socket.error:
            print("Couldn't connect to server")
            pass
        except Exception as e:
            raise


def main():
    ports = [p for p in range(1,1025)]
    #Splitting the port list in small chunks according to the thread number
    ports_splitted = list(split(ports,n_threads))
    try:
        process = []
        all_alive = True
        for i in range(0,n_threads):
            sleeped = 0
            if firewall_timer:
                sleeped = randrange(6)
            process.append(multiprocessing.Process(target=scan_ip, args=(hostname,ports_splitted[i],sleeped),daemon=True))
        print("Starting scanner")
        for p in process:
            p.start()
        while all_alive:
            for p in process:
                if not p.is_alive():
                    all_alive = False
                else:
                    all_alive = True
        print('Scanner finished')

    except KeyboardInterrupt:
        for p in process:
            p.terminate()
        print("Keyboard Interrupt terminating scan")

if __name__ == "__main__":
    main()