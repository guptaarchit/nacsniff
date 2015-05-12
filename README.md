# nacsniff
A simple network sniffer and scanner built in python.


###Usage
It is pretty simple, but it requires super user privileges and a linux system.

```
   sudo python main.py	
```

The program requires some other python packages as well.

* wxpython: The GUI is built with wxpython
* python-nmap: Uses python-nmap to issue nmap commands to scan the network and collect host information
* netifaces: Loads the interface list
* scapy: Needed to aquire the underlying network details (Network Mask and Address)


On ```Ubuntu``` you can install the dependencies as:

```
sudo apt-get install python-scapy python-wxgtk2.8 python-netifaces
```

##Disclaimer
Built while learning python. Code is not pretty. May have hidden bugs.

Some buttons work now. More on the way.

Uses a lot of third party code snippets.

Feedback
-----------------
Open an issue to report a bug or request a new feature. All contributions are welcome.

