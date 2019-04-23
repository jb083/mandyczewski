#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from new_note import new_note
from deploy import deploy


if __name__ == "__main__":
    sys.stderr.write("mandyczewski 0.2.3\n")
    
    if len(sys.argv) == 1:
        from gen_html import gen_html
        gen_html()
    elif sys.argv[1] == "gen":
        from gen_html import gen_html
        gen_html()
    elif sys.argv[1] == "new":
        new_note()
    elif sys.argv[1] == "deploy":
        deploy()
        
