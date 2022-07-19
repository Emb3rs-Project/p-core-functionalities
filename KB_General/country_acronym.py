from dataclasses import dataclass


@dataclass
class CountryAcronym:
    kb_data: dict

    def get_values(self, country):
        """
        Get country acronym

        Parameters
        ----------
        country: str
            country of the location

        Returns
        -------
        country_acronym: str
            country_acronym

        """

        data_eu_countries = self.kb_data.get('eu_country_acronym')

        try:
            country_acronym = data_eu_countries[country]
        except:
            country_acronym = data_eu_countries['Portugal']
            raise Exception(" Country does not exist in the KB")

        return country_acronym
