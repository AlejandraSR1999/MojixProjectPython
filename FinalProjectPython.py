import streamlit as st
import pandas as pd

st.markdown('# Mojix Discrepancy Project ')
st.markdown('This tool helps during the join proccess of important files for Mojix Business')
st.markdown('Please watch the video demo for better understanding of the tool')


video1 = open ("streamlit-FinalProjectPython.mp4","rb")

st.video(video1)

def merge_files(df_expected, df_counted):
    """
    Merge the files

    """
    df_counted = df_counted.drop_duplicates("RFID")
    df_B = df_counted.groupby("Retail_Product_SKU").count()[["RFID"]].reset_index().rename(columns={"RFID":"Retail_CCQTY"})
    my_cols_selected = ["Retail_Product_Color",
    "Retail_Product_Level1",
    "Retail_Product_Level1Name",
    "Retail_Product_Level2Name",
    "Retail_Product_Level3Name",
    "Retail_Product_Level4Name",
    "Retail_Product_Name",
    "Retail_Product_SKU",
    "Retail_Product_Size",
    "Retail_Product_Style",
    "Retail_SOHQTY"]
    df_A = df_expected[my_cols_selected]
    return pd.merge(df_A, df_B, how="outer", left_on="Retail_Product_SKU", right_on="Retail_Product_SKU", indicator=True)


@st.cache
def convert_df(df):
    """
    Dataframe to CSV
    """
    return df.to_csv().encode('utf-8')



# uploads
expected_list_upload_file = st.file_uploader('STEP 1: Upload the Expected Data List from Mojix')
counted_list_upload_file = st.file_uploader('STEP 2: Upload the Counted Data List from Mojix')

if expected_list_upload_file is not None:
    df_expected = pd.read_csv(expected_list_upload_file)

if counted_list_upload_file is not None:
    df_counted = pd.read_csv(counted_list_upload_file)

if st.button('Merge'):
    if (expected_list_upload_file is not None) & (counted_list_upload_file is not None):
        df_merge = merge_files(df_expected, df_counted)

# summary stats
        col1, col2, col3 = st.columns(3)
        col1.metric('Number of Rows', len(df_merge))
        try:
            cnt_name = len(df_merge.loc[~df_merge['Retail_Product_Name'].isnull()])
        except:
            cnt_name = 0
        skip_trace_name_prct = str(int(cnt_name / len(df_merge) * 100)) + '%'
        col2.metric('% Skip Traced RetailName', skip_trace_name_prct)

        try:
            cnt_SKU = len(df_merge.loc[~df_merge['Retail_Product_SKU'].isnull()])
        except:
            cnt_SKU = 0
        skip_trace_SKU_prct = str(int(cnt_SKU / len(df_merge) * 100)) + '%'
        col3.metric('% Skip Traced SKU', skip_trace_SKU_prct)
    
        # output
        st.dataframe(df_merge.head(10)) # show first 10
    elif (expected_list_upload_file == None) & (counted_list_upload_file is not None):
        st.error('Please upload the Expected Data List file')
    elif (expected_list_upload_file is not None) & (counted_list_upload_file == None):
        st.error('Please upload the Counted Data List file')
    else:
        st.error('Please upload the Expected Data AND Counted Data List file')