from Functions.Utilities.rocketReader import rocketReader


class Rocket:

    def __init__(self, rocketFilePath):
        rocketReader(self, rocketFilePath)
