

def centrar_ventana_product(self):
    anc_v = 818 #self.winfo_reqwidth() # anchura de la ventana
    alt_v = 568 #self.winfo_reqheight() # altura de la ventana
    anc_p = self.winfo_screenwidth() # anchura de la pantalla
    alt_p = self.winfo_screenheight() # altura de la pantalla
    self.geometry('%dx%d+%d+%d' %(anc_v, alt_v,(anc_p - anc_v)/2,(alt_p - alt_v)/2))
    # Debug
    #print(anc_v, alt_v, anc_p, alt_p)

def centrar_ventana_edit(self):
    anc_v = 594 #self.winfo_reqwidth() # anchura de la ventana
    alt_v = 230 #self.winfo_reqheight() # altura de la ventana
    anc_p = self.winfo_screenwidth() # anchura de la pantalla
    alt_p = self.winfo_screenheight() # altura de la pantalla
    self.geometry('%dx%d+%d+%d' %(anc_v, alt_v,(anc_p - anc_v)/2,(alt_p - alt_v)/2))
    # Debug
    #print(anc_v, alt_v, anc_p, alt_p)
