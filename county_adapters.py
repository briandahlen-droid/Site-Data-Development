"""
County Adapters Module
Handles property lookups for all supported Florida counties
"""

import requests
from typing import Optional, Dict


def lookup_property(county: str, parcel_id: str) -> Dict:
    """
    Main lookup function that routes to appropriate county adapter.
    
    Args:
        county: County name
        parcel_id: Parcel ID in county-specific format
    
    Returns:
        Dict with success status and property data or error message
    """
    county = county.strip().title()
    
    if county == "Hillsborough":
        return lookup_hillsborough(parcel_id)
    elif county == "Pinellas":
        return lookup_pinellas(parcel_id)
    elif county == "Manatee":
        return lookup_manatee(parcel_id)
    elif county == "Pasco":
        return {'success': False, 'error': 'Pasco County lookup coming in Phase 2'}
    elif county == "Sarasota":
        return {'success': False, 'error': 'Sarasota County lookup coming in Phase 2'}
    else:
        return {'success': False, 'error': f'County "{county}" not supported'}


def lookup_hillsborough(parcel_id: str) -> Dict:
    """
    Lookup property from Hillsborough County.
    FOLIO format: Remove dashes (192605-0030 becomes 1926050030)
    """
    base_url = "https://www25.swfwmd.state.fl.us/arcgis12/rest/services/BaseVector/parcel_search/MapServer/7/query"
    
    # Normalize: remove dashes and spaces
    folio_normalized = parcel_id.replace('-', '').replace(' ', '').replace('.', '')
    
    params = {
        'where': f"FOLIONUM='{folio_normalized}'",
        'outFields': '*',
        'returnGeometry': 'false',
        'f': 'json'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('features') and len(data['features']) > 0:
            attr = data['features'][0]['attributes']
            
            return {
                'success': True,
                'address': attr.get('SITUSADD1', ''),
                'city': attr.get('SCITY', 'TAMPA'),
                'zip': attr.get('SZIP', ''),
                'owner': attr.get('OWNERNAME', ''),
                'owner_address': attr.get('OWNERADD1', ''),
                'owner_city': attr.get('OWNERCITY', ''),
                'owner_state': attr.get('OWNERSTATE', ''),
                'owner_zip': attr.get('OWNERZIP', ''),
                'legal_description': attr.get('LEGDECFULL', ''),
                'legal_description2': attr.get('LEGAL2', ''),
                'acres': attr.get('ACRES', 0),
                'area_sqft': attr.get('AREANO', 0),
                'zoning': attr.get('ZONING', 'Contact City/County for zoning info'),
                'land_use': attr.get('PARUSEDESC', ''),
                'land_use_code': attr.get('DOR4CODE', ''),
                'assessed_land': attr.get('ASSD_LND', 0),
                'assessed_building': attr.get('ASSD_BLD', 0),
                'assessed_total': attr.get('ASSD_TOT', 0),
                'market_value': attr.get('PARVAL', 0),
                'subdivision': attr.get('SUBDIV_NM', ''),
                'block': attr.get('BLOCK', ''),
                'lot': attr.get('LOT', ''),
                'section': attr.get('S_SECTION', ''),
                'township': attr.get('S_TOWNSHIP', ''),
                'range': attr.get('S_RANGE', ''),
                'year_built': attr.get('YRBLT_ACT', ''),
                'num_buildings': attr.get('NO_BULDNG', 0),
                'num_units': attr.get('NO_RES_UNITS', 0),
                'total_living_area': attr.get('TOT_LVG_AREA', 0),
                'sale_date': attr.get('SALE1_DATE', ''),
                'sale_amount': attr.get('SALE1_AMT', 0),
                'parcel_link': attr.get('PAWEBPAGE', ''),
                'error': None
            }
        else:
            return {
                'success': False,
                'error': f'Parcel {folio_normalized} not found in Hillsborough County database'
            }
    
    except Exception as e:
        return {'success': False, 'error': f'API Error: {str(e)}'}


def lookup_pinellas(parcel_id: str) -> Dict:
    """
    Lookup property from Pinellas County using their direct API.
    Parcel ID format: XX-XX-XX-XXXXX-XXX-XXXX
    Example: 03-32-16-11737-001-0010
    """
    
    # Try Pinellas County's direct 2025 parcel layer first
    pinellas_urls = [
        "https://egis.pinellas.gov/arcgis/rest/services/PaoTpv/Parcels_2025/MapServer/0/query",
        "https://www45.swfwmd.state.fl.us/arcgis12/rest/services/BaseVector/parcel_search/MapServer/13/query"
    ]
    
    # Create format variations
    parcel_variations = [
        parcel_id,  # With dashes: 03-32-16-11737-001-0010
        parcel_id.replace('-', ''),  # Without dashes: 03321611737001010
    ]
    
    # Try different field names that Pinellas uses
    field_names = ['PARCELID', 'ALTKEY', 'PIN', 'PARNO']
    
    for base_url in pinellas_urls:
        for parcel_variant in parcel_variations:
            for field in field_names:
                params = {
                    'where': f"{field}='{parcel_variant}'",
                    'outFields': '*',
                    'returnGeometry': 'false',
                    'f': 'json'
                }
                
                try:
                    response = requests.get(base_url, params=params, timeout=15)
                    if response.status_code != 200:
                        continue
                        
                    data = response.json()
                    
                    if data.get('features') and len(data['features']) > 0:
                        attr = data['features'][0]['attributes']
                        
                        # Handle different field names from different APIs
                        return {
                            'success': True,
                            'address': (attr.get('SITUSADD1') or attr.get('SITEADD') or 
                                      attr.get('SITUS_ADDRESS') or ''),
                            'city': (attr.get('SCITY') or attr.get('SITUSCITY') or ''),
                            'zip': (attr.get('SZIP') or attr.get('SITUSZIP') or ''),
                            'owner': attr.get('OWNERNAME', ''),
                            'owner_address': attr.get('OWNERADD1', ''),
                            'owner_city': attr.get('OWNERCITY', ''),
                            'owner_state': attr.get('OWNERSTATE', ''),
                            'owner_zip': attr.get('OWNERZIP', ''),
                            'legal_description': (attr.get('LEGDECFULL') or 
                                                attr.get('LEGALDESC') or ''),
                            'legal_description2': attr.get('LEGAL2', ''),
                            'acres': attr.get('ACRES', 0),
                            'area_sqft': (attr.get('AREANO') or attr.get('LOTSIZE') or 0),
                            'zoning': attr.get('ZONING', 'Contact City/County for zoning info'),
                            'land_use': (attr.get('PARUSEDESC') or attr.get('LANDUSE') or ''),
                            'land_use_code': (attr.get('DOR4CODE') or attr.get('DOR_UC') or ''),
                            'assessed_land': (attr.get('ASSD_LND') or attr.get('LANDVAL') or 0),
                            'assessed_building': (attr.get('ASSD_BLD') or attr.get('BLDGVAL') or 0),
                            'assessed_total': (attr.get('ASSD_TOT') or attr.get('JUSTVAL') or 0),
                            'market_value': (attr.get('PARVAL') or attr.get('ASMTVAL') or 0),
                            'subdivision': (attr.get('SUBDIV_NM') or attr.get('SUBDIVISION') or ''),
                            'block': attr.get('BLOCK', ''),
                            'lot': attr.get('LOT', ''),
                            'section': (attr.get('S_SECTION') or attr.get('SECTION') or ''),
                            'township': (attr.get('S_TOWNSHIP') or attr.get('TOWNSHIP') or ''),
                            'range': (attr.get('S_RANGE') or attr.get('RANGE') or ''),
                            'year_built': (attr.get('YRBLT_ACT') or attr.get('YRBUILT') or ''),
                            'num_buildings': attr.get('NO_BULDNG', 0),
                            'num_units': attr.get('NO_RES_UNITS', 0),
                            'total_living_area': (attr.get('TOT_LVG_AREA') or 
                                                attr.get('TOTLIVAREA') or 0),
                            'sale_date': (attr.get('SALE1_DATE') or attr.get('SALEDT1') or ''),
                            'sale_amount': (attr.get('SALE1_AMT') or attr.get('SALEPRICE1') or 0),
                            'parcel_link': f"https://www.pcpao.gov/PropertyDetail?ParcelID={parcel_id}",
                            'error': None
                        }
                
                except Exception:
                    continue  # Try next combination
    
    # If not found, provide helpful error message
    return {
        'success': False,
        'error': f'''Parcel {parcel_id} not found in available databases.

Possible reasons:
• The parcel may not be in the regional SWFWMD database yet
• Try the direct link: https://www.pcpao.gov/PropertyDetail?ParcelID={parcel_id}

If you can see the property on Pinellas County's website, please report this as a bug.
        '''
    }


def lookup_manatee(parcel_id: str) -> Dict:
    """
    Lookup property from Manatee County.
    Excellent data completeness - all fields in single layer.
    """
    base_url = "https://www.mymanatee.org/gisits/rest/services/opendata/Planning/MapServer/22/query"
    
    params = {
        'where': f"PIN='{parcel_id}'",
        'outFields': '*',
        'returnGeometry': 'false',
        'f': 'json'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('features') and len(data['features']) > 0:
            attr = data['features'][0]['attributes']
            
            return {
                'success': True,
                'address': attr.get('PRIMARY_ADDRESS', ''),
                'city': attr.get('PROP_CITYNAME', ''),
                'zip': attr.get('PROP_ZIP', ''),
                'owner': attr.get('OWNER', ''),
                'owner_address': attr.get('MAILING_ADDRESS', ''),
                'owner_city': attr.get('MAIL_CITY', ''),
                'owner_state': attr.get('MAIL_STATE', ''),
                'owner_zip': attr.get('MAIL_ZIP', ''),
                'legal_description': attr.get('LEGAL_DESCRIPTION', ''),
                'legal_description2': '',
                'acres': attr.get('ACRES', 0),
                'area_sqft': attr.get('AREA_SQFT', 0),
                'zoning': attr.get('ZONING', ''),
                'land_use': attr.get('FUTURE_LAND_USE', ''),
                'land_use_code': attr.get('DOR_UC', ''),
                'assessed_land': attr.get('LAND_VALUE', 0),
                'assessed_building': attr.get('BLDG_VALUE', 0),
                'assessed_total': attr.get('JUST_VALUE', 0),
                'market_value': attr.get('MARKET_VALUE', 0),
                'subdivision': attr.get('SUBDIVISION', ''),
                'block': attr.get('BLOCK', ''),
                'lot': attr.get('LOT', ''),
                'section': attr.get('SECTION', ''),
                'township': attr.get('TOWNSHIP', ''),
                'range': attr.get('RANGE', ''),
                'year_built': attr.get('YR_BLT', ''),
                'num_buildings': attr.get('NO_BLDG', 0),
                'num_units': attr.get('NO_RES_UNTS', 0),
                'total_living_area': attr.get('TOT_LVG_AREA', 0),
                'sale_date': attr.get('SALE_DATE', ''),
                'sale_amount': attr.get('SALE_PRC', 0),
                'parcel_link': '',
                'error': None
            }
        else:
            return {'success': False, 'error': 'Parcel ID not found in Manatee County'}
    
    except Exception as e:
        return {'success': False, 'error': f'API Error: {str(e)}'}
