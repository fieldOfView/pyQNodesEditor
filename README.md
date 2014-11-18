pyQNodesEditor
==============

pyQt5 port of ALGOholic's QNodesEditor
See ALGOholic for more information:
http://algoholic.eu/qnodeseditor-qt-nodesports-based-data-processing-flow-editor/

Port to Python3 pyQt5
Note: Saving/Loading is currently not implemented

The fov_dev branch has the following changes from the original:

* Implements "shift-click" to select multiple blocks
* Implements zooming in/out of node graph
* Selected blocks jump to the front
* Ports are moved halfway into the block
* Blocks are slightly transparant to show underlying connections
  when blocks overlap
* Uses system colors
