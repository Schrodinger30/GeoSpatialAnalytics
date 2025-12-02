# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 16:11:04 2025

@author: C53585
"""
# Import packages
# ----------------------------------------------------------------------------
import time
import pandas as pd
from tqdm import tqdm
from geopy.geocoders import Nominatim



# Define functions
# ----------------------------------------------------------------------------
def geocoder_nominatim(
        df,
        ObjectName,
        ObjectStreet,
        ObjectNumber,
        ObjectPostalCode,
        ObjectCity,
        ObjectCountry,
    ):
        """Geocoding using Nominatim API (https://wiki.openstreetmap.org/wiki/Nominatim)
    
        Args:
            df (dataframe):             Dataframe containing the objects
    
            ObjectName (str):           Columnname containing object name
    
            ObjectStreet (str):         Columnname containing object streetname
    
            ObjectNumber (str):         Columnname containing object number
    
            ObjectPostalCode (str):     Columnname containing object postalcode
    
            ObjectCity (str):           Columnname containing object city
    
            ObjectCountry (str):        Columnname containing object country
    
        Returns:
            locs_list (dataframe):      Dataframe of collected OSM data for each object
        """
    
        # Create emtpy list to store location data for each row
        locs_list = []
    
        # Iterate through dataframe and collect location data for each object
        for index, row in tqdm(
            df.iterrows(), total=df.shape[0], desc="Get location data from OSM"
        ):
    
            # Define query
            query = (
                row[ObjectName]
                + ","
                + row[ObjectStreet]
                + " "
                + row[ObjectNumber]
                + ","
                + row[ObjectPostalCode]
                + ","
                + row[ObjectCity]
                + ","
                + row[ObjectCountry]
            )
    
            # Initiate API
            app = Nominatim(user_agent="GeoTools")
    
            try:
                # Get data from API
                loc = app.geocode(query).raw
    
                # Initiate 1 second wait before next request due to API limits
                time.sleep(1)
    
                # Append collected location data to list
                locs_list.append(loc)
    
            except:
                # If no data can be collected append empty dictionary to list
                locs_list.append({})
    
        return pd.DataFrame(locs_list)



# Get location data using geocoder_nominatim function.
# ----------------------------------------------------------------------------
# Example locations in the Netherlands.
data = {
    "Name": [
        "Anne Frank House",
        "Van Gogh Museum",
        "Rijksmuseum",
        "Keukenhof",
        "Efteling",
        "Markthal",
        "Giethoorn",
        "",
    ],
    "Street": ["", "", "", "", "", "", "", "John Adams Park"],
    "Number": ["", "", "", "", "", "", "", "1"],
    "PostalCode": ["", "", "", "", "", "", "", "2244BZ"],
    "City": [
        "Amsterdam",
        "Amsterdam",
        "Amsterdam",
        "",
        "",
        "Rotterdam",
        "",
        "Wassenaar",
    ],
    "Country": ["NL", "NL", "NL", "NL", "NL", "NL", "NL", "NL"],
}

# Create dataframe from locations.
locations = pd.DataFrame(data)

# Get OSM data for each location.
location_data = geocoder_nominatim(
    locations, 
    "Name", 
    "Street", 
    "Number", 
    "PostalCode", 
    "City", 
    "Country"
    )