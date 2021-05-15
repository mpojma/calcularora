from Calculadora_ui import *
from PyQt5.QtGui import *

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
class MainWindow(QtWidgets.QMainWindow, Ui_Calculadora):
#-----------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        
        self.bits=64
        self.currentVal = 0
        # Conectamos los eventos con sus acciones
        self.rb64.toggled[bool].connect (self.on_rb_toggled)
        self.rb48.toggled[bool].connect (self.on_rb_toggled)
        self.rb32.toggled[bool].connect (self.on_rb_toggled)
        self.rb16.toggled[bool].connect (self.on_rb_toggled)
        self.rb8.toggled[bool].connect (self.on_rb_toggled)

        for var in range (64):
            if (var < 10):
                index = "0"+str(var)
            else:
                index = str(var)
            cb = self.findChild(QtWidgets.QCheckBox,"cb_"+index)
            cb.stateChanged[int].connect(self.on_CB_clicked)
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
    def on_rb_toggled(self, checked):
        valor = self.sender().objectName()[2:]
        self.bits = int(valor)
        mask = (1 << self.bits)-1
        self.currentVal &= mask
        self.sbShift.setMaximum(self.bits-1)
        self.show_hide_bits (self.bits, checked)
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbNot_pressed(self):
        for i in range (self.bits):
            self.currentVal = self.currentVal ^ (1 << i)
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbAnd_pressed(self):
        if (""==self.leBinOperator.text()):
            self.leBinOperator.setText("0")
        val = int(self.leBinOperator.text(),16)
        self.currentVal &= val
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbXor_pressed(self):
        if (""==self.leBinOperator.text()):
            self.leBinOperator.setText("0")
        val = int(self.leBinOperator.text(),16)
        self.currentVal ^= val
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbOr_pressed(self):
        if (""==self.leBinOperator.text()):
            self.leBinOperator.setText("0")
        val = int(self.leBinOperator.text(),16)
        self.currentVal |= val
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbAdd_pressed(self):
        if (""==self.leHex_Mat.text()):
            self.leHex_Mat.setText("0")
        val = int(self.leHex_Mat.text(),16)
        self.currentVal += val
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbRest_pressed(self):
        if (""==self.leHex_Mat.text()):
            self.leHex_Mat.setText("0")
        val = int(self.leHex_Mat.text(),16)
        self.currentVal -= val
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbExp_pressed(self):
        if (""==self.leHex_Mat.text()):
            self.leHex_Mat.setText("0")
        val = int(self.leHex_Mat.text(),16)
        self.currentVal = pow(self.currentVal, val)
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbPor_pressed(self):
        if (""==self.leHex_Mat.text()):
            self.leHex_Mat.setText("0")
        val = int(self.leHex_Mat.text(),16)
        self.currentVal *= val
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbDiv_pressed(self):
        if (""==self.leHex_Mat.text()):
            self.leHex_Mat.setText("0")
        val = int(self.leHex_Mat.text(),16)
        self.currentVal = int(self.currentVal / val)
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbSqr_pressed(self):
        if (""==self.leHex_Mat.text()):
            self.leHex_Mat.setText("0")
        val = int(self.leHex_Mat.text(),16)
        self.currentVal = int(pow(self.currentVal, 1.0/val))
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbSalir_clicked (self):
        self.close()
#-----------------------------------------------------------------------------------
    def on_pbRshift_pressed(self):
        shift = self.sbShift.value()
        self.currentVal >>= shift
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_pbLshift_pressed(self):
        shift = self.sbShift.value()
        self.currentVal <<= shift
        self.updateValues("hsub")
#-----------------------------------------------------------------------------------
    def on_leHex_Mat_textEdited(self, arg1):
        self.leHex_Mat.blockSignals(True)
        self.leDecS_Mat.blockSignals(True)
        if (self.leCheck (self.leHex_Mat, arg1, 16, False, False)):
            self.leDecS_Mat.setText(str(int(self.leHex_Mat.text(),16)))
        self.leHex_Mat.blockSignals(False)
        self.leDecS_Mat.blockSignals(False)
#-----------------------------------------------------------------------------------
    def on_leDecS_Mat_textEdited(self, arg1):
        self.leHex_Mat.blockSignals(True)
        self.leDecS_Mat.blockSignals(True)
        if (self.leCheck (self.leDecS_Mat, arg1, 10, True, False)):
            txt = self.leDecS_Mat.text()
            var = ""
            if ('-'!= txt):
                unsigned = int(txt) & 0xFFFFFFFFffffffff
                var = hex(unsigned)[2:]
            if ("" == var):
                var = "0"
            self.leHex_Mat.setText(var)
        self.leHex_Mat.blockSignals(False)
        self.leDecS_Mat.blockSignals(False)
#-----------------------------------------------------------------------------------
    def on_leHex_textChanged (self, arg1):
        self.blockSignals(True)
        if (self.leCheck ( self.leHex, arg1, 16)):
            self.updateValues("sub")
        self.blockSignals(False)
#-----------------------------------------------------------------------------------
    def on_leDSig_textChanged(self, arg1):
        self.blockSignals(True)
        if (self.leCheck (self.leDSig, arg1, 10, True)):
            self.updateValues("hub")
        self.blockSignals(False)
#-----------------------------------------------------------------------------------
    def on_leDUSig_textChanged(self, arg1):
        self.blockSignals(True)
        if (self.leCheck (self.leDUSig, arg1, 10)):
            self.updateValues("hsb")
        self.blockSignals(False)
#-----------------------------------------------------------------------------------
    def on_CB_clicked(self, arg1):
        valor = self.sender().objectName()
        valor = valor[3:]
        try:
            o = int(valor)
            ok = True
        except ValueError:
            ok = False
        if (ok):
            mask = 1
            for i in range(o):
                mask = (mask << 1)
            if (arg1):
                self.currentVal |= mask
            else:
                self.currentVal &= (~mask)
        self.updateValues("hsu")
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
    def show_hide_bits(self, to, show):
        for var in range (0, 64):
            if (var < 10):
                index = "0"+str(var)
            else:
                index = str(var)
            self.findChild(QtWidgets.QCheckBox,"cb_"+index).hide()
            self.findChild(QtWidgets.QLabel,"label_"+index).hide()
        if (show):
            for var in range (0,to):
                if (var < 10):
                    index = "0"+str(var)
                else:
                    index = str(var)
                self.findChild(QtWidgets.QCheckBox,"cb_"+index).show()
                self.findChild(QtWidgets.QLabel,"label_"+index).show()
#-----------------------------------------------------------------------------------
    def leCheck (self, lineEdit, txt, base, signed=False, updateCurrent=True):
        ok = True
        arg = ""
        cp = lineEdit.cursorPosition()
        factor = ""
        if (""!=txt):
            if ((signed)and('-' == txt[0])):
                factor = "-"
            for ch in (txt.lower()):
                if ((('0'<=ch)and('9'>=ch))or((16==base)and('a'<=ch)and('f'>=ch))):
                    arg = arg + ch

            try:
                while ('0' == arg[0]):
                    cp += 1
                    arg = arg[1:]
            except:
                arg = ""
            arg = factor+arg
        if ("" == arg):
            arg = "0"
            cp = cp - (len(txt) - len(arg))
            lineEdit.setText(arg)
        elif (txt != arg):
            cp = cp - (len(txt) - len(arg))
            lineEdit.setText(arg)
        if (updateCurrent):
            try:
                self.currentVal =  (int(arg,base) & 0xFFFFFFFFffffffff)
                ok = True
            except ValueError:
                ok = False
        lineEdit.setCursorPosition(cp)
        return (ok)
#-----------------------------------------------------------------------------------
    def blockSignals(self, block):
        self.leHex.blockSignals(block)
        self.leDSig.blockSignals(block)
        self.leDUSig.blockSignals(block)
        for var in range (64):
                if (var < 10):
                    index = "0"+str(var)
                else:
                    index = str(var)
                self.findChild(QtWidgets.QCheckBox,"cb_"+index).blockSignals(block)
#-----------------------------------------------------------------------------------
    def updateValues(self, updates):
        index=""
        updates = updates.lower()
        if (0 <= updates.find("h")):
            unsigned = self.currentVal
            if (self.bits == 64):   unsigned &= 0xFFFFFFFFffffffff
            elif (self.bits == 48): unsigned &= 0x0000FFFFffffffff
            elif (self.bits == 32): unsigned &= 0x00000000ffffffff
            elif (self.bits == 16): unsigned &= 0x000000000000ffff
            elif (self.bits == 8):  unsigned &= 0x00000000000000ff
            index = hex(unsigned)
            try:
                while (('0' == index[0])or('x' == index[0])):
                    index = index[1:]
            except:
                index = "0"
            self.leHex.setText(index)
        if (0 <= updates.find("s")):
            sig = self.currentVal

            if   ((self.bits == 64)and(0x8000000000000000 & sig)):   sig -= 18446744073709551616
            elif ((self.bits == 48)and(0x0000800000000000 & sig)):   sig -= 281474976710656
            elif ((self.bits == 32)and(0x0000000080000000 & sig)):   sig -= 4294967296
            elif ((self.bits == 16)and(0x0000000000008000 & sig)):   sig -= 65536
            elif ((self.bits ==  8)and(0x0000000000000080 & sig)):   sig -= 256

            self.leDSig.setText(str (sig))

        if (0 <= updates.find("u")):
            unsigned = self.currentVal
            if (self.bits == 64):   unsigned &= 0xFFFFFFFFffffffff
            elif (self.bits == 48): unsigned &= 0x0000FFFFffffffff
            elif (self.bits == 32): unsigned &= 0x00000000ffffffff
            elif (self.bits == 16): unsigned &= 0x000000000000ffff
            elif (self.bits == 8):  unsigned &= 0x00000000000000ff

            self.leDUSig.setText(str (unsigned))

        if (0 <= updates.find("b")):
            for var in range (64):
                if (var < 10):
                    index = "0"+str(var)
                else:
                    index = str(var)
                self.findChild(QtWidgets.QCheckBox,"cb_"+index).setChecked((1 & (self.currentVal >> var)))
#-----------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
