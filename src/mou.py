import os

class Platform:
    def __init__(self, filename, path):
        self.loadPlugins(filename, path)

    def loadPlugins(self, file, path):
        for filename in os.listdir("moudles"):
            if filename == file:
                self.runPlugin(filename, path)

    def runPlugin(self, filename, path):
        plugin = __import__("moudles."+filename+'.main', fromlist=['main'])
        plugin.run(path)
