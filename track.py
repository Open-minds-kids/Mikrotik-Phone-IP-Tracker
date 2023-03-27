import asyncio
import re
import subprocess

# Use regular expressions to match phone numbers and IP addresses in the log file
phone_number_regex = re.compile(r'\b0\d{9}\b')
ip_address_regex = re.compile(r'\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)')

# Initialize the list of online IP addresses
online_ips = []

async def check_log_file():
    while True:
        # Open the log file in read mode
        with open('/var/log/mikrotik.log', 'r') as f:
            # Read the last 100 lines of the log file
            log_contents = f.readlines()[-100:]

        # Use regular expressions to match phone numbers and IP addresses in the new lines of the log file
        phone_numbers = set()
        ip_addresses = set()
        for line in log_contents:
            # Extract the phone number and IP address from the log entry
            phone_number_match = phone_number_regex.search(line)
            ip_address_match = ip_address_regex.search(line)

            if phone_number_match is not None:
                phone_numbers.add(phone_number_match.group(0))

            if ip_address_match is not None:
                ip_addresses.add(ip_address_match.group(1))

        # Create a dictionary mapping phone numbers to IP addresses
        phone_ip_dict = {}
        for line in log_contents:
            phone_number_match = phone_number_regex.search(line)
            ip_address_match = ip_address_regex.search(line)

            if phone_number_match is not None and ip_address_match is not None:
                phone_ip_dict[phone_number_match.group(0)] = ip_address_match.group(1)

        # Ping each IP address in the list and check if it's reachable
        online_phones = []
        tasks = []
        for phone, ip_address in phone_ip_dict.items():
            tasks.append(asyncio.create_task(ping_ip_address(phone, ip_address)))

        results = await asyncio.gather(*tasks)
        for phone, online in results:
            if online:
                online_phones.append(phone)
            else:
                # If the IP address is unreachable, remove it from the online IPs list
                if ip_address in online_ips:
                    online_ips.remove(ip_address)

        # Print out any new online IP addresses
        new_online_ips = list(set(phone_ip_dict.values()) & set(ip_addresses) - set(online_ips))
        if new_online_ips and '192.168.1.25' not in new_online_ips:
            print('New online IP addresses:', new_online_ips)

            # Update the list of online IP addresses
            online_ips.extend(new_online_ips)

            # Print out the list of online phone numbers
            print('Online phone numbers:', online_phones)

        await asyncio.sleep(5)

async def ping_ip_address(phone, ip_address):
    ping_process = await asyncio.create_subprocess_exec('ping', '-c', '1', ip_address, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await ping_process.communicate()
    online = ping_process.returncode == 0
    return phone, online

async def check_internet_connection():
    while True:
        ping_process = await asyncio.create_subprocess_exec('ping', '-c', '1', '8.8.8.8', stdout=asyncio.subprocess.PIPE)
        stdout, _ = await ping_process.communicate()
        if ping_process.returncode == 0:
            print('Internet is up')
        else:
            print('Internet is down')

        await asyncio.sleep(5)

