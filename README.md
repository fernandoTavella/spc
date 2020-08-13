# **SPC - Simple Port Scanner**
    
A simple port scanner made it in python3 to check open ports from 1-1024 on a single hostname.   
Supports the following features: 
   - [Iteration 1] Open port detection
   - [Iteration 2] Select the amount of threads, default 5 
   - [Iteration 3] Firewall evasion using a random value over each thread
   - [Iteration 4] Detects if the open port is an HTTP Server 

# Installation
    git clone https://github.com/fernandoTavella/spc.git
    Windows:
        python -m pip install -r requirements.txt
    Unix:
        pip3 install -r requirements.txt

# Requisites
    Python libraries required
    argparse 
    socket 
    multiprocessing 
    time 
    random

# Usage
    PS E:\> python.exe .\port-scanner.py -t 20 -f evil.com
    Starting scanner
    21 open
    25 open
    80 open (http)
    110 open
    143 open
    443 open (http)
    465 open
    587 open
    993 open
    Scanner finished

# Limitations
    The amount of thread creation is limitated by the number of ports to scan