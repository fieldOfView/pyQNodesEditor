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
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPen,
    QFontMetrics)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPathItem, QGraphicsDropShadowEffect)

from qneport import QNEPort

class QNEBlock(QGraphicsPathItem):
    (Type) = (QGraphicsItem.UserType +3)

    def __init__(self, parent):
        super(QNEBlock, self).__init__(parent)

        self.normalBrush = QApplication.palette().dark()
        normalColor = self.normalBrush.color()
        normalColor.setAlphaF(0.8)
        self.normalBrush.setColor(normalColor)

        self.selectedBrush = QApplication.palette().light()
        selectedColor = self.selectedBrush.color()
        selectedColor.setAlphaF(0.8)
        self.selectedBrush.setColor(selectedColor)

        path = QPainterPath()
        path.addRoundedRect(-50, -15, 100, 30, 5, 5);
        self.setPath(path)
        self.setPen(QPen(Qt.black))
        self.setBrush(self.normalBrush)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.effect = QGraphicsDropShadowEffect(None)
        self.effect.setBlurRadius(8)
        self.effect.setOffset(2,2)
        self.setGraphicsEffect(self.effect)

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
        if self.scene():
            self.scene().removeItem(self)


    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setBrush(self.selectedBrush)
        else:
            painter.setBrush(self.normalBrush)

        painter.drawPath(self.path())


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self.setZValue( 1 if value else 0 )

        return value


    def addPort(self, name, isOutput = False, flags = 0, ptr = None):
        port = QNEPort(self)
        port.setName(name)
        port.setIsOutput(isOutput)
        port.setNEBlock(self)
        port.setPortFlags(flags)
        port.setPtr(ptr)

        fontmetrics = QFontMetrics(self.scene().font());
        width = fontmetrics.width(name)
        height = fontmetrics.height()
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
