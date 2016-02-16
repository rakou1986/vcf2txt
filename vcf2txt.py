#!/usr/bin/env python
#coding: cp932

"""
F-02EのNX!電話帳がエクスポートするvcfファイルから名前などのテキストと電話番号とメールアドレスを救出して印刷が簡単なプレーンテキストに書き出すスクリプト

usage: $ python vcf2txt.py src.vcf dst.txt
"""

import sys

separator = "---------------------"
out = [separator]
with open(sys.argv[1], "rb") as f:
  lines = f.readlines()

units = []
unit = []
buf = ""
for line in lines:
  line = line.strip()
  if "END:VCARD" in line:
    units.append(unit)
    unit = []
    continue
  if "ENCODING=QUOTED-PRINTABLE" in line:
    if line.endswith("="):
      buf = line
    else:
      unit.append(line)
    continue
  if buf:
    buf = buf + line
    if buf.endswith(";;;;"):
      buf = buf.replace("==", "=")
      unit.append(buf)
      buf = ""
    continue
  if line.startswith("TEL") or line.startswith("EMAIL"):
    unit.append(line)
    continue

for unit in units:
  for element in unit:
    if "ENCODING=QUOTED-PRINTABLE" in element:
      bytes_str = element.split("PRINTABLE:")[1].replace(";", "").strip("=")
      if not bytes_str:
        continue
      bytes_ = []
      for byte_str in bytes_str.split("="):
        exec("""b = '\\x%s'""" % byte_str)
        bytes_.append(b)
      bytes_ = "".join(bytes_)
      out.append(bytes_.decode("utf-8").encode("cp932"))
    if element.startswith("TEL"):
      out.append(element.split(":")[-1])
    if element.startswith("EMAIL"):
      out.append(element.split(":")[-1])
  out.append("\n" + separator)

with open(sys.argv[2], "w") as f:
  f.write("\n".join(out))
