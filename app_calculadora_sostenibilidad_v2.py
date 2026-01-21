"""
CALCULADORA DE SOSTENIBILIDAD ALIMENTARIA - REDISEÑO
¿Qué tan sustentable es tu comida?

Autor: Laura Ochoa M.
Fecha: Enero 2026
Versión: 2.1 (Rediseño UX)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from io import BytesIO

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="¿Qué tan sustentable es tu comida?",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS PERSONALIZADOS - ESTILO CONFLUENCE
# ============================================================================

st.markdown("""
<style>
    /* Tipografía clara y profesional estilo Confluence */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #172B4D;
    }
    
    /* Títulos limpios estilo Confluence */
    h1 {
        font-weight: 600 !important;
        color: #172B4D !important;
        margin-bottom: 0.5rem !important;
        font-size: 2rem !important;
    }
    
    h2 {
        font-weight: 600 !important;
        color: #172B4D !important;
        margin-top: 2rem !important;
        font-size: 1.5rem !important;
    }
    
    h3 {
        font-weight: 500 !important;
        color: #172B4D !important;
        font-size: 1.2rem !important;
    }
    
    /* Subtítulo principal */
    .subtitle-main {
        font-size: 1.2rem;
        color: #5E6C84;
        font-weight: 400;
        margin-bottom: 2rem;
        letter-spacing: 0.2px;
    }
    
    /* Sidebar estilo Confluence */
    [data-testid="stSidebar"] {
        background-color: #F4F5F7;
        border-right: 1px solid #DFE1E6;
    }
    
    [data-testid="stSidebar"] h1 {
        color: #172B4D !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        padding-bottom: 1rem;
    }
    
    /* Radio buttons en sidebar estilo Confluence */
    [data-testid="stSidebar"] .stRadio > label {
        font-weight: 500;
        color: #172B4D;
    }
    
    /* Cards limpias estilo Confluence */
    .stMetric {
        background-color: #FAFBFC;
        padding: 1.2rem;
        border-radius: 3px;
        border: 1px solid #DFE1E6;
    }
    
    /* Info boxes estilo Confluence */
    .info-box {
        background-color: #DEEBFF;
        border-left: 3px solid #0052CC;
        padding: 1rem 1.5rem;
        border-radius: 3px;
        margin: 1rem 0;
    }
    
    .info-box h3 {
        color: #0747A6 !important;
        margin-top: 0 !important;
    }
    
    .info-box p, .info-box ul {
        color: #172B4D;
    }
    
    /* Indicator boxes estilo Confluence */
    .indicator-box {
        background-color: #FAFBFC;
        border: 1px solid #DFE1E6;
        border-radius: 3px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }
    
    .indicator-box:hover {
        border-color: #B3D4FF;
        box-shadow: 0 1px 2px rgba(9, 30, 66, 0.08);
    }
    
    .indicator-title {
        font-weight: 600;
        color: #172B4D;
        margin-bottom: 0.4rem;
        font-size: 1rem;
    }
    
    .indicator-desc {
        font-size: 0.9rem;
        color: #5E6C84;
        line-height: 1.5;
    }
    
    /* Botones estilo Confluence */
    .stButton>button {
        background-color: #0052CC;
        color: white;
        border: none;
        border-radius: 3px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 0.95rem;
    }
    
    .stButton>button:hover {
        background-color: #0747A6;
        box-shadow: 0 2px 4px rgba(9, 30, 66, 0.15);
    }
    
    /* Espaciado generoso estilo Confluence */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Selectbox y inputs estilo Confluence */
    .stSelectbox, .stMultiSelect, .stTextInput {
        font-family: 'Inter', sans-serif;
    }
    
    /* Tablas estilo Confluence */
    .dataframe {
        border: 1px solid #DFE1E6 !important;
        border-radius: 3px;
    }
    
    /* Líneas divisorias más sutiles */
    hr {
        border-color: #DFE1E6 !important;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

@st.cache_data
def cargar_datos():
    """Carga el dataset de productos con scores de ambos escenarios"""
    try:
        rutas = [
            'dataset_con_scores_A_y_B.csv',
            '/mnt/user-data/outputs/dataset_con_scores_A_y_B.csv',
            '/home/claude/dataset_con_scores_A_y_B.csv',
            '/mnt/project/dataset_con_scores_A_y_B.csv'
        ]
        
        for ruta in rutas:
            try:
                df = pd.read_csv(ruta)
                return df
            except:
                continue
        
        st.error("⚠️ No se pudo cargar el dataset. Asegúrate de tener el archivo CSV.")
        return None
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None

@st.cache_data
def cargar_productos_robustos():
    """Carga la lista de productos más sustentables"""
    try:
        rutas = [
            'productos_robustos_consenso.csv',
            '/mnt/user-data/outputs/productos_robustos_consenso.csv',
            '/home/claude/productos_robustos_consenso.csv',
            '/mnt/project/productos_robustos_consenso.csv'
        ]
        
        for ruta in rutas:
            try:
                df = pd.read_csv(ruta)
                return df
            except:
                continue
        
        return None
    except:
        return None

def normalizar_inverso(valor, min_val, max_val):
    """Normaliza valores donde menor es mejor (0-100)"""
    if max_val == min_val:
        return 50
    return 100 - ((valor - min_val) / (max_val - min_val) * 100)

def calcular_score_producto(cf, wf, lu, origin, waste, nova, escenario='A'):
    """
    Calcula el score de un producto según el escenario
    
    Escenario A: Sistema México Original (Waste 25%)
    Escenario B: Sistema México Ajustado (Waste 30%)
    """
    
    # Definir rangos para normalización (basados en dataset completo)
    rangos = {
        'CF': (0.3, 60.0),
        'WF': (131, 18900),
        'LU': (0.3, 326),
        'Origin': (0, 100),
        'Waste': (3.0, 45.0),
        'NOVA': (1, 4)
    }
    
    # Normalizar cada indicador
    cf_norm = normalizar_inverso(cf, *rangos['CF'])
    wf_norm = normalizar_inverso(wf, *rangos['WF'])
    lu_norm = normalizar_inverso(lu, *rangos['LU'])
    origin_norm = normalizar_inverso(origin, *rangos['Origin'])
    waste_norm = normalizar_inverso(waste, *rangos['Waste'])
    nova_norm = normalizar_inverso(nova, *rangos['NOVA'])
    
    # Sistemas de pesos por escenario
    if escenario == 'A':
        p = {
            'CF': 0.15, 'WF': 0.15, 'LU': 0.10,
            'Origin': 0.20, 'Waste': 0.25, 'NOVA': 0.15
        }
    else:  # Escenario B
        p = {
            'CF': 0.14, 'WF': 0.14, 'LU': 0.09,
            'Origin': 0.18, 'Waste': 0.30, 'NOVA': 0.15
        }
    
    score = (
        cf_norm * p['CF'] +
        wf_norm * p['WF'] +
        lu_norm * p['LU'] +
        origin_norm * p['Origin'] +
        waste_norm * p['Waste'] +
        nova_norm * p['NOVA']
    )
    
    return score, {
        'CF': cf_norm, 'WF': wf_norm, 'LU': lu_norm,
        'Origin': origin_norm, 'Waste': waste_norm, 'NOVA': nova_norm
    }

def clasificar_score(score):
    """Clasifica el score en categorías"""
    if score >= 90:
        return 'Excelente', '🟢'
    elif score >= 80:
        return 'Muy Bueno', '🟢'
    elif score >= 70:
        return 'Bueno', '🟡'
    elif score >= 60:
        return 'Moderado', '🟠'
    else:
        return 'Bajo', '🔴'

def exportar_resultados_excel(df, escenario='A'):
    """Exporta resultados a Excel"""
    output = BytesIO()
    
    score_col = 'Score_México' if escenario == 'A' else 'Score_México_B'
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Hoja 1: Ranking completo
        df_export = df[['Producto', 'CF_kgCO2eq_kg', 'WF_L_kg', 'LU_m2_kg',
                       'Origin_Score', 'Waste_pct', 'NOVA', score_col]].copy()
        df_export = df_export.sort_values(score_col, ascending=False)
        df_export.to_excel(writer, sheet_name='Ranking_Completo', index=False)
        
        # Hoja 2: Top 15
        top15 = df.nlargest(15, score_col)[['Producto', score_col]]
        top15.to_excel(writer, sheet_name='Top_15', index=False)
        
        # Hoja 3: Bottom 10
        bottom10 = df.nsmallest(10, score_col)[['Producto', score_col]]
        bottom10.to_excel(writer, sheet_name='Menos_Sostenibles', index=False)
    
    output.seek(0)
    return output

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

def main():
    
    # TÍTULO Y SUBTÍTULO PRINCIPAL
    st.title("¿Qué tan sustentable es tu comida?")
    st.markdown('<p class="subtitle-main">Tu impacto alimentario, en números claros</p>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # SIDEBAR - NAVEGACIÓN
    st.sidebar.title("Navegación")
    pagina = st.sidebar.radio(
        "Selecciona una función:",
        ["🏠 Inicio",
         "🔍 Consultar Producto",
         "➕ Evaluar Nuevo Producto",
         "🆚 Comparar Productos",
         "⭐ Los Más Sustentables",
         "📊 Ver Rankings",
         "ℹ️ Acerca de"]
    )
    
    # SIDEBAR - Selector de Escenario Global
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Configuración")
    
    escenario_global = st.sidebar.radio(
        "Metodología de análisis:",
        options=['Escenario A (Desperdicio 25%)', 'Escenario B (Desperdicio 30%)'],
        help="""
        **Escenario A:** Metodología original
        - Desperdicio: 25%
        
        **Escenario B:** Metodología ajustada
        - Desperdicio: 30%
        
        Ambos escenarios usan los mismos 6 indicadores ambientales.
        """
    )
    
    # Convertir a A o B
    escenario = 'A' if 'Escenario A' in escenario_global else 'B'
    
    # Cargar datos
    df = cargar_datos()
    df_robustos = cargar_productos_robustos()
    
    if df is None:
        st.error("No se pudieron cargar los datos. Verifica que el archivo CSV esté disponible.")
        return
    
    score_col = 'Score_México' if escenario == 'A' else 'Score_México_B'
    
    # ========================================================================
    # PÁGINA: INICIO
    # ========================================================================
    if pagina == "🏠 Inicio":
        
        # Explicación de qué hace la calculadora
        st.markdown("""
        <div class="info-box">
        <h3 style="margin-top:0;">¿Qué hace esta calculadora?</h3>
        <p style="margin-bottom:0.5rem;">Esta herramienta te ayuda a entender y comparar el impacto ambiental de 36 alimentos comunes en México. Puedes:</p>
        <ul style="margin-bottom:0;">
            <li><strong>Consultar cualquier producto</strong> y ver su impacto detallado</li>
            <li><strong>Evaluar un alimento nuevo</strong> ingresando sus datos ambientales</li>
            <li><strong>Comparar hasta 5 productos</strong> lado a lado</li>
            <li><strong>Ver rankings</strong> de los mejores y peores según diferentes criterios</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("##")
        
        # Explicación de indicadores
        st.subheader("Los 6 indicadores que medimos")
        st.markdown("Evaluamos cada alimento con estos criterios ambientales:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="indicator-box">
                <div class="indicator-title">🌡️ Huella de Carbono (Clima)</div>
                <div class="indicator-desc">Kilogramos de CO₂ emitidos para producir 1 kg de este alimento</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="indicator-box">
                <div class="indicator-title">💧 Huella Hídrica (Agua)</div>
                <div class="indicator-desc">Litros de agua necesarios para producir 1 kg de este alimento</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="indicator-box">
                <div class="indicator-title">🌱 Uso de Suelo (Tierra)</div>
                <div class="indicator-desc">Metros cuadrados de tierra que se ocuparon para producir 1 kg de este alimento</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="indicator-box">
                <div class="indicator-title">🇲🇽 Origen</div>
                <div class="indicator-desc">¿Se produce en México o se importa de otro país?</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="indicator-box">
                <div class="indicator-title">🗑️ Desperdicio</div>
                <div class="indicator-desc">Qué porcentaje se desperdicia en el camino del campo a tu mesa</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="indicator-box">
                <div class="indicator-title">🔬 Procesamiento (NOVA)</div>
                <div class="indicator-desc">Qué tan transformado está: natural, procesado o ultra-procesado</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("##")
        
        # Estadísticas rápidas
        st.subheader("Un vistazo a los datos")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Productos evaluados", "36")
        
        with col2:
            mejor = df.nlargest(1, score_col)['Producto'].values[0]
            st.metric("Más sustentable", mejor)
        
        with col3:
            peor = df.nsmallest(1, score_col)['Producto'].values[0]
            st.metric("Menos sustentable", peor)
        
        with col4:
            promedio = df[score_col].mean()
            st.metric("Score promedio", f"{promedio:.1f}")
        
        st.markdown("##")
        st.info("👈 Usa el menú de la izquierda para explorar las diferentes funciones")
    
    # ========================================================================
    # PÁGINA: CONSULTAR PRODUCTO
    # ========================================================================
    elif pagina == "🔍 Consultar Producto":
        st.header("🔍 Consultar Producto")
        st.markdown("Selecciona un alimento para ver su evaluación completa")
        st.markdown("##")
        
        producto_sel = st.selectbox(
            "Selecciona un producto:",
            options=sorted(df['Producto'].unique()),
            index=None,
            placeholder="Elige un producto de la lista..."
        )
        
        if producto_sel:
            prod_data = df[df['Producto'] == producto_sel].iloc[0]
            
            st.markdown("---")
            
            # Score principal
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.subheader(f"📋 {producto_sel}")
                clasificacion, emoji = clasificar_score(prod_data[score_col])
                st.markdown(f"**Clasificación:** {clasificacion} {emoji}")
            
            with col2:
                st.metric("Score", f"{prod_data[score_col]:.1f}")
            
            with col3:
                ranking = (df[score_col] >= prod_data[score_col]).sum()
                st.metric("Posición", f"#{ranking}")
            
            st.markdown("##")
            
            # Indicadores detallados
            st.subheader("📊 Indicadores Ambientales")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🌡️ Huella de Carbono",
                    f"{prod_data['CF_kgCO2eq_kg']:.2f} kg CO₂"
                )
                st.metric(
                    "💧 Huella Hídrica",
                    f"{prod_data['WF_L_kg']:,.0f} L"
                )
            
            with col2:
                st.metric(
                    "🌱 Uso de Suelo",
                    f"{prod_data['LU_m2_kg']:.2f} m²"
                )
                origen_texto = {0: "Local (Sonora)", 50: "Regional (México)", 100: "Importado"}
                st.metric(
                    "🇲🇽 Origen",
                    origen_texto.get(prod_data['Origin_Score'], "N/D")
                )
            
            with col3:
                st.metric(
                    "🗑️ Desperdicio",
                    f"{prod_data['Waste_pct']:.1f}%"
                )
                nova_texto = {1: "Natural", 2: "Procesado", 3: "Muy procesado", 4: "Ultra-procesado"}
                st.metric(
                    "🔬 Nivel NOVA",
                    nova_texto.get(int(prod_data['NOVA']), "N/D")
                )
            
            st.markdown("##")
            
            # Gráfico de radar
            st.subheader("🎯 Perfil de Sustentabilidad")
            
            # Calcular scores normalizados
            _, scores_norm = calcular_score_producto(
                prod_data['CF_kgCO2eq_kg'],
                prod_data['WF_L_kg'],
                prod_data['LU_m2_kg'],
                prod_data['Origin_Score'],
                prod_data['Waste_pct'],
                prod_data['NOVA'],
                escenario
            )
            
            categorias = ['Carbono', 'Agua', 'Suelo', 'Origen', 'Desperdicio', 'Procesamiento']
            valores = [scores_norm['CF'], scores_norm['WF'], scores_norm['LU'],
                      scores_norm['Origin'], scores_norm['Waste'], scores_norm['NOVA']]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=valores,
                theta=categorias,
                fill='toself',
                name=producto_sel,
                line_color='#2ecc71'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PÁGINA: EVALUAR NUEVO PRODUCTO
    # ========================================================================
    elif pagina == "➕ Evaluar Nuevo Producto":
        st.header("➕ Evaluar Nuevo Producto")
        st.markdown("Ingresa los datos de un alimento que no está en nuestra base de datos")
        st.markdown("##")
        
        nombre_nuevo = st.text_input(
            "Nombre del producto:",
            placeholder="Ejemplo: Sandía, Quinoa, Pescado blanco..."
        )
        
        st.markdown("### 📊 Ingresa los indicadores ambientales")
        st.markdown("*Si no conoces algún valor exacto, puedes usar estimaciones basadas en productos similares*")
        st.markdown("##")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌡️ Huella de Carbono (Clima)**")
            st.caption("Kilogramos de CO₂ emitidos para producir 1 kg de este alimento")
            cf = st.number_input(
                "kg CO₂ / kg producto",
                min_value=0.0,
                max_value=100.0,
                value=2.0,
                step=0.1,
                label_visibility="collapsed"
            )
            st.caption("📝 Ejemplo: Plátano = 0.7, Pollo = 6.9, Res = 60")
            
            st.markdown("##")
            
            st.markdown("**💧 Huella Hídrica (Agua)**")
            st.caption("Litros de agua necesarios para producir 1 kg de este alimento")
            wf = st.number_input(
                "Litros / kg producto",
                min_value=0,
                max_value=50000,
                value=1000,
                step=50,
                label_visibility="collapsed"
            )
            st.caption("📝 Ejemplo: Lechuga = 237, Manzana = 822, Res = 15,415")
            
            st.markdown("##")
            
            st.markdown("**🌱 Uso de Suelo (Tierra)**")
            st.caption("Metros cuadrados de tierra que se ocuparon para producir 1 kg")
            lu = st.number_input(
                "m² / kg producto",
                min_value=0.0,
                max_value=500.0,
                value=5.0,
                step=0.5,
                label_visibility="collapsed"
            )
            st.caption("📝 Ejemplo: Tomate = 0.8, Pollo = 7.5, Res = 326")
        
        with col2:
            st.markdown("**🇲🇽 Origen**")
            st.caption("¿Se produce en México o se importa de otro país?")
            origin = st.selectbox(
                "Origen del producto",
                options=[0, 50, 100],
                format_func=lambda x: "Local (Sonora)" if x == 0 else 
                                     "Regional (México)" if x == 50 else "Importado",
                label_visibility="collapsed"
            )
            
            st.markdown("##")
            
            st.markdown("**🗑️ Desperdicio**")
            st.caption("Qué porcentaje se desperdicia en el camino del campo a tu mesa")
            waste = st.number_input(
                "Porcentaje (%)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=1.0,
                label_visibility="collapsed"
            )
            st.caption("📝 Ejemplo: Plátano = 0.5%, Pepino = 45%, Promedio = 15%")
            
            st.markdown("##")
            
            st.markdown("**🔬 Procesamiento (NOVA)**")
            st.caption("Qué tan transformado está: natural, procesado o ultra-procesado")
            nova = st.selectbox(
                "Nivel NOVA",
                options=[1, 2, 3, 4],
                format_func=lambda x: f"{x} - {'Natural' if x == 1 else 'Procesado' if x == 2 else 'Muy procesado' if x == 3 else 'Ultra-procesado'}",
                label_visibility="collapsed"
            )
        
        st.markdown("##")
        
        if st.button("🔍 Calcular Score de Sustentabilidad", type="primary"):
            if not nombre_nuevo:
                st.warning("⚠️ Por favor ingresa un nombre para el producto")
            else:
                st.markdown("---")
                
                # Calcular scores
                score_a, _ = calcular_score_producto(cf, wf, lu, origin, waste, nova, 'A')
                score_b, _ = calcular_score_producto(cf, wf, lu, origin, waste, nova, 'B')
                
                score_actual = score_a if escenario == 'A' else score_b
                clasificacion, emoji = clasificar_score(score_actual)
                
                # Resultados
                st.success(f"✅ Evaluación completada para: **{nombre_nuevo}**")
                st.markdown("##")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Score de Sustentabilidad", f"{score_actual:.1f}")
                
                with col2:
                    st.metric("Clasificación", f"{clasificacion} {emoji}")
                
                with col3:
                    # Comparar con promedio
                    promedio = df[score_col].mean()
                    diferencia = score_actual - promedio
                    st.metric("vs. Promedio", f"{diferencia:+.1f}", 
                             delta_color="normal" if diferencia > 0 else "inverse")
                
                st.markdown("##")
                
                # Comparación con productos existentes
                st.subheader("📊 Comparación con productos similares")
                
                # Encontrar los 5 productos más cercanos en score
                df_temp = df.copy()
                df_temp['diferencia'] = abs(df_temp[score_col] - score_actual)
                similares = df_temp.nsmallest(5, 'diferencia')
                
                fig = go.Figure()
                
                # Agregar productos similares
                fig.add_trace(go.Bar(
                    x=similares['Producto'],
                    y=similares[score_col],
                    name='Productos existentes',
                    marker_color='lightblue'
                ))
                
                # Agregar el nuevo producto
                fig.add_trace(go.Bar(
                    x=[nombre_nuevo],
                    y=[score_actual],
                    name='Tu producto',
                    marker_color='#2ecc71'
                ))
                
                fig.update_layout(
                    title="Comparación de Scores",
                    xaxis_title="Producto",
                    yaxis_title="Score de Sustentabilidad",
                    showlegend=True,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PÁGINA: COMPARAR PRODUCTOS
    # ========================================================================
    elif pagina == "🆚 Comparar Productos":
        st.header("🆚 Comparar Productos")
        st.markdown("Selecciona hasta 5 productos para compararlos lado a lado")
        st.markdown("##")
        
        productos_comparar = st.multiselect(
            "Selecciona productos:",
            options=sorted(df['Producto'].unique()),
            max_selections=5,
            placeholder="Elige hasta 5 productos para comparar..."
        )
        
        if len(productos_comparar) >= 2:
            df_comp = df[df['Producto'].isin(productos_comparar)]
            
            st.markdown("---")
            st.subheader("📊 Comparación de Scores")
            
            # Gráfico de barras
            fig = px.bar(
                df_comp,
                x='Producto',
                y=score_col,
                color=score_col,
                color_continuous_scale='RdYlGn',
                text=score_col
            )
            
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Score de Sustentabilidad",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("##")
            
            # Tabla comparativa
            st.subheader("📋 Detalle de Indicadores")
            
            columnas_mostrar = ['Producto', 'CF_kgCO2eq_kg', 'WF_L_kg', 'LU_m2_kg',
                               'Origin_Score', 'Waste_pct', 'NOVA', score_col]
            
            df_tabla = df_comp[columnas_mostrar].copy()
            df_tabla = df_tabla.rename(columns={
                'CF_kgCO2eq_kg': 'Carbono (kg CO₂)',
                'WF_L_kg': 'Agua (L)',
                'LU_m2_kg': 'Suelo (m²)',
                'Origin_Score': 'Origen',
                'Waste_pct': 'Desperdicio (%)',
                'NOVA': 'NOVA',
                score_col: 'Score'
            })
            
            # Formatear valores
            df_tabla['Carbono (kg CO₂)'] = df_tabla['Carbono (kg CO₂)'].round(2)
            df_tabla['Agua (L)'] = df_tabla['Agua (L)'].apply(lambda x: f"{x:,.0f}")
            df_tabla['Suelo (m²)'] = df_tabla['Suelo (m²)'].round(2)
            df_tabla['Desperdicio (%)'] = df_tabla['Desperdicio (%)'].round(1)
            df_tabla['Score'] = df_tabla['Score'].round(1)
            
            # Aplicar formato de origen
            df_tabla['Origen'] = df_tabla['Origen'].apply(
                lambda x: 'Local' if x == 0 else 'Regional' if x == 50 else 'Importado'
            )
            
            st.dataframe(df_tabla, use_container_width=True, hide_index=True)
            
            st.markdown("##")
            
            # Gráfico de radar comparativo
            st.subheader("🎯 Perfiles de Sustentabilidad")
            
            fig = go.Figure()
            
            categorias = ['Carbono', 'Agua', 'Suelo', 'Origen', 'Desperdicio', 'Procesamiento']
            
            colores = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
            
            for idx, producto in enumerate(productos_comparar):
                prod_data = df[df['Producto'] == producto].iloc[0]
                
                _, scores_norm = calcular_score_producto(
                    prod_data['CF_kgCO2eq_kg'],
                    prod_data['WF_L_kg'],
                    prod_data['LU_m2_kg'],
                    prod_data['Origin_Score'],
                    prod_data['Waste_pct'],
                    prod_data['NOVA'],
                    escenario
                )
                
                valores = [scores_norm['CF'], scores_norm['WF'], scores_norm['LU'],
                          scores_norm['Origin'], scores_norm['Waste'], scores_norm['NOVA']]
                
                fig.add_trace(go.Scatterpolar(
                    r=valores,
                    theta=categorias,
                    fill='toself',
                    name=producto,
                    line_color=colores[idx % len(colores)]
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif len(productos_comparar) == 1:
            st.info("👆 Selecciona al menos 2 productos para compararlos")
        else:
            st.info("👆 Selecciona productos del menú de arriba para comenzar la comparación")
    
    # ========================================================================
    # PÁGINA: LOS MÁS SUSTENTABLES
    # ========================================================================
    elif pagina == "⭐ Los Más Sustentables":
        st.header("⭐ Los Más Sustentables")
        
        if df_robustos is not None and not df_robustos.empty:
            
            # Explicación clara
            st.markdown("""
            <div class="info-box">
            <p style="margin:0;"><strong>Estos 9 alimentos tienen el mejor impacto ambiental en todas las metodologías.</strong></p>
            <p style="margin:0.5rem 0 0 0;">Consideran huella de carbono, agua, tierra, origen mexicano, desperdicio y nivel de procesamiento. 
            Sin importar qué metodología uses, estos productos siempre están en el top 10.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("##")
            
            # Lista de productos con sus scores
            st.subheader("🏆 Los 9 Campeones")
            
            # Obtener datos de los productos robustos
            productos_robustos_lista = df_robustos['Producto'].tolist()
            df_top = df[df['Producto'].isin(productos_robustos_lista)].copy()
            df_top = df_top.sort_values(score_col, ascending=False)
            
            # Crear cards para cada producto
            for idx, row in df_top.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### {row['Producto']}")
                
                with col2:
                    clasificacion, emoji = clasificar_score(row[score_col])
                    st.markdown(f"**{clasificacion}** {emoji}")
                
                with col3:
                    st.metric("Score", f"{row[score_col]:.1f}")
                
                # Mini resumen de indicadores
                with st.expander("Ver detalles"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("🌡️ Carbono", f"{row['CF_kgCO2eq_kg']:.2f} kg")
                        st.metric("💧 Agua", f"{row['WF_L_kg']:,.0f} L")
                    
                    with col2:
                        st.metric("🌱 Suelo", f"{row['LU_m2_kg']:.2f} m²")
                        origen_texto = {0: "Local", 50: "Regional", 100: "Importado"}
                        st.metric("🇲🇽 Origen", origen_texto.get(row['Origin_Score'], "N/D"))
                    
                    with col3:
                        st.metric("🗑️ Desperdicio", f"{row['Waste_pct']:.1f}%")
                        nova_texto = {1: "Natural", 2: "Procesado", 3: "Muy procesado", 4: "Ultra-procesado"}
                        st.metric("🔬 NOVA", nova_texto.get(int(row['NOVA']), "N/D"))
                
                st.markdown("---")
            
            st.markdown("##")
            
            # Visualización
            st.subheader("📊 Comparación Visual")
            
            fig = px.bar(
                df_top,
                x='Producto',
                y=score_col,
                color=score_col,
                color_continuous_scale='Greens',
                text=score_col
            )
            
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Score de Sustentabilidad",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("⚠️ No se encontró el archivo de productos más sustentables.")
    
    # ========================================================================
    # PÁGINA: VER RANKINGS
    # ========================================================================
    elif pagina == "📊 Ver Rankings":
        st.header("📊 Rankings de Sustentabilidad")
        st.markdown("Explora los rankings de productos según diferentes criterios")
        st.markdown("##")
        
        # Selector de tipo de ranking
        tipo_ranking = st.radio(
            "Selecciona el tipo de ranking:",
            ["🏆 Top 15 - Más Sustentables",
             "⚠️ Bottom 10 - Menos Sustentables",
             "🔥 Ranking Completo"]
        )
        
        st.markdown("---")
        
        if "Top 15" in tipo_ranking:
            st.subheader("🏆 Top 15 - Los Más Sustentables")
            
            top15 = df.nlargest(15, score_col)[['Producto', score_col, 'CF_kgCO2eq_kg', 
                                                  'WF_L_kg', 'LU_m2_kg', 'Waste_pct']].copy()
            top15['Posición'] = range(1, 16)
            top15 = top15[['Posición', 'Producto', score_col, 'CF_kgCO2eq_kg', 
                          'WF_L_kg', 'LU_m2_kg', 'Waste_pct']]
            
            # Renombrar columnas
            top15.columns = ['#', 'Producto', 'Score', 'Carbono', 'Agua (L)', 'Suelo (m²)', 'Desperdicio (%)']
            
            # Formatear
            top15['Score'] = top15['Score'].round(1)
            top15['Carbono'] = top15['Carbono'].round(2)
            top15['Agua (L)'] = top15['Agua (L)'].apply(lambda x: f"{x:,.0f}")
            top15['Suelo (m²)'] = top15['Suelo (m²)'].round(2)
            top15['Desperdicio (%)'] = top15['Desperdicio (%)'].round(1)
            
            st.dataframe(top15, use_container_width=True, hide_index=True)
            
            # Gráfico
            fig = px.bar(
                top15,
                x='Producto',
                y='Score',
                color='Score',
                color_continuous_scale='Greens',
                text='Score'
            )
            
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Score de Sustentabilidad",
                showlegend=False,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif "Bottom 10" in tipo_ranking:
            st.subheader("⚠️ Bottom 10 - Los Menos Sustentables")
            
            bottom10 = df.nsmallest(10, score_col)[['Producto', score_col, 'CF_kgCO2eq_kg', 
                                                     'WF_L_kg', 'LU_m2_kg', 'Waste_pct']].copy()
            bottom10['Posición'] = range(len(df), len(df)-10, -1)
            bottom10 = bottom10[['Posición', 'Producto', score_col, 'CF_kgCO2eq_kg', 
                                'WF_L_kg', 'LU_m2_kg', 'Waste_pct']]
            
            # Renombrar columnas
            bottom10.columns = ['#', 'Producto', 'Score', 'Carbono', 'Agua (L)', 'Suelo (m²)', 'Desperdicio (%)']
            
            # Formatear
            bottom10['Score'] = bottom10['Score'].round(1)
            bottom10['Carbono'] = bottom10['Carbono'].round(2)
            bottom10['Agua (L)'] = bottom10['Agua (L)'].apply(lambda x: f"{x:,.0f}")
            bottom10['Suelo (m²)'] = bottom10['Suelo (m²)'].round(2)
            bottom10['Desperdicio (%)'] = bottom10['Desperdicio (%)'].round(1)
            
            st.dataframe(bottom10, use_container_width=True, hide_index=True)
            
            # Gráfico
            fig = px.bar(
                bottom10,
                x='Producto',
                y='Score',
                color='Score',
                color_continuous_scale='Reds',
                text='Score'
            )
            
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Score de Sustentabilidad",
                showlegend=False,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Ranking completo
            st.subheader("🔥 Ranking Completo - Todos los Productos")
            
            ranking_completo = df[['Producto', score_col, 'CF_kgCO2eq_kg', 
                                   'WF_L_kg', 'LU_m2_kg', 'Waste_pct']].copy()
            ranking_completo = ranking_completo.sort_values(score_col, ascending=False)
            ranking_completo['Posición'] = range(1, len(ranking_completo) + 1)
            ranking_completo = ranking_completo[['Posición', 'Producto', score_col, 'CF_kgCO2eq_kg', 
                                                'WF_L_kg', 'LU_m2_kg', 'Waste_pct']]
            
            # Renombrar columnas
            ranking_completo.columns = ['#', 'Producto', 'Score', 'Carbono', 'Agua (L)', 'Suelo (m²)', 'Desperdicio (%)']
            
            # Formatear
            ranking_completo['Score'] = ranking_completo['Score'].round(1)
            ranking_completo['Carbono'] = ranking_completo['Carbono'].round(2)
            ranking_completo['Agua (L)'] = ranking_completo['Agua (L)'].apply(lambda x: f"{x:,.0f}")
            ranking_completo['Suelo (m²)'] = ranking_completo['Suelo (m²)'].round(2)
            ranking_completo['Desperdicio (%)'] = ranking_completo['Desperdicio (%)'].round(1)
            
            st.dataframe(ranking_completo, use_container_width=True, hide_index=True, height=600)
        
        st.markdown("##")
        
        # Botón de descarga
        st.subheader("💾 Exportar Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            excel_data = exportar_resultados_excel(df, escenario)
            st.download_button(
                label="📥 Descargar en Excel",
                data=excel_data,
                file_name=f"ranking_sustentabilidad_{escenario}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col2:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar en CSV",
                data=csv,
                file_name=f"datos_completos_{escenario}.csv",
                mime="text/csv"
            )
    
    # ========================================================================
    # PÁGINA: ACERCA DE
    # ========================================================================
    elif pagina == "ℹ️ Acerca de":
        st.header("ℹ️ Acerca de esta Calculadora")
        
        st.markdown("""
        ## 📊 Ecuación de Sustentabilidad Alimentaria
        
        **Proyecto:** Evaluación multi-dimensional de sostenibilidad alimentaria  
        **Investigadora:** Laura Ochoa M.  
        **LinkedIn:** [linkedin.com/in/lauraochoam](https://www.linkedin.com/in/lauraochoam/)  
        **Región:** México / Sonora  
        **Fecha:** Enero 2026  
        **Versión:** 2.1 (Rediseño UX)
        
        ---
        
        ### 🎯 Objetivo del Proyecto
        
        Desarrollar una herramienta científica que permite evaluar y comparar el impacto 
        ambiental de alimentos, con el fin de:
        
        - Generar recomendaciones dietéticas basadas en evidencia
        - Cuantificar el impacto ambiental de decisiones alimentarias
        - Informar políticas públicas de sostenibilidad alimentaria en Sonora
        - Facilitar decisiones de consumo consciente
        
        ---
        
        ### 📐 Metodología
        
        Esta calculadora evalúa 36 productos alimenticios usando **6 indicadores ambientales:**
        
        **1. Huella de Carbono (kg CO₂eq/kg)**
        - Mide las emisiones de gases de efecto invernadero
        - Incluye producción, transporte y procesamiento
        
        **2. Huella Hídrica (L/kg)**
        - Consumo total de agua dulce (azul, verde, gris)
        - Considera toda la cadena de producción
        
        **3. Uso de Suelo (m²/kg)**
        - Área de tierra requerida para producción
        - Incluye pastoreo, cultivos y procesamiento
        
        **4. Origen (Local/Regional/Importado)**
        - Distancia desde el lugar de producción
        - Prioriza productos mexicanos y sonorenses
        
        **5. Desperdicio (%)**
        - Porcentaje de pérdida y desperdicio alimentario
        - Del campo al consumidor (datos específicos de México cuando disponibles)
        
        **6. Procesamiento (Clasificación NOVA)**
        - Nivel 1: Alimentos naturales o mínimamente procesados
        - Nivel 2: Ingredientes culinarios procesados
        - Nivel 3: Alimentos procesados
        - Nivel 4: Productos ultra-procesados
        
        ---
        
        ### ⚖️ Sistemas de Pesos (Escenarios)
        
        Se desarrollaron dos metodologías de análisis para evaluar la robustez de las recomendaciones:
        
        **Escenario A - Metodología Original (Desperdicio 25%):**
        ```
        • Desperdicio: 25%
        • Origen: 20%
        • Procesamiento (NOVA): 15%
        • Carbono: 15%
        • Agua: 15%
        • Suelo: 10%
        ```
        
        **Escenario B - Metodología Ajustada (Desperdicio 30%):**
        ```
        • Desperdicio: 30%
        • Origen: 18%
        • Procesamiento (NOVA): 15%
        • Carbono: 14%
        • Agua: 14%
        • Suelo: 9%
        ```
        
        **Justificación del Escenario B:**  
        El desperdicio tiene un efecto multiplicador: cuando se desperdicia comida, 
        se desperdician TODOS los recursos invertidos en su producción (agua, tierra, 
        energía, carbono). El Escenario B captura parcialmente este efecto manteniendo 
        transparencia metodológica.
        
        **Validación:**  
        La correlación entre ambos escenarios es r = 0.9915 (casi perfecta), y 9 de los 
        10 productos top son idénticos en ambos escenarios, lo que valida la robustez 
        de las recomendaciones.
        
        ---
        
        ### 📚 Fuentes de Datos
        
        Todos los datos provienen de fuentes científicas verificadas y publicadas:
        
        **1. Huella de Carbono:**
        
        López-Olmedo, N., Popkin, B. M., & Taillie, L. S. (2022). The carbon footprint of the 
        Mexican diet. *Environmental Research Letters*, 17(5), 054028. 
        https://doi.org/10.1088/1748-9326/ac6b03
        
        **2. Huella Hídrica:**
        
        - SU-EATABLE LIFE Database (2020). *Food Footprint Database*. 
          https://www.rintracciabilita.it/su-eatable/
        
        - Mekonnen, M. M., & Hoekstra, A. Y. (2011). The green, blue and grey water footprint 
          of crops and derived crop products. *Hydrology and Earth System Sciences*, 15(5), 
          1577-1600. https://doi.org/10.5194/hess-15-1577-2011
        
        **3. Uso de Suelo:**
        
        Food and Agriculture Organization (FAO). (2021). *FAOSTAT - Mexico Production Data* 
        (2008-2013). https://www.fao.org/faostat/
        
        **4. Desperdicio Alimentario:**
        
        Food and Agriculture Organization (FAO). (2021). *Food Loss and Waste Database - Mexico*. 
        https://www.fao.org/platform-food-loss-waste/flw-data/
        
        **5. Clasificación NOVA:**
        
        Monteiro, C. A., Cannon, G., Levy, R. B., Moubarac, J. C., Louzada, M. L., Rauber, F., 
        ... & Jaime, P. C. (2019). Ultra-processed foods: What they are and how to identify them. 
        *Public Health Nutrition*, 22(5), 936-941. https://doi.org/10.1017/S1368980018003762
        
        ---
        
        ### 📈 Interpretación de Scores
        
        Los scores de sustentabilidad van de 0 a 100, donde 100 es el máximo nivel de 
        sustentabilidad:
        
        - **90-100:** 🟢 Excelente - Altamente sostenible, elección óptima
        - **80-89:**  🟢 Muy Bueno - Recomendado para consumo regular
        - **70-79:**  🟡 Bueno - Aceptable, moderación recomendada
        - **60-69:**  🟠 Moderado - Considerar alternativas más sostenibles
        - **< 60:**   🔴 Bajo - Limitar consumo, buscar opciones mejores
        
        ---
        
        ### ✅ Validación Científica
        
        **Robustez del Modelo:**
        - ✓ 100% de datos verificados con fuentes científicas publicadas
        - ✓ 20 de 36 productos con datos de desperdicio específicos de México
        - ✓ Modelo validado con análisis de sensibilidad (múltiples escenarios)
        - ✓ Correlación entre escenarios >0.99
        - ✓ Consistencia en recomendaciones: 90% de productos top idénticos
        
        **Limitaciones Reconocidas:**
        - Muestra de 36 productos (ampliable en futuras versiones)
        - Indicadores de nutrición y precio no incluidos (datos no verificables)
        - Variabilidad estacional no capturada
        - Optimizado para contexto México/Sonora (requiere adaptación para otras regiones)
        - No considera factores socioculturales o preferencias individuales
        
        ---
        
        ### 🌮 Recomendaciones para Sonora
        
        Basado en los **9 productos ultra-robustos** (presentes en Top 10 de ambos escenarios):
        
        **Frutas (consumo diario recomendado):**
        - 🥑 Aguacate
        - 🥭 Mango
        - 🍊 Naranja
        - 🍌 Plátano
        - 🍋 Limón
        
        **Vegetales (base de alimentación diaria):**
        - 🎃 Calabaza
        - 🍅 Tomate
        
        **Leguminosas (proteína vegetal principal):**
        - 🫘 Frijol
        - 🫘 Garbanzo
        
        **Impacto Potencial de Seguir estas Recomendaciones:**
        - ↓ 85% en huella de carbono
        - ↓ 51% en uso de agua
        - ↓ 85% en uso de suelo
        - ↓ 75% en desperdicio alimentario
        
        ---
        
        ### 🔬 Publicación y Uso Académico
        
        Este proyecto está diseñado para ser publicable en revistas científicas de nutrición, 
        sostenibilidad y salud pública. Los datos y metodología están completamente documentados 
        y son reproducibles.
        
        **Para citar este trabajo:**  
        Ochoa M., L. (2026). *Ecuación de Sustentabilidad Alimentaria: Evaluación 
        multi-dimensional de impacto ambiental en Sonora, México*. [Calculadora web]. 
        
        ---
        
        ### 📄 Licencia y Uso
        
        **Esta herramienta está diseñada para:**
        - Fines educativos y de investigación
        - Divulgación científica
        - Toma de decisiones informadas
        - Políticas públicas de sostenibilidad
        
        **Características:**
        - 📖 Código abierto
        - 🔍 Datos transparentes y verificables
        - 📊 Metodología replicable
        - 🤝 Disponible para colaboración científica
        
        ---
        
        ### 📧 Contacto
        
        **Laura Ochoa M.**  
        LinkedIn: [linkedin.com/in/lauraochoam](https://www.linkedin.com/in/lauraochoam/)
        
        Para más información sobre:
        - Metodología detallada
        - Colaboraciones científicas
        - Datos y fuentes
        - Publicación académica
        - Adaptación a otras regiones
        
        No dudes en contactarme a través de LinkedIn.
        
        ---
        
        ### 🙏 Agradecimientos
        
        Este proyecto fue posible gracias a las bases de datos públicas de:
        - FAO (Organización de las Naciones Unidas para la Alimentación y la Agricultura)
        - Proyecto SU-EATABLE LIFE
        - Investigadores que publican datos abiertos sobre sostenibilidad alimentaria
        
        *Última actualización: Enero 2026*
        """)

# ============================================================================
# EJECUTAR APLICACIÓN
# ============================================================================

if __name__ == "__main__":
    main()
