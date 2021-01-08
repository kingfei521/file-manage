import os

# 字节转换
def format_size(bytes):
    try:
        bytes = float(bytes)
        KB = bytes / 1024

    except:
        return 'Erroe'

    if KB >= 1024:
        M = KB / 1024
        if M >= 1024:
            G = M / 1024
            return "%.1fGB" %(G)
        else:
            return "%.1fMB" %(M)
    else:
        return "%.1fKB" % (KB)