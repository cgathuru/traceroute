import platform
import sys
import subprocess
import re
import csv
import time
import statistics

__author__ = 'Charles'


def main():
    domain = sys.argv[1] if len(sys.argv) > 1 else "www.google.ca"
    frequency = sys.argv[2] if len(sys.argv) > 2 else 1
    multiplicity = sys.argv[3] if len(sys.argv) > 3 else 1
    command = 'tracert'
    if platform.system() != 'Windows':
        command = 'traceroute'

    print('command is ' + command)
    output = subprocess.check_output([command, domain])
    decode_out = output.decode("utf-8")
    lines = decode_out.split('\n')
    # p = re.compile('(\d)|(\d+\sms)|([A-za-z\.]+)|(\*)|(\[[0-9\\.]+\])')
    ip_p = "((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))"
    time_pattern = "\d+\sms"
    hops_p = "\d[\s]{2,}"
    i = 0
    hops = 0
    ip_list = list()
    avg_ttl = list()
    for line in lines:
        if line:
            print("Line {}".format(i) + " " + line)
            if len([match[0] for match in re.findall(hops_p, line)]) > 0:
                ip = [match[0] for match in re.findall(ip_p, line)]
                # ip_list.append(str(ip).strip('[]').strip('\'\''))
                ip_list.append(ip[0])
                print("IP is " + str(ip[0]))
                times = re.findall(time_pattern, line)
                avg_ttl.append(times[0].rstrip('ms'))
                hops += 1
                print('Found {} ip matches'.format(len(ip)))
                print('Found {} time matches'.format(len(times)))
        i += 1

    print("Total hops: {}".format(hops))
    print("Ips are:")
    print(ip_list)
    print("Times are:")
    # avg_ttl = list(map(int, avg_ttl))

    with open(domain + '.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Route Number', 'Date', 'Time', 'Destination', 'Route', 'Route TTL', 'Num Hops'])
        ips = ', '.join(ip_list)
        print(ips)
        writer.writerow(['1', time.strftime("%x"), time.strftime("%X"), domain, ', '.join(ip_list),
                         ', '.join(avg_ttl), hops])


if __name__ == '__main__':
    main()
