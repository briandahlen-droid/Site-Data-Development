"""
Site Data Development Tool
Streamlit web application for Florida property parcel lookups
Kimley-Horn & Associates, Inc.
"""

import streamlit as st
from datetime import datetime, date
import pandas as pd
from io import BytesIO
import sys
import os

# Verify all required modules are present
required_files = ['county_adapters.py', 'excel_generator.py', 'municode_parser.py']
missing_files = [f for f in required_files if not os.path.exists(f)]

if missing_files:
    st.error(f"""
    ❌ **Missing Required Files**
    
    The following files are missing: {', '.join(missing_files)}
    
    Please ensure all files are uploaded to the same directory.
    """)
    st.stop()

# Import our modules
try:
    from county_adapters import lookup_property
    from excel_generator import generate_parcel_report
    from municode_parser import get_municode_link
except ImportError as e:
    st.error(f"❌ **Import Error:** {str(e)}")
    st.stop()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Site Data Development Tool - Kimley-Horn",
    page_icon="🏗️",
    layout="wide"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

# Initialize all session state variables
if 'property_data' not in st.session_state:
    st.session_state.property_data = None

if 'county' not in st.session_state:
    st.session_state.county = "Hillsborough"

if 'parcel_id' not in st.session_state:
    st.session_state.parcel_id = ""

if 'property_address' not in st.session_state:
    st.session_state.property_address = ""

if 'city' not in st.session_state:
    st.session_state.city = ""

if 'owner_name' not in st.session_state:
    st.session_state.owner_name = ""

if 'acres' not in st.session_state:
    st.session_state.acres = 0.0

if 'zoning' not in st.session_state:
    st.session_state.zoning = ""

# Report sections (all enabled by default)
if 'include_property_info' not in st.session_state:
    st.session_state.include_property_info = True
if 'include_site_characteristics' not in st.session_state:
    st.session_state.include_site_characteristics = True
if 'include_zoning' not in st.session_state:
    st.session_state.include_zoning = True
if 'include_assessment' not in st.session_state:
    st.session_state.include_assessment = True
if 'include_sales' not in st.session_state:
    st.session_state.include_sales = True

# ============================================================================
# CUSTOM STYLING - KIMLEY-HORN BRANDING
# ============================================================================

st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Headers */
    h1 {
        color: #A20C33;
        font-family: Arial, sans-serif;
    }
    
    h2 {
        color: #5F5F5F;
        font-family: Arial, sans-serif;
        font-size: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #5F5F5F;
        font-family: Arial, sans-serif;
        font-size: 1.2rem;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #A20C33;
        margin: 1rem 0;
    }
    
    /* Success box */
    .success-box {
        background-color: #D4EDDA;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28A745;
        margin: 1rem 0;
    }
    
    /* Section dividers */
    hr {
        margin: 2rem 0;
        border: 1px solid #E0E0E0;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER SECTION
# ============================================================================

# Create header with Kimley-Horn branding
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.markdown("# Kimley**»**Horn")

with col_title:
    st.title("🏗️ Site Data Development Tool")
    st.caption("Florida Property Parcel Lookup & Analysis")

st.markdown("---")

# ============================================================================
# MAIN CONTENT - TWO COLUMN LAYOUT
# ============================================================================

col_left, col_right = st.columns([2, 3])

# ============================================================================
# LEFT COLUMN - INPUTS AND CONTROLS
# ============================================================================

with col_left:
    st.header("Property Lookup")
    
    # County Selection
    st.session_state.county = st.selectbox(
        "County",
        ["Hillsborough", "Pinellas", "Pasco", "Manatee", "Sarasota"],
        index=["Hillsborough", "Pinellas", "Pasco", "Manatee", "Sarasota"].index(st.session_state.county)
    )
    
    # Format hints
    format_examples = {
        "Hillsborough": "Example: 1926050030",
        "Pinellas": "Example: 03321611737001010",
        "Pasco": "Example: 123456789012345",
        "Manatee": "Example: 1234567890",
        "Sarasota": "Example: (Remove dashes)"
    }
    
    st.caption(f"ℹ️ {format_examples.get(st.session_state.county, 'Enter parcel ID')}")
    
    # Parcel ID Input
    parcel_input = st.text_input(
        "Parcel ID / Folio Number",
        value=st.session_state.parcel_id,
        placeholder="Enter without dashes or spaces...",
        help="Remove all dashes and spaces from the parcel ID"
    )
    
    st.caption("💡 **Important:** Enter parcel ID WITHOUT dashes or spaces")
    
    # Lookup Button
    if st.button("🔍 Lookup Property", type="primary", use_container_width=True):
        if parcel_input:
            with st.spinner(f"Looking up property in {st.session_state.county} County..."):
                try:
                    result = lookup_property(st.session_state.county, parcel_input)
                    
                    if result['success']:
                        # Store the full data
                        st.session_state.property_data = result
                        
                        # Auto-populate individual fields
                        st.session_state.parcel_id = parcel_input
                        st.session_state.property_address = result.get('address', '')
                        st.session_state.city = result.get('city', '')
                        st.session_state.owner_name = result.get('owner', '')
                        st.session_state.acres = result.get('acres', 0.0)
                        st.session_state.zoning = result.get('zoning', '')
                        
                        st.success("✅ Property data retrieved successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('error', 'Lookup failed')}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a parcel ID")
    
    st.markdown("---")
    
    # Display auto-populated fields
    st.subheader("Property Information")
    
    st.text_input(
        "Property Address",
        value=st.session_state.property_address,
        disabled=True,
        key="display_address"
    )
    
    col_city, col_acres = st.columns(2)
    with col_city:
        st.text_input(
            "City",
            value=st.session_state.city,
            disabled=True,
            key="display_city"
        )
    
    with col_acres:
        st.text_input(
            "Acres",
            value=f"{st.session_state.acres:.2f}" if st.session_state.acres else "",
            disabled=True,
            key="display_acres"
        )
    
    col_owner, col_zoning = st.columns(2)
    with col_owner:
        st.text_input(
            "Owner",
            value=st.session_state.owner_name,
            disabled=True,
            key="display_owner"
        )
    
    with col_zoning:
        st.text_input(
            "Zoning",
            value=st.session_state.zoning,
            disabled=True,
            key="display_zoning"
        )
    
    st.markdown("---")
    
    # Report Configuration Section
    st.subheader("Report Configuration")
    
    st.caption("Select sections to include in Excel report:")
    
    st.session_state.include_property_info = st.checkbox(
        "Property Information",
        value=st.session_state.include_property_info
    )
    
    st.session_state.include_site_characteristics = st.checkbox(
        "Site Characteristics",
        value=st.session_state.include_site_characteristics
    )
    
    st.session_state.include_zoning = st.checkbox(
        "Zoning & Land Use",
        value=st.session_state.include_zoning
    )
    
    st.session_state.include_assessment = st.checkbox(
        "Assessment Values",
        value=st.session_state.include_assessment
    )
    
    st.session_state.include_sales = st.checkbox(
        "Sales History",
        value=st.session_state.include_sales
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("✅ Select All", use_container_width=True):
            st.session_state.include_property_info = True
            st.session_state.include_site_characteristics = True
            st.session_state.include_zoning = True
            st.session_state.include_assessment = True
            st.session_state.include_sales = True
            st.rerun()
    
    with col_b:
        if st.button("❌ Clear All", use_container_width=True):
            st.session_state.include_property_info = False
            st.session_state.include_site_characteristics = False
            st.session_state.include_zoning = False
            st.session_state.include_assessment = False
            st.session_state.include_sales = False
            st.rerun()

# ============================================================================
# RIGHT COLUMN - RESULTS AND ACTIONS
# ============================================================================

with col_right:
    st.header("Property Details & Report")
    
    if st.session_state.property_data:
        data = st.session_state.property_data
        
        # Property Overview Card
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("### 📍 Property Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Address", data.get('address', 'N/A')[:30] + "..." if len(data.get('address', '')) > 30 else data.get('address', 'N/A'))
            st.metric("City", data.get('city', 'N/A'))
        
        with col2:
            st.metric("Owner", data.get('owner', 'N/A')[:30] + "..." if len(data.get('owner', '')) > 30 else data.get('owner', 'N/A'))
            st.metric("Acres", f"{data.get('acres', 0):.2f}")
        
        with col3:
            st.metric("Zoning", data.get('zoning', 'N/A'))
            assessed = data.get('assessed_total', 0)
            st.metric("Assessed Value", f"${assessed:,}" if assessed else "N/A")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed Information Expander
        with st.expander("📊 View Complete Property Details", expanded=False):
            
            tab_detail1, tab_detail2, tab_detail3 = st.tabs(["Owner & Legal", "Site Data", "Values & Sales"])
            
            with tab_detail1:
                st.markdown("**Owner Information:**")
                st.write(f"Name: {data.get('owner', 'N/A')}")
                st.write(f"Mailing Address: {data.get('owner_address', 'N/A')}")
                st.write(f"City/State/Zip: {data.get('owner_city', '')}, {data.get('owner_state', '')} {data.get('owner_zip', '')}")
                
                st.markdown("**Legal Description:**")
                st.write(data.get('legal_description', 'Not Available'))
                if data.get('legal_description2'):
                    st.write(data.get('legal_description2'))
            
            with tab_detail2:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Site Characteristics:**")
                    st.write(f"Acres: {data.get('acres', 0):.2f}")
                    st.write(f"Sq Ft: {data.get('area_sqft', 0):,.0f}")
                    st.write(f"Section: {data.get('section', 'N/A')}")
                    st.write(f"Township: {data.get('township', 'N/A')}")
                    st.write(f"Range: {data.get('range', 'N/A')}")
                
                with col2:
                    st.markdown("**Subdivision:**")
                    st.write(f"Name: {data.get('subdivision', 'N/A')}")
                    st.write(f"Block: {data.get('block', 'N/A')}")
                    st.write(f"Lot: {data.get('lot', 'N/A')}")
                    
                    if data.get('fema_flood_zone'):
                        st.markdown("**FEMA Flood Zone:**")
                        st.write(data.get('fema_flood_zone'))
            
            with tab_detail3:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Assessment Values:**")
                    st.write(f"Land: ${data.get('assessed_land', 0):,}")
                    st.write(f"Building: ${data.get('assessed_building', 0):,}")
                    st.write(f"Total: ${data.get('assessed_total', 0):,}")
                
                with col2:
                    if data.get('sale_date') or data.get('sale_amount'):
                        st.markdown("**Most Recent Sale:**")
                        st.write(f"Date: {data.get('sale_date', 'N/A')}")
                        st.write(f"Amount: ${data.get('sale_amount', 0):,}")
        
        st.markdown("---")
        
        # Report Generation Section
        st.subheader("Generate Report")
        
        # Show what will be included
        sections_enabled = []
        if st.session_state.include_property_info:
            sections_enabled.append("Property Information")
        if st.session_state.include_site_characteristics:
            sections_enabled.append("Site Characteristics")
        if st.session_state.include_zoning:
            sections_enabled.append("Zoning & Land Use")
        if st.session_state.include_assessment:
            sections_enabled.append("Assessment Values")
        if st.session_state.include_sales:
            sections_enabled.append("Sales History")
        
        if sections_enabled:
            st.info(f"**Report will include:** {', '.join(sections_enabled)}")
        else:
            st.warning("⚠️ No sections selected. Please select at least one section.")
        
        # Generate Report Button
        can_generate = bool(sections_enabled)
        
        if st.button("📥 Generate Excel Report", type="primary", use_container_width=True, disabled=not can_generate):
            with st.spinner("Generating Excel report..."):
                try:
                    sections = {
                        'property_info': st.session_state.include_property_info,
                        'site_characteristics': st.session_state.include_site_characteristics,
                        'zoning_land_use': st.session_state.include_zoning,
                        'building_requirements': False,  # Phase 2
                        'parking_requirements': False,  # Phase 2
                        'assessment_values': st.session_state.include_assessment,
                        'sales_history': st.session_state.include_sales,
                        'links_references': True
                    }
                    
                    output_path = f"/tmp/parcel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    
                    report_path = generate_parcel_report(
                        property_data=data,
                        zoning_data=None,
                        output_path=output_path,
                        sections=sections
                    )
                    
                    with open(report_path, 'rb') as f:
                        excel_data = f.read()
                    
                    st.success("✅ Report generated successfully!")
                    
                    filename = f"Parcel_Report_{st.session_state.city}_{st.session_state.parcel_id}_{date.today().strftime('%Y%m%d')}.xlsx"
                    
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
        
        # Quick Actions
        st.markdown("---")
        st.subheader("Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔗 View on County Site", use_container_width=True):
                link = data.get('parcel_link') or f"https://www.pcpao.gov/PropertyDetail?ParcelID={st.session_state.parcel_id}"
                st.info(f"[Open Property Details]({link})")
        
        with col2:
            municode_link = get_municode_link(st.session_state.county, data.get('city', ''))
            if municode_link:
                st.link_button("📖 View Zoning Code", municode_link, use_container_width=True)
    
    else:
        # Instructions when no property loaded
        st.info("""
        👆 **Get Started:**
        
        1. Select a county
        2. Enter the parcel ID (without dashes)
        3. Click "Lookup Property"
        
        Property information will auto-populate below.
        """)
        
        st.markdown("---")
        
        st.subheader("Supported Counties")
        st.markdown("""
        - ✅ **Hillsborough County**
        - ✅ **Pinellas County**  
        - ✅ **Pasco County**
        - ✅ **Manatee County**
        - 🚧 **Sarasota County** (Phase 2)
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #5F5F5F; padding: 1rem 0;'>
    <strong>Site Data Development Tool</strong> | Kimley-Horn & Associates, Inc. | © 2026<br>
    <em>For internal use only</em>
</div>
""", unsafe_allow_html=True)
