import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        self.list = []
        self.identity = \
            garlicsim.general_misc.persistent.CrossProcessPersistent()
        self.clock = 0

        
    def inplace_step(self):
        self.clock += 1
        
        
    @staticmethod
    def create_root():
        return State()
    