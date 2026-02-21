class InconsistentLevelInteractionException(Exception):
    def __init__(self):
        self.message = 'Interaction inconsistent with character counts in level games'
