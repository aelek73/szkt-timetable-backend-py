#!/usr/bin/env python3

import os
import time

def write_log(msg):
    if os.path.exists('logs'):
        os.system('touch logs')
    log_file = open('logs', 'a')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_file.write(current_time,'-',msg)
