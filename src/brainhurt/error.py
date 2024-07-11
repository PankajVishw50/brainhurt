

class ExhaustiveOperationHandlingError(Exception):
    def __init__(self, message=''):
        self.message = 'Exhaustive handling of operations %s' % message
        super().__init__(self.message)

