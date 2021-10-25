import matplotlib.pyplot as plt

def plot_gcc(net_heat_flow,temperature_vector):

    plt.plot(net_heat_flow, temperature_vector)
    plt.title('GCC', fontsize=14)
    plt.xlabel('Net Heat [MJ/h]')
    plt.ylabel('Shifted Temperature [ºC]')
    plt.xlim(0, max(net_heat_flow) + max(net_heat_flow) * 0.1)
    plt.grid(True)
    #plt.show()
