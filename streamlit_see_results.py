
import os
import pandas as pd
import sqlite3
import streamlit as st


drop_cols = [
    'index',
    'max_ml_odds',
    'runtime',
    'min_dist',
    'max_dist',
    'min_field_size',
    'bottom_n_ascending',
    'bottom_n',
    'bottom_n_metrics',
]


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    st.header('Results')


    fileuploadcsv = st.file_uploader(f'Load CSV results file')
    if not fileuploadcsv:
        st.stop()

    df_all_results = pd.read_csv(fileuploadcsv)

    mind = st.slider('Select minimum distance', value=6.5, min_value=6.5, max_value=11.0, step=0.50)
    maxd = st.slider('Select max distance', value=9.0, min_value=6.5, max_value=11.0, step=0.50)

    all_query = f"""
    SELECT *
    FROM strat_results
    WHERE min_dist >= {mind}
    AND max_dist <= {maxd}
    """


    all_strats = df_all_results['strategy'].unique()
    minfieldsize = st.slider('Select the minimum field size to be used in strategy evaluation', value=6, min_value=5, max_value=10, step=1)
    selected_strats = st.multiselect('Select strategies to include', options=list(all_strats))
    df_filtered = df_all_results.loc[
        (df_all_results['min_dist'] == mind) &
        (df_all_results['max_dist'] == maxd) &
        (df_all_results['min_field_size'] == minfieldsize) &
        (df_all_results['strategy'].isin(selected_strats))
    ]
    df_filtered.drop([x for x in drop_cols if x in set(df_all_results.columns)], axis=1, inplace=True)
    df_filtered = df_filtered.sort_values(['hit_rate', 'evaluable'], ascending=False)
    st.dataframe(df_filtered.head(200), height=800)






