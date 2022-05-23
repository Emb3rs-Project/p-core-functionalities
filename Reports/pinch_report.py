import mpld3
from mpld3 import plugins
from mpld3.utils import get_id
import numpy as np
import matplotlib.pyplot as plt

import os
import json

from module.utilities.kb import KB
from module.utilities.kb_data import kb
from module.Source.simulation.Heat_Recovery.Pinch.convert_pinch import convert_pinch
from module.Source.simulation.Heat_Recovery.Pinch.make_pinch_design_draw import make_pinch_design_draw

script_dir = os.path.dirname(__file__)
data_test = json.load(open(os.path.join(script_dir,
                                        "../Tests/Sources/simulation/test_files/pinch_isolated_streams_test_2.json")))
test = convert_pinch(data_test, KB(kb))


### REPORT_RENDERING_codes [BEGIN]
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('asset'),
    autoescape=False
)

template = env.get_template('index.pinch_template.html')

PLOTFIG = []

plots_s = {
    'co2_optimization':
        {
            'name': "CO<sub>2</sub> Savings",
            'codes': [],
            'color': '#40DBA5'
        },
    'energy_recovered_optimization': {
        'name': "Energy Savings",
        'codes': [],
        'color': '#CDE848'
    },
    'energy_investment_optimization': {
        'name':"Energy Savings Specific Cost",
        'codes': [],
        'color': '#E86BBD'
    },
}



for key in test:
    category_solutions = test[str(key)]
    for solution in category_solutions:
        plots_s[key]['codes'].append(make_pinch_design_draw(solution['_info_pinch']))


sols = range(1,4)
template_content = template.render(plots_it=plots_s)




f = open("../../index.html", "w")
f.write(template_content)
f.close()

output = {
    "every" : "thing",
    "else" : "yes",
    "report" : template_content
}