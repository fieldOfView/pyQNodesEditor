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


from PySide6.QtCore import (Qt, QPointF)
from PySide6.QtGui import (QBrush, QPen, QPainterPath)
from PySide6.QtWidgets import (QGraphicsItem, QGraphicsPathItem)

class QNEConnection(QGraphicsPathItem):
    (Type) = (QGraphicsItem.UserType +2)

    def __init__(self, parent):
        super(QNEConnection, self).__init__(parent)

        self.setPen(QPen(Qt.black, 2))
        self.setBrush(QBrush(Qt.NoBrush))
        self.setZValue(-1)

        self.m_port1 = None
        self.m_port2 = None

        self.pos1 = QPointF()
        self.pos2 = QPointF()


    def __del__(self):
        #print("Del QNEConnection")
        pass


    def delete(self):
        if self.m_port1:
            self.m_port1.removeConnection(self)
        if self.m_port2:
            self.m_port2.removeConnection(self)
        self.m_port1 = None
        self.m_port2 = None
        self.scene().removeItem(self)


    def setPos1(self, pos):
        self.pos1 = pos


    def setPos2(self, pos):
        self.pos2 = pos


    def setPort1(self, port):
        self.m_port1 = port
        self.m_port1.addConnection(self)


    def setPort2(self, port):
        self.m_port2 = port
        self.m_port2.addConnection(self)


    def updatePosFromPorts(self):
        self.pos1 = self.m_port1.scenePos()
        self.pos2 = self.m_port2.scenePos()


    def updatePath(self):
        path = QPainterPath()
        path.moveTo(self.pos1)

        dx = self.pos2.x() - self.pos1.x()
        dy = self.pos2.y() - self.pos1.y()

        ctr1 = QPointF(self.pos1.x() + dx * 0.25, self.pos1.y() + dy * 0.1)
        ctr2 = QPointF(self.pos1.x() + dx * 0.75, self.pos1.y() + dy * 0.9)

        path.cubicTo(ctr1, ctr2, self.pos2)
        self.setPath(path)


    def type(self):
        return self.Type


    def port1(self):
        return self.m_port1


    def port2(self):
        return self.m_port2

