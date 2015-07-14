# explain-py
short script to make reading man pages less painful (now in Python flavor)

The Gist
========

This is a Python implementation of a small C program I wrote a few months ago called explain.  Explain is a command line tool that takes in a command with options and prints out what those options do, straight from the man page.  This new Python version also allows 'general searching,' which I'll talk about below.

The original, C version of explain [can be found here.](https://github.com/andysalerno/explain)

I no longer plan on updating the C version.  Explain-py is the new explain.

Installing
==========

This is up to you.  What I do is put the two files (explain and ManParser.py) in a folder I made, ~/.scripts/explain, and create a symlink from ~/.scripts/explain/explain to /usr/local/bin.

Examples
========

(coming soon, this readme not finished yet)
