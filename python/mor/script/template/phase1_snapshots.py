# -*- coding: utf-8 -*-
import imp

#	STLIB IMPORT
from splib.animation import AnimationManager , animate
from stlib.scene.wrapper import Wrapper

# MOR IMPORT
from mor import animation
from mor.script import ObjToAnimate
from mor.script.sceneCreationUtility import SceneCreationUtility

# Our Original Scene IMPORT
originalScene = '$ORIGINALSCENE'
originalScene = imp.load_source(originalScene.split('/')[-1], originalScene)

# Animation parameters
listObjToAnimate = []
#for $obj in $LISTOBJTOANIMATE:
listObjToAnimate.append(ObjToAnimate('$obj.location',$obj.animFct,objName='$obj.objName',duration=$obj.duration,**$obj.params))
#end for
phase = $PHASE
nbIterations = $nbIterations
paramWrapper = $PARAMWRAPPER

# We create our SceneCreationUtility that will ease our scene transformation
u = SceneCreationUtility()

###############################################################################

def createScene(rootNode):
    print ("Scene Phase :"+str(phase))

    # Import Original scene

    originalScene.createScene(rootNode)
    dt = rootNode.dt
    timeExe = nbIterations * dt

    # Add Animation Manager to Scene
    # (ie: python script controller to which we will pass our differents animations)
    # more details at splib.animation.AnimationManager (https://stlib.readthedocs.io/en/latest/)

    if isinstance(rootNode, Wrapper):
        AnimationManager(rootNode.node)
    else:
        AnimationManager(rootNode)

    # Now that we have the AnimationManager & a list of the node we want to animate
    # we can add an animation to then according to the arguments in listObjToAnimate

    u.addAnimation(rootNode,phase,timeExe,dt,listObjToAnimate)

    # Now that all the animation are defined we need to record there results
    # for that we take the parent node normally given as an argument in paramWrapper

    toFind = []
    for item in paramWrapper:
        path, param = item
        toFind.append(path.split('/')[-1])
    toFind = toFind[0]

    myParent = u.searchNodeInGraphScene(rootNode,toFind)

    # We need rest_position and because its normally always the same we record it one time
    # during the first phase with the argument writeX0 put to True
    if phase == [0]*len(phase):
        myParent.createObject('WriteState', filename="stateFile.state",period=listObjToAnimate[0].params["incrPeriod"]*dt,
                                            writeX="1", writeX0="1", writeV="0")
    else :
        myParent.createObject('WriteState', filename="stateFile.state", period=listObjToAnimate[0].params["incrPeriod"]*dt,
                                            writeX="1", writeX0="0", writeV="0")