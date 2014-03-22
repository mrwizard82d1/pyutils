"""Removes the BOM from files."""
"""Module to remove BOM from a file (in-place)."""


import codecs
import sys


for filename in sys.argv:
    with open(filename) as raw_in:
        with_bom = raw_in.read()
    no_bom = with_bom
    candidate_bom = with_bom[:3]
    if candidate_bom in [codecs.BOM_UTF8, codecs.BOM_UTF16_BE,
                         codecs.BOM_UTF16_LE, codecs.BOM_UTF32_BE,
                         codecs.BOM_UTF32_LE]:
        no_bom = with_bom[3:]
    with open(filename, "wt") as out_stream:
        out_stream.write(no_bom)

