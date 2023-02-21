#!/Users/dengjinxi/mambaforge/envs/yuki/bin/python
# -*- coding: UTF-8 -*-

from pathlib import Path
import os

path = "../checkout_tool/"
p1 = Path(path)
print(p1)

p2 = os.path.realpath(path)
print(p2)
