from coco_sdecb import keywords

kw2code = {}
code2kw = {}

for kw in keywords:
    print(kw)
    kw2code[kw[0]] = kw[1]
    code2kw[kw[1]] = kw[0]

print(kw2code)
print(kw2code.keys())
print(code2kw)
print(code2kw.keys())
