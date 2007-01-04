"""
<name>Regression Tree</name>
<description>Constructs a tree regression learner and given data a regression tree classifier
</description>
<icon>RegressionTree.png</icon>
<contact>Ales Erjavec (ales.erjavec(@at@)fri.uni-lj.si)</contact> 
<priority>100</priority>
"""

import orange
import orngTree
import OWGUI
import qt
from OWWidget import *
import sys

class OWRegressionTree(OWWidget):
    settingsList=["Name","MinInstCheck", "MinInstVal", "MinNodeCheck", "MinNodeVal,"
                  "MaxMajCheck", "MaxMajVal", "PostMaj", "PostMPCheck", "PostMPVal", "Bin"]
    callbackDeposit=[]
    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, "Regression Tree")
        self.Name="Regression Tree"
        self.MinInstCheck=1
        self.MinInstVal=5
        self.MinNodeCheck=1
        self.MinNodeVal=10
        self.MaxMajCheck=1
        self.MaxMajVal=70
        self.PostMaj=1
        self.PostMPCheck=1
        self.PostMPVal=5
        self.Bin=1
        self.loadSettings()

        self.data=None

        self.inputs=[("Example Table",ExampleTable,self.dataset)]
        self.outputs=[("Learner",orange.Learner),("Classifier",orange.Classifier),("Classification Tree",orange.TreeClassifier)]
        
        ##
        #GUI
        ##
        OWGUI.lineEdit(self.controlArea, self, "Name", box="Learner/Classifier name")
        OWGUI.checkBox(self.controlArea, self, "Bin", label="Binarization", box ="Tree structure")
        
        self.prePBox=OWGUI.widgetBox(self.controlArea, "Pre-Pruning")
        self.postPBox=OWGUI.widgetBox(self.controlArea, "Post-Pruning")

        #OWGUI.checkWithSpin(self.prePBox, self, "Min. instances in leaves: ", 1, 1000,
        #                    "MinInstCheck", "MinInstVal")

        OWGUI.checkWithSpin(self.prePBox, self, "Stop splitting nodes with ", 1, 1000,
                            "MinNodeCheck", "MinNodeVal", " or fewer instances")
        
        #OWGUI.checkWithSpin(self.prePBox, self, "Stop splitting nodes with ", 1, 100,
        #                    "MaxMajCheck", "MaxMajVal", "% of majority class")

        #OWGUI.checkBox(self.postPBox, self, 'PostMaj', 'Recursively merge leaves with same majority class')
        OWGUI.checkWithSpin(self.postPBox, self, "m for m-error pruning ", 0, 1000, 'PostMPCheck', 'PostMPVal')

        OWGUI.button(self.controlArea, self, "&Apply settings",callback=self.setLearner)
        self.setLearner()
        self.resize(100,100)

    def setLearner(self):
        learner=orngTree.TreeLearner(mesure="retis",
                         binarization=self.Bin,
                         mForPruning=self.PostMPCheck and self.PostMPVal,
                         minExamples=self.MinNodeCheck and self.MinNodeVal,
                         storeExamples=1)
        learner.name=self.Name
        self.send("Learner",learner)
        if not self.data:
            return
        
        try:
            classifier=learner(self.data)
            classifier.name=self.Name
            self.send("Classifier",classifier)
            self.send("Classification Tree",classifier)
        except orange.KernelException, (errValue):
            self.error(str(errValue),2)
            print errValue
            self.send("Classifier",None)
            self.send("Classification Tree", None)
        #orngTree.printTxt(classifier)
    
    def dataset(self, data):
        self.data=data
        if data:
            self.setLearner()
        else:
            self.send("Learner",None)
            self.send("Classifier",None)


if __name__=="__main__":
    app=QApplication(sys.argv)
    w=OWRegressionTree()
    data=orange.ExampleTable("../../doc/datasets/housing.tab")
    w.dataset(data)
    app.setMainWidget(w)
    w.show()
    app.exec_loop()
