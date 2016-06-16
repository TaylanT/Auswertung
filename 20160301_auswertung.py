#!/usr/bin/python
import csv
import os
import pandas as pd
# from influxdb import DataFrameClient
import sys
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt




def multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)
    if figs is None:
        figs = [plt.figure(n) for n in plt.get_fignums()]
    for fig in figs:
        fig.set_size_inches(18.5, 10.5)
        fig.savefig(pp, format='pdf')
    pp.close()


dateiname = sys.argv[1]

print dateiname
filename = dateiname.replace('.lvm', '.csv')
dbname = 'Messwerte'
messung = 'neu'


sr = open(dateiname, "rb")
in_txt = csv.reader(sr, delimiter='\t')
output = open(filename, 'wb')
writer = csv.writer(output)
for row in in_txt:
    if row:
        writer.writerow(row)

sr.close()
output.close()


datei = open(filename, 'r')

inhalt = datei.read()

t = inhalt.split('\n')

day = t[1][0:2]
tagsi = t[0]
print tagsi
month = t[1][3:5]
year = t[1][6:10]
uhrzeit = t[5][0:8].replace('.', ':')
datumzeit = year+'-'+month+'-'+day+' '+uhrzeit
datei2 = pd.read_csv(filename, skiprows=3, index_col=False).fillna(0)
del datei2['Zeit']
zeiti = pd.date_range(datumzeit, periods=len(datei2), freq='S')
datei2.index = zeiti
s = pd.DataFrame(datei2, index=zeiti)



druck=s[[u'PI 01', u'PI 02', u'PI 04',u'PI 05', u'PI 07', u'PI 08', u'PI 11', u'PI 12', u'PI 14']]
temp_arm = s[[u'TI 01', u'TI 02', u'TI 04', u'TI 05', u'TI 06', u'TI 06a', u'TI 07', u'TI 08', u'TI 09']]
temp_reich = s[[u'TI 10', u'TI 11', u'TI 12', u'TI 13', u'TI 14', u'TI 14a']]
temp_oil = s[[u'TI 20', u'TI 21', u'TI 21a', u'TI 22']]
temp_outside = s[[u'TI 32', u'TI 33', u'TI 35', u'TI 36', u'TI 38', u'TI 39']]
drehzahl = s[['Drehzahl']]
# s[['Verdichterleistung']]=s[['Verdichterleistung']]*1000

massenstrom_km = s[[u'FI 07', u'FI 13']]


konzentration = s[[u'Konzentration']]
leistung = s[['Q-Entgaser', 'Q-Resorber', 'Verdichterleistung']]
ventile = s[[u'ExpV']]
cop = s[[u'COP']]


dateiname = os.path.basename(dateiname)
# plt.style.use(['dark_background'])


# Seite 1 Temperaturen
ax1 = plt.subplot(221)

temp_arm.plot(ax=ax1)
plt.ylabel('[$^\circ$C]')
temp_reich.plot(ax=plt.subplot(222, sharex=ax1))
plt.ylabel('[$^\circ$C]')
temp_outside.plot(ax=plt.subplot(223, sharex=ax1))
plt.ylabel('[$^\circ$C]')
temp_oil.plot(ax=plt.subplot(224, sharex=ax1))
plt.ylabel('[$^\circ$C]')
fig = plt.gcf()
fig.canvas.set_window_title('Temperaturen')
fig.suptitle(dateiname.replace('.lvm', ''))

# Seite2 Druck und Leistung
plt.figure(2)
drehzahl.plot(ax=plt.subplot(221, sharex=ax1))
plt.ylabel('[U/min]')
leistung.plot(ax=plt.subplot(222, sharex=ax1))
plt.ylabel('[kW]')
massenstrom_km.plot(ax=plt.subplot(223, sharex=ax1), ylim=(0, 20))
plt.ylabel('[l/min]')
konzentration.plot(ax=plt.subplot(224, sharex=ax1))
plt.ylabel('[-]')
fig = plt.gcf()
fig.canvas.set_window_title('Druck & Leistung')
fig.suptitle(dateiname.replace('.lvm', ''))

plt.figure(3)
druck.plot(ax=plt.subplot(221, sharex=ax1))
plt.ylabel('bar')

ventile.plot(ax=plt.subplot(222, sharex=ax1))
plt.ylabel('[%]')
cop.plot(ax=plt.subplot(223, sharex=ax1), ylim=(0, 5))
plt.ylabel('[-]')
fig = plt.gcf()
fig.canvas.set_window_title('Misc')
fig.suptitle(dateiname.replace('.lvm', ''))
# fig = plt.gcf()
# fig.set_size_inches(18.5, 10.5)
# fig.savefig('test2png.pdf', dpi=300)
savepath = '/home/ttaylan/Dokumente/Auswertung'+'/'+dateiname.replace('.lvm', '') + '.pdf'

multipage(savepath)
plt.show()
