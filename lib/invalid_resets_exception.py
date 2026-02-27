class InvalidResetsException(Exception):
    def __init__(self):
        self.message = 'Invalid Resets - over maximum or below 0 not allowed'
