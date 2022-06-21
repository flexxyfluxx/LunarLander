# -*- coding: utf-8 -*-
class Toaster(object):
    zustand = ["ungetoastet", "leicht getoastet", "stark getoastet","verbrannt"]        
    name = "Toaster"
    def __init__(self,schaechte,farbe):
        self.__farbe = farbe
        self.__schaechte = schaechte
        self.anzahl_toasts = 0
        self.brot_zustand = 0
        self.toast_zeit = 10
    
    
    def toastReintun(self,anzahl):
        if anzahl > self.__schaechte:
            print u"Geht nicht, nicht so viele Schächte im Toaster!"
        elif (self.anzahl_toasts>0) and (self.brot_zustand>0):
            print "Bitte erstmal das getoastete Brot auswerfen!"
        elif (self.anzahl_toasts + anzahl) > self.__schaechte:
            print u"Es ist nicht mehr genügend Platz dafür!"
        else:
            self.anzahl_toasts += anzahl
            
   
    def toasten(self):
        if self.anzahl_toasts > 0:
               zeit = self.toast_zeit
               if zeit<=15:
                    self.brot_zustand +=1
               if zeit >15:
                    self.brot_zustand +=2
               if self.brot_zustand >3:
                    self.brot_zustand = 3
               return (str(zeit)+" Sekunden vergangen, Toasten erledigt, das Brot ist "+self.zustand[self.brot_zustand])
        else:
               return ("Kein Toast im Toaster!")
    def toastAuswerfen(self):
        info = str(self.anzahl_toasts)+" mal Toast ausgeworfen. Zustand: "+self.zustand[self.brot_zustand] 
        self.anzahl_toasts = 0
        self.brot_zustand = 0
        return info

    def __str__(self):
        info = "Farbe des Toasters: "+self.__farbe+"\n"
        info += u"Toastschächte: "+str(self.__schaechte)+"\n"
        info += "Eingestellte Zeit: "+str(self.toast_zeit)+" Sekunden\n"
        info += "Toasts im Toaster: "+str(self.anzahl_toasts)+"\n"
        info += "Zustand der Toasts: "+self.zustand[self.brot_zustand]+"\n"
        return info
       
class SuperToaster(Toaster):
        temperatur = 300
        def temptoasten(self):
            if self.temperatur > 500:
                return u"Alarm: Der Toaster ist zu heiß!"
            elif self.temperatur < 100:
                return "Das Brot wird nicht getoastet - zu kalt."
            else:
                return self.toasten()
    
    