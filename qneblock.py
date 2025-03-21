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


from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPen,
    QFontMetrics)
from PySide6.QtWidgets import (QGraphicsItem, QGraphicsPathItem)

from qneport import QNEPort

class QNEBlock(QGraphicsPathItem):
    (Type) = (QGraphicsItem.UserType +3)

    def __init__(self, parent):
        super(QNEBlock, self).__init__(parent)

        path = QPainterPath()
        path.addRoundedRect(-50, -15, 100, 30, 5, 5);
        self.setPath(path)
        self.setPen(QPen(Qt.darkGreen))
        self.setBrush(Qt.green)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.horzMargin = 20
        self.vertMargin = 5
        self.width = self.horzMargin
        self.height = self.vertMargin


    def __del__(self):
        #print("Del QNEBlock")
        pass


    def delete(self):
        for port in self.ports():
            for connection in port.connections():
                connection.delete()
            port.delete()
        self.scene().removeItem(self)


    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setPen(QPen(Qt.darkYellow))
            painter.setBrush(Qt.yellow)
        else:
            painter.setPen(QPen(Qt.darkGreen))
            painter.setBrush(Qt.green)

        painter.drawPath(self.path())


    def addPort(self, name, isOutput = False, flags = 0, ptr = None):
        port = QNEPort(self)
        port.setName(name)
        port.setIsOutput(isOutput)
        port.setNEBlock(self)
        port.setPortFlags(flags)
        port.setPtr(ptr)

        fontmetrics = QFontMetrics(self.scene().font())
        size = fontmetrics.size(Qt.TextSingleLine, name)
        width = size.width()
        height = size.height()
        if width > self.width - self.horzMargin:
            self.width = width + self.horzMargin
        self.height += height

        path = QPainterPath()
        path.addRoundedRect(-self.width/2, -self.height/2, self.width, self.height, 5, 5)
        self.setPath(path)

        y = -self.height / 2 + self.vertMargin + port.radius()
        for port_ in self.childItems():
            if port_.type() != QNEPort.Type:
                continue

            if port_.isOutput():
                port_.setPos(self.width/2 + port.radius(), y)
            else:
                port_.setPos(-self.width/2 - port.radius(), y)
            y += height;

        return port


    def addInputPort(self, name):
        self.addPort(name, False)


    def addOutputPort(self, name):
        self.addPort(name, True)


    def addInputPorts(self, names):
        for name in names:
            self.addInputPort(name)


    def addOutputPorts(self, names):
        for name in names:
            self.addOutputPort(name)


    def clone(self):
        block = QNEBlock(None)
        self.scene().addItem(block)

        for port_ in self.childItems():
            block.addPort(port_.portName(), port_.isOutput(), port_.portFlags(), port_.ptr())

        return block


    def ports(self):
        result = []
        for port_ in self.childItems():
            if port_.type() == QNEPort.Type:
                result.append(port_)

        return result

    def type(self):
        return self.Type
