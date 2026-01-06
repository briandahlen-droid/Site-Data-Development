"""
Municode Parser Module
Provides links to Municode zoning codes
Phase 2 will add full parsing capabilities
"""

from typing import Optional


def get_municode_link(county: str, city: str = "") -> Optional[str]:
    """
    Get Municode link for the appropriate jurisdiction.
    
    Args:
        county: County name
        city: City name (if applicable)
    
    Returns:
        URL to Municode or None if not available
    """
    city = city.strip().upper() if city else ""
    county = county.strip().title()
    
    # City-specific Municodes (priority over county)
    city_municodes = {
        'TAMPA': 'https://library.municode.com/fl/tampa/codes/code_of_ordinances',
        'ST. PETERSBURG': 'https://library.municode.com/fl/st._petersburg/codes/code_of_ordinances',
        'ST PETERSBURG': 'https://library.municode.com/fl/st._petersburg/codes/code_of_ordinances',
        'CLEARWATER': 'https://library.municode.com/fl/clearwater/codes/land_development_code',
        'SARASOTA': 'https://library.municode.com/fl/sarasota/codes/code_of_ordinances',
        'BRADENTON': 'https://library.municode.com/fl/bradenton/codes/code_of_ordinances',
        'PALMETTO': 'https://library.municode.com/fl/palmetto/codes/code_of_ordinances',
        'PLANT CITY': 'https://library.municode.com/fl/plant_city/codes/code_of_ordinances',
        'TEMPLE TERRACE': 'https://library.municode.com/fl/temple_terrace/codes/code_of_ordinances'
    }
    
    if city in city_municodes:
        return city_municodes[city]
    
    # County Municodes (fallback)
    county_municodes = {
        'Hillsborough': 'https://library.municode.com/fl/hillsborough_county/codes/land_development_code',
        'Pinellas': 'https://library.municode.com/fl/pinellas_county/codes/code_of_ordinances',
        'Pasco': 'https://library.municode.com/fl/pasco_county/codes/land_development_code',
        'Manatee': 'https://library.municode.com/fl/manatee_county/codes/land_development_code',
        'Sarasota': 'https://library.municode.com/fl/sarasota_county/codes/code_of_ordinances'
    }
    
    return county_municodes.get(county)


def get_zoning_requirements(jurisdiction: str, zoning_code: str) -> dict:
    """
    Get zoning requirements from Municode.
    
    Args:
        jurisdiction: City or County name
        zoning_code: Zoning district code (e.g., "RMF-16", "PD")
    
    Returns:
        Dict with zoning requirements
    
    Note: Phase 2 implementation will add web scraping/API calls
    """
    # Placeholder for Phase 2
    return {
        'success': False,
        'message': 'Municode parsing coming in Phase 2',
        'setbacks': {},
        'height_max': 'TBD',
        'parking_standard': 'TBD',
        'bicycle_parking': 'TBD',
        'municode_link': get_municode_link(jurisdiction)
    }


def search_municode(jurisdiction: str, search_term: str) -> Optional[str]:
    """
    Search Municode for specific terms.
    
    Args:
        jurisdiction: City or County name
        search_term: Term to search for
    
    Returns:
        URL to search results or None
    
    Note: Phase 2 implementation
    """
    base_link = get_municode_link(jurisdiction, "")
    
    if base_link:
        # Municode search URL pattern
        return f"{base_link}?searchText={search_term.replace(' ', '+')}"
    
    return None
