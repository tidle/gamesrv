#!/usr/bin/env python3
import sys

esc = "\x1b"
clear = esc + "[0m" + esc + "[39m"
bold = esc + "[1m"
dim = esc + "[2m"
cyan = esc + "[96m"
red = esc + "[91m"
move = clear + dim
info = clear + cyan
warn = clear + bold + red

f = open("log.txt", "r")

def get_header(line):
    return line.split(" ")[0]

def p(line):
    header = get_header(line)
    if header == "[MOVE]":
        print(move + line, end="")
    if header == "[INFO]":
        print(info + line, end="")
    if header == "[WARN]":
        print(warn + line, end="")

i = f.readline()
while i:
    try:
        mode = sys.argv[1]
    except:
        print("use all, move, info or warn!")
        break
    if mode == "all" or mode == "move":
        p(i)
    elif mode == "info":
        if get_header(i) != "[MOVE]":
            p(i)
    elif mode == "warn":
        if get_header(i) == "[WARN]":
            p(i)
    else:
        print("use all, move, info or warn!")
        break
    i = f.readline()

f.close()
print(clear, end="")
