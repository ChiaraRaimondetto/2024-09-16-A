import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.form=None


    def handle_graph(self, e):
        lat=self._view.txt_latitude.value
        lon=self._view.txt_longitude.value
        lat_min,lat_max=self._model.getCorrectionLat()
        lng_min,lng_max=self._model.getCorrectionLng()
        if not lat or not lon or not self.form:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Selezioare una forma, un alongitudine e una latitudine"))
            self._view.update_page()
            return

        try:
            latitude=float(lat)
            longitude = float(lon)
            if latitude>lat_min and latitude<lat_max and longitude>lng_min and longitude<lng_max:
                self._model.buildGraph(latitude, longitude,self.form)
                n,a,topNodi,topArchi=self._model.getInfo()
                if n and a and topNodi and topArchi:
                    self._view.txt_result1.controls.clear()
                    self._view.txt_result1.controls.append(
                        ft.Text(f"Grafo correttamente creato con {n} nodi e {a} archi\n"
                                f"Di seguito i nodi con i maggior peso:"))
                    for nodi in topNodi:
                        self._view.txt_result1.controls.append(ft.Text(f"{nodi[0]} --> gradi:{nodi[1]} "))
                    self._view.txt_result1.controls.append(ft.Text(f"I 5 archi con peso maggiore sono:"))
                    for a in topArchi:
                        self._view.txt_result1.controls.append(ft.Text(f"{a[0]} <-> {a[1]} | peso: {a[2]}"))
                else:
                    self._view.txt_result1.controls.clear()
                    self._view.txt_result1.controls.append(ft.Text("Non siamo riusciti a creare il grafo"))
                    self._view.update_page()
                    return


            else:
                self._view.txt_result1.controls.clear()
                self._view.txt_result1.controls.append(ft.Text(f"Selezioare longitudine nel range ({lng_min})-({lng_max}).\n"
                                                               f"Selezionare latidudine nel range ({lat_min})-({lat_max})"))
                self._view.update_page()
                return
        except ValueError:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Inserire dei valori numerici corretti"))
            self._view.update_page()
            return
        self._view.btn_path.disabled=False
        self._view.update_page()




    def handle_path(self, e):
        cammin,punti=self._model.bestCammino()
        if cammin and punti:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Cammino correttamente trovato con {len(cammin)} nodi e con un punteggio pari a {punti}\n"
                                                           f"Di seguito i nodi del cammino:"))
            for c in cammin:
                self._view.txt_result2.controls.append(ft.Text(f"{c[0]} Popolazione: {c[1]} abitanti"))
        else:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text("Non siamo riusciti a creare il cammino ottimo"))
            self._view.update_page()
            return
        self._view.update_page()


    def fill_ddshape(self):
        forme= self._model.getAllShape()
        for f in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(data=f,text=f,on_click=self.readShape))
    def readShape(self,e):
        if e.control.data is None:
            self.form=None
        else:
            self.form=e.control.data
