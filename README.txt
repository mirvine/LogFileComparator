===============================================================================
Log File Comparator
Author: Mark Irvine (mark@irvinesonline.org)
Date:   12 April 2012
===============================================================================

License:
===============================================================================
Creative Commons CC BY-NC-SA license 
http://creativecommons.org/licenses/by-sa/3.0/

Description:
===============================================================================
Log File Comparator is a tool for comparing log files.

Comparing the content of two logs files is a common operation in automated 
software testing.
First, you run the program and  capture the log file.
This becomes your baseline 'known good' log file
Later, after the software has been modified, you rerun the program and again 
capture the log file.
By comparing the latest log file with the baseline log file you can detect 
errors or unintended behavioural changes.

This approach can be problematic if the log files contain data which changes
for each program run. For example, if the log file contains a timestamp on each
line, which is common for log files, then and simple comparison will identify 
all the lines as changed.

The Log File Comparator taclkes this problem in two ways:

1. Mask any dynamic data that we are not interested in
2. calculate the 'edit distance' between the two log files after the logs are 
masked.

1. Masking:
===============================================================================
The application under test generates log files with some data elements are 
somewhat random and unpredictable. By masking these dynamic elements, we can 
then safely compare the lines.

Masking involves removing dynamic data such as:
 - date/time stamps
 - raw memory locations
 - network port numbers

Example:

	NTR1 12/02/07 19:20:40 <I> [01] Data tx to MP [0x83a9ec8,01:000:01]:len=0020,0x839eb94
	
gets masked to:
	
	###################### <I> [01] Data tx to MP [#,01##]#len=0020,#

2. Edit Distance
===============================================================================
I started with the edit distance solution shown by @PeterUdacity
The edit distance function was initially modified to measure the distance between two lists.
I then modified this to use a caching mechanism which allows for much improved performance.

So the edit distance indicates there are mismatched lines in the log file.

Running the sample script.
===============================================================================

There are 4 sample log files in the test-data folder.
Log files 1 and 2 are closely matched except for the dynamic data, and they
have an edit distance of 0

Logfiles 3 and 4 represent a typical failure where logfile 4 is significantly
different to log file 3, and so it shows an edit distance of 50.

To run the comparator on these files, run the file test_log_files.py
