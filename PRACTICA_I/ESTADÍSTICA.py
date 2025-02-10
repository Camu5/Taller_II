# ==============================
#       Análisis Estadístico
#   Santiago Caballero Rosas
# ==============================

# ==============================
#       Análisis Estadístico
#   Comparación CONTROL vs ECI
# ==============================

import pandas as pd
import scipy.stats as stats

# Datos extraídos
data = {
    "GFAP_Control": [0.00014430, 0.0002991, 0.0004652, 0.000216],
    "GFAP_ECI": [0.000403639, 0.00034807, 0.000298, 0.00013],
    "Ki67_Control": [0.00007312, 0.00024777, 0.00013613, 0.000443],
    "Ki67_ECI": [0.0000396, 0.0000449993, 0.0000765, 0.00058],
    "DCX_Control": [0.00041615, 0.00033835, 0.000352744, 0.000357],
    "DCX_ECI": [0.00028845, 0.000178043, 0.000303, 0.0004305],
    "CB_Control": [26528.4323, 11969.211, 42891.9113, 93528.26],
    "CB_ECI": [15550.297, 15226.4145, 17100.714, 49788.77]
}

# Convertir a DataFrame
df = pd.DataFrame(data)

# Diccionario para almacenar resultados
results_ec = {}

# Función para evaluar normalidad
def test_normality(data_control, data_eci, marker):
    p_control = stats.shapiro(data_control).pvalue
    p_eci = stats.shapiro(data_eci).pvalue
    
    print(f"\n🔍 **Prueba de Normalidad (Shapiro-Wilk) para {marker}**")
    print(f"   - p-valor CONTROL: {p_control:.5f}")
    print(f"   - p-valor ECI: {p_eci:.5f}")
    
    normal_control = p_control > 0.05
    normal_eci = p_eci > 0.05
    both_normal = normal_control and normal_eci
    
    if both_normal:
        print(f"✅ Ambos grupos son normales. Se aplicará **t-Student**.")
    else:
        print(f"⚠️ Al menos uno de los grupos **NO** es normal. Se aplicará **Mann-Whitney U**.")
    
    return both_normal

# Función para realizar prueba estadística adecuada
def perform_test(data_control, data_eci, marker):
    if test_normality(data_control, data_eci, marker):
        # Prueba t de Student para muestras independientes si los datos son normales
        t_stat, p_value = stats.ttest_ind(data_control, data_eci, equal_var=False)
        test_type = "t-Student"
    else:
        # Prueba de Mann-Whitney U si los datos no son normales
        t_stat, p_value = stats.mannwhitneyu(data_control, data_eci, alternative='two-sided')
        test_type = "Mann-Whitney U"
    
    print(f"📊 **Prueba aplicada para {marker}:** {test_type}")
    print(f"   - T-Statistic: {t_stat:.5f}")
    print(f"   - P-Value: {p_value:.5f}\n")
    
    return t_stat, p_value, test_type

# Realizar pruebas estadísticas
for marker in ["GFAP", "Ki67", "DCX", "CB"]:
    t_stat, p_value, test_type = perform_test(df[f"{marker}_Control"], df[f"{marker}_ECI"], marker)
    results_ec[marker] = {"Test Type": test_type, "T-Statistic": t_stat, "P-Value": p_value}

# Convertir resultados a DataFrame y mostrar
results_ec_df = pd.DataFrame.from_dict(results_ec, orient="index")
print("\n🔹 **Resultados Finales:**")
print(results_ec_df)

# Función para interpretar los resultados
def interpret_results(t_stat, p_value, marker, test_type):
    significance_threshold = 0.05  # Nivel de significancia
    if p_value < significance_threshold:
        if t_stat > 0:
            return f"✅ Para {marker}, el grupo ECI tiene valores significativamente mayores que el grupo CONTROL según la prueba **{test_type}** (p = {p_value:.5f})."
        else:
            return f"✅ Para {marker}, el grupo CONTROL tiene valores significativamente mayores que el grupo ECI según la prueba **{test_type}** (p = {p_value:.5f})."
    else:
        return f"❌ Para {marker}, no se encontraron diferencias significativas entre CONTROL y ECI según la prueba **{test_type}** (p = {p_value:.5f})."

# Interpretar resultados
print("\n🔹 **Interpretación de Resultados:**")
for marker in results_ec:
    interpretation = interpret_results(results_ec[marker]["T-Statistic"], results_ec[marker]["P-Value"], marker, results_ec[marker]["Test Type"])
    print(interpretation)
