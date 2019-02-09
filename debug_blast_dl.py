import os
import platform
print(platform.system())
print(platform.architecture()[0])
try:
    print(os.environ["PROCESSOR_ARCHITEW6432"])
except KeyError:
    print("True platform not found")
