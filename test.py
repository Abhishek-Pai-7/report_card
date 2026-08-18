# Importing Libraries
import streamlit as st
import pandas as pd
import os 




# Designing Streamlit Page
st.set_page_config(page_title="Report Card", layout="wide") 
st.title("📊 Report Card")



# -------- USER INPUT -------- 
gstin = st.text_input("Enter GSTIN")

if gstin:
    
    def parse_sections(path, sheet_name=0):
        raw = pd.read_excel(path, sheet_name=sheet_name, header=None)

        # split into blocks on fully blank rows
        blocks, current = [], []
        for _, row in raw.iterrows():
            if row.isna().all():
                if current:
                    blocks.append(current)
                    current = []
            else:
                current.append(row)
        if current:
            blocks.append(current)

        sections = []
        for block in blocks:
            first = block[0]
            filled = first.notna().sum()

            if filled == 1 and len(block) >= 2:          # title present
                title = str(first.dropna().iloc[0]).strip()
                header, body = block[1], block[2:]
            else:                                        # header-only block
                title = None
                header, body = block[0], block[1:]

            cols = [str(c).strip() if pd.notna(c) else "" for c in header]
            keep = [i for i, c in enumerate(cols) if c != ""]

            df = pd.DataFrame([[r.iloc[i] for i in keep] for r in body],
                            columns=[cols[i] for i in keep])
            df = df.dropna(how="all").reset_index(drop=True)

            sections.append((title, df))

        return sections


    def to_dict(sections):
        """Same content keyed by title, for lookup by name."""
        return {t: df for t, df in sections if t}






    st.info("Downloading file...")
    try:
        sections = parse_sections("sample1.xlsx")
        l1=[]
        l2=[]

        for title, df in sections:
            l1.append(title)
            l2.append(df)

    except Exception as e:
        st.error(f"Error loading report: {e}")

    st.subheader("Showing Report Card")

    for title, table in zip(l1, l2):
        st.markdown(f"### {title}")
        st.dataframe(table, use_container_width=True)