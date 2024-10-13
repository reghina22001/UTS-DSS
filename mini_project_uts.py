import streamlit as st
import pandas as pd
import numpy as np

# Function to load the CSV file directly in the code
def load_data():
    data = pd.read_csv('dataset.csv', encoding='ISO-8859-1')
    return data

# SAW algorithm
def saw(data, targets, target_values):
    normalized_data = data.copy()
    for column in targets:
        normalized_data[column] = normalized_data[column] / normalized_data[column].max()
    normalized_data['Score'] = normalized_data[targets].dot(target_values)
    normalized_data['Rank'] = normalized_data['Score'].rank(ascending=False, method='min')
    return normalized_data

# TOPSIS algorithm
def topsis(data, targets, target_values):
    normalized_data = data.copy()
    for column in targets:
        normalized_data[column] = normalized_data[column] / np.sqrt((normalized_data[column]**2).sum())
    weighted_matrix = normalized_data[targets] * target_values
    ideal_solution = weighted_matrix.max()
    anti_ideal_solution = weighted_matrix.min()
    normalized_data['Positive Distance'] = np.sqrt(((weighted_matrix - ideal_solution) ** 2).sum(axis=1))
    normalized_data['Negative Distance'] = np.sqrt(((weighted_matrix - anti_ideal_solution) ** 2).sum(axis=1))
    normalized_data['Score'] = normalized_data['Negative Distance'] / (normalized_data['Positive Distance'] + normalized_data['Negative Distance'])
    normalized_data['Rank'] = normalized_data['Score'].rank(ascending=False, method='min')
    return normalized_data

# AHP algorithm (simplified version)
def ahp(data, targets, target_values):
    normalized_data = data.copy()
    for column in targets:
        normalized_data[column] = normalized_data[column].max() / normalized_data[column]
    normalized_data['Score'] = normalized_data[targets].dot(target_values)
    normalized_data['Rank'] = normalized_data['Score'].rank(ascending=False, method='min')
    return normalized_data

# WP algorithm
def wp(data, targets, target_values):
    normalized_data = data.copy()
    for column in targets:
        normalized_data[column] = normalized_data[column] / normalized_data[column].max()
    normalized_data['Score'] = np.prod(np.power(normalized_data[targets], target_values), axis=1)
    normalized_data['Rank'] = normalized_data['Score'].rank(ascending=False, method='min')
    return normalized_data

# Streamlit app layout
def main():
    st.set_page_config(page_title="Kalori Cermat", page_icon="🍽️", layout="centered")

    st.markdown("""
        <div style='background-color:#f8f9fa;padding:20px;border-radius:10px;text-align:center;'>
            <h1 style='color:black;font-size:38px;'>🍽️Kalori Cermat🍽️</h1>
            <h3 style='color:#e91e63;font-size:24px;'> Sistem Pendukung Keputusan untuk Menu Diet Seimbang </h3>
        </div>
        """, unsafe_allow_html=True)

    st.write("### Selamat datang di Kalori Cermat! 🎉")
    st.write("""Dengan ini, kamu dapat menemukan menu diet terbaik yang sesuai dengan kebutuhan kalorimu. Pilih kriteria yang ingin kamu gunakan dan kami akan menghitung peringkat makanan terbaik! 🍴💪""")

    data = load_data()
    st.write(data)

    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown("### Pilih Kriteria dan Bobotnya 📊")
    target_columns = ['Kalori (kcal)', 'Protein (g)', 'Lemak (g)', 'Karbohidrat (g)', 'Serat (g)', 'Sodium (mg)']
    targets = st.multiselect("Select Criteria for Decision-Making", target_columns, default=target_columns)

    if len(targets) == 0:
        st.warning("Please select at least one criterion.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown("### Pilih Metode Algoritma 🧠")
    algorithm = st.selectbox("Select Algorithm", ["SAW", "TOPSIS", "AHP", "WP"])

    st.markdown("### Masukkan Bobot Kriteria ⚖️")
    target_values = []
    for target in targets:
        value = st.slider(f"Weight for {target} (0.0-1.0)", 0.0, 1.0, value=0.5)
        target_values.append(value)

    sorted_result = None  # Define sorted_result here

    if st.button("Hitung Peringkat 🍲"):
        result = None
        if algorithm == "SAW":
            result = saw(data, targets, target_values)
        elif algorithm == "TOPSIS":
            result = topsis(data, targets, target_values)
        elif algorithm == "AHP":
            result = ahp(data, targets, target_values)
        elif algorithm == "WP":
            result = wp(data, targets, target_values)

        if result is not None:
            st.markdown("## Hasil Peringkat 🏆")
            sorted_result = result.sort_values('Rank')
            sorted_result['Sequential Rank'] = range(1, len(sorted_result) + 1)
            st.write(sorted_result[['Nama Menu'] + targets + ['Score', 'Rank', 'Sequential Rank']])
            st.markdown('</div>', unsafe_allow_html=True)

    if sorted_result is not None:  # Only access sorted_result if it was defined
        st.write("### Top 5 Menu Terbaik 🎯")
        top_5 = sorted_result.head(5)
        st.table(top_5.style.apply(lambda x: ['background-color: #f8bbd0' if i < 5 else '' for i in range(len(x))], axis=0))

    st.markdown("""<hr style="margin-top: 50px;">
        <div style="text-align:center; color:#5f6368;">
            <p>Dikembangkan oleh <b>Tim Kalori Cermat</b> | 2024 🍽️</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
