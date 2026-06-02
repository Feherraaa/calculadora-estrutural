import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(page_title="Plataforma Avançada de Engenharia Estrutural", layout="wide")

# ==========================================
# FUNÇÕES DE ENGENHARIA E OTIMIZAÇÃO
# ==========================================
def otimizar_bitola(As_req, bw, min_barras=2):
    """Busca a combinação de barras comerciais com menor desperdício de aço"""
    bitolas = [8.0, 10.0, 12.5, 16.0, 20.0, 25.0]
    melhor_opcao = None
    menor_excesso = float('inf')
    
    for phi in bitolas:
        area_barra = (math.pi * (phi/10)**2) / 4
        num_barras = max(min_barras, math.ceil(As_req / area_barra))
        area_total = num_barras * area_barra
        
        if area_total >= As_req and (area_total - As_req) < menor_excesso:
            menor_excesso = area_total - As_req
            melhor_opcao = (num_barras, phi, area_total)
            
    return melhor_opcao

# ==========================================
# FUNÇÕES GRÁFICAS DE COMPORTAMENTO MECÂNICO
# ==========================================
def plot_viga_esforcos(L, q):
    x = np.linspace(0, L, 200)
    V = q * (L / 2 - x)
    M = (q * x / 2) * (L - x)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 4))
    ax1.plot(x, V, color='teal', lw=2)
    ax1.fill_between(x, V, color='teal', alpha=0.1)
    ax1.axhline(0, color='black', lw=0.8)
    ax1.set_title("Diagrama de Força Cortante - DEC (kN)", fontsize=9)
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    ax2.plot(x, M, color='crimson', lw=2)
    ax2.fill_between(x, M, color='crimson', alpha=0.1)
    ax2.axhline(0, color='black', lw=0.8)
    ax2.set_title("Diagrama de Momento Fletor - DMF (kN.m)", fontsize=9)
    ax2.invert_yaxis()
    ax2.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    return fig

def plot_viga_dominios(bw, h, d, x_ln, As_sup_req):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5), gridspec_kw={'width_ratios': [1, 1.5]})
    
    ax1.add_patch(patches.Rectangle((0, 0), bw, h, fill=False, lw=2, color='black'))
    ax1.axhline(h - x_ln, color='red', linestyle='--', label='L.N.')
    ax1.add_patch(patches.Rectangle((0, h - 0.8*x_ln), bw, 0.8*x_ln, color='red', alpha=0.2))
    ax1.scatter([bw*0.25, bw*0.5, bw*0.75], [h - d, h - d, h - d], color='blue', s=80, label='As (Tração)')
    
    if As_sup_req > 0:
        ax1.scatter([bw*0.25, bw*0.75], [h - (h-d), h - (h-d)], color='orange', s=80, label="As' (Compressão)")
    
    ax1.set_xlim(-5, bw+5)
    ax1.set_ylim(-5, h+5)
    ax1.axis('off')
    ax1.legend(loc='lower center', fontsize=7)
    
    ax2.plot([0, 0], [0, h], color='black', lw=1.5)
    ax2.axhline(h - x_ln, color='red', linestyle='--')
    x_d = x_ln / d
    eps_s = 10.0 if x_d <= 0.259 else (3.5 * (d - x_ln)) / x_ln
    eps_c = (x_ln * 10.0) / (d - x_ln) if x_d <= 0.259 else 3.5
    
    ax2.plot([-eps_c, eps_s], [h, h - d], color='purple', lw=2, marker='o')
    ax2.set_title("Deformações da Seção", fontsize=9)
    ax2.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig

def plot_viga_elevacao(L, h, tem_armadura_dupla):
    L_cm = L * 100
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.add_patch(patches.Rectangle((0, 0), L_cm, h, fill=False, lw=2, color='gray'))
    c = 3.0
    ax.plot([c, L_cm-c], [c, c], color='blue', lw=3.5, label='Inferior (Tração)')
    if tem_armadura_dupla:
        ax.plot([c, L_cm-c], [h-c, h-c], color='orange', lw=3.5, label='Superior (Estrutural)')
    else:
        ax.plot([c, L_cm-c], [h-c, h-c], color='blue', lw=1.5, linestyle='--', label='Superior (Porta-Estribo)')
    
    for x in np.arange(c, L_cm-c, max(15.0, L_cm / 30)):
        ax.plot([x, x], [c, h-c], color='darkred', lw=1.2)
    ax.set_xlim(-10, L_cm + 10)
    ax.set_ylim(-10, h + 10)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=3, fontsize=8)
    return fig

def plot_pilar_detalhe(formato, b, h, num_barras):
    fig, ax = plt.subplots(figsize=(4, 4))
    if formato == "Retangular":
        ax.add_patch(patches.Rectangle((0, 0), b, h, fill=False, lw=3, color='grey'))
        ax.add_patch(patches.Rectangle((2.5, 2.5), b-5, h-5, fill=False, lw=1.5, color='darkred'))
        
        # Geração dinâmica de coordenadas de barras
        if num_barras == 4:
            xs = [3.5, b-3.5, 3.5, b-3.5]
            ys = [3.5, 3.5, h-3.5, h-3.5]
        else:
            xs = [3.5, b-3.5, 3.5, b-3.5, 3.5, b-3.5]
            ys = [3.5, 3.5, h-3.5, h-3.5, h/2, h/2] if h >= b else [3.5, 3.5, h-3.5, h-3.5, b/2, b/2]
        ax.scatter(xs, ys, color='black', s=120, zorder=3)
        ax.set_xlim(-5, b+5); ax.set_ylim(-5, h+5)
    else:
        raio = b / 2
        ax.add_patch(patches.Circle((raio, raio), raio, fill=False, lw=3, color='grey'))
        ax.add_patch(patches.Circle((raio, raio), raio - 2.5, fill=False, lw=1.5, color='darkred'))
        angulos = np.linspace(0, 2*np.pi, num_barras, endpoint=False)
        r_barra = raio - 3.5
        xs = raio + r_barra * np.cos(angulos)
        ys = raio + r_barra * np.sin(angulos)
        ax.scatter(xs, ys, color='black', s=120, zorder=3)
        ax.set_xlim(-5, b+5); ax.set_ylim(-5, b+5)
        
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

def plot_secao_T(bf, bw, h, hf, d, x_ln):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.add_patch(patches.Rectangle((-bw/2, 0), bw, h - hf, fill=False, lw=2, color='black'))
    ax.add_patch(patches.Rectangle((-bf/2, h - hf), bf, hf, fill=False, lw=2, color='black'))
    ax.axhline(h - x_ln, color='red', linestyle='--')
    y_comp = 0.8 * x_ln
    if y_comp <= hf:
        ax.add_patch(patches.Rectangle((-bf/2, h - y_comp), bf, y_comp, color='red', alpha=0.3))
    else:
        ax.add_patch(patches.Rectangle((-bf/2, h - hf), bf, hf, color='red', alpha=0.3))
        ax.add_patch(patches.Rectangle((-bw/2, h - y_comp), bw, y_comp - hf, color='red', alpha=0.3))
    ax.scatter([-bw/4, bw/4], [h - d, h - d], color='blue', s=80)
    ax.set_xlim(-bf/2 - 5, bf/2 + 5); ax.set_ylim(-5, h + 5)
    ax.set_aspect('equal'); ax.axis('off')
    return fig

def plot_laje_ruptura(lx, ly):
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.add_patch(patches.Rectangle((0, 0), lx, ly, fill=False, lw=2, color='black'))
    if lx <= ly:
        x1, y1 = lx/2, lx/2; x2, y2 = lx/2, ly - lx/2
    else:
        x1, y1 = ly/2, ly/2; x2, y2 = lx - ly/2, ly/2
    ax.plot([0, x1], [0, y1], color='orange', lw=2, linestyle='--')
    ax.plot([lx, x1], [0, y1], color='orange', lw=2, linestyle='--')
    ax.plot([0, x2], [ly, y2], color='orange', lw=2, linestyle='--')
    ax.plot([lx, x2], [ly, y2], color='orange', lw=2, linestyle='--')
    ax.plot([x1, x2], [y1, y2], color='orange', lw=2, linestyle='--')
    ax.set_xlim(-0.5, lx+0.5); ax.set_ylim(-0.5, ly+0.5)
    ax.axis('off')
    return fig

# ==========================================
# MÓDULOS DE INTERFACE E CÁLCULO
# ==========================================
def modulo_cargas():
    st.header("Módulo 0: Estimativa e Descida de Cargas (NBR 6120)")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        area_planta = st.number_input("Área da Planta por Pavimento (m²)", min_value=10.0, value=100.0)
        uso = st.selectbox("Tipo de Uso (Carga Acidental)", ["Residencial", "Comercial / Escritórios", "Garagem"])
        num_pilares = st.number_input("Quantidade estimada de Pilares", min_value=4, value=8)
        pavimentos_tipo = st.radio("Tipologia da Edificação:", ["Térrea (1 Laje)", "Sobrado / Prédio (Múltiplos Andares)"])
        andares = st.number_input("Número de Lajes Total", min_value=2, value=2) if "Sobrado" in pavimentos_tipo else 1

    with col2:
        if st.button("Gerar Descida de Cargas"):
            carga_acidental = 1.5 if uso == "Residencial" else (2.5 if "Comercial" in uso else 3.0)
            carga_total_m2 = 5.5 + carga_acidental
            total_edificacao = area_planta * carga_total_m2 * andares
            carga_pilar_media = (total_edificacao / num_pilares) * 1.15
            
            st.metric("Peso Total Estimado da Obra", f"{total_edificacao:.1f} kN")
            st.markdown("### 🎯 Força de Cálculo para os Pilares")
            st.success(rf"Carga Axial de Serviço Recomendada ($N_k$): **{carga_pilar_media:.2f} kN**")

def modulo_vigas():
    st.header("Módulo 1: Vigas - Flexão Inteligente e Detalhamento")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("Vão da Viga L (m)", min_value=1.0, value=5.0)
        q_reg = st.number_input("Carga Total Distribuída q (kN/m)", min_value=1.0, value=20.0)
        bw = st.number_input("Largura bw (cm)", min_value=10.0, value=15.0)
        h = st.number_input("Altura h (cm)", min_value=20.0, value=45.0)
        fck = st.number_input("fck do Concreto (MPa)", min_value=20.0, value=25.0)

    with col2:
        if st.button("Calcular Estrutura da Viga"):
            q_d = q_reg * 1.4
            M_sd = (q_d * (L**2)) / 8
            V_sd = (q_d * L) / 2
            d = h - 4.0
            fcd = (fck / 1.4) / 10
            fyd = (500 / 1.15) / 10
            M_sd_cm = M_sd * 100
            
            x_lim = 0.45 * d
            M_lim = 0.68 * bw * x_lim * fcd * (d - 0.4 * x_lim)
            tem_dupla = M_sd_cm > M_lim
            
            if not tem_dupla:
                a_eq = 0.272 * bw * fcd
                b_eq = -0.68 * bw * fcd * d
                delta = b_eq**2 - 4 * a_eq * M_sd_cm
                x_ln = (-b_eq - math.sqrt(delta)) / (2 * a_eq)
                As_inf = max(M_sd_cm / (fyd * (d - 0.4 * x_ln)), (0.15/100)*bw*h)
                As_sup = 0
            else:
                x_ln = x_lim
                As_inf = (M_lim / (fyd * (d - 0.4 * x_lim))) + ((M_sd_cm - M_lim) / (fyd * (d - 4.0)))
                As_sup = (M_sd_cm - M_lim) / (fyd * (d - 4.0))
            
            num_inf, phi_inf, a_inf = otimizar_bitola(As_inf, bw)
            st.success(rf"Aço Inferior (Tração): **{num_inf} barras de $\phi$ {phi_inf} mm**")
            if tem_dupla:
                num_sup, phi_sup, a_sup = otimizar_bitola(As_sup, bw, min_barras=2)
                st.warning(rf"🚨 Armadura Dupla Requerida! Aço Superior: **{num_sup} barras de $\phi$ {phi_sup} mm**")
                
            # Cortante Mínimo NBR 6118
            fctm = 0.3 * (fck**(2/3))
            Asw_min = ((0.2 * fctm / 500) * bw * 100)
            st.info(rf"Estribos Mínimos de Segurança: **{Asw_min:.2f} cm²/m**")
            
            st.pyplot(plot_viga_esforcos(L, q_d))
            st.pyplot(plot_viga_dominios(bw, h, d, x_ln, As_sup))
            st.pyplot(plot_viga_elevacao(L, h, tem_dupla))

def modulo_pilares():
    st.header("Módulo 2: Pilares - Variantes Geométricas e Locais (NBR 6118)")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Configurações Avançadas de Esforço")
        formato = st.selectbox("Formato da Seção do Pilar", ["Retangular", "Circular"])
        posicao = st.selectbox("Posição do Pilar na Planta", ["Central (Sem excentricidade de viga)", "Extremidade (Excentricidade em 1 eixo)", "Canto (Excentricidade em 2 eixos)"])
        
        if formato == "Retangular":
            b = st.number_input("Largura do Pilar b (cm) - Mínimo 14cm", min_value=14.0, value=15.0)
            h_p = st.number_input("Comprimento do Pilar h (cm)", min_value=14.0, value=30.0)
        else:
            b = st.number_input("Diâmetro do Pilar D (cm) - Mínimo 19cm", min_value=19.0, value=25.0)
            h_p = b
            
        N_k = st.number_input("Força Axial de Serviço Nk (kN)", min_value=10.0, value=500.0)
        num_barras = st.selectbox("Quantidade de Barras Solicitadas", [4, 6, 8] if formato == "Retangular" else [6, 8, 10])

    with col2:
        st.subheader("Resultados Regulamentares da Norma")
        if st.button("Verificar Pilar"):
            N_sd_base = N_k * 1.4
            
            # Variante Coeficiente Gama_n para seções retangulares esbeltas/estreitas (< 19 cm)
            gamma_n = 1.0
            if formato == "Retangular" and b < 19.0:
                gamma_n = 1.95 - 0.05 * b
                st.warning(rf"⚠️ Penalização Normativa aplicada: Menor dimensão < 19cm. Coeficiente $\gamma_n$ = {gamma_n:.2f}")
            
            # Variante Posição do Pilar (Excentricidades Teóricas Estimadas por Majoradores Simplificados)
            coef_posicao = 1.0 if "Central" in posicao else (1.2 if "Extremidade" in posicao else 1.4)
            N_sd = N_sd_base * gamma_n * coef_posicao
            
            Ac = (b * h_p) if formato == "Retangular" else (math.pi * b**2) / 4
            fyd = (500 / 1.15) / 10
            
            # Limites mínimos e máximos da NBR 6118
            As_min = max(0.15 * (N_sd / fyd), 0.004 * Ac)
            As_max = 0.08 * Ac
            
            st.write(rf"- Força de Projeto Majorada Final ($N_{{sd}}$): **{N_sd:.2f} kN**")
            st.write(rf"- Área Mínima de Aço Necessária ($A_{{s,min}}$): **{As_min:.2f} cm²**")
            st.write(rf"- Área Máxima de Aço Admissível ($A_{{s,max}}$): **{As_max:.2f} cm²**")
            
            num_b, phi_b, a_real = otimizar_bitola(As_min, b, min_barras=num_barras)
            st.markdown("### 📊 Escolha Ótima Conforme Variantes")
            
            if a_real > As_max:
                st.error("🚨 Seção de Concreto Subdimensionada! O aço estrapolou os 8% de taxa máxima. Aumente as dimensões do pilar.")
            else:
                st.success(rf"✅ Adotar: **{num_b} barras de $\phi$ {phi_b} mm** (Área real: {a_real:.2f} cm²)")
                
                # Detalhe Transversal contra Flambagem (Estudo TCC)
                phi_t = max(5.0, phi_b / 4)
                s_max = min(20.0, b, 12 * (phi_b / 10))
                st.info(rf"Estribos de Travamento: $\phi$ {phi_t:.1f} mm espaçados a cada **{math.floor(s_max)} cm**")
                st.pyplot(plot_pilar_detalhe(formato, b, h_p, num_b))

def modulo_lajes():
    st.header("Módulo 3: Lajes Maciças")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        lx = st.number_input("Vão lx (m)", min_value=1.0, value=4.0)
        ly = st.number_input("Vão ly (m)", min_value=1.0, value=5.0)
        q = st.number_input("Carga Total de Cálculo (kN/m²)", min_value=1.0, value=7.0)
        h_l = st.number_input("Espessura h (cm)", min_value=7.0, value=10.0)

    with col2:
        if st.button("Calcular Laje"):
            lam = ly / lx
            M_x = (q * (lx**2)) / 8 if lam > 2.0 else (((ly**4)/(lx**4 + ly**4)) * q * (lx**2)) / 8
            As = max((M_x * 1.4 * 100) / ((500/1.15)/10 * (h_l - 2.5) * 0.9), (0.15/100)*100*h_l)
            st.success(rf"Armadura de Tração Principal: **{As:.2f} cm²/m**")
            st.pyplot(plot_laje_ruptura(lx, ly))

def modulo_laje_trelicada():
    st.header("Módulo 4: Lajes Treliçadas / Nervuradas (Seção T)")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("Vão da Laje L (m) ", min_value=1.0, value=4.5)
        q_l = st.number_input("Carga Total (kN/m²) ", min_value=1.0, value=5.0)
        bf = st.number_input("Intereixo bf (cm) ", value=40.0)
        bw = st.number_input("Largura Sapata bw (cm) ", value=12.0)
        h = st.number_input("Altura total h (cm) ", value=16.0)
        hf = st.number_input("Capa hf (cm) ", value=4.0)
        fck = st.number_input("fck do Concreto (MPa)  ", value=25.0)

    with col2:
        if st.button("Calcular Nervura T"):
            q_lineal = q_l * (bf / 100) * 1.4
            M_sd = (q_lineal * (L**2)) / 8
            d = h - 2.5
            fcd = (fck/1.4)/10; fyd = (500/1.15)/10
            
            a_eq = 0.272 * bf * fcd
            b_eq = -0.68 * bf * fcd * d
            delta = b_eq**2 - 4 * a_eq * (M_sd * 100)
            
            if delta < 0: st.error("Seção insuficiente.")
            else:
                x = (-b_eq - math.sqrt(delta)) / (2 * a_eq)
                As = (M_sd * 100) / (fyd * (d - 0.4 * x))
                st.success(rf"Armadura por Vigota Requerida: **{As:.2f} cm²**")
                st.pyplot(plot_secao_T(bf, bw, h, hf, d, x))

# ==========================================
# MENU LATERAL E NAVEGAÇÃO
# ==========================================
st.sidebar.title("Navegação do Edifício")
modulo = st.sidebar.radio("Selecione o Componente:", [
    "0. Cargas (NBR 6120)", 
    "1. Vigas (Flexão/Cortante)", 
    "2. Pilares (Variantes)", 
    "3. Lajes Maciças", 
    "4. Lajes Treliçadas"
])

if "0." in modulo: modulo_cargas()
elif "1." in modulo: modulo_vigas()
elif "2." in modulo: modulo_pilares()
elif "3." in modulo: modulo_lajes()
else: modulo_laje_trelicada()