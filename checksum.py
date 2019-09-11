#! /usr/bin/env python3
# coding: utf-8

import hashlib, zlib
from pathlib import Path

filepath = Path('Super Mario World.smc')
chunk = filepath.read_bytes()

# checksum avec différentes tables de hachâge (sha1, md5 et crc32)
checksummer = hashlib.sha1()
checksummer.update(chunk)
sha1sum = checksummer.hexdigest()

checksummer = hashlib.md5()
checksummer.update(chunk)
md5sum = checksummer.hexdigest()

crc32sum = hex(zlib.crc32(chunk) & 0xffffffff)[2:]

print(f"sha1: {sha1sum}\nmd5: {md5sum}\ncrc32: {crc32sum}")