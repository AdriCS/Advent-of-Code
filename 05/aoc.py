#!/usr/bin/env python
# -*- coding: utf-8 -*-

https://stackoverflow.com/questions/53634190/python-regex-that-matches-char-followed-preceded-by-same-char-but-uppercase-lowe




You may do it with PyPi regex module (note it will work with Java, PCRE (PHP, R, Delphi), Perl, .NET, but won't work with ECMAScript (JavaScript, C++ std::regex), RE2 (Go, Google Apps Script)) using

(\p{L})(?!\1)(?i:\1)

See the regex demo and a proof it works in Python:

import regex
rx = r'(\p{L})(?!\1)(?i:\1)'
print([x.group() for x in regex.finditer(rx, ' aA, Aa, bB, cC but not aB, aa, AA, aC, Ca')])
# => ['aA', 'Aa', 'bB', 'cC']

The solution is based on the inline modifier group (?i:...) inside which all chars are treated in a case insensitive way while other parts are case sensitive (granted there are no other (?i) or re.I).

Details

    (\p{L}) - any letter captured into Group 1
    (?!\1) - a negative lookahead that fails the match if the next char is absolutely identical to the one captured in Group 1 - note that the regex index is still right after the char captured with (\p{L})
    (?i:\1) - a case insensitive modifier group that contains a backreference to the value of Group 1 but since it matches it in a case insensitive way it could match both a and A - BUT the preceding lookahead excludes the variant with the alternate case (since the preceding \1 matched in a case sensitive way).

What about a re solution?

In re, you cannot make part of a pattern optional as (?i) in any part of a pattern makes all of it case insensitive. Besides, re does not support modifier groups.

You may use something like

import re
rx = r'(?i)([^\W\d_])(\1)'
print([x.group() for x in re.finditer(rx, ' aA, Aa, bB, cC but not aB, aa, AA, aC, Ca') if x.group(1) != x.group(2)])

See the Python demo.

    (?i) - set the whole regex case insensitive
    ([^\W\d_]) - a letter is captured into Group 1
    (\1) - the same letter is captured into Group 2 (case insensitive, so Aa, aA, aa and AA will match).

The if x.group(1) != x.group(2) condition filters out the unwanted matches.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

mport re
import string

pattern = re.compile('|'.join([''.join(i) for i in zip(list(string.ascii_lowercase), list(string.ascii_uppercase))])
pattern.search(your_text)

pattern = '|'.join([''.join(i) for i in zip(list(string.ascii_uppercase), list(string.ascii_lowercase))] + [''.join(i) for i in zip(list(string.ascii_lowercase), list(string.ascii_uppercase))])