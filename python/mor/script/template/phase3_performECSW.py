# -*- coding: utf-8 -*-
import os
import sys
import imp

#   STLIB IMPORT
from stlib.scene.wrapper import Wrapper
from mor.script import sceneCreationUtility
from mor.script.sceneCreationUtility import SceneCreationUtility

# MOR IMPORT
from mor.wrapper import MORWrapper
from mor.wrapper import writeScene

# Our Original Scene IMPORT
originalScene = '$ORIGINALSCENE'
originalScene = imp.load_source(originalScene.split('/')[-1], originalScene)

# Scene parameters
nbrOfModes = $NBROFMODES
paramWrapper = $PARAMWRAPPER
toKeep = $TOKEEP
packageName = '$PACKAGENAME'

# We had these differents parameters to be able to save the scene
for item in paramWrapper:
    path, param = item
    param['nbrOfModes'] = $NBROFMODES
    param['save'] = True
    param['toKeep'] = $TOKEEP

# We create our SceneCreationUtility that will ease our scene transformation
u = SceneCreationUtility()

def createScene(rootNode):

    print(  "This Scene will crash : it is NORMAL\n\
            Its purpose is only to save the scene (thanks to MORWrapper)\n\
            To create the package with it afterward")

    # Import Original Scene
    # Here we use a wrapper (MORWrapper) that will allow us (with MORreplace)
    # to modify the initial scene and get informations on its structures
    # For more details on the process involved additionnal doc are with :
    #       - mor.wrapper.MORWrapper
    #       - mor.script.sceneCreationUtility

    originalScene.createScene(MORWrapper(rootNode, u.MORreplace, paramWrapper))  # 1

    # Search the nodes we are reducing

    toFind = []
    for item in paramWrapper:
        path, param = item
        toFind.append(path.split('/')[-1])

    nodeFound = u.searchInGraphScene(rootNode,toFind)

    # Modify the scene to perform hyper-reduction according
    # to the informations collected by the wrapper

    u.modifyGraphScene(nbrOfModes,nodeFound,paramWrapper,save=True) # 2

    # We collect all the informations during 1 & 2 to be able to create with
    # writeGraphScene a SOFA scene containing only our reduced model that we can instanciate
    # as a whole component with differents usefull argument (translation/rotation/color...)
    # For more details on the process involved additionnal doc are with :
    #       - mor.wrapper.writeScene

    if packageName:
        myMORModel = sceneCreationUtility.myMORModel
        myModel = sceneCreationUtility.myModel

        nodeName = paramWrapper[0][0].split('/')[-1]

        writeScene.writeHeader(packageName)
        modelTransform = writeScene.writeGraphScene(packageName,nodeName,myMORModel,myModel)
        writeScene.writeFooter(packageName,nodeName,modelTransform)