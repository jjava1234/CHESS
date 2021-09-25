class Game():
    def __init__(self):
        self.bPIECES = self.rPIECES = 16 
        self.pColors = [(255,255,255), (0,0,0)]
        self.turn = self.pColors[0]
        self.allMOVES = {}
