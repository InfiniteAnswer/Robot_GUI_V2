class RuntimeState():
    def __init__(self):
        # Define control flags
        self.homeax1 = False
        self.homeax2 = False
        self.homeax3 = False
        self.homeax4 = False
        self.printing =False
        self.magazineinitialised = False
        self.paletteinitialised = False
        self.fileloaded = False
        self.printpause =False
