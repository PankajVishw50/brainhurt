
# BrainHurt 

This is an Interpreter and debugger for the programming language `BrainFuck` written in `Python`


## Features and Notes
* Need to end input with `cntrl + z` on windows and `cmd + d + d` on mac
* Returns `0` as `EOF`
* Generally would have an array of `65535` elements each being an unsigned integer of `8 bytes`

## How To Use

**Install the package** 

```powershell
pip install brainhurt
```

You can either call it Programmiticaly in script or direclty from terminal 

**From Command Line**
```powershell
python -m brainhurt file_name.bf
```

**From Python Script**
```py
from brainhurt import BrainHurt

brainhurt = BrainHurt()
brainhurt.load_file('file_name.bf')
brainhurt.execute_programm()
```

## Debugging
In order to use debug mode First you need to do these 2 things 
* Set debug points
* turn on debug mode


**What is debug points?**  
It is an list of tuples with 2 items first is the line number and the other is character number in that line.  
_Example._
```py
debug_points = [
    (0, 3),
    (3, 10),
    (100, 2),
    # ....
]
```

setting debug mode
```py
brainhurt = BrainHurt(
    debug=True,
    conf=debug_points
)

# or you can also do it later  
brainhurt.conf_debug(debug_points, True)
```

Now whenever you will execute your programm using `execute_programm` method the code execution will stop at breaking point and return an tuple with information
```py
# Example of return tuple in debug mode
print(brainhurt.execute_programm())

# The code execution would stop at the next breakpoint

"""
OUTPUT:
(
    2, # it is return type, could be debug, success etc..

    (
        0, #memory offset
        2, #memory pointer
        [0, 0, 10, 0, 0] #memory 
    ),

    (
        5 #programm pointer ,
    )

"""
```

Now if you would try to see the return value of same method when debug mode is off you will get something like this 
```py
brainhurt.conf_debug(None, False)
print(brainhurt.execute_programm())

# Whole programm would be executed while ignoring all the debug breakpoints

"""
OUTPUT::
(
    0, # it is return type 
)
"""
```

## IO Operations
Both input and output are stored inside python list and Follows FIFO. 

### INPUT
**How can you provide input**  
One way to provide input it to pass an list or string in the contructor
```py
brainhurt = BrainHurt(input='pankaj') # passing string 
# OR 
brainhurt = BrainHurt(input=['p','a', 'n', 'k', 'a', 'j']) # passing list
```

other way is to pass list or string in the `load_input` method
```py
brainhurt.load_input('pankaj')
# OR
brainhurt.load_input(['p', 'a', 'n', 'k'])
brainhurt.load_input(['a', 'j'])
```

By default if input array is empty and programm is asking for input, then our interpreter would use the python's `sys.stdin.read` method to read for input and would store it in input extending with `0` as `EOF`

If you want to change this default behaviour you can pass an `callback(function)` to the constructor as keyword argument `input_callback` which will be executed whenever programm wants input and input array is empty.  
_Example..._
```py
brainhurt = BrainHurt(input_callback=some_function)
# OR
brainhurt.input_callback = some_function
```

### OUTPUT
By default whenever the programm wants to output something, interpreter would output to the standard output using python's `print` function 

If you want to change this default behaviour, you can pass an `callback(fuction)` to the constructor as keyword argument `output_callback` which should accept 1 argument. Once setted, whenever your programm wants to output something this callback function would be executed with the data passed to it.  
