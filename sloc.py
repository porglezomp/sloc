#!/usr/bin/python3

import sys
import os

C = 0
PY = 1
modes = {"c": C, "h": C, "py": PY}
extensions = {C: "C", PY: "Python"}

message = """{file}:
Language: {lang}
Lines: {lines}
Lines of code: {code}
Blank lines: {blank}
Lines of comments: {comments}
Lines of preprocessor: {pre}"""

if len(sys.argv) < 2:
    print("Usage: sloc <files>")

total_lines = 0
total_code = 0
total_blanks = 0
total_comments = 0
total_pre = 0

num_files = 0
skipped = []
for fname in sys.argv[1:]:
    # Find the file extension and set the mode based on that
    extension = fname.split(".")[-1]
    if extension not in modes:
        skipped.append(fname)
        continue
    mode = modes[extension]

    lines = 0
    code = 0
    blanks = 0
    comments = 0
    preprocessor = 0

    num_files += 1

    with open(fname, "r") as f:
        block_comment = False
        for line in f:
            line = line.strip()

            lines += 1
            line_is_comment = False
            line_is_preprocessor = False
            line_is_blank = line == ""

            if not line_is_blank:
                if mode == PY:
                    if line[0] == "#":
                        line_is_comment = True
                elif mode == C:
                    if block_comment:
                        line_is_comment = True
                        # TODO: Handle code on same line as block comment
                        # /* stuff happens on this line */ code();
                        if "*/" in line:
                            block_comment = False
                    elif line[:2] == "//":
                        line_is_comment = True
                    # TODO: Handle code on same line as block comment                        
                    if "/*" in line:
                        block_comment = True
                        line_is_comment = True
                    elif line[0] == "#":
                        line_is_preprocessor = True

            if line_is_blank:
#                print("Blank")
                blanks += 1
            elif line_is_comment:
#                print("Comment: {}".format(line))
                comments += 1
            elif line_is_preprocessor:
#                print("Preprocessor: {}".format(line))
                preprocessor += 1
            else:
#                print("Code: {}".format(line))
                code += 1

    total_lines += lines
    total_code += code
    total_blanks += blanks
    total_comments += comments
    total_pre += preprocessor
    
    if (num_files > 1):
        print()
    print(message.format(
        file=fname,
        lang=extensions[mode],
        lines=lines,
        blank=blanks,
        pre=preprocessor,
        comments=comments,
        code=code
   ))

if num_files > 1:
    print()
    print(message.format(
        file="Total",
        lang="NA",
        lines=total_lines,
        code=total_code,
        blank=total_blanks,
        comments=total_comments,
        pre=total_pre
    ))

if skipped:
    print()
    if len(skipped) == 1:
        print("Skipped {}".format(skipped[0]))
    else:
        print("Skipped {} files:".format(len(skipped)))
        for file in skipped:
            print(file)
    print("""The extensions are unrecognized. \
Please file a report, or even better, contribute \
code to handle these file types.""")
