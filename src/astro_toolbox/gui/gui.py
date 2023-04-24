"""Module containing GUI class.
"""
import sys
import pathlib
import json
import datetime
import pkg_resources

from PyQt6 import QtCore, QtGui, QtWidgets, uic

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt

from astro_toolbox.coordinates.location import Location
from astro_toolbox.coordinates.equatorial import Equatorial
from astro_toolbox.angle.degrees import AngleDeg
from astro_toolbox.angle.hms import AngleHMS
from astro_toolbox.query.catalogs import Simbad
from astro_toolbox.query.ephemeris import Horizons
from astro_toolbox.time.core import AstroDateTime
from astro_toolbox.query.weather import OpenMeteo

from astro_toolbox.scripts.plots import airmas_map
from astro_toolbox.scripts.plots import polarstar_plt_northern
from astro_toolbox.scripts.plots import polarstar_plt_southern
from astro_toolbox.scripts.planning import get_multiple_informations

from astro_toolbox.query.ephemeris import DICT_OBJECTS

PATH_GUI = pkg_resources.resource_filename('astro_toolbox', 'gui/')
PATH = pkg_resources.resource_filename('astro_toolbox', 'coordinates/data/')
PATH_2 = pkg_resources.resource_filename('astro_toolbox', 'query/weather_icons/')

class Application():
    """GUI class which allow using command line interface in a GUI.
    """
    def __init__(self, application) -> None:
        """Constructor method.

        Parameters
        ----------
        app : Object
            Sys object.
        """
        self.app = application
        self.gui = uic.loadUi(PATH_GUI + 'main.ui')
        self.gui.show()
        self.dict_sites = self.load_json()
        self.canvas = None
        ut_time = datetime.datetime.now(datetime.timezone.utc).timetuple()
        str_datetime = (f"{ut_time[0]:04d}-{ut_time[1]:02d}-{ut_time[2]:02d}T" +
                        f"{ut_time[3]:02d}:{ut_time[4]:02d}:{ut_time[5]:02d}")
        self.gui.dateTimeEditInfo.setDateTime(
            self.gui.dateTimeEditInfo.dateTimeFromText(str_datetime))
        self.gui.dateTimeEditPolaris.setDateTime(
            self.gui.dateTimeEditPolaris.dateTimeFromText(str_datetime))
        self.gui.dateEditAirmass.setDate(
            QtCore.QDate.currentDate())
        self.initialisation_location()
        self.initialisation(
                self.gui.comboBoxLocation.currentText())
        self.weather()
        self.polaris()
        self.gui.comboBoxLocation.currentTextChanged.connect(lambda
            name=self.gui.comboBoxLocation.currentText:
            self.initialisation(name))
        self.gui.comboBoxInfo.currentTextChanged.connect(lambda
            name=self.gui.comboBoxInfo.currentText:
            self.initialisation(name))
        self.gui.comboBoxPolaris.currentTextChanged.connect(lambda
            name=self.gui.comboBoxPolaris.currentText():
            self.initialisation(name))
        self.gui.comboBoxWeather.currentTextChanged.connect(lambda
            name=self.gui.comboBoxWeather.currentText():
            self.initialisation(name))
        self.gui.pushButtonSaveLocation.clicked.connect(self.save_site)
        self.gui.pushButtonDeleteLocation.clicked.connect(self.delete_site)
        self.gui.pushButtonInfo.clicked.connect(self.info)
        self.gui.pushButtonPolaris.clicked.connect(self.polaris)
        self.gui.pushButtonWeather.clicked.connect(self.weather)
        self.gui.pushButtonAirmass_browse.clicked.connect(self.select_folder)
        self.gui.pushButtonAirmass.clicked.connect(self.airmass)
        self.run()
    def run(self):
        """run
        """
        self.app.exec()
    def initialisation_location(self):
        """Init all location fields.
        """
        self.dict_sites = self.load_json()
        self.gui.comboBoxLocation.clear()
        self.gui.comboBoxInfo.clear()
        self.gui.comboBoxPolaris.clear()
        self.gui.comboBoxWeather.clear()
        self.gui.listLocation.clear()
        name_list = list(self.dict_sites.keys())
        count = 1
        for name in name_list:
            self.gui.listLocation.addItem(
                f"{name}: latitude: {self.dict_sites[name]['latitude']} "+
                f"longitude: {self.dict_sites[name]['longitude']} "+
                f"elevation = {self.dict_sites[name]['elevation']} m")
            self.gui.comboBoxLocation.addItem(f"{name}")
            self.gui.comboBoxInfo.addItem(f"{name}")
            self.gui.comboBoxPolaris.addItem(f"{name}")
            self.gui.comboBoxWeather.addItem(f"{name}")
            self.gui.comboBoxAirmass.addItem(f"{name}")
            count = count + 1
    def initialisation(self, name):
        """Init lineEdit widgets in Location mode.

        Parameters
        ----------
        name : Site name.
        """
        if name in self.dict_sites.keys():
            self.gui.lineEditLatitude.setText(self.dict_sites[name]['latitude'])
            self.gui.lineEditLongitude.setText(self.dict_sites[name]['longitude'])
            self.gui.lineEditElevation.setText(str(self.dict_sites[name]['elevation']))
            self.gui.comboBoxLocation.setCurrentText(name)
            self.gui.comboBoxPolaris.setCurrentText(name)
            self.gui.comboBoxInfo.setCurrentText(name)
            self.gui.comboBoxWeather.setCurrentText(name)
            self.gui.comboBoxAirmass.setCurrentText(name)
    def select_folder(self):
        """Selecting folder method.
        """
        folder_explorer = QtWidgets.QFileDialog.getExistingDirectory()
        self.gui.lineEditAirmass_browser.setText(folder_explorer+'/')
    def save_site(self):
        """Saving site method.
        """
        location_name = self.gui.comboBoxLocation.currentText()
        latitude = self.gui.lineEditLatitude.text()
        longitude = self.gui.lineEditLongitude.text()
        elevation = self.gui.lineEditElevation.text()
        if '.' in latitude and ('°' and "'") not in latitude:
            latitude = AngleDeg(float(latitude)).degtodms()
        if '.' in longitude and ('°' and "'") not in longitude:
            longitude = AngleDeg(float(longitude)).degtodms()
        Location(location_name, latitude, longitude, elevation).save_site()
        self.initialisation_location()
        self.initialisation(self.gui.comboBoxLocation.currentText())
        self.polaris()
        self.weather()
    def delete_site(self):
        """Deleting site method.
        """
        location_name = self.gui.comboBoxLocation.currentText()
        Location(name=location_name).delete_site()
        self.initialisation_location()
        self.initialisation(self.gui.comboBoxLocation.currentText())
        self.polaris()
        self.weather()
    def info(self):
        """Info display method.
        """
        self.gui.listInfo.clear()
        location = self.gui.comboBoxInfo.currentText()
        objects_list = self.gui.lineEditInfo.text().split(' ')
        if '' in objects_list:
            objects_list.remove('')
        site = Location(name=location)
        time = self.gui.dateTimeEditInfo.textFromDateTime(
                    self.gui.dateTimeEditInfo.dateTime())
        for object_name in objects_list:
            if object_name.lower() in [key.lower() for key in DICT_OBJECTS]:
                item = Horizons(object_name, time, site)
                alpha, delta = item.get_equatorial_coord()
                obj_name = item.get_name()
                obj_magnitude = item.get_magnitude()
            else:
                item = Simbad(object_name)
                alpha, delta = item.get_equatorial_coord()
                obj_name = item.get_name()
                obj_magnitude = item.get_magnitude()
            coord = Equatorial(alpha=alpha, delta=delta, name=obj_name, magnitude=obj_magnitude)
            coord.compute_on_date_coord(AstroDateTime(time).get_year())
            gamma = AstroDateTime(time).get_lst(site)
            self.gui.listInfo.addItem(f'{coord}' +
                    f' HA = {AngleHMS(coord.get_hourangle(gamma=gamma))}'
                    f' X = {coord.calculate_airmass(gamma=gamma, location=site):.2f}' +
                    f' @ {site.name} {AstroDateTime(time)}')
    def polaris(self):
        """Polaris display method.
        """
        plt.clf()
        time = self.gui.dateTimeEditPolaris.textFromDateTime(
                    self.gui.dateTimeEditPolaris.dateTime())
        location_name = self.gui.comboBoxPolaris.currentText()
        location = Location(location_name)
        if location.latitude.dmstodeg() > 0:
            fig = polarstar_plt_northern(location, time)
        elif location.latitude.dmstodeg() < 0:
            fig = polarstar_plt_southern(location, time)
        if self.canvas is not None:
            self.canvas.deleteLater()
        self.canvas = FigureCanvas(fig)
        self.gui.verticalLayoutPolaris.addWidget(self.canvas)
        #self.ui.horizontalLayoutPolaris.replaceWidget(self.ui.widgetPolaris, FigureCanvas(fig))
    def weather(self):
        """Weather display method.
        """
        self.gui.tabWidgetWeather.clear()
        last_time = '0000-00-00T00:00:00'
        location = self.gui.comboBoxWeather.currentText()
        days = self.gui.spinBoxWeather_1.value()
        past = self.gui.spinBoxWeather_2.value()
        weather_forecasts = OpenMeteo(Location(location))
        for i, time in enumerate(weather_forecasts.data['hourly']['time']
                                 [72 - 24 * past :72 + 24*days]):
            time += ':00'
            label_wind_direction = QtWidgets.QLabel()
            label_wind_direction.setPixmap(
                    self.winddirectiontoimage(int(weather_forecasts.get_wind_direction(time))))
            label_wmo = QtWidgets.QLabel()
            label_wmo.setPixmap(
                    self.wmotoimage(weather_forecasts.get_wmo(time)))
            time_weather = [QtWidgets.QLabel(f'{time[11:]}'),
                        label_wmo,
                        QtWidgets.QLabel(f'{weather_forecasts.get_temperature(time)}'),
                        QtWidgets.QLabel(f'{weather_forecasts.get_humidity(time)}'),
                        QtWidgets.QLabel(f'{weather_forecasts.get_precipitation(time)}'),
                        QtWidgets.QLabel(f'{weather_forecasts.get_wind_speed(time)}'),
                        label_wind_direction,
                        QtWidgets.QLabel(f'{weather_forecasts.get_cloud_cover(time)}')]
            if int(time[8:10]) != int(last_time[8:10]):
                table = QtWidgets.QTableWidget()
                table.setColumnCount(8)
                table.setRowCount(24)
                table.setShowGrid(True)
                self.gui.tabWidgetWeather.addTab(table, time[:10])
                table.setHorizontalHeaderLabels(["Time\n(UT)",
                                        "",
                                        "Temperature\n(°C)",
                                        "Humidity\n(%)",
                                        "Precipitation\n(mm)",
                                        "Wind speed\n(km/h)",
                                        "Wind direction",
                                        "Cloud cover"])
                table.setVerticalHeaderLabels(['']*24)
            for j, weatherwidget in enumerate(time_weather):
                if j in (1, 6):
                    weatherwidget.setStyleSheet(
                    "background-color: white; qproperty-alignment: AlignCenter;")
                else:
                    weatherwidget.setStyleSheet(
                    "qproperty-alignment: AlignCenter;")
                table.setCellWidget(i%24, j, weatherwidget)
            last_time = time
    def load_json(self):
        """Json loading method.
        """
        with open(PATH  + 'sites.json', encoding="utf-8") as json_file:
            return json.load(json_file)
    def wmotoimage(self, code):
        """Function to convert WMO code to icon.

        Parameters
        ----------
        code : str
            WMO code as str.

        Returns
        -------
        Object
            QtGui.QPixmap Object.
        """
        code = str(code)
        if code == '00':
            icon = QtGui.QPixmap(PATH_2 + 'sunny.png')
        elif code == '01':
            icon = QtGui.QPixmap(PATH_2 + 'mainly_clear.png')
        elif code == '02':
            icon = QtGui.QPixmap(PATH_2 + 'partly_cloudy.png')
        elif code == '03':
            icon = QtGui.QPixmap(PATH_2 + 'cloudy.png')
        elif code[0] == '4':
            icon = QtGui.QPixmap(PATH_2 + 'fog.png')
        elif code[0] == '5':
            icon = QtGui.QPixmap(PATH_2 + 'drizzle.png')
        elif code[0] == '6':
            icon = QtGui.QPixmap(PATH_2 + 'rain.png')
        elif code[0] == '7' or code in ('85', '86'):
            icon = QtGui.QPixmap(PATH_2 + 'snow.png')
        elif code in ('80', '81', '82'):
            icon = QtGui.QPixmap(PATH_2 + 'showers.png')
        elif code[0] == ('9'):
            icon = QtGui.QPixmap(PATH_2 + 'thunderstorm.png')
        else:
            icon = QtGui.QPixmap(PATH_2 + 'na.png')
        return icon
    def winddirectiontoimage(self, wind_direction):
        """Funcion to convert wind direction to icon.

        Parameters
        ----------
        wind_direction : float
            Wind direction

        Returns
        -------
        Object
            QtGui.QPixmap Object.
        """
        wind_direction = float(wind_direction)
        if 0 <= wind_direction <= 22.5 or 337.5 <= wind_direction <= 360:
            icon = QtGui.QPixmap(PATH_2 + 'direction_up.png')
        elif 22.5 < wind_direction < 67.5:
            icon = QtGui.QPixmap(PATH_2 + 'direction_up_left.png')
        elif 67.5 < wind_direction < 112.5:
            icon = QtGui.QPixmap(PATH_2 + 'direction_left.png')
        elif 112.5 < wind_direction < 157.5:
            icon = QtGui.QPixmap(PATH_2 + 'direction_down_left.png')
        elif 157.5 < wind_direction < 202.5:
            icon = QtGui.QPixmap(PATH_2 + 'direction_down.png')
        elif 202.5 < wind_direction < 247.5:
            icon = QtGui.QPixmap(PATH_2 + 'direction_down_right.png')
        elif 247.5 < wind_direction < 292.5:
            icon = QtGui.QPixmap(PATH_2 + 'direction_right.png')
        elif 292.5 < wind_direction < 337.5:
            icon = QtGui.QPixmap(PATH_2 + 'direction_up_right.png')
        return icon
    def airmass(self):
        """Airmass method.
        """
        objects_list = self.gui.lineEditAirmass_objects.text().split(' ')
        if '' in objects_list:
            objects_list.remove('')
        objects_list.sort(key=str.casefold)
        date = self.gui.dateEditAirmass.date()
        date = f"{date.year():4d}-{date.month():2d}-{date.day():2d}"
        location = self.gui.comboBoxAirmass.currentText()
        bounds = [self.gui.spinBoxAirmass_1.value(),
                  self.gui.spinBoxAirmass_2.value()]
        ut_time = AstroDateTime(date)
        site = Location(location)
        object_dict = get_multiple_informations(objects_list, site, date, bounds)
        temporary_dict = {}
        if self.gui.radioButtonAirmass.isChecked():
            pdf = PdfPages(pathlib.Path(self.gui.lineEditAirmass_browser.text() +
                            f'Airmass_Map_{ut_time.get_day():02.0f}_{ut_time.get_month():02.0f}'
                            +f'_{ut_time.get_year():04.0f}_@_{site.name}.pdf'))
        for count, key in enumerate(object_dict):
            temporary_dict.update({key:object_dict[key]})
            if count == len(object_dict)-1 or ((count+1)%50 == 0):
                map_fig = airmas_map(temporary_dict, site, date, bounds)
                if self.gui.radioButtonAirmass.isChecked():
                    pdf.savefig(map_fig)
                else:
                    map_fig.canvas.toolbar_visible = False
                    win = map_fig.canvas.window()
                    win.setFixedSize(win.size())
                    map_fig.show()
                temporary_dict = {}
        del temporary_dict
        if self.gui.radioButtonAirmass.isChecked():
            pdf.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(PATH_GUI + 'logo_astro_toolbox.ico'))
    Application(app)
