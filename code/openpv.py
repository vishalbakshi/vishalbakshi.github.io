from __future__ import print_function, division
import pandas as pd
import numpy as np
import json
import requests
import matplotlib.pyplot as plt


from pandas.io.json import json_normalize
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import ColorbarBase
from matplotlib.patches import Polygon

def AvgCostMap(df, state_dict, label):
    avg_cost = [group[1].avg_cost.mean() for group in df.groupby('state')]
    states_names = [state_dict[group[0]] for group in df.groupby('state')]
    avg_cost_dict = dict(zip(states_names, avg_cost))
    fig, ax = plt.subplots(1)
    fig.set_size_inches(15, 10)

    m = Basemap(llcrnrlon=-130, llcrnrlat=18, urcrnrlon=-60,urcrnrlat=54.9, projection='lcc', lat_1 = 33, lat_2=45, lon_0=-95)
    shp_info = m.readshapefile('cb_2016_us_state_500k', 'states', drawbounds=True)
    colors = {}
    statenames = []
    cmap = plt.cm.Oranges
    vmin = min(avg_cost_dict.values())
    vmax = max(avg_cost_dict.values())

    for shapedict in m.states_info:
        statename = shapedict['NAME']
        if statename in states_names:
            cost = avg_cost_dict[statename]
            colors[statename] = cmap(abs(cost-vmin)/(vmax-vmin))[:3]
        statenames.append(statename)

    for nshape, seg in enumerate(m.states):
        if statenames[nshape] in states_names:
            if statenames[nshape] == 'Alaska':
                seg = list(map(lambda (x,y): (0.35*x + 750000, 0.35*y + 1250000), seg))
            if statenames[nshape] == 'Hawaii':
                seg = list(map(lambda (x,y): (1.3*x + 3800000, 1.3*y-1600000), seg))
        
            color = rgb2hex(colors[statenames[nshape]])
            poly = Polygon(seg, facecolor=color, edgecolor=color)
            ax.add_patch(poly)
        

    norm = Normalize(vmin=vmin, vmax=vmax)
    mapper = ScalarMappable(norm=norm, cmap=cmap)
    cax = fig.add_axes([0.27, 0.05, 0.5, 0.05])
    cb = ColorbarBase(cax, cmap=cmap, norm=norm, orientation='horizontal')
    cb.ax.set_xlabel('Average Cost per Watt (USD)')
    ax.set_title('Cost per Watt in Dollars for PV Installs in U.S. States - PV Size: ' + label, fontsize=16)
    plt.show()
        