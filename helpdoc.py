doc = '''\
mandyczewski is a convertor from markdown to HTML.

# Command line argument/option

Default argument/option is 'gen' (i.e. 'gen' is used when there are no argument/option).
    --version
        Print the version of mandyczewski.
    --help
        Print this document.
    new
        Generate a new book in the current directory.
    gen
        Generate HTML files according to the "SUMMARY.toml" file.
'''

def println():
    print(doc, end="")
    
