import sys
import re

line=re.compile('^([0-9]+) .*$')
a=sys.stdin.read().split('\n')
for b in a:
    match = line.match(b)
    if match:
        ln = int(match[1])
        print(b)
    else:
        ln = ln+1
        print(ln, b)
        
    
