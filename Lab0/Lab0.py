import socket 

ip = socket.gethostbyname('www.google.com')
print(ip)

'''
1.  Reflection Questions (All answered in one paragraph)
    Its improper access with limited access control meaning its at risk
    of any network based attack. It also gives the answer in the next question, 
    input validation (there is none), access control (very limited unless you spend 
    extensive time setting it up), and protocol awareness.
4.  While its neat to set up a local network with python, as someone with 
    relatively little programming knowledge I found it quite confusing as to how 
    we were supposed to set this up and it took me a very long time to figure out 
    the minor changes required to the code. 
'''