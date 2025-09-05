import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Balance de Masa | Pulpa de Fruta",
    page_icon="🍓",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Título y Descripción ---
st.title("Calculadora de Balance de Masa 🍇")
st.header("Ajuste de °Brix en Pulpa de Fruta")

st.markdown("""
Esta aplicación te ayuda a calcular la cantidad de azúcar necesaria para
aumentar la concentración de sólidos solubles (°Brix) en una pulpa de fruta,
basado en un problema de balance de materia.
""")

st.image('https://images.unsplash.com/photo-1599394591348-18c394432c9e?q=80&w=2070&auto=format&fit=crop',
         caption='Procesamiento de pulpa de fruta')

# --- Entradas del Usuario con Columnas para Mejor Diseño ---
st.sidebar.header("Parámetros de Entrada")

# Valores por defecto del problema
default_mass = 50.0
default_initial_brix = 7.0
default_final_brix = 10.0

# Usamos la barra lateral para las entradas
m_pulpa = st.sidebar.number_input(
    'Masa inicial de pulpa (kg)',
    min_value=0.1,
    value=default_mass,
    step=1.0,
    help="Ingresa la cantidad de pulpa que tienes actualmente."
)

c_inicial = st.sidebar.number_input(
    'Concentración inicial (°Brix)',
    min_value=0.0,
    max_value=100.0,
    value=default_initial_brix,
    step=0.1,
    help="Ingresa el porcentaje de sólidos (°Brix) medido en la pulpa inicial."
)

c_final = st.sidebar.number_input(
    'Concentración final deseada (°Brix)',
    min_value=c_inicial, # La concentración final no puede ser menor a la inicial
    max_value=100.0,
    value=default_final_brix,
    step=0.1,
    help="Ingresa el porcentaje de sólidos (°Brix) que deseas alcanzar."
)

# --- Lógica de Cálculo ---
if st.sidebar.button('Calcular Cantidad de Azúcar', type="primary"):
    if c_final <= c_inicial:
        st.error("Error: La concentración final deseada debe ser mayor que la concentración inicial.")
    else:
        # Conversión de °Brix (porcentaje) a fracción
        c_inicial_frac = c_inicial / 100
        c_final_frac = c_final / 100

        # Ecuación de balance de masa despejada para la masa de azúcar
        # M_azucar = (M_pulpa * (C_final - C_inicial)) / (1 - C_final)
        try:
            m_azucar = (m_pulpa * (c_final_frac - c_inicial_frac)) / (1 - c_final_frac)

            st.success(f"**Resultado del Cálculo:**")
            st.metric(
                label="Cantidad de azúcar a agregar",
                value=f"{m_azucar:.2f} kg"
            )

            # --- Expander para mostrar el desarrollo del cálculo ---
            with st.expander("Ver el desarrollo del cálculo y las ecuaciones"):
                st.subheader("Ecuaciones de Balance de Materia")
                st.markdown("""
                1.  **Balance General de Masa:**
                    La masa final es la suma de la masa inicial de la pulpa más el azúcar agregado.
                    $$ M_{final} = M_{pulpa} + M_{azúcar} $$
                2.  **Balance de Sólidos (Azúcar):**
                    Los sólidos en la mezcla final son la suma de los sólidos iniciales más el azúcar puro agregado.
                    $$ M_{final} \\times C_{final} = (M_{pulpa} \\times C_{inicial}) + M_{azúcar} $$
                """)

                st.subheader("Desarrollo del Problema")
                st.markdown(f"""
                **1. Datos Iniciales:**
                -   Masa de pulpa ($M_{{pulpa}}$): **{m_pulpa} kg**
                -   Concentración inicial ($C_{{inicial}}$): **{c_inicial}%**
                -   Concentración final ($C_{{final}}$): **{c_final}%**

                **2. Sustituyendo el Balance General en el Balance de Sólidos:**
                $$ (M_{{pulpa}} + M_{{azúcar}}) \\times C_{{final}} = (M_{{pulpa}} \\times C_{{inicial}}) + M_{{azúcar}} $$

                **3. Despejando $M_{{azúcar}}$:**
                $$ M_{{azúcar}} = \\frac{{M_{{pulpa}} \\times (C_{{final}} - C_{{inicial}})}}{{1 - C_{{final}}}} $$

                **4. Cálculo con los valores ingresados (usando fracciones):**
                $$ M_{{azúcar}} = \\frac{{{m_pulpa} \\text{{ kg}} \\times ({c_final_frac} - {c_inicial_frac})}}{{1 - {c_final_frac}}} $$
                $$ M_{{azúcar}} = \\frac{{{m_pulpa} \\times ({c_final_frac - c_inicial_frac:.3f})}}{{{1 - c_final_frac:.3f}}} $$
                $$ M_{{azúcar}} = \\frac{{{m_pulpa * (c_final_frac - c_inicial_frac):.3f}}}{{{1 - c_final_frac:.3f}}} = \\bf{{{m_azucar:.3f} \\text{{ kg}}}} $$
                """)
        except ZeroDivisionError:
            st.error("Error: La concentración final no puede ser 100 °Brix (100%), ya que resultaría en una división por cero.")

# --- Pie de página ---
st.markdown("---")
st.markdown("Creado con ❤️ usando [Streamlit](https://streamlit.io).")
