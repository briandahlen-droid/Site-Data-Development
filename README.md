# 🏗️ Site Data Development Tool

A comprehensive Streamlit web application for Florida property parcel lookups and analysis.

![Kimley-Horn](https://www.kimley-horn.com/wp-content/themes/kh/images/logo.svg)

## Features

- **Multi-County Support**: Lookup properties in Hillsborough, Pinellas, Pasco, Manatee, and Sarasota counties
- **Comprehensive Data**: Owner information, site characteristics, zoning, assessments, and more
- **Customizable Reports**: Select which sections to include in Excel reports
- **Favorites System**: Save frequently accessed parcels
- **Municode Integration**: Direct links to zoning codes (Phase 2: full parsing)
- **Professional Formatting**: Excel reports matching Kimley-Horn standards

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/briandahlen-droid/Site-Data-Development.git
cd Site-Data-Development

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Usage

1. **Parcel Lookup**
   - Select county
   - Enter parcel ID
   - Click "Lookup Property"

2. **Generate Report**
   - Configure sections to include
   - Click "Generate Report"
   - Download Excel file

3. **Save Favorites**
   - Add frequently used parcels to favorites
   - Quick access for future lookups

## Supported Counties

| County | Status | Parcel Format |
|--------|--------|---------------|
| Hillsborough | ✅ Active | XX-XX-XX-XXXXX-XXX.X |
| Pinellas | ✅ Active | XX-XX-XX-XXXXX-XXX-XXXX |
| Manatee | ✅ Active | XXXXXXXXXX (10 digits) |
| Pasco | 🚧 Phase 2 | XX-XX-XX-XX-XXX-XXX-XXXX |
| Sarasota | 🚧 Phase 2 | XXXX-XX-XXXX-XX-XX-XXXX-X |

## Data Sources

- **Property Data**: SWFWMD ArcGIS REST Services
- **Zoning Codes**: Municode Library
- **GIS Data**: County property appraiser websites

## Project Structure

```
Site-Data-Development/
├── app.py                  # Main Streamlit application
├── county_adapters.py      # Property lookup functions
├── excel_generator.py      # Excel report generation
├── municode_parser.py      # Municode integration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Configuration

### API Endpoints

The app uses public ArcGIS REST services:
- Hillsborough: SWFWMD Layer 7
- Pinellas: SWFWMD Layer 13
- Manatee: MyManatee GIS Layer 22

### Customization

Edit `app.py` to customize:
- Branding and colors
- Default report sections
- County configurations

## Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

Your app will be live at: `https://[your-app-name].streamlit.app`

### Local Deployment

```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

## Roadmap

### Phase 1 (Current)
- ✅ Hillsborough, Pinellas, Manatee county lookups
- ✅ Excel report generation
- ✅ Favorites system
- ✅ Municode links

### Phase 2 (In Development)
- 🚧 Pasco & Sarasota counties
- 🚧 Municode zoning parsing
- 🚧 FEMA flood zone lookup
- 🚧 Future Land Use mapping

### Phase 3 (Planned)
- 📋 Property comparison tool
- 📋 Batch processing (CSV upload)
- 📋 PDF export option
- 📋 Map integration
- 📋 DS Proposal Generator integration

## Contributing

This is an internal Kimley-Horn tool. For feature requests or bug reports:
1. Create a GitHub Issue
2. Contact the Development Team
3. Submit a Pull Request

## Support

**Technical Support:**
- Email: support@kimley-horn.com
- Internal Wiki: [Link to wiki]

**For Questions:**
- Contact: Brian Dahlen
- Team: Development Services

## License

© 2026 Kimley-Horn & Associates, Inc.  
For internal use only.

## Disclaimer

This tool provides reference data from public sources. Always verify:
- Property information with county records
- Zoning requirements with local jurisdictions
- Legal descriptions with title companies

Not intended for:
- Legal documentation
- Title searches
- Survey purposes
- Regulatory submissions (without verification)

## Acknowledgments

- Property data provided by county property appraisers
- GIS services by Southwest Florida Water Management District
- Zoning codes via Municode

---

**Version:** 1.0  
**Last Updated:** January 2026  
**Maintained By:** Kimley-Horn Development Team
