from . import BrainHurt
import sys



program = """
+++++ +++++ initialize counter (cell #0) to 10
[ set the next four cells to 70 100 30 and 10 respectively
> +++++ ++ add 7 to cell #1
> +++++ +++++ add 10 to cell #2
> +++ add 3 to cell #3
> + add 1 to cell #4
<<<< - decrement counter (cell #0)
]

> ++ . print 'H' (H = ASC (72))
> + . print 'e' (e = ASC (101))
+++++ ++ . print 'l'
. print 'l'
+++ . print 'o'

> ++ . print ' '

<< +++++ +++++ +++++ . print 'W'
> . print 'o'
+++ . print 'r'
----- - . print 'l'
----- --- . print 'd'
> + . print '!'
> . print '\n'
"""

brainhurt = BrainHurt()
brainhurt.load_programm(program)
# brainhurt.execute_programm()

brainhurt.conf_debug([
    (2, 1),
    (5, 4),
], True)

while True:
    result = brainhurt.execute_programm()
    print(result)

    if result[0] == brainhurt.SUCCESS or result[0] == brainhurt.FAIL:
        break