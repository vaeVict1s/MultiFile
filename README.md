# multi_file

`multi_file` module purpose is to provide the user with a `MultiFile` class.

`MultiFile` can be used both as a standalone object and in a with statement,  
and the signature of its `__init__` is:  
`__init__(self, *files, logging = False, permissive = False)`  

This class is meant to be used to parallel-read lines from an arbitrary number of files.  
file paths are passed as single strings, when the class is instantiated,  
and they are read line by line in this order.  
At any iteration, the `MultiFile` object behaviour is regulated by two bool parameters.  
The `permissive` parameter, if set to `True` makes the iteration break if one file ends.  
Otherwise, the iteration continues on the files which still have content to be read.  
The `logging` parameter, if set to `Ture` makes the `MultiFile` object log on the stderr  
the list of files which finishes at some point during the iteration.  


