from LogFileComparator import LogFileComparator

c = LogFileComparator()

log1 = open('test_data/log1.txt','r').read()
log2 = open('test_data/log2.txt','r').read()

ed = c.edit_distance_logs(log1,log2,mask_len=23)

print "Edit distance between log1.txt and log2.txt:", ed

"""
NTR1 12/02/02 11:12:38 <I> [01] HSCB Call Failed
"""
log3 = open('test_data/log3.txt','r').read()
log4 = open('test_data/log4.txt','r').read()

ed =  c.edit_distance_logs(log3,log4,mask_len=23)
print "Edit distance between log3.txt and log4.txt:", ed
