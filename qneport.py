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


from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPen)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsPathItem, QGraphicsTextItem)

class QNEPort(QGraphicsPathItem):
    (NamePort, TypePort) = (1, 2)
    (Type) = (QGraphicsItem.UserType +1)

    def __init__(self, parent):
        super(QNEPort, self).__init__(parent)

        self.label = QGraphicsTextItem(self)
        self.radius_ = 4
        self.margin = 3

        path = QPainterPath()
        path.addEllipse(-self.radius_, -self.radius_, 2*self.radius_, 2*self.radius_);
        self.setPath(path)

        self.setPen(QPen(Qt.darkRed))
        self.setBrush(Qt.red)

        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        self.m_portFlags = 0
        self.isOutput_ = False

        self.m_block = None
        self.m_connections = []


    def __del__(self):
        #print("Del QNEPort %s" % self.name)

        for connection in self.m_connections:
            if connection.port1():
                connection.port1().removeConnection(connection)
            if connection.port2():
                connection.port2().removeConnection(connection)
            if self.scene():
                self.scene().removeItem(connection)


    def setName(self, name):
        self.name = name
        self.label.setPlainText(name)


    def setIsOutput(self, isOutput):
        self.isOutput_ = isOutput

        if self.isOutput_:
            self.label.setPos(-self.radius_ - self.margin - self.label.boundingRect().width(),
                -self.label.boundingRect().height()/2);
        else:
            self.label.setPos(self.radius_ + self.margin,
                -self.label.boundingRect().height()/2);



    def setNEBlock(self, block):
        self.m_block = block


    def setPortFlags(self, flags):
        self.m_portFlags = flags

        if self.m_portFlags & self.TypePort:
            font = self.scene().font()
            font.setItalic(True)
            self.label.setFont(font)
            self.setPath(QPainterPath())
        elif self.m_portFlags & self.NamePort:
            font = self.scene().font()
            font.setBold(True)
            self.label.setFont(font)
            self.setPath(QPainterPath())


    def setPtr(self, ptr):
        self.m_ptr = ptr


    def type(self):
        return self.Type


    def radius(self):
        return self.radius_


    def portName(self):
        return self.name


    def isOutput(self):
        return self.isOutput_


    def block(self):
        return self.m_block


    def portFlags(self):
        return self.m_portFlags


    def ptr(self):
        return self.m_ptr;


    def addConnection(self, connection):
        self.m_connections.append(connection)


    def removeConnection(self, connection):
        try:
            self.m_connections.remove(connection)
        except: pass


    def connections(self):
        return self.m_connections


    def isConnected(self, other):
        for connection in self.m_connections:
            if connection.port1() == other or connection.port2() == other:
                return True

        return False


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            for connection in self.m_connections:
                connection.updatePosFromPorts()
                connection.updatePath()

        return value
