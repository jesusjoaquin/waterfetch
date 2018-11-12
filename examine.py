import pandas as pd
import geopandas as gpd
from simpledbf import Dbf5

print('Pandas version:')
print(pd.__version__)
print('Geopandas version:')
print(gpd.__version__)

def main():
    # Edit the paths when working with different shapefile
    dbf_path = 'world_borders/world_borders.dbf'
    shp_path = 'world_borders/world_borders.shp'

    analyze_dbf(dbf_path)
    analyze_shp(shp_path)


def analyze_dbf(path):
    print('\n===== .dbf analysis =====')
    dbf = Dbf5(path, codec='UTF-8')

    dbf_records = dbf.numrec
    dbf_fields = dbf.fields

    print('The number of records in the .dbf:', dbf_records)
    print('The fields of the .dbf:\n', dbf_fields)

    # Ideally, the dbf data should be converted to a dataframe and it should be
    # printed. Sometimes not possible due to Unicode/Decode errors. Check.
    #df = dbf.to_dataframe()
    #print('Data of the .dbf file:\n', df))


def analyze_shp(path):
    print('\n===== .shp analysis =====')
    gdf = gpd.read_file(path)
    print(gdf.dtypes)
    print(gdf.head())
    print(gdf.columns)

    # The code below should be editted to examine the current .shp file.

    # Extracting the fields I am interested in.
    # Drop the columns I don't need. =======> do
    gdf = gdf[['NAME', 'geometry']]

    # Now I want to extract the countries whose polygon is in desperate need.
    new_shp = country_selection(gdf)

    # This is the GeoDataFrame that we want to work with
    #print('Extracted', len(shape_list), 'countries.')
    #print(shape_list)

    #new_gdf = GeoDataFrame(
    # It is important that I export this new GeoDataFrame so I can use it in
    # the future, and not have to do the selections all over again.
    # I should drop the colums of the data frame that I don't need.`
    new_shp.to_file('sub_saharan_africa.shp')



def country_selection(shp_data):
    # A list is created with all the countries that would like to extract.
    countries = ['Angola', 'Burkina Faso', 'Benin', 'Burundi',
            'Democratic Republic of the Congo', 'Central African Republic',
            'Cote d\'Ivoire', 'Cameroon', 'Gabon', 'Ghana', 'Guinea', 'Kenya',
            'Comoros', 'Liberia', 'Lesotho', 'Madagascar', 'Mali', 'Malawi',
            'Mozambique', 'Nigeria', 'Niger', 'Namibia', 'Rwanda',
            'Sierra Leone', 'Senegal', 'Chad', 'Togo', 'United Republic of Tanzania', 'Uganda',
            'Zambia', 'Zimbabwe']


    # Change variable names
    final_list = list()
    for index, row in shp_data.iterrows():
        if row['NAME'] in countries:
            final_list.append(row)


    cols = ['NAME', 'geometry']
    final_df = gpd.GeoDataFrame(final_list, columns=cols)

    print(final_df.head())

    return final_df


if __name__ == '__main__':
    main()
