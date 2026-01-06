"""
Site Data Development Tool
Streamlit web application for Florida property parcel lookups
Kimley-Horn & Associates, Inc.
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO

# Import our lookup and generation modules
from county_adapters import lookup_property
from excel_generator import generate_parcel_report
from municode_parser import get_municode_link

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Site Data Development Tool",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - KIMLEY-HORN BRANDING
# ============================================================================

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #A20C33;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #5F5F5F;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #5F5F5F;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #A20C33;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 1.5rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'property_data' not in st.session_state:
    st.session_state.property_data = None

if 'lookup_history' not in st.session_state:
    st.session_state.lookup_history = []

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Report section defaults (all enabled)
if 'report_sections' not in st.session_state:
    st.session_state.report_sections = {
        'property_info': True,
        'site_characteristics': True,
        'zoning_land_use': True,
        'building_requirements': True,
        'parking_requirements': True,
        'assessment_values': True,
        'sales_history': True,
        'links_references': True
    }

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<div class="main-header">🏗️ Site Data Development Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Florida Property Parcel Lookup & Analysis | Kimley-Horn & Associates</div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - QUICK ACTIONS & INFO
# ============================================================================

with st.sidebar:
    st.image("https://www.kimley-horn.com/wp-content/themes/kh/images/logo.svg", width=200)
    
    st.markdown("---")
    st.subheader("Quick Actions")
    
    if st.session_state.property_data:
        st.success("✅ Property Data Loaded")
        if st.button("🔄 Clear Data", use_container_width=True):
            st.session_state.property_data = None
            st.rerun()
    else:
        st.info("ℹ️ No property loaded")
    
    st.markdown("---")
    st.subheader("Supported Counties")
    st.markdown("""
    - ✅ **Hillsborough** (Folio)
    - ✅ **Pinellas**
    - 🚧 **Pasco** (Coming Soon)
    - ✅ **Manatee** (Folio)
    - 🚧 **Sarasota** (Coming Soon)
    """)
    
    st.markdown("---")
    st.subheader("Recent Lookups")
    if st.session_state.lookup_history:
        for item in st.session_state.lookup_history[-5:]:
            st.caption(f"{item['county']}: {item['parcel_id']}")
    else:
        st.caption("No recent lookups")
    
    st.markdown("---")
    st.caption("© 2026 Kimley-Horn & Associates, Inc.")
    st.caption(f"Version 1.0 | {datetime.now().strftime('%Y-%m-%d')}")

# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Parcel Lookup", 
    "📋 Report Configuration", 
    "⭐ Favorites & Comparison",
    "📚 Help & Documentation"
])

# ============================================================================
# TAB 1: PARCEL LOOKUP
# ============================================================================

with tab1:
    st.header("Property Parcel Lookup")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Lookup Parameters")
        
        county = st.selectbox(
            "County",
            ["Hillsborough", "Pinellas", "Pasco", "Manatee", "Sarasota"],
            key="lookup_county"
        )
        
        # Show format hint based on county
        format_hints = {
            "Hillsborough": "Format: XX-XX-XX-XXXXX-XXX.X or XXXXXXXXXX",
            "Pinellas": "Format: XX-XX-XX-XXXXX-XXX-XXXX",
            "Pasco": "Format: XX-XX-XX-XX-XXX-XXX-XXXX",
            "Manatee": "Format: XXXXXXXXXX (10 digits)",
            "Sarasota": "Format: XXXX-XX-XXXX-XX-XX-XXXX-X"
        }
        
        st.caption(format_hints.get(county, "Enter parcel ID"))
        
        parcel_id = st.text_input(
            "Parcel ID / Folio Number",
            key="lookup_parcel_id",
            placeholder="Enter parcel ID..."
        )
        
        st.markdown("---")
        
        lookup_button = st.button(
            "🔍 Lookup Property",
            type="primary",
            use_container_width=True,
            disabled=not parcel_id
        )
        
        if st.button("📋 Example Parcels", use_container_width=True):
            st.info("""
            **Example Parcel IDs:**
            - Hillsborough: 192605-0000
            - Pinellas: (Contact for test parcel)
            - Manatee: (Contact for test parcel)
            """)
    
    with col2:
        st.subheader("Property Information")
        
        if lookup_button:
            with st.spinner(f"Looking up property in {county} County..."):
                try:
                    result = lookup_property(county, parcel_id)
                    
                    if result['success']:
                        st.session_state.property_data = result
                        
                        # Add to lookup history
                        st.session_state.lookup_history.append({
                            'county': county,
                            'parcel_id': parcel_id,
                            'timestamp': datetime.now(),
                            'address': result.get('address', 'N/A')
                        })
                        
                        st.success("✅ Property data retrieved successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Lookup failed: {result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        # Display property data if available
        if st.session_state.property_data:
            data = st.session_state.property_data
            
            # Property Overview
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("### 📍 Property Overview")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Address", data.get('address', 'N/A'))
                st.metric("City", data.get('city', 'N/A'))
                st.metric("Owner", data.get('owner', 'N/A'))
            
            with col_b:
                st.metric("Acres", f"{data.get('acres', 0):.2f}")
                st.metric("Zoning", data.get('zoning', 'N/A'))
                st.metric("Land Use", data.get('land_use', 'N/A'))
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Detailed Information Expander
            with st.expander("📊 View All Property Details", expanded=False):
                
                # Owner Information
                st.markdown("**Owner Information:**")
                st.write(f"- Name: {data.get('owner', 'N/A')}")
                st.write(f"- Address: {data.get('owner_address', 'N/A')}")
                st.write(f"- City/State/Zip: {data.get('owner_city', 'N/A')}, {data.get('owner_state', 'N/A')} {data.get('owner_zip', 'N/A')}")
                
                st.markdown("---")
                
                # Legal Description
                st.markdown("**Legal Description:**")
                st.write(data.get('legal_description', 'Not Available'))
                if data.get('legal_description2'):
                    st.write(data.get('legal_description2'))
                
                st.markdown("---")
                
                # Site Characteristics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("**Site Area:**")
                    st.write(f"- Acres: {data.get('acres', 0):.2f}")
                    st.write(f"- Sq Ft: {data.get('area_sqft', 0):,.0f}")
                
                with col2:
                    st.markdown("**Section/Township/Range:**")
                    st.write(f"- Section: {data.get('section', 'N/A')}")
                    st.write(f"- Township: {data.get('township', 'N/A')}")
                    st.write(f"- Range: {data.get('range', 'N/A')}")
                
                with col3:
                    st.markdown("**Subdivision:**")
                    st.write(f"- Name: {data.get('subdivision', 'N/A')}")
                    st.write(f"- Block: {data.get('block', 'N/A')}")
                    st.write(f"- Lot: {data.get('lot', 'N/A')}")
                
                st.markdown("---")
                
                # Assessment Values
                st.markdown("**Assessment Values:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Land Value", f"${data.get('assessed_land', 0):,}")
                with col2:
                    st.metric("Building Value", f"${data.get('assessed_building', 0):,}")
                with col3:
                    st.metric("Total Value", f"${data.get('assessed_total', 0):,}")
                
                # Building Characteristics (if available)
                if data.get('year_built') or data.get('num_units'):
                    st.markdown("---")
                    st.markdown("**Building Characteristics:**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if data.get('year_built'):
                            st.write(f"- Year Built: {data.get('year_built')}")
                    with col2:
                        if data.get('num_buildings'):
                            st.write(f"- Buildings: {data.get('num_buildings')}")
                    with col3:
                        if data.get('num_units'):
                            st.write(f"- Units: {data.get('num_units')}")
                
                # Sales History (if available)
                if data.get('sale_date') or data.get('sale_amount'):
                    st.markdown("---")
                    st.markdown("**Recent Sale:**")
                    st.write(f"- Date: {data.get('sale_date', 'N/A')}")
                    st.write(f"- Amount: ${data.get('sale_amount', 0):,}")
            
            # Quick Actions
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⭐ Add to Favorites", use_container_width=True):
                    if data not in st.session_state.favorites:
                        st.session_state.favorites.append({
                            'county': county,
                            'parcel_id': parcel_id,
                            'address': data.get('address'),
                            'data': data
                        })
                        st.success("Added to favorites!")
            
            with col2:
                if st.button("📋 Copy Address", use_container_width=True):
                    st.info(f"Address: {data.get('address', 'N/A')}, {data.get('city', 'N/A')}, FL {data.get('zip', 'N/A')}")
            
            with col3:
                municode_link = get_municode_link(county, data.get('city', ''))
                if municode_link:
                    st.link_button("🔗 View Municode", municode_link, use_container_width=True)
        
        else:
            st.info("👆 Enter a parcel ID and click 'Lookup Property' to get started")

# ============================================================================
# TAB 2: REPORT CONFIGURATION
# ============================================================================

with tab2:
    st.header("Report Configuration & Generation")
    
    if not st.session_state.property_data:
        st.warning("⚠️ Please lookup a property first in the 'Parcel Lookup' tab")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Report Sections")
            st.caption("Select which sections to include in your report:")
            
            sections = {
                'property_info': 'Property Information (Owner, Address, Legal)',
                'site_characteristics': 'Site Characteristics (Area, Dimensions)',
                'zoning_land_use': 'Zoning & Land Use',
                'building_requirements': 'Building Requirements (Setbacks, Height)*',
                'parking_requirements': 'Parking Requirements*',
                'assessment_values': 'Assessment Values',
                'sales_history': 'Sales History',
                'links_references': 'Links & References'
            }
            
            for key, label in sections.items():
                st.session_state.report_sections[key] = st.checkbox(
                    label,
                    value=st.session_state.report_sections.get(key, True),
                    key=f"checkbox_{key}"
                )
            
            st.caption("* Requires Municode integration (Phase 2)")
            
            st.markdown("---")
            
            # Quick Select Buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Select All", use_container_width=True):
                    for key in st.session_state.report_sections:
                        st.session_state.report_sections[key] = True
                    st.rerun()
            
            with col_b:
                if st.button("❌ Clear All", use_container_width=True):
                    for key in st.session_state.report_sections:
                        st.session_state.report_sections[key] = False
                    st.rerun()
            
            st.markdown("---")
            
            # Export Format
            st.subheader("Export Options")
            export_format = st.radio(
                "Format",
                ["Excel (.xlsx)", "PDF (Coming Soon)", "Both (Coming Soon)"],
                key="export_format"
            )
            
            include_map = st.checkbox("Include Property Map", value=False, disabled=True)
            st.caption("🚧 Map integration coming in Phase 2")
            
        with col2:
            st.subheader("Report Preview")
            
            data = st.session_state.property_data
            
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("### 📄 Report Contents")
            
            enabled_sections = [label for key, label in sections.items() 
                              if st.session_state.report_sections.get(key, False)]
            
            if enabled_sections:
                st.markdown("**Sections to be included:**")
                for section in enabled_sections:
                    st.markdown(f"- ✅ {section}")
            else:
                st.warning("⚠️ No sections selected! Please select at least one section.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Property Summary
            st.markdown("### 📋 Property Summary")
            summary_data = {
                "County": st.session_state.lookup_history[-1]['county'] if st.session_state.lookup_history else "N/A",
                "Parcel ID": st.session_state.lookup_history[-1]['parcel_id'] if st.session_state.lookup_history else "N/A",
                "Address": data.get('address', 'N/A'),
                "City": data.get('city', 'N/A'),
                "Acres": f"{data.get('acres', 0):.2f}",
                "Zoning": data.get('zoning', 'N/A')
            }
            
            df_summary = pd.DataFrame(list(summary_data.items()), columns=['Field', 'Value'])
            st.dataframe(df_summary, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            # Generate Button
            generate_enabled = any(st.session_state.report_sections.values())
            
            if st.button(
                "📥 Generate Report",
                type="primary",
                use_container_width=True,
                disabled=not generate_enabled
            ):
                with st.spinner("Generating Excel report..."):
                    try:
                        # Generate report with selected sections
                        output_path = f"/tmp/parcel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        
                        report_path = generate_parcel_report(
                            property_data=data,
                            zoning_data=None,  # Phase 2: Add Municode data
                            output_path=output_path,
                            sections=st.session_state.report_sections
                        )
                        
                        # Read file for download
                        with open(report_path, 'rb') as f:
                            excel_data = f.read()
                        
                        st.success("✅ Report generated successfully!")
                        
                        # Download button
                        filename = f"Parcel_Report_{data.get('city', 'Property')}_{datetime.now().strftime('%Y%m%d')}.xlsx"
                        
                        st.download_button(
                            label="📥 Download Excel Report",
                            data=excel_data,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.document",
                            type="primary",
                            use_container_width=True
                        )
                    
                    except Exception as e:
                        st.error(f"❌ Error generating report: {str(e)}")

# ============================================================================
# TAB 3: FAVORITES & COMPARISON
# ============================================================================

with tab3:
    st.header("Favorites & Property Comparison")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⭐ Saved Favorites")
        
        if st.session_state.favorites:
            for idx, fav in enumerate(st.session_state.favorites):
                with st.expander(f"{fav['address']} - {fav['county']} County"):
                    st.write(f"**Parcel ID:** {fav['parcel_id']}")
                    st.write(f"**Address:** {fav['address']}")
                    st.write(f"**Acres:** {fav['data'].get('acres', 0):.2f}")
                    st.write(f"**Zoning:** {fav['data'].get('zoning', 'N/A')}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button(f"🔍 Load", key=f"load_{idx}"):
                            st.session_state.property_data = fav['data']
                            st.success("Property loaded!")
                            st.rerun()
                    with col_b:
                        if st.button(f"🗑️ Remove", key=f"remove_{idx}"):
                            st.session_state.favorites.pop(idx)
                            st.rerun()
        else:
            st.info("No favorites saved yet. Add properties from the Parcel Lookup tab!")
    
    with col2:
        st.subheader("📊 Property Comparison")
        st.info("🚧 Coming Soon: Compare multiple properties side-by-side")
        
        st.markdown("""
        **Planned Features:**
        - Compare up to 4 properties
        - Side-by-side metrics
        - Export comparison table
        - Visual charts and graphs
        """)

# ============================================================================
# TAB 4: HELP & DOCUMENTATION
# ============================================================================

with tab4:
    st.header("Help & Documentation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📖 Quick Start Guide")
        
        st.markdown("""
        ### How to Use This Tool
        
        **Step 1: Lookup a Property**
        1. Go to the "Parcel Lookup" tab
        2. Select the county
        3. Enter the parcel ID
        4. Click "Lookup Property"
        
        **Step 2: Configure Your Report**
        1. Go to "Report Configuration"
        2. Check/uncheck sections to include
        3. Click "Generate Report"
        4. Download your Excel file
        
        **Step 3: Save Favorites (Optional)**
        - Click "Add to Favorites" on any property
        - Access them later in "Favorites & Comparison"
        """)
        
        st.markdown("---")
        
        st.subheader("🎯 Parcel ID Formats")
        
        st.markdown("""
        Each county uses different formats:
        
        - **Hillsborough:** XX-XX-XX-XXXXX-XXX.X
        - **Pinellas:** XX-XX-XX-XXXXX-XXX-XXXX
        - **Pasco:** XX-XX-XX-XX-XXX-XXX-XXXX
        - **Manatee:** XXXXXXXXXX (10 digits)
        - **Sarasota:** XXXX-XX-XXXX-XX-XX-XXXX-X
        """)
    
    with col2:
        st.subheader("🔧 Troubleshooting")
        
        st.markdown("""
        **Parcel Not Found?**
        - Verify the parcel ID format
        - Check if you selected the correct county
        - Try without dashes: 1234567890
        
        **Missing Data Fields?**
        - Some counties provide limited public data
        - Zoning requirements require Municode lookup (Phase 2)
        - FEMA zones require separate GIS query (Phase 2)
        
        **Report Generation Failed?**
        - Ensure at least one section is selected
        - Check your internet connection
        - Contact IT support if issue persists
        """)
        
        st.markdown("---")
        
        st.subheader("📞 Support")
        
        st.info("""
        **For Technical Support:**
        - Email: support@kimley-horn.com
        - Internal Wiki: [Link]
        
        **For Feature Requests:**
        - Submit via GitHub Issues
        - Contact the Development Team
        """)
        
        st.markdown("---")
        
        st.subheader("🚀 Upcoming Features")
        
        st.markdown("""
        **Phase 2 (In Development):**
        - ✅ Municode zoning integration
        - ✅ FEMA flood zone lookup
        - ✅ Future Land Use mapping
        - ✅ Pasco & Sarasota counties
        
        **Phase 3 (Planned):**
        - Property comparison tool
        - Batch processing (CSV upload)
        - PDF export option
        - Property map integration
        - Integration with DS Proposal Generator
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #5F5F5F; padding: 2rem 0;'>
    <strong>Site Data Development Tool v1.0</strong><br>
    Kimley-Horn & Associates, Inc. | © 2026<br>
    <em>For internal use only</em>
</div>
""", unsafe_allow_html=True)
