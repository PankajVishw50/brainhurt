import array
import sys 

from .iota import iota
from .error import ExhaustiveOperationHandlingError

class BrainHurt:
    """An interpretter and debugger 
    for the programming language called 'BrainFuck' 
    """


    # Masks
    SUCCESS = iota(reset=True)
    FAIL = iota()
    DEBUG = iota()

    # Operation
    "><+-[].,"
    NEXT_OP = iota(reset=True)
    PREV_OP = iota()
    ADD_OP = iota()
    SUB_OP = iota()
    LOOP_START_OP = iota()
    LOOP_END_OP = iota()
    OUTPUT_OP = iota()
    INPUT_OP = iota()
    COUNTER_OP = iota()



    def __init__(
            self,
            input=list(),
            debug=False,
            conf=None,
            input_callback=None,
            output_callback=None,
    ) -> None:
        self.OUTPUT = list()
        self.INPUT = list()

        self.MEMORY_RETURN = 10

        self.DEBUG_MODE = False
        self.debug_points = []
        self.debug_pointer = 0

        self.MEMORY_LENGTH = 65535

        self.programm = list()
        self.programm_pointer = 0
        self.open_loop = list()

        self.memory = array.array('Q', [0] * self.MEMORY_LENGTH)
        self.pointer = 0
        self.ITEM_UPPER_BOUND = (2**(self.memory.itemsize*8)-1)

        self.input_callback = input_callback
        self.output_callback = output_callback

        self.load_input(input)
        self.conf_debug(conf, debug)

    def conf_debug(self, conf=None, debug=True):
        if conf:
            self.debug_points = conf

        self.DEBUG_MODE = debug

    def load_input(self, buffer: str|list):
            if type(buffer) == str:
                self.INPUT.extend([ord(letter) for letter in buffer])
            elif type(buffer) == list:
                self.INPUT.extend(buffer)

    def reset(self) -> None:
        self.programm = list()

    def navigate_memory(self, direction):
        if direction != 1 and direction != -1:
            raise ValueError('direction args accepts either 1 or -1 but %s provided' % direction)

        if direction == 1:
            if (self.pointer-1) >= self.MEMORY_LENGTH:
                self.pointer = 0

            self.pointer += 1

        else:
            if self.pointer <= 0:
                self.pointer = self.MEMORY_LENGTH
            self.pointer -= 1

        return self.pointer

    def get_word_as_op(self, letter) -> int:

        if self.COUNTER_OP != 8:
            raise ExhaustiveOperationHandlingError()

        match letter:
            case '>':
                return self.NEXT_OP
            
            case '<':
                return self.PREV_OP
            
            case '+':
                return self.ADD_OP
            
            case '-':
                return self.SUB_OP
            
            case '[':
                return self.LOOP_START_OP
            
            case ']':
                return self.LOOP_END_OP
            
            case ',':
                return self.INPUT_OP

            case '.':
                return self.OUTPUT_OP
            
            case _:
                return None

    def get_input(self):
        if callable(self.input_callback):
            return self.input_callback()

        for letter in sys.stdin.read() + chr(0):
            self.INPUT.append(ord(letter))

    def send_output(self):
        if callable(self.output_callback):
            return self.output_callback(self.OUTPUT.pop(0))
        
        print(self.OUTPUT.pop(0), end='')

        
    def load_programm(self, buffer: str, debugs: dict=None) -> None:
        self.reset()
        line = 0
        word = -1
        open_loop = list()

        for letter in buffer:
            if letter == '\n':
                line += 1
                word = -1
                continue

            word += 1
            op = self.get_word_as_op(letter)
            meta = {}

            if op is None:
                continue

            elif op == self.LOOP_START_OP:
                open_loop.append((len(self.programm), ))
            elif op == self.LOOP_END_OP:
                if len(open_loop) <= 0:
                    raise SyntaxError('there is no open loop tag for corresponded close loop tag at line (%i, %i)' % (line, word))
                open_tag = open_loop.pop()
                self.programm[open_tag[0]][2]['loop'] = len(self.programm) 
                meta['loop'] = open_tag[0]

        
            self.programm.append((op, (line, word), meta))


        if len(open_loop) > 0:
            raise SyntaxError('No close tag provided for open loop')

    def load_file(self, file_path):
        
        try:
            with open(file_path, 'r') as buffer:
                raw_data = buffer.read()
        except Exception as e:
              raise ValueError('No file found at %s' % file_path)
        
        self.load_programm(raw_data)

    def add(self, pointer) -> int:

        if self.memory[pointer] >= self.ITEM_UPPER_BOUND:
            self.memory[pointer] = 0
        else:
            self.memory[pointer] += 1

        return self.memory[pointer]
    
    def sub(self, pointer) -> int:

        if self.memory[pointer] <= 0:
            self.memory[pointer] = self.ITEM_UPPER_BOUND
        else:
            self.memory[pointer] -= 1

        return self.memory[pointer]


    def execute(self):
        # print('%i | %i - %i  - executing' % (self.programm_pointer, self.pointer, self.memory[self.pointer]))
        # print(self.INPUT)
        if self.COUNTER_OP != 8:
            raise ExhaustiveOperationHandlingError()

        statement = self.programm[self.programm_pointer]
        programm_pointer = self.programm_pointer
        self.programm_pointer += 1


        match statement[0]:
            case self.NEXT_OP:
                self.navigate_memory(1)
                return (self.SUCCESS, )
            
            case self.PREV_OP:
                self.navigate_memory(-1)
                return (self.SUCCESS, )
            
            case self.ADD_OP:
                self.add(self.pointer)
                return (self.SUCCESS, )
            
            case self.SUB_OP:
                self.sub(self.pointer)
                return (self.SUCCESS, )
            
            case self.LOOP_START_OP:
                if self.memory[self.pointer] <= 0:
                    self.programm_pointer = statement[2]['loop']+1
                return (self.SUCCESS, )
            
            case self.LOOP_END_OP:
                self.programm_pointer = statement[2]['loop']
                return (self.SUCCESS, )
            case self.INPUT_OP:
                if len(self.INPUT) <= 0:
                    self.programm_pointer -= 1
                    return self.get_input()

                self.memory[self.pointer] = self.INPUT.pop(0)                
                return (self.SUCCESS, )

            case self.OUTPUT_OP:
                self.OUTPUT.append(chr(self.memory[self.pointer]))
                self.send_output()
                return (self.SUCCESS, )
            
            case _:
                raise SyntaxError('Unexpected operator %s' % statement[0])      

    def execute_programm(self) -> tuple:
        """Execute the programm 
        Returns an tuples whose first element 
        tells about the return type.
        """

        next_debug = None
        if len(self.debug_points) > self.debug_pointer:
            next_debug = self.debug_points[self.debug_pointer]


        while self.programm_pointer < len(self.programm):
            programm = self.programm[self.programm_pointer]
            if (self.DEBUG_MODE and next_debug and next_debug[0] <= programm[1][0] and next_debug[1] <= programm[1][1]):
                self.debug_pointer += 1
                return (self.DEBUG, self.around_memory(), self.programm[self.programm_pointer])

            self.execute()

        return (self.SUCCESS, )
    
    def around_memory(self, pointer=None):
        pointer = pointer or self.pointer

        memory = array.array('I')
        mid = self.MEMORY_RETURN // 2
        index = 1

        while index <= mid:
            if (self.pointer-index) < 0:
                index -= 1
                break 

            memory.append(
                self.memory[self.pointer-index]
            )
            index += 1

        starting = self.pointer - index
        index = 0

        while len(memory) < self.MEMORY_RETURN:
            if (self.pointer+index) >= self.MEMORY_LENGTH:
                break 

            memory.append(
                self.memory[self.pointer + index]
            )
            index += 1

        return (starting, pointer, memory, )

