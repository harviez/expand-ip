#
#Input format : 
#192.168.1.0-192.168.1.3
#
#Output
#192.168.1.0
#192.168.1.1
#192.168.1.2
#192.168.1.3
#

import socket
import struct
import re
import os
import csv

#-------------------------------------------------------------------------------
# Exceptions that can be thrown
class InvalidIPAddress(ValueError):
    "The ip address given to ipaddr is improperly formatted"

#-------------------------------------------------------------------------------
def ipaddr_to_binary(ipaddr):
    """
    A useful routine to convert a ipaddr string into a 32 bit long integer
    """
    # from Greg Jorgensens python mailing list message 
    q = ipaddr.split('.')
    return reduce(lambda a,b: long(a)*256 + long(b), q)
   
#-------------------------------------------------------------------------------
def binary_to_ipaddr(ipbinary):
    """
    Convert a 32-bit long integer into an ipaddr dotted-quad string
    """
    # This one is from Rikard Bosnjakovic
    return socket.inet_ntoa(struct.pack('!I', ipbinary))
    
#-------------------------------------------------------------------------------
def iprange(ipaddr):
    """
    Creates a generator that iterates through all of the IP addresses.
    The range can be specified in multiple formats.

        "192.168.1.0-192.168.1.255"    : beginning-end
        "192.168.1.0/24"               : single ip
    
    """
    # Did we get the IP address in the span format? 
    span_re = re.compile(r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   # The beginning IP Address
                             \s*-\s*
                             (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   # The end IP Address
                          ''', re.VERBOSE)

    res = span_re.match(ipaddr)
    if res:
        beginning = res.group(1)
        end = res.group(2)
        return span_iprange(beginning, end)
                                 
    # Did we get a single ip? 
    single_re = re.compile(r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*$   # The IP Address
                          ''', re.VERBOSE)

    res = single_re.match(ipaddr)
    if res:
		addr = res.group(1)
		ip_range=[]
		ip_range.append(addr)
		return ip_range


#-------------------------------------------------------------------------------
def span_iprange(beginning, end):
    """
    Takes a beginning and an end IP and creates a generator
    """
    b = ipaddr_to_binary(beginning) 
    e = ipaddr_to_binary(end) 

    while (b <= e):
        yield binary_to_ipaddr(b)
        b = b + 1
#    return


reader = csv.reader(open("range.txt"))
filename = "expanded.txt"
num_ips = 0


for lines in reader:
	print "lines: " + str(lines) + "\n"       #type list[a,b]
	for line in lines:
                print "Outer Counter" + "\n"
		line = line.replace(" ","")			#removes spaces that precedes every element after first element
		print "Line is: " + line  + "\n"   #type string[a]
		x = iprange(line)
		print "range is: " + str(x)
    		for ip in x:
                    print "Inner counter: " + "\n"
                    num_ips += 1
                    with open(filename, mode='a') as a_file:
                            a_file.write(ip+'\n')
                            a_file.close()


print "total ips: " + str(num_ips)

    
