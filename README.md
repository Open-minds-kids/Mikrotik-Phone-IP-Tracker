# Mikrotik-Phone-IP-Tracker

This is a program that checks the Mikrotik router logs for new phone numbers and IP addresses, pings each IP address to check if it's online and keeps track of online IPs and phone numbers.

Requirements:

    Python 3.7 or later
    Mikrotik router with logging enabled
    Linux or macOS operating system

Installation:

    Clone the repository to your local machine
    Install the required Python packages using pip. Run pip install -r requirements.txt
    Edit the ckeckup-withasyc.py file and replace 192.168.1.25 with the IP address of your Mikrotik router
    Run the program using python ckeckup-withasyc.py

Usage:

The program runs continuously and checks the log file every 5 seconds. Whenever a new phone number or IP address is found in the log file, the program pings the IP address to check if it's online. If the IP address is online, the program adds it to the list of online IPs and prints out the new online IP addresses and the phone numbers that are currently online.

To stop the program, press Ctrl+C.

Contributing:

Contributions are welcome. Please create a pull request with your changes.

License:

This program is licensed under the MIT License. See the LICENSE file for details.
