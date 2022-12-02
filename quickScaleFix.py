# quickScaleFix.py - Python Script

# DESCRIPTION: Tool for quick scale adjustment
# REQUIRE: Python3
# AUTHOR: BulinThira - GitHub

import maya.cmds as mc
import math

def scaleLayout():
    if mc.window('scaleLayout_window', q=True, ex=True):
        mc.deleteUI('scaleLayout_window', window=True)
    mc.window('scaleLayout_window', title='Quick scale adjustment')
    mc.columnLayout(adj=True)
    
    mc.frameLayout(label='Scale by Unit', bgc=(0.1, 0.5, 0.5))
    mc.rowLayout(numberOfColumns=4)
    mc.text(label='source')
    mc.textField('source_TF', w=150)
    mc.button(label='Get', w=50, c=getSource)
    mc.button(label='Create Ruler', w=100, c=createSourceRuler)
    mc.setParent('..')
    
    mc.rowLayout(numberOfColumns=4)
    mc.text(label='target ') 
    mc.textField('target_TF', w=150)
    mc.button(label='Get', w=50, c=getTarget)
    mc.button(label='Create Ruler', w=100, c=createTargetRuler)
    mc.setParent('..')
    
    mc.button('ss_but', label='Set scale', c=scaleSetting)
    
    mc.showWindow('scaleLayout_window')
    mc.window('scaleLayout_window', e=True, wh=(350,150))
    
    
def msRuler(*args):
    #ruler = mc.polyCube()
    mc.polyCube(n='msRuler', d=0.5)
    mc.move(0,0.5,0, 'msRuler')
    mc.move(0,0,0, "msRuler.scalePivot","msRuler.rotatePivot", absolute=True)
    
def rulerShader(*args):
    shd = mc.shadingNode("lambert", asShader=True)
    
def getSource(*args):
    sels = mc.ls(sl=True)
    
    if sels:
        mc.textField('source_TF', e=True, tx=sels[0])
    else:
        mc.textField('source_TF', e=True, tx='')
    
def getTarget(*args):
    sels = mc.ls(sl=True)
    
    if sels:
        mc.textField('target_TF', e=True, tx=sels[0])
    else:
        mc.textField('target_TF', e=True, tx='')
        
def createSourceRuler(*args):
    sourceAttr = mc.textField('source_TF', q=True, tx=True)
    
    mc.circle(nr=(0,1,0), c=(0,0,0), n='source_ruler_base', r=10, ch=0)
    mc.circle(nr=(0,1,0), c=(0,0,0), n='source_ruler_measure', r=6, ch=0)
    mc.circle(nr=(0,1,0), c=(0,0,0), n='source_ruler_head', r=8, ch=0)
    
    mc.parentConstraint('source_ruler_base','source_ruler_head', mo=True, st='y', weight=1)
    mc.parentConstraint('source_ruler_base','source_ruler_measure', mo=True, st='y', weight=1)
    
    mc.setAttr('source_ruler_base.tx', lock=True)
    mc.setAttr('source_ruler_base.ty', lock=True)
    mc.setAttr('source_ruler_base.tz', lock=True)
    
    mc.setAttr('source_ruler_head.tx', lock=True)
    mc.setAttr('source_ruler_head.tz', lock=True)
    
    mc.setAttr('source_ruler_measure.tx', lock=True)
    mc.setAttr('source_ruler_measure.tz', lock=True)
    
    mc.scaleConstraint('source_ruler_base','source_ruler_head', mo=True, weight=1)
    mc.scaleConstraint('source_ruler_base','source_ruler_measure', mo=True, weight=1)
    
    sourceGroup = mc.group('source_ruler_base','source_ruler_head','source_ruler_measure', n='sourceRuler_grp')
    
    tX_source = mc.getAttr(f'{sourceAttr}.translateX')
    tY_source = mc.getAttr(f'{sourceAttr}.translateY')
    tZ_source = mc.getAttr(f'{sourceAttr}.translateZ')
    
    mc.setAttr(f'{sourceGroup}.translateX', tX_source)
    #mc.setAttr(f'{sourceGroup}.translateY', tY_source
    # in case obj isn't on the ground, can be unbypass if wanted.
    mc.setAttr(f'{sourceGroup}.translateZ', tZ_source)
    mc.delete('source_ruler_measure')

def createTargetRuler(*args):
    targetAttr = mc.textField('target_TF', q=True, tx=True)
    
    mc.circle(nr=(0,1,0), c=(0,0,0), n=f'{targetAttr}_ruler_base', r=10, ch=0)
    mc.circle(nr=(0,1,0), c=(0,0,0), n=f'{targetAttr}_ruler_head', r=8, ch=0)
    
    mc.parentConstraint(f'{targetAttr}_ruler_base',f'{targetAttr}_ruler_head', mo=True, st='y', weight=1)
    mc.setAttr(f'{targetAttr}_ruler_base.tx', lock=True)
    mc.setAttr(f'{targetAttr}_ruler_base.ty', lock=True)
    mc.setAttr(f'{targetAttr}_ruler_base.tz', lock=True)
    
    mc.setAttr(f'{targetAttr}_ruler_head.tx', lock=True)
    mc.setAttr(f'{targetAttr}_ruler_head.tz', lock=True)
    
    mc.scaleConstraint(f'{targetAttr}_ruler_base',f'{targetAttr}_ruler_head', mo=True, weight=1)
    targetGroup = mc.group(f'{targetAttr}_ruler_base',f'{targetAttr}_ruler_head', n=f'{targetAttr}Ruler_grp')
    
    tX_target = mc.getAttr(f'{targetAttr}.translateX')
    tY_target = mc.getAttr(f'{targetAttr}.translateY')
    tZ_target = mc.getAttr(f'{targetAttr}.translateZ')
    
    mc.setAttr(f'{targetGroup}.translateX', tX_target)
    #mc.setAttr(f'{targetGroup}.translateY', tY_target
    # in case obj isn't on the ground, can be unbypass if wanted.
    mc.setAttr(f'{targetGroup}.translateZ', tZ_target)
    
    
def scaleSetting(*args):
    source = mc.textField('source_TF', q=True, tx=True)
    target = mc.textField('target_TF', q=True, tx=True)
    
    
    sourceLen = mc.getAttr('source_ruler_head.translateY')
    targetLen = mc.getAttr(f'{target}_ruler_head.translateY')
    targetScale = (1/sourceLen)*targetLen
    targetRealScale = 1/targetScale
    
    print(targetRealScale)
    
    mc.setAttr(f'{target}.scaleX', targetRealScale)
    mc.setAttr(f'{target}.scaleY', targetRealScale)
    mc.setAttr(f'{target}.scaleZ', targetRealScale)
    
    #mc.group(f'{target}', n=f'{target}_grp')
    # to set zero attributes
    


scaleLayout()