
from module.Sink.characterization.greenhouse import greenhouse

class Greenhouse_2:
    def __init__(self):
        ###################
        # Mandatory/Basic USER INPUT
        self.latitude = 49.5
        self.longitude = -97.28
        self.greenhouse_orientation = "S"
        self.width = 28
        self.length = 6.7
        self.height = 2.1  # greenhouse height [m]
        self.shutdown_periods = []
        self.daily_periods = [[0, 24]]  # heating needed all day
        self.sunday_on = 1
        self.saturday_on = 1
        self.lights_on = 0  # on
        self.T_cool_on = 35  # cooling start temperature working hours [ºC]
        self.T_heat_on = 12  # heating start temperature working hours [ºC]
        self.greenhouse_efficiency = 1  # show options of greenhouse efficiency - 1=tight sealed greenhouse; 2=medium; 3=loose
        self.thermal_blanket = 0

def testGreenhouse_2():

    data = Greenhouse_2()
    input_data = {}
    input_data['platform'] = data.__dict__
    test = greenhouse(input_data,option=1)

    test_2 = greenhouse(input_data,option=2)

    print(test['hot_stream']['hourly_generation'])

    import pandas as pd
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 20})

    greenhouse_data = pd.read_csv('/module/Sink/characterization/Building/teste_case_greenhouse.csv', sep=';')

    x = range(len(test['hot_stream']['hourly_generation']))
    x = [i+1 for i in x]
    greenhouse_data.index +=1

    print('aaaaaaaaa')
    print(len(test['cold_stream']['hourly_generation']))
    print(len(greenhouse_data['t_indoor']))

    data = [test['cold_stream']['hourly_generation'][0],test['cold_stream']['hourly_generation'][0]] + test['cold_stream']['hourly_generation']
    data_2 = [test_2['cold_stream']['hourly_generation'][0],test_2['cold_stream']['hourly_generation'][0]] + test_2['cold_stream']['hourly_generation']

    print(len(data))
    x = range(len(data))

    plt.plot(x, data, label='theoretical')

    greenhouse_data['t_indoor'].plot(label='experiment')
    plt.title('Greenhouse indoor temperature - Comparison between model and experimental data')
    plt.ylabel('Temperature [ºC]')
    plt.xlabel('Time [h]')
    plt.legend(loc='lower left')
    plt.xlim(1, 71)

    plt.show()



    data = [test['hot_stream']['hourly_generation'][0]] + test['hot_stream']['hourly_generation']
    x = range(len(data))

    plt.step(x, data, label='theoretical')
    greenhouse_data['power'].plot(drawstyle='steps',label='experiment')
    plt.title('Heating requirements - Comparison between model and experimental data')
    plt.ylabel('Heating requirements [kJ/h]')
    plt.xlabel('Time [h]')
    plt.legend(loc='lower left')
    plt.xlim(1, 71)

    plt.show()

    """"
    Expected:
    [34360.06786579071, 27126.003499951665, 27565.57197713766, 21650.832164568514, 14797.813745460455, 10800.824021053113, 6460.46181873828, 7254.042281065299, 9533.84325632785, 17493.78056170256, 34676.07498035828, 36286.162510339]
    """

