import pandas as pd
import geopandas as gpd
from simpledbf import Dbf5

print('Pandas version:')
print(pd.__version__)
print('Geopandas version:')
print(gpd.__version__)

def main():
    # Edit the paths when working with different shapefile
    dbf_path = '../africa/africa_countries.dbf'
    shp_path = '../africa/africa_countries.shp'

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
    #print(gdf.columns)
    #print(gdf.FIPS_CNTRY)
    #print(gdf.CNTRY_NAME)

    # The code below should be editted to examine the current .shp file.


    # Extracting the fields I am interested in.
    # Drop the columns I don't need. =======> do
    gdf = gdf[['CNTRY_NAME', 'geometry']]

    # Now I want to extract the countries whose polygon is in desperate need.
    new_shp = country_selection(gdf)


    # It is important that I export this new GeoDataFrame so I can use it in
    # the future, and not have to do the selections all over again.
    new_shp.to_file('../africa/sub_saharan_africa.shp')



def country_selection(shp_data):
    # A list is created with all the countries that would like to extract.
    # Shapefiles have various country names, so this might need to change.
    countries = ['angola', 'burkina faso', 'benin', 'burundi',
            'congo', 'central african republic',
            'ivory coast', 'cameroon', 'gabon', 'ghana', 'guinea', 'kenya',
            'comoros', 'liberia', 'lesotho', 'madagascar', 'mali', 'malawi',
            'mozambique', 'nigeria', 'niger', 'namibia', 'rwanda',
            'sierra leone', 'senegal', 'chad', 'togo', 'tanzania, united republic of', 'uganda',
            'zambia', 'zimbabwe']

    req_shape_num = len(countries)

    # Start to extract the need polygons from the original shapefile.
    print('\nBeginning geometry extraction. . .')
    print('Attempting to retieve', req_shape_num,'countries.\n')

    # Making a list of the geometries that are needed 'countries' list.
    # Making another list for the names of countries that have been found,
    # for future verification.
    final_list = list()
    found_list = list()
    for index, row in shp_data.iterrows():
        if row['CNTRY_NAME'].lower() in countries:
            row['CNTRY_NAME'] = assign_dhscc(row['CNTRY_NAME'].lower())
            found_list.append(row['CNTRY_NAME'].lower())
            final_list.append(row)

    # Converting the list of geometries back to a GeoDataFrame
    cols = ['CNTRY_NAME', 'geometry']
    final_df = gpd.GeoDataFrame(final_list, columns=cols)

    print('\nExtracted:\n')

    print(final_df)
    if len(final_df) == req_shape_num:
        print('\nYou have all the shapes you need!')
    else:
        print('\nWe are still missing the following shapes:')
        for c in countries:
            if c not in found_list:
                print(c)

    return final_df


    # This function will assign a much need DHS Country Code, that will
    # allow the geometry to be easily referenced when working with dhs
    # survey data.
    def assign_dhscc(country_name):
        return


if __name__ == '__main__':
    main()
