import copy
def dhn_correct_losses(power_source, grid_losses, T_supply_sink, T_return_sink, max_T_grid_allowed):

    ambient_temperature = 15
    do_iterations = True

    # initial assumptions
    mcp = power_source / (T_supply_sink - T_return_sink)
    supply_coef = 0.5
    return_coef = 0.5
    T_supply_source_old = copy.copy(T_supply_sink)

    while do_iterations is True:

        # get losses per pipe
        supply_pipe_losses = grid_losses * supply_coef
        return_pipe_losses = grid_losses * return_coef

        # get source side temperatures
        T_supply_source = T_supply_sink + supply_pipe_losses/mcp
        T_return_source = T_return_sink - return_pipe_losses/mcp

        # correct losses coefs.
        hot_pipe_delta_T = (T_supply_source + T_supply_sink) / 2 - ambient_temperature  # delta T, grid supply temperature pipe
        cold_pipe_delta_T = (T_return_source + T_return_sink) / 2 - ambient_temperature  # delta T, grid return temperature pipe
        supply_coef = hot_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)  # correction coefficient
        return_coef = cold_pipe_delta_T / (hot_pipe_delta_T + cold_pipe_delta_T)

        # get grid mcp
        mcp = power_source / (T_supply_source - T_return_source)

        if abs(T_supply_source - T_supply_source_old) < 0.01:
            do_iterations = False

            if T_supply_source > max_T_grid_allowed:
                T_supply_source = None
                T_return_source = None
        else:
            T_supply_source_old = copy.copy(T_supply_source)

            if T_supply_source > max_T_grid_allowed:
                T_supply_source = None
                T_return_source = None
                break

    return T_supply_source,T_return_source

dhn_correct_losses(391.468, 562.001875, 95, 70, 120)
