# BASIC utils
A collection of python scripts for processing BASIC program files for
vintage computers.
## Global options: `<command> <function> [<options>] [<infile>] [<outfile>]`  
* `-a`/`--address`: set starting address for tokenized code
* `-h`/`--help`: display function level help info
* `-i`/`--input`: input file name
* `-o`/`--output`: output file name
## Supported Machines
### Tandy/Radio Shack Color Computer 1, 2, and 3 and Dragon 32/64: coco.py
#### General options
* `-b`/`--basic`: select basic dialect (cb, ecb, decb, secb, sdecb, dragon, ddos)
* `-c`/`--cassette`: tokenized files in cassette format
* `-d`/`--disk`: tokenized file in disk format
#### `d`/`detokenize`
Convert a tokenized BASIC program into text (text output only)
#### `h`/`help`
Print command level help summary
#### `p`/`pack`
Make a BASIC program take as little space as possible. Allows for certain optimizations.
##### Options
* `-D`/`--fix-data`: avoid/fix DATA statement bug
* `-P`/`--point`: convert zero (0) constants to "."
* `-X`/`--hex`: convert integer constants from 0-65535 to hex (&HXXXX) form
* `-k`/`--token-len`: line length is computed from tokenized form
* `-m`/`--maxline`: set maximum line length
* `-t`/`--text`: output as text file
* `-x`/`--text-len`: line length is computed from text form        
#### `ri`/`reid`
Transform variable names. This allows source code with long
meaningful variable names to fit the restrictions of BASIC. It
will also obfusticate existing variable names.
##### Options
* `-t`/`--text`: output as text file
#### `rn`/`renum`/`renumber`
Adjust line numbers
##### Options
* `-s`/`--start`: starting line number
* `-t`/`--text`: output as text file
* `-v`/`--interval`: line number interval
#### `t`/`tokenize`
Convert BASIC program in text form to tokenized form (tokenized output only)
#### `u`/`unpack`
Split lines and add whitespace for readability (text output only)
##### Options
* `-w`/`--no-whitespace`: do not add unnecessary whitespace
