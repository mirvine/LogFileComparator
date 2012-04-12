import re
"""
Log file comparison tool.
Author: Mark Irvine (mark@irvinesonline.org)
Date:   12 April 2012
"""

class LogFileComparator:
    """
    Performs a 'edit distance' calculation on two text files.
    
    The intended use of this function is to compare two log files as part of an 
    automated test in order to determine if there are any significant differences
    between the current log file, and a baseline 'known good' log file.
    
    The expectation is that if the edit distance is low, the the differences are 
    probably not significant.
    
    Prior to measuring the edit distance, the data is masked so as to ignore any
    differences cause by dynamic elements. Examples include:
     - date/time stamps
     - memory addresses
     - network port numbers
    
    Once we mask these data items, we can expect the edit distance to be very
    low if there is no significant difference between the two log files.
    
    """
    def __init__(self):
        self.cache = {}


    def cached_execution(self,code):
        """
        Stores the results of a calculation in order to eliminate repeated
        calculation of identical data. This improves the performance of the 
        program.
        """
        cache = self.cache
        if code in cache:
            return cache[code]
        else:
            result = eval(code)
            cache[code]=result
            return result
        
    def edit_distance(self,s,t):
        """
        >>> c = LogFileComparator()
        >>> c.edit_distance(['the','cat'], ['the','dog'])
        1
        
        >>> l1 = ['One','two','mismatch','four','five','six','seven','eight','nine','ten','alpha','beta']
        >>> l2 = ['One','two','three','four','five','six','mismatch','eight','nine','ten','alpha']
        >>> c.edit_distance(l1, l2) 
        3
        >>> c.edit_distance(l1, []) 
        12
        >>> c.edit_distance([], l1) 
        12
        >>> c.edit_distance([], [])
        0
        """
        if len(s) == 0: return len(t)
        if len(t) == 0: return len(s)
        
        if s[0]==t[0]:
            return self.cached_execution('self.edit_distance(' + str(s[1:]) +',' + str(t[1:]) + ')')
    
        else:
            return min( self.cached_execution('1 + self.edit_distance(' + str(s[1:]) +',' + str(t[1:]) + ')'),
                        self.cached_execution('1 + self.edit_distance(' + str(s)     +',' + str(t[1:]) + ')'),
                        self.cached_execution('1 + self.edit_distance(' + str(s[1:]) +',' + str(t)     + ')'))
    
    def edit_distance_lines(self,l1,l2, mask_len=10):
        """
        >>> c = LogFileComparator()
        >>> l1 = 'xxx xxx three four five six seven eight nine ten mismatch beta'
        >>> l2 = 'One two three four five six seven mismatch nine ten alpha '
        >>> c.edit_distance_lines(l1, l2) 
        3
        """
        l1 = self.mask(l1,mask_len)
        l2 = self.mask(l2,mask_len)
        l1 = l1.split()
        l2 = l2.split()
        return self.edit_distance(l1,l2)
        
    def edit_distance_logs(self,log1,log2, mask_len=10):
        log1 = log1.split('\n')
        log2 = log2.split('\n')
        
        log1=[self.mask(n,mask_len) for n in log1]
        log2=[self.mask(n,mask_len) for n in log2]
        return self.edit_distance(log1,log2)
    
    def mask(self,line, length):
        """
        >>> c = LogFileComparator()
        >>> line = 'NTR1 12/02/07 19:20:40 <I> [01] Data tx to MP [0x83a9ec8,01:000:01]:len=0020,0x839eb94'
        >>> c.mask(line,5)
        '#####12/02/07 19## <I> [01] Data tx to MP [#,01##]#len=0020,#'
        
        >>> line = '12345'
        >>> c.mask(line,10)
        '##########'
        """
        line = re.sub(r'0x\w*', '#', line)
        line = re.sub(r':\d*', '#', line)
        masked_line =  '#'*length + line[length:]
        return masked_line

if __name__=='__main__':
    import doctest
    doctest.testmod(verbose = True)


