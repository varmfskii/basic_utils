import sys

from gwbasic import basica, ega, pcjr, sperry

from msbasic.options import Options as BaseOptions


class Options(BaseOptions):
    keywords = basica.keywords
    remarks = basica.remarks

    def subopts(self, other):
        (o, a) = other
        dialects = {
            "basica": (basica.keywords, basica.remarks),
            "ega": (ega.keywords, basica.remarks),
            "pcjr": (pcjr.keywords, basica.remarks),
            "sperry": (sperry.keywords, basica.remarks),
        }
        if o in ["-b", "--basic"]:
            if a in dialects.keys():
                self.keywords, self.remarks = dialects[a]
            elif a == "help":
                print("Supported dialects:")
                for key in dialects.keys():
                    print(f'\t{key}')
                sys.exit(0)
            else:
                sys.stderr.write(f'Unsupported dialect: {a}\n')
                sys.stderr.write("--basic=help to list available dialects")
                sys.exit(2)
        else:
            self.unused.append(other)


if __name__ == "__main__":
    sys.stderr.write("This is a library")
