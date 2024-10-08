# Folder synchronization
A basic folder synchronization CRUD API implemented in Python3.x. User defines source/replica/log folder paths and synchronization interval in seconds. A copy of the source folder is maintained at the source path.

Command line arguments:

--source [source directory path]

--replica [replica directory path]

--log [log directory path]

--interval [synchronization interval]

The interval argument is optional and the default value is set to 10 (seconds).

Copy and modify the following command to execute the script:

python3 script.py --source [SOURCE] --replica [REPLICA] --log [LOG] --interval [INTERVAL]
