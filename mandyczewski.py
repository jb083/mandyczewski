#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from new_note import new_note
from deploy import deploy

version = "0.4.0"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--version":
            print("mandyczewski {}".format(version))
            sys.exit()
        elif sys.argv[1] == "--help":
            print("mandyczewski {}\n".format(version))
            import helpdoc
            helpdoc.println()
            sys.exit()
        
    
    sys.stderr.write("mandyczewski {}\n".format(version))
    
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
    else:
        sys.stderr.write("\nInvalid arguments or options. Use '--help' to get help.\n")
        
    
        
