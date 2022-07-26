from dataclasses import dataclass


@dataclass
class BuildingProperties:
    kb_data: dict

    def get_values(self, country, building_type):
        """Get building properties according to location and building type for simulation

        Parameters
        ----------
        country : str
            Country of the location

        building_type : str
            Type of building residential ('residential) or non residential ( 'office' or 'hotel')

        Returns
        -------
        u_wall : float
            U value [W/m2.K]

        u_roof : float
            U value [W/m2.K]

        u_glass : float
            U value [W/m2.K]

        u_floor : float
            U value [W/m2.K]

        tau_glass : float
            Transmissivity Glass []

        alpha_wall : float
            Absorption coefficient wall []

        alpha_floor : float
            Absorption coefficient floor []

        alpha_glass : float
            Absorption coefficient glass []

        capacitance_wall : float
            Capacitance wall [J/kg.K]

        capacitance_floor : float
            Capacitance floor [J/kg.K]

        capacitance_roof : float
            Capacitance roof [J/kg.K]

        air_change_hour : float
            Air change hour [1/h]

        emissivity_wall : float
            Emissivity wall []

        emissivity_glass : float
            Emissivity glass []

        """

        data = self.kb_data.get('building_properties')

        try:
            if building_type == "residential" or building_type == "hotel":
                u_wall = float(
                    data[country]["residential_u_wall"]
                )  # Wall heat transfer coefficient [W/m2.K]
                u_roof = float(
                    data[country]["residential_u_roof"]
                )  # Roof heat transfer coefficient [W/m2.K]
                u_glass = float(
                    data[country]["residential_u_glass"]
                )  # Glass heat transfer coefficient [W/m2.K]
                u_floor = float(
                    data[country]["residential_u_floor"]
                )  # Floor heat transfer coefficient [W/m2.K]
            else:
                u_wall = float(data[country]["non-residential_u_wall"])
                u_roof = float(data[country]["non-residential_u_roof"])
                u_glass = float(data[country]["non-residential_u_glass"])
                u_floor = float(data[country]["non-residential_u_floor"])

            alpha_wall = float(data[country]["alpha_wall"])
            alpha_floor = float(data[country]["alpha_floor"])
            alpha_glass = float(data[country]["alpha_glass"])
            tau_glass = float(data[country]["tau_glass"])
            capacitance_floor = float(
                data[country]["capacitance_floor"]
            )  # Floor specific heat capacitance [J/m2.K]
            capacitance_roof = float(
                data[country]["capacitance_roof"]
            )  # Roof specific heat capacitance [J/m2.K]
            capacitance_wall = float(
                data[country]["capacitance_wall"]
            )  # Wall specific heat capacitance [J/m2.K]
            air_change_hour = float(data[country]["air_change_hour"]) / 3600  # [1/s]

        except:
            print("Country does not exist in the Knowledge Base. "
                  "Default: Portugal set as country and respective buildings' characteristics are used.")

            country = "Portugal"

            if building_type == "residential" or building_type == "hotel":
                u_wall = float(data[country]["residential_u_wall"])
                u_roof = float(data[country]["residential_u_roof"])
                u_glass = float(data[country]["residential_u_glass"])
                u_floor = float(data[country]["residential_u_floor"])
            else:
                u_wall = float(data[country]["non-residential_u_wall"])
                u_roof = float(data[country]["non-residential_u_roof"])
                u_glass = float(data[country]["non-residential_u_glass"])
                u_floor = float(data[country]["non-residential_u_floor"])

            alpha_wall = float(data[country]["alpha_wall"])
            alpha_floor = float(data[country]["alpha_floor"])
            alpha_glass = float(data[country]["alpha_glass"])
            tau_glass = float(data[country]["tau_glass"])
            capacitance_floor = float(data[country]["capacitance_floor"])
            capacitance_roof = float(data[country]["capacitance_roof"])
            capacitance_wall = float(data[country]["capacitance_wall"])
            air_change_hour = float(data[country]["air_change_hour"])  # [1/h]

        emissivity_wall = 0.9
        emissivity_glass = 0.85

        return (
            u_wall,
            u_roof,
            u_glass,
            u_floor,
            tau_glass,
            alpha_wall,
            alpha_floor,
            alpha_glass,
            capacitance_wall,
            capacitance_floor,
            capacitance_roof,
            air_change_hour,
            emissivity_wall,
            emissivity_glass
        )
