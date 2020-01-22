class Commands(object):
    def __init__(self):
        """
        """
        pass

    @property
    def initialize(self):
        """
        main UI init
        """
        returnStr = 'self.win = cmds.window("animBuddyWin", width = 1000, title = "Anim Buddy")\n'
        returnStr += 'filePath = os.path.dirname(os.path.abspath(__file__))\n'
        returnStr += 'imagesPath = os.path.join(filePath, "images")\n'
        returnStr += 'self.undoChunk = False\n'
        returnStr += 'self.imagesPath = imagesPath\n'
        returnStr += 'cmds.frameLayout("main", labelVisible = False, borderVisible = False, bgs = True, width = 10, marginHeight = 0, marginWidth = 0, labelIndent = 0, collapsable = False)\n'
        return returnStr

    @property
    def runUI(self):
        """
        running UI
        """
        returnStr = 'allowedAreas = ["top", "bottom"]\n'
        returnStr += 'cmds.toolBar("abToolBar", area="bottom", content=self.win, allowedArea=allowedAreas)'
        return returnStr
