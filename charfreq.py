#!/usr/bin/env python
import sys, optparse, re

def group(message, window, shift=-1, skipspaces=True):

    if shift == -1:
        shift = window

    if skipspaces:
        message = re.sub("\s+", "", message)

    tokens = []
    i = 0
    while i + window <= len(message):
        tokens += [ message[i:i+window] ]
        i += shift
    return tokens

def frequency(tokens):
    freq = {}
    for token in tokens:
        if token not in freq:
            freq[token] = 1
        else:
            freq[token] += 1

    rank_first = []
    for key in freq:
        rank_first += [(freq[key], key)]

    rank_first.sort(lambda (a,b),(c,d): c-a)
    return rank_first

def main():
    usage = "usage: %prog [options] [YOUR FILE]"
    p = optparse.OptionParser(usage = usage, version='0.1')
    p.add_option('--window', '-w', action="store", type="int", help="Windows Size (Default WINDOW=1)", default=1)
    p.add_option('--roll', '-r', action="store", type="int", help="Rolling Window (Shift window by ROLL rather than WINDOW)", default=-1)
    p.add_option('--skipspaces', '-s', action="store_true", help="Skip Space Characters [ \\t\\r\\n]", default=False)
    p.add_option('--graph', '-g', action="store_true", help="Create an ASCII graph of the results.", default=False)
    options, arguments = p.parse_args()

    if len(arguments) != 1:
        print "Error: Needs 1 file for processing character frequencies."
        return 1

    message = file(arguments[0]).read()
    tokens = group(message, options.window, options.roll, options.skipspaces)
    rank_first = frequency(tokens)

    if options.graph == False:
        for (f, key) in rank_first:
            if options.window == 1:
                print "%s [%2x]: %4s" % (key, ord(key), f)
            else:
                print "%s: %4s" % (key, f)
    else:
        for (f, key) in rank_first:
            if options.window == 1:
                print "%s [%2x]: %4s : %s" % (key, ord(key), f, "X"*f)
            else:
                print "%s: %4s : %s" % (key, f, "X"*f)

    return 0

if __name__ == '__main__':
    sys.exit(main())
