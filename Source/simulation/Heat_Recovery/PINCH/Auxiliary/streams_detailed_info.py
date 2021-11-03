
from ......KB_General.fluid_material import fluid_material_cp

def streams_detailed_info(df_char, pinch_delta_T_min):

    df_char['Cp'] = df_char.apply(
        lambda row:fluid_material_cp(row['Fluid'], row['Supply_Temperature']), axis=1
        )

    df_char['mcp'] = df_char['Flowrate'] * df_char['Cp'] / 3600  # [kW/K]

    df_char['Stream_Type'] = df_char.apply(
        lambda row:'Hot' if row['Supply_Temperature'] > row['Target_Temperature']
        else 'Cold', axis=1
        )

    df_char['Supply_Shift'] = df_char.apply(
        lambda row:row['Supply_Temperature'] - pinch_delta_T_min if row['Stream_Type'] == 'Hot'
        else row['Supply_Temperature'] + pinch_delta_T_min, axis=1
        )

    df_char['Target_Shift'] = df_char.apply(
        lambda row:row['Target_Temperature'] - pinch_delta_T_min if row['Stream_Type'] == 'Hot'
        else row['Target_Temperature'] + pinch_delta_T_min, axis=1
        )

    return df_char
