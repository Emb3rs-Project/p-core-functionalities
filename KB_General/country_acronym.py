

from dataclasses import dataclass


@dataclass
class CountryAcronym:
    kb_data: dict

    def get_values(self, country):

        data_eu_countries = self.kb_data.get('eu_country_acronym')

        try:
            country_acronym = data_eu_countries[country]
        except:
            print('Error getting country acronym. Default: PT')
            country_acronym = data_eu_countries['Portugal']

        return country_acronym
