import pandas as pd
import geopandas as gpd
from simpledbf import Dbf5

print('Pandas version:')
print(pd.__version__)
print('Geopandas version:')
print(gpd.__version__)

# Define the names of the countries based the current .shp. Countries are
# identified with variables that are their dhs country code.
ao = 'angola'
bf = 'burkina faso'
bj = 'benin'
bu = 'burundi'
cd = 'zaire' # common change
cf = 'central african republic'
ci = 'ivory coast'    # common change
cm = 'cameroon'
ga = 'gabon'
gh = 'ghana'
gn = 'guinea'
ke = 'kenya'
km = 'comoros'
lb = 'liberia'
ls = 'lesotho'
md = 'madagascar'
ml = 'mali'
mw = 'malawi'
mz = 'mozambique'
ng = 'nigeria'
ni = 'niger'
nm = 'namibia'
rw = 'rwanda'
sl = 'sierra leone'
sn = 'senegal'
td = 'chad'
tg = 'togo'
tz = 'tanzania, united republic of' # common change
ug = 'uganda'
zm = 'zambia'
zw = 'zimbabwe'


def main():
    # Edit the paths when working with different shapefile
    dbf_path = '../data/shapefiles/africa/africa_countries.dbf'
    shp_path = '../data/shapefiles/africa/africa_countries.shp'

    analyze_dbf(dbf_path)
    analyze_shp(shp_path)


def analyze_dbf(path):
    print('\n===== .dbf analysis =====')
    dbf = Dbf5(path, codec='UTF-8')

    dbf_records = dbf.numrec

    print('The number of records in the .dbf:', dbf_records)

    # Ideally, the dbf data should be converted to a dataframe and it should be
    # printed. Sometimes not possible due to Unicode/Decode errors. Check.
    df = dbf.to_dataframe()
    print('Data of the .dbf file:\n', df.head())
    print(df.columns)
    print('Unique country names:')
    print(df.CNTRY_NAME.unique())


def analyze_shp(path):
    print('\n===== .shp analysis =====')
    gdf = gpd.read_file(path)
    print(gdf.dtypes)
    print(gdf.head())

    # After looking at the info in the .dbf, set country_col
    # Stores the column name which contains the full country string.
    country_col = 'CNTRY_NAME'
    needed_info = [country_col, 'geometry']

    # Drop the columns that are not needed
    for c in gdf.columns:
        if c not in needed_info:
            gdf.drop(c, axis=1, inplace=True)

    # Rename columns now, so code below this point does not have to be altered.
    gdf.columns = ['dhscc', 'geometry']

    # Now I want to extract the countries whose polygon is in desperate need.
    new_shp = country_selection(gdf)


    # It is important that I export this new GeoDataFrame so I can use it in
    # the future, and not have to do the selections all over again.
    new_shp.to_file('../data/shapefiles/africa/sub_saharan_africa.shp')



def country_selection(shp_data):
    # A list is created with all the countries that would like to extract.
    # Shapefiles have various country names, so this might need to change.
    countries = [ao, bf, bj, bu, cd, cf, ci, cm, ga, gh, gn, ke, km, lb, ls,
            md, ml, mw, mz, ng, ni, nm, rw, sl, sn, td, tg, tz, ug, zm, zw]

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
        if row['dhscc'].lower() in countries:
            row['dhscc'] = assign_dhscc(row['dhscc'].lower())
            found_list.append(row['dhscc'])
            final_list.append(row)

    # Converting the list of geometries back to a GeoDataFrame
    final_df = gpd.GeoDataFrame(final_list)

    print('\nExtracted:\n')
    print(final_df)

    # Checking if all needed countries were found
    completed = True
    for c in countries:
        if assign_dhscc(c) not in found_list:
            print('Missing:', c)
            completed = False

    if completed:
        print('You have obtained all needed shapes.')
    else:
        print('Go get those shapes!')

    return final_df


# This function will assign a much need DHS Country Code, that will
# allow the geometry to be easily referenced when working with dhs
# survey data.
def assign_dhscc(country_name):
    dhscc = dict()
    dhscc[ao] = 'AO'; dhscc[bf] = 'BF'; dhscc[bj] = 'BJ'; dhscc[bu] = 'BU'
    dhscc[cd] = 'CD'; dhscc[cf] = 'CF'; dhscc[ci] = 'CI'; dhscc[cm] = 'CM'
    dhscc[ga] = 'GA'; dhscc[gh] = 'GH'; dhscc[gn] = 'GN'; dhscc[ke] = 'KE'
    dhscc[km] = 'KM'; dhscc[lb] = 'LB'; dhscc[ls] = 'LS'; dhscc[md] = 'MD'
    dhscc[ml] = 'ML'; dhscc[mw] = 'MW'; dhscc[mz] = 'MZ'; dhscc[ng] = 'NG'
    dhscc[ni] = 'NI'; dhscc[nm] = 'NM'; dhscc[rw] = 'RW'; dhscc[sl] = 'SL'
    dhscc[sn] = 'SN'; dhscc[td] = 'TD'; dhscc[tg] = 'TG'; dhscc[tz] = 'TZ'
    dhscc[ug] = 'UG'; dhscc[zm] = 'ZM'; dhscc[zw] = 'ZW'

    return dhscc[country_name]


if __name__ == '__main__':
    main()
