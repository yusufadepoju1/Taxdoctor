import streamlit as st
import pdfplumber
import pandas as pd
import io

# Page configuration
st.set_page_config(
    page_title="PDF to CSV Converter",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF to CSV Converter")
st.write("Upload a PDF file and convert it to CSV format")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success(f"✅ Uploaded: {uploaded_file.name}")
    
    # Process button
    if st.button("Convert to CSV", type="primary"):
        with st.spinner("Processing PDF..."):
            try:
                data = []
                
                # Read PDF
                with pdfplumber.open(uploaded_file) as pdf:
                    st.info(f"Processing {len(pdf.pages)} page(s)...")
                    
                    for page in pdf.pages:
                        # Extract tables
                        tables = page.extract_tables()
                        if tables:
                            for table in tables:
                                for row in table:
                                    data.append(row)
                        else:
                            # Extract text if no tables found
                            text = page.extract_text()
                            if text:
                                lines = text.split('\n')
                                for line in lines:
                                    if line.strip():  # Skip empty lines
                                        data.append([line])
                
                if not data:
                    st.error("No data extracted from PDF. The PDF might be empty or contain only images.")
                else:
                    # Create DataFrame
                    df = pd.DataFrame(data)
                    
                    # Show preview
                    st.subheader("📊 Preview (First 10 rows)")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    st.info(f"Total rows extracted: {len(df)}")
                    
                    # Convert to CSV
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False, header=False)
                    csv_data = csv_buffer.getvalue()
                    
                    # Download button
                    csv_filename = uploaded_file.name.replace(".pdf", ".csv")
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv_data,
                        file_name=csv_filename,
                        mime="text/csv",
                        type="primary"
                    )
                    
                    st.success("✅ Conversion complete!")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Please make sure your PDF is not corrupted and try again.")
else:
    st.info("👆 Please upload a PDF file to get started")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
