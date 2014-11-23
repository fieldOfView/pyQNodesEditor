# Copyright (c) 2014, ALDO HOEBEN
# Copyright (c) 2012, STANISLAW ADASZEWSKI
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of STANISLAW ADASZEWSKI nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL STANISLAW ADASZEWSKI BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from PySide.QtCore import (Qt, QObject, QEvent, QSizeF, QRectF, QPointF)
from PySide.QtGui import (QGraphicsItem, QGraphicsSceneMouseEvent)

from qneblock import QNEBlock
from qneport import QNEPort
from qneconnection import QNEConnection

class QNodesEditor(QObject):
    def __init__(self, parent):
        super(QNodesEditor, self).__init__(parent)

        self.connection = None


    def install(self, scene):
        self.scene = scene
        self.scene.installEventFilter(self)


    def itemAt(self, position):
        items = self.scene.items(QRectF( position - QPointF(1,1) , QSizeF(3,3) ))

        for item in items:
            if item.type() > QGraphicsItem.UserType:
                return item

        return None;


    def eventFilter(self, object, event):
        if event.type() == QEvent.GraphicsSceneMousePress:

            if event.button() == Qt.LeftButton:
                item = self.itemAt(event.scenePos())
                if item and item.type() == QNEPort.Type:
                    self.connection = QNEConnection(None)
                    self.scene.addItem(self.connection)

                    self.connection.setPort1(item)
                    self.connection.setPos1(item.scenePos())
                    self.connection.setPos2(event.scenePos())
                    self.connection.updatePath()

                    return True

            elif event.button() == Qt.RightButton:
                item = self.itemAt(event.scenePos())

                if item and (item.type() == QNEConnection.Type or item.type() == QNEBlock.Type):
                    if item.type() == QNEConnection.Type:
                        item.delete()
                    elif item.type() == QNEBlock.Type:
                        item.delete()

                    return True


        elif event.type() == QEvent.GraphicsSceneMouseMove:
            if self.connection:
                self.connection.setPos2(event.scenePos())
                self.connection.updatePath()

                return True


        elif event.type() == QEvent.GraphicsSceneMouseRelease:
            if self.connection and event.button() == Qt.LeftButton:
                item = self.itemAt(event.scenePos())
                if item and item.type() == QNEPort.Type:
                    port1 = self.connection.port1()
                    port2 = item

                    if port1.block() != port2.block() and port1.isOutput() != port2.isOutput() and not port1.isConnected(port2):

                        self.connection.setPos2(port2.scenePos())
                        self.connection.setPort2(port2)
                        self.connection.updatePath()
                        self.connection = None

                        return True

                self.connection.delete()
                self.connection = None
                return True

        return super(QNodesEditor, self).eventFilter(object, event)

