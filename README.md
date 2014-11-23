pyQNodesEditor
==============

Python port of ALGOholic's QNodesEditor  
See ALGOholic for more information:
http://algoholic.eu/qnodeseditor-qt-nodesports-based-data-processing-flow-editor/

This port uses to Python3 PySide  
Note: Saving/Loading is currently not implemented

The fov_dev branch has the following changes from the original:

* Ports can have input, output, both, or no connections
* Implements "rubberband" (multiple) selection
* Select All/Select Inverse
* Press "Del" to delete selected items, instead of right mouse button
* Implements zooming in/out of node graph
* Selected blocks jump to the front
* Ports are moved halfway into the block
* Blocks are slightly transparant to show underlying connections
  when blocks overlap
* Uses system colors
