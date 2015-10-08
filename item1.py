# Item 1: Know Which Version Of Python You're Using

# Besides using the CLI-switch to get the Python version's info (python --version
# or python3 --version, respectively), the sys module provides access to the
# version info:
#  sys.version: Version string
#  sys.version_info: Tuple containing major, minor, micro, releaselevel and serial
#  components

import sys
print(sys.version)
print(sys.version_info)

# 3.5.0 (v3.5.0:374f501f4567, Sep 13 2015, 02:16:59) [MSC v.1900 32 bit (Intel)]
 # sys.version_info(major=3, minor=5, micro=0, releaselevel='final', serial=0)