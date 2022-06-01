"""
##############################
INFO: Get country acronym

##############################
INPUT:  country - country of the location


##############################
OUTPUT: country_acronym

"""

from dataclasses import dataclass


@dataclass
class CountryAcronym:
    kb_data: dict

    def get_values(self, country):

        data_eu_countries = self.kb_data.get('eu_country_acronym')

        try:
            country_acronym = data_eu_countries[country]
        except:
            print("Error getting country acronym. "
                  "Default: Portugal set as country")

            country_acronym = data_eu_countries['Portugal']

        return country_acronym
