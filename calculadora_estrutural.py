import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import os

# ==========================================
# CONFIGURAÇÃO DE PÁGINA E ESTÉTICA (HFF)
# ==========================================
st.set_page_config(page_title="HFF - Arquitetura e Urbanismo", layout="wide")

st.markdown("""
<style>
    /* Estética Minimalista HFF (Tons de Grafite e Cinza) */
    [data-testid="stSidebar"] {
        background-color: #111111;
    }
    [data-testid="stSidebar"] * {
        color: #E5E5E5 !important;
    }
    .stButton>button {
        background-color: #111111;
        color: #FFFFFF;
        border: 1px solid #555555;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #333333;
        border: 1px solid #FFFFFF;
    }
    h1, h2, h3 { color: #111111; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# FUNÇÕES DE ENGENHARIA E OTIMIZAÇÃO
# ==========================================
def otimizar_bitola(As_req, bw, min_barras=2):
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

def calc_Mcr(L, E, G, Iy, J, Cw, Cb=1.0):
    if L <= 0: return float('inf')
    term1 = (math.pi**2 * E * Iy) / (L**2)
    term2 = (Cw / Iy) + (L**2 * G * J) / (math.pi**2 * E * Iy)
    return Cb * term1 * math.sqrt(term2)

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
    ax1.set_xlim(-5, bw+5); ax1.set_ylim(-5, h+5); ax1.axis('off'); ax1.legend(loc='lower center', fontsize=7)
    
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
    if tem_armadura_dupla: ax.plot([c, L_cm-c], [h-c, h-c], color='orange', lw=3.5, label='Superior (Estrutural)')
    else: ax.plot([c, L_cm-c], [h-c, h-c], color='blue', lw=1.5, linestyle='--', label='Superior (Porta-Estribo)')
    for x in np.arange(c, L_cm-c, max(15.0, L_cm / 30)): ax.plot([x, x], [c, h-c], color='darkred', lw=1.2)
    ax.set_xlim(-10, L_cm + 10); ax.set_ylim(-10, h + 10); ax.set_aspect('equal'); ax.axis('off')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=3, fontsize=8)
    return fig

def plot_pilar_detalhe(formato, b, h, num_barras):
    fig, ax = plt.subplots(figsize=(4, 4))
    if formato == "Retangular":
        ax.add_patch(patches.Rectangle((0, 0), b, h, fill=False, lw=3, color='grey'))
        ax.add_patch(patches.Rectangle((2.5, 2.5), b-5, h-5, fill=False, lw=1.5, color='darkred'))
        if num_barras == 4: xs, ys = [3.5, b-3.5, 3.5, b-3.5], [3.5, 3.5, h-3.5, h-3.5]
        else:
            xs = [3.5, b-3.5, 3.5, b-3.5, 3.5, b-3.5]
            ys = [3.5, 3.5, h-3.5, h-3.5, h/2, h/2] if h >= b else [3.5, 3.5, h-3.5, h-3.5, b/2, b/2]
        ax.scatter(xs, ys, color='black', s=120, zorder=3)
        ax.set_xlim(-5, b+5); ax.set_ylim(-5, h+5)
    else:
        raio = b / 2
        ax.add_patch(patches.Circle((raio, raio), raio, fill=False, lw=3, color='grey'))
        ax.add_patch(patches.Circle((raio, raio), raio - 2.5, fill=False, lw=1.5, color='darkred'))
        angulos = np.linspace(0, 2*math.pi, num_barras, endpoint=False)
        xs = raio + (raio - 3.5) * np.cos(angulos)
        ys = raio + (raio - 3.5) * np.sin(angulos)
        ax.scatter(xs, ys, color='black', s=120, zorder=3)
        ax.set_xlim(-5, b+5); ax.set_ylim(-5, b+5)
    ax.set_aspect('equal'); ax.axis('off')
    return fig

def plot_secao_T(bf, bw, h, hf, d, x_ln):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.add_patch(patches.Rectangle((-bw/2, 0), bw, h - hf, fill=False, lw=2, color='black'))
    ax.add_patch(patches.Rectangle((-bf/2, h - hf), bf, hf, fill=False, lw=2, color='black'))
    ax.axhline(h - x_ln, color='red', linestyle='--')
    y_comp = 0.8 * x_ln
    if y_comp <= hf: ax.add_patch(patches.Rectangle((-bf/2, h - y_comp), bf, y_comp, color='red', alpha=0.3))
    else:
        ax.add_patch(patches.Rectangle((-bf/2, h - hf), bf, hf, color='red', alpha=0.3))
        ax.add_patch(patches.Rectangle((-bw/2, h - y_comp), bw, y_comp - hf, color='red', alpha=0.3))
    ax.scatter([-bw/4, bw/4], [h - d, h - d], color='blue', s=80)
    ax.set_xlim(-bf/2 - 5, bf/2 + 5); ax.set_ylim(-5, h + 5); ax.set_aspect('equal'); ax.axis('off')
    return fig

def plot_secao_mista(d, bf, tw, tf, tc, beff, pna_y):
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.add_patch(patches.Rectangle((-tw/2, 0), tw, d, fill=True, color='slategray', label='Perfil de Aço')) 
    ax.add_patch(patches.Rectangle((-bf/2, 0), bf, tf, fill=True, color='slategray')) 
    ax.add_patch(patches.Rectangle((-bf/2, d-tf), bf, tf, fill=True, color='slategray')) 
    ax.add_patch(patches.Rectangle((-beff/2, d), beff, tc, fill=True, color='lightgray', hatch='//', label='Laje'))
    ax.axhline(pna_y, color='red', linestyle='--', lw=2.5, label=rf'L.N. Plástica (y={pna_y:.1f} cm)')
    if pna_y > d: 
        ax.add_patch(patches.Rectangle((-beff/2, pna_y), beff, (d+tc)-pna_y, color='red', alpha=0.2, label='Zona Comprimida'))
    else: 
        ax.add_patch(patches.Rectangle((-beff/2, d), beff, tc, color='red', alpha=0.2, label='Zona Comprimida'))
        ax.add_patch(patches.Rectangle((-bf/2, pna_y), bf, d-pna_y, color='red', alpha=0.2))
    ax.set_xlim(-beff/2 - 5, beff/2 + 5); ax.set_ylim(-5, d + tc + 5)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title("Seção Transversal - Viga Mista", fontsize=10)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=8)
    return fig

def plot_laje_ruptura(lx, ly):
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.add_patch(patches.Rectangle((0, 0), lx, ly, fill=False, lw=2, color='black'))
    if lx <= ly: x1, y1, x2, y2 = lx/2, lx/2, lx/2, ly - lx/2
    else: x1, y1, x2, y2 = ly/2, ly/2, lx - ly/2, ly/2
    ax.plot([0, x1], [0, y1], color='orange', lw=2, linestyle='--')
    ax.plot([lx, x1], [0, y1], color='orange', lw=2, linestyle='--')
    ax.plot([0, x2], [ly, y2], color='orange', lw=2, linestyle='--')
    ax.plot([lx, x2], [ly, y2], color='orange', lw=2, linestyle='--')
    ax.plot([x1, x2], [y1, y2], color='orange', lw=2, linestyle='--')
    ax.set_xlim(-0.5, lx+0.5); ax.set_ylim(-0.5, ly+0.5); ax.axis('off')
    return fig

def plot_curva_flt(Lp, Lr, Mpl, Mr, Lb_user, MRd_user, E, G, Iy, J, Cw):
    L_max = max(Lr * 1.3, Lb_user * 1.2)
    L_vals = np.linspace(0.1, L_max, 200)
    M_vals = []
    for L in L_vals:
        if L <= Lp: M = Mpl
        elif L <= Lr: M = Mpl - (Mpl - Mr) * ((L - Lp) / (Lr - Lp))
        else: M = calc_Mcr(L, E, G, Iy, J, Cw, 1.0)
        M_vals.append((min(M, Mpl)) / 1.10 / 100)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(L_vals/100, M_vals, color='darkred', lw=2, label='Curva Resistente NBR 8800')
    ax.axvline(Lp/100, color='gray', linestyle='--', lw=1, label=rf'$L_p$ ({Lp/100:.2f}m)')
    ax.axvline(Lr/100, color='gray', linestyle=':', lw=1, label=rf'$L_r$ ({Lr/100:.2f}m)')
    ax.scatter([Lb_user/100], [MRd_user/100], color='blue', s=100, zorder=5, label='Sua Viga')
    ax.plot([0, Lb_user/100], [MRd_user/100, MRd_user/100], color='blue', linestyle='-.', lw=1)
    ax.plot([Lb_user/100, Lb_user/100], [0, MRd_user/100], color='blue', linestyle='-.', lw=1)
    ax.set_title("Análise de Flambagem Lateral com Torção (FLT)", fontsize=10)
    ax.set_xlabel("Comprimento Destravado Lb (m)")
    ax.set_ylabel("Momento de Projeto MRd (kN.m)")
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    return fig

# ==========================================
# MÓDULOS 0 A 5: ENGENHARIA E CÁLCULOS
# ==========================================
def modulo_cargas():
    st.header("Módulo 0: Estimativa e Descida de Cargas (NBR 6120)")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        area_planta = st.number_input("Área da Planta por Pavimento (m²)", min_value=10.0, value=100.0)
        uso = st.selectbox("Tipo de Uso", ["Residencial", "Comercial / Escritórios", "Garagem"])
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
            st.success(rf"Carga Axial de Serviço Recomendada ($N_k$): **{carga_pilar_media:.2f} kN**")

def modulo_vigas():
    st.header("Módulo 1: Vigas CA - Flexão Inteligente e Detalhamento")
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
            st.success(rf"Aço Inferior (Tração): **{num_inf} varões de $\phi$ {phi_inf} mm**")
            if tem_dupla:
                num_sup, phi_sup, a_sup = otimizar_bitola(As_sup, bw, min_barras=2)
                st.warning(rf"🚨 Armadura Dupla Requerida! Aço Superior: **{num_sup} varões de $\phi$ {phi_sup} mm**")
            
            st.pyplot(plot_viga_esforcos(L, q_d))
            st.pyplot(plot_viga_dominios(bw, h, d, x_ln, As_sup))
            st.pyplot(plot_viga_elevacao(L, h, tem_dupla))

def modulo_pilares():
    st.header("Módulo 2: Pilares CA - Variantes Geométricas")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        formato = st.selectbox("Formato da Seção", ["Retangular", "Circular"])
        b = st.number_input("Dimensão/Diâmetro (cm)", min_value=14.0, value=20.0)
        h_p = st.number_input("Comprimento (cm)", min_value=14.0, value=30.0) if formato == "Retangular" else b
        N_k = st.number_input("Força Normal Nk (kN)", min_value=10.0, value=500.0)
        num_barras = st.selectbox("Quantidade de Barras", [4, 6, 8] if formato == "Retangular" else [6, 8, 10])

    with col2:
        if st.button("Verificar Pilar"):
            N_sd = N_k * 1.4
            Ac = (b * h_p) if formato == "Retangular" else (math.pi * b**2) / 4
            fyd = (500 / 1.15) / 10
            As_min = max(0.15 * (N_sd / fyd), 0.004 * Ac)
            As_max = 0.08 * Ac
            
            num_b, phi_b, a_real = otimizar_bitola(As_min, b, min_barras=num_barras)
            if a_real > As_max: st.error("🚨 Seção Subdimensionada! O aço extrapolou os 8% permitidos.")
            else: st.success(rf"✅ Adotar: **{num_b} varões de $\phi$ {phi_b} mm** (Área: {a_real:.2f} cm²)")
            st.pyplot(plot_pilar_detalhe(formato, b, h_p, num_b))

def modulo_lajes():
    st.header("Módulo 3: Lajes Maciças")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        lx = st.number_input("Vão lx (m)", min_value=1.0, value=4.0)
        ly = st.number_input("Vão ly (m)", min_value=1.0, value=5.0)
        q = st.number_input("Carga Total (kN/m²)", min_value=1.0, value=7.0)
        h_l = st.number_input("Espessura h (cm)", min_value=7.0, value=10.0)

    with col2:
        if st.button("Calcular Laje"):
            lam = ly / lx
            M_x = (q * (lx**2)) / 8 if lam > 2.0 else (((ly**4)/(lx**4 + ly**4)) * q * (lx**2)) / 8
            As = max((M_x * 1.4 * 100) / ((500/1.15)/10 * (h_l - 2.5) * 0.9), (0.15/100)*100*h_l)
            st.success(rf"Armadura de Tração: **{As:.2f} cm²/m**")
            st.pyplot(plot_laje_ruptura(lx, ly))

def modulo_laje_trelicada():
    st.header("Módulo 4: Lajes Treliçadas / Nervuradas (Seção T)")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("Vão L (m) ", min_value=1.0, value=4.5)
        q_l = st.number_input("Carga (kN/m²) ", min_value=1.0, value=5.0)
        bf = st.number_input("Intereixo bf (cm) ", value=40.0)
        bw = st.number_input("Sapata bw (cm) ", value=12.0)
        h = st.number_input("Altura total h (cm) ", value=16.0)
        hf = st.number_input("Capa hf (cm) ", value=4.0)

    with col2:
        if st.button("Calcular Nervura T"):
            M_sd = (q_l * (bf/100) * 1.4 * (L**2)) / 8
            d = h - 2.5
            a_eq = 0.272 * bf * (25/1.4/10)
            b_eq = -0.68 * bf * (25/1.4/10) * d
            delta = b_eq**2 - 4 * a_eq * (M_sd * 100)
            if delta < 0: st.error("Seção insuficiente.")
            else:
                x = (-b_eq - math.sqrt(delta)) / (2 * a_eq)
                As = (M_sd * 100) / ((500/1.15)/10 * (d - 0.4 * x))
                st.success(rf"Armadura por Vigota Requerida: **{As:.2f} cm²**")
                st.pyplot(plot_secao_T(bf, bw, h, hf, d, x))

def modulo_metalicas_mistas():
    st.header("Módulo 5: Estruturas Metálicas e Vigas Mistas (FLT)")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        tipo_perfil = st.selectbox("Tipo de Perfil", ["Perfil I Laminado/Soldado", "Perfil U Laminado"])
        d_aco = st.number_input("Altura d (cm)", min_value=5.0, value=25.0)
        bf_aco = st.number_input("Largura Mesa bf (cm)", min_value=5.0, value=12.5)
        tw_aco = st.number_input("Espessura Alma tw (mm)", min_value=2.0, value=6.3) / 10 
        tf_aco = st.number_input("Espessura Mesa tf (mm)", min_value=2.0, value=9.5) / 10 
        aco_fy = st.selectbox("Tensão Escoamento", ["ASTM A36 (250 MPa)", "ASTM A572 (345 MPa)"])
        fy = 25.0 if "250" in aco_fy else 34.5
        viga_mista = st.checkbox("Considerar Laje de Concreto (Viga Mista)?")
        
        if viga_mista:
            tc_concreto = st.number_input("Espessura Laje tc (cm)", min_value=5.0, value=10.0)
            beff_concreto = st.number_input("Largura Efetiva beff (cm)", min_value=30.0, value=150.0)
            fck_misto = st.number_input("fck Laje (MPa)", min_value=20.0, value=25.0)
        else:
            contida = st.radio("Contenção Lateral (FLT):", ["100% Contida", "Destravada"])
            Lb = st.number_input("Lb (m)", min_value=0.1, value=3.0) * 100 if "Destravada" in contida else 0.0

    with col2:
        if st.button("Calcular Resistência do Aço"):
            Area = 2 * (bf_aco * tf_aco) + (d_aco - 2*tf_aco) * tw_aco
            h0 = d_aco - tf_aco 
            Iy = 2 * (tf_aco * bf_aco**3)/12 + ((d_aco - 2*tf_aco) * tw_aco**3)/12
            Ix = (bf_aco * d_aco**3)/12 - ((bf_aco - tw_aco) * (d_aco - 2*tf_aco)**3)/12
            Wx = Ix / (d_aco/2)
            Zx = bf_aco * tf_aco * h0 + (tw_aco * (d_aco - 2*tf_aco)**2)/4
            J = (2 * bf_aco * tf_aco**3 + (d_aco - 2*tf_aco) * tw_aco**3)/3
            Cw = (Iy * h0**2)/4 
            ry = math.sqrt(Iy / Area)
            Rs = Area * (fy / 1.10)
            
            if viga_mista:
                fcd = (fck_misto / 1.4) / 10
                Rc = 0.85 * fcd * beff_concreto * tc_concreto
                if Rc >= Rs:
                    a_comp = Rs / (0.85 * fcd * beff_concreto)
                    pna_y = d_aco + tc_concreto - a_comp
                    M_misto_Rd = Rs * ((d_aco / 2) + tc_concreto - (a_comp / 2))
                else:
                    Ra_comp = (Rs - Rc) / 2
                    R_mesa_sup = (bf_aco * tf_aco) * (fy / 1.10)
                    if Ra_comp <= R_mesa_sup: pna_y = d_aco - (Ra_comp / (bf_aco * (fy/1.10)))
                    else: pna_y = d_aco - tf_aco - ((Ra_comp - R_mesa_sup) / (tw_aco * (fy/1.10)))
                    M_misto_Rd = Rc * ((d_aco / 2) + (tc_concreto / 2)) + (Rs - Rc) * (d_aco/4)
                st.success(rf"Momento Plástico Viga Mista: **{M_misto_Rd/100:.2f} kN.m**")
                st.pyplot(plot_secao_mista(d_aco, bf_aco, tw_aco, tf_aco, tc_concreto, beff_concreto, pna_y))
            else:
                E, G = 20000.0, 7700.0
                Mpl, Mr, Lp = Zx * fy, 0.7 * fy * Wx, 1.76 * ry * math.sqrt(E / fy)
                if Lb <= 0: st.success(rf"Momento Plástico 100% Contido: **{Mpl/1.10/100:.2f} kN.m**")
                else:
                    L_low, L_high = Lp, 20000.0
                    for _ in range(40):
                        L_mid = (L_low + L_high)/2
                        if calc_Mcr(L_mid, E, G, Iy, J, Cw, 1.0) > Mr: L_low = L_mid
                        else: L_high = L_mid
                    Lr = (L_low + L_high)/2
                    Mcr = calc_Mcr(Lb, E, G, Iy, J, Cw, 1.0) 
                    
                    if Lb <= Lp: Mk = Mpl
                    elif Lb <= Lr: Mk = min(Mpl - (Mpl - Mr) * ((Lb - Lp) / (Lr - Lp)), Mpl)
                    else: Mk = min(Mcr, Mpl)
                        
                    st.success(rf"Momento Resistente (FLT): **{Mk/1.10/100:.2f} kN.m**")
                    st.pyplot(plot_curva_flt(Lp, Lr, Mpl, Mr, Lb, Mk/1.10, E, G, Iy, J, Cw))


# ==========================================
# MÓDULO 6: ORÇAMENTAÇÃO E QUANTITATIVOS (ERP HFF)
# ==========================================
def modulo_materiais_avancado():
    st.header("Módulo 6: Dimensionamento de Materiais e Insumos ERP")
    st.markdown("Gestão de insumos e quantitativos precisos para o canteiro de obras.")
    st.markdown("---")
    
    st.markdown("### 1. Selecione os itens a orçamentar:")
    col_opt1, col_opt2, col_opt3 = st.columns(3)
    calc_alvenaria = col_opt1.checkbox("🧱 Alvenaria", value=True)
    calc_fundacoes = col_opt2.checkbox("🕳️ Fundações", value=True)
    calc_superest = col_opt3.checkbox("🏛️ Superestrutura", value=True)
    
    st.markdown("---")
    dados = {}
    tracos = {}

    st.markdown("### 2. Geometria do Projeto")
    if calc_alvenaria:
        with st.expander("🧱 Dados da Alvenaria", expanded=True):
            col1, col2, col3 = st.columns(3)
            dados['pe_direito'] = col1.number_input("Pé-direito (m)", min_value=0.0, value=2.8)
            dados['ml_1_vez'] = col2.number_input("Metragem Linear Parede 1 Vez (m)", min_value=0.0, value=20.0)
            dados['ml_meia_vez'] = col3.number_input("Metragem Linear Parede Meia Vez (m)", min_value=0.0, value=50.0)
            
    if calc_fundacoes:
        with st.expander("🕳️ Geometria das Estacas", expanded=True):
            col_e1, col_e2, col_e3 = st.columns(3)
            dados['qtd_estacas'] = col_e1.number_input("Quantidade de Estacas", min_value=0, value=20)
            dados['diam_estaca'] = col_e2.number_input("Diâmetro da Estaca (cm)", min_value=10.0, value=25.0)
            dados['prof_estaca'] = col_e3.number_input("Profundidade (m)", min_value=0.0, value=6.0)
            
            col_e4, col_e5, col_e6 = st.columns(3)
            dados['qtd_long_est'] = col_e4.number_input("Qtd Varões Long/Estaca", min_value=3, value=4)
            dados['espac_estribo_est'] = col_e5.number_input("Espaçamento Estribos (cm) ", min_value=5.0, value=15.0)
            dados['cob_est'] = col_e6.number_input("Cobrimento Estacas (cm)", min_value=1.0, value=4.0)
            dados['transp_est'] = st.number_input("Transpasse Aço Estacas (cm)", min_value=10.0, value=40.0)

    if calc_superest:
        with st.expander("🏛️ Pilares e Vigas", expanded=True):
            st.markdown("**Pilares**")
            col_p1, col_p2, col_p3 = st.columns(3)
            dados['qtd_pil'] = col_p1.number_input("Qtd Pilares", min_value=0, value=12)
            dados['b_pil'] = col_p2.number_input("Base Pilar (cm)", min_value=14.0, value=15.0)
            dados['h_pil'] = col_p3.number_input("Altura Pilar (cm)", min_value=14.0, value=30.0)
            dados['comp_pil'] = st.number_input("Comprimento Pilar (m)", min_value=0.0, value=3.0)
            
            col_p4, col_p5, col_p6 = st.columns(3)
            dados['qtd_long_pil'] = col_p4.number_input("Qtd Varões Long/Pilar", min_value=4, value=4)
            dados['espac_estribo_pil'] = col_p5.number_input("Espaç. Estribos Pilar (cm)", min_value=5.0, value=15.0)
            dados['cob_pil'] = col_p6.number_input("Cobrimento Pilares (cm)", min_value=1.0, value=3.0)
            dados['transp_pil'] = st.number_input("Transpasse Aço Pilar (cm)", min_value=10.0, value=40.0)

            st.markdown("---")
            st.markdown("**Vigas**")
            col_v1, col_v2, col_v3 = st.columns(3)
            dados['qtd_vig'] = col_v1.number_input("Qtd Vigas", min_value=0, value=15)
            dados['bw_vig'] = col_v2.number_input("Base Viga (cm)", min_value=10.0, value=15.0)
            dados['h_vig'] = col_v3.number_input("Altura Viga (cm)", min_value=15.0, value=40.0)
            dados['comp_vig'] = st.number_input("Comprimento Médio Viga (m)", min_value=0.0, value=4.0)
            
            col_v4, col_v5, col_v6 = st.columns(3)
            dados['qtd_long_vig'] = col_v4.number_input("Qtd Varões Long/Viga", min_value=2, value=4)
            dados['espac_estribo_vig'] = col_v5.number_input("Espaç. Estribos Viga (cm)", min_value=5.0, value=15.0)
            dados['cob_vig'] = col_v6.number_input("Cobrimento Vigas (cm)", min_value=1.0, value=3.0)
            dados['transp_vig'] = st.number_input("Transpasse Aço Viga (cm)", min_value=5.0, value=20.0)

    st.markdown("---")
    st.markdown("### 🪣 3. Configuração de Traços (Proporção Volumétrica)")
    tipo_concreto = st.radio("Preparo do Betão Estrutural", ["Usinado na Concreteira", "Virado na Obra"], horizontal=True)

    # 4 CAIXAS SEPARADAS DE TRAÇOS (O que foi pedido!)
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    
    with col_t1:
        st.markdown("**1. Assentamento** (Ex: 1:0.5:6)")
        tracos['ass_cim'] = st.number_input("Cimento (Ass)", value=1.0, step=0.1)
        tracos['ass_cal'] = st.number_input("Cal (Ass)", value=0.5, step=0.1)
        tracos['ass_ar']  = st.number_input("Areia (Ass)", value=6.0, step=0.1)
        
    with col_t2:
        st.markdown("**2. Revestimento** (Ex: 1:1:6)")
        tracos['rev_cim'] = st.number_input("Cimento (Rev)", value=1.0, step=0.1)
        tracos['rev_cal'] = st.number_input("Cal (Rev)", value=1.0, step=0.1)
        tracos['rev_ar']  = st.number_input("Areia (Rev)", value=6.0, step=0.1)

    with col_t3:
        st.markdown("**3. Chapisco** (Ex: 1:0:3)")
        tracos['chap_cim'] = st.number_input("Cimento (Chap)", value=1.0, step=0.1)
        tracos['chap_cal'] = st.number_input("Cal (Chap)", value=0.0, step=0.1)
        tracos['chap_ar']  = st.number_input("Areia (Chap)", value=3.0, step=0.1)

    with col_t4:
        st.markdown("**4. Betão / Concreto**")
        if tipo_concreto == "Virado na Obra":
            tracos['conc_cim'] = st.number_input("Cimento (Betão)", value=1.0, step=0.1)
            tracos['conc_ar']  = st.number_input("Areia (Betão)", value=2.0, step=0.1)
            tracos['conc_br']  = st.number_input("Brita (Betão)", value=3.0, step=0.1)
        else:
            st.info("Insumos manuais ignorados para Usinado.")
            dados['fck_usinado'] = st.selectbox("FCK (MPa)", [20, 25, 30, 35])
            tracos['conc_cim'] = tracos['conc_ar'] = tracos['conc_br'] = 0

    st.markdown("---")
    with st.expander("💸 4. Preços Unitários e Aço Comercial", expanded=False):
        comp_barra = st.radio("Tamanho Padrão do Varão de Aço", [12.0, 6.0], horizontal=True)
        col_pr1, col_pr2, col_pr3, col_pr4 = st.columns(4)
        pr_tij_1v = col_pr1.number_input("Tijolo 1 Vez (un)", value=1.20)
        pr_tij_m = col_pr2.number_input("Tijolo Meia Vez (un)", value=0.80)
        pr_cimento = col_pr3.number_input("Saco Cimento 50kg", value=35.00)
        pr_cal = col_pr4.number_input("Saco Cal 20kg", value=15.00)
        
        col_pr5, col_pr6, col_pr7, col_pr8 = st.columns(4)
        pr_areia = col_pr5.number_input("Areia (m³)", value=120.00)
        pr_brita = col_pr6.number_input("Brita (m³)", value=110.00)
        pr_aco_fino = col_pr7.number_input("Aço Fino/Estribo", value=25.00)
        pr_aco_grosso = col_pr8.number_input("Aço Grosso/Longit.", value=60.00)
        pr_conc_usinado = st.number_input("Preço Betão Usinado (m³)", value=450.00) if tipo_concreto != "Virado na Obra" else 0.0

    # PROCESSAMENTO DO ERP
    if st.button("📊 GERAR ORÇAMENTO E RELATÓRIO", type="primary", use_container_width=True):
        
        total_cimento_sacos = total_cal_sacos = 0
        total_areia_m3 = total_brita_m3 = 0.0
        qtd_tij_1v = qtd_tij_mv = 0
        vol_concreto_total = comp_total_estribos = comp_total_longit = 0.0

        def calcular_insumos_traco(volume_necessario_m3, t_cim, t_cal, t_ar):
            if volume_necessario_m3 <= 0 or t_ar == 0: return 0, 0, 0
            vol_uma_parte = volume_necessario_m3 / t_ar
            sacos_cim = (vol_uma_parte * t_cim) / 0.036
            sacos_cal = (vol_uma_parte * t_cal) / 0.036
            return math.ceil(sacos_cim), math.ceil(sacos_cal), volume_necessario_m3

        if calc_alvenaria:
            area_1v = dados['ml_1_vez'] * dados['pe_direito']
            area_mv = dados['ml_meia_vez'] * dados['pe_direito']
            
            qtd_tij_1v = math.ceil(area_1v * 38.45) 
            qtd_tij_mv = math.ceil(area_mv * 25.0)  
            
            vol_assent = (area_1v * 0.03) + (area_mv * 0.015)
            vol_chapisco = (area_1v + area_mv) * 2 * 0.005
            vol_revest = (area_1v + area_mv) * 2 * 0.02
            
            cim_a, cal_a, ar_a = calcular_insumos_traco(vol_assent, tracos['ass_cim'], tracos['ass_cal'], tracos['ass_ar'])
            cim_c, cal_c, ar_c = calcular_insumos_traco(vol_chapisco, tracos['chap_cim'], tracos['chap_cal'], tracos['chap_ar'])
            cim_r, cal_r, ar_r = calcular_insumos_traco(vol_revest, tracos['rev_cim'], tracos['rev_cal'], tracos['rev_ar'])
            
            total_cimento_sacos += (cim_a + cim_c + cim_r)
            total_cal_sacos += (cal_a + cal_c + cal_r)
            total_areia_m3 += (ar_a + ar_c + ar_r)

        if calc_fundacoes:
            vol_conc_estacas = dados['qtd_estacas'] * (math.pi * ((dados['diam_estaca']/100)/2)**2) * dados['prof_estaca']
            comp_e_est_u = (math.pi * ((dados['diam_estaca'] - 2*dados['cob_est'])/100)) + (2 * dados['transp_est']/100)
            comp_e_long_u = dados['prof_estaca'] + (dados['transp_est']/100)
            
            vol_concreto_total += vol_conc_estacas
            comp_total_estribos += comp_e_est_u * math.ceil((dados['prof_estaca'] * 100) / dados['espac_estribo_est']) * dados['qtd_estacas']
            comp_total_longit += comp_e_long_u * dados['qtd_long_est'] * dados['qtd_estacas']
            
        if calc_superest:
            vol_conc_pil = dados['qtd_pil'] * (dados['b_pil']/100) * (dados['h_pil']/100) * dados['comp_pil']
            comp_p_est_u = 2*((dados['b_pil'] - 2*dados['cob_pil'])/100) + 2*((dados['h_pil'] - 2*dados['cob_pil'])/100) + (2 * dados['transp_pil']/100)
            comp_p_long_u = dados['comp_pil'] + (dados['transp_pil']/100)
            
            vol_concreto_total += vol_conc_pil
            comp_total_estribos += comp_p_est_u * math.ceil((dados['comp_pil'] * 100) / dados['espac_estribo_pil']) * dados['qtd_pil']
            comp_total_longit += comp_p_long_u * dados['qtd_long_pil'] * dados['qtd_pil']
            
            vol_conc_vig = dados['qtd_vig'] * (dados['bw_vig']/100) * (dados['h_vig']/100) * dados['comp_vig']
            comp_v_est_u = 2*((dados['bw_vig'] - 2*dados['cob_vig'])/100) + 2*((dados['h_vig'] - 2*dados['cob_vig'])/100) + (2 * dados['transp_vig']/100)
            comp_v_long_u = dados['comp_vig'] + (dados['transp_vig']/100)
            
            vol_concreto_total += vol_conc_vig
            comp_total_estribos += comp_v_est_u * math.ceil((dados['comp_vig'] * 100) / dados['espac_estribo_vig']) * dados['qtd_vig']
            comp_total_longit += comp_v_long_u * dados['qtd_long_vig'] * dados['qtd_vig']

        barras_fino = math.ceil(comp_total_estribos / comp_barra) if comp_total_estribos > 0 else 0
        barras_grosso = math.ceil(comp_total_longit / comp_barra) if comp_total_longit > 0 else 0

        if tipo_concreto == "Virado na Obra" and vol_concreto_total > 0:
            vol_seco_total = vol_concreto_total * 1.5 
            soma_partes = tracos['conc_cim'] + tracos['conc_ar'] + tracos['conc_br']
            vol_uma_parte = vol_seco_total / soma_partes
            total_cimento_sacos += math.ceil((vol_uma_parte * tracos['conc_cim']) / 0.036)
            total_areia_m3 += (vol_uma_parte * tracos['conc_ar'])
            total_brita_m3 += (vol_uma_parte * tracos['conc_br'])

        custo_tij_1v = qtd_tij_1v * pr_tij_1v
        custo_tij_mv = qtd_tij_mv * pr_tij_m
        custo_cimento = total_cimento_sacos * pr_cimento
        custo_cal = total_cal_sacos * pr_cal
        custo_areia = total_areia_m3 * pr_areia
        custo_brita = total_brita_m3 * pr_brita
        custo_aco_fino = barras_fino * pr_aco_fino
        custo_aco_grosso = barras_grosso * pr_aco_grosso
        custo_conc_usinado = vol_concreto_total * pr_conc_usinado if tipo_concreto != "Virado na Obra" else 0.0
            
        custo_total_geral = sum([custo_tij_1v, custo_tij_mv, custo_cimento, custo_cal, custo_areia, custo_brita, custo_aco_fino, custo_aco_grosso, custo_conc_usinado])

        st.markdown("### 📑 Resultado do Orçamento")
        tab_a, tab_b, tab_c = st.tabs(["🏗️ Insumos Brutos", "⚙️ Metragem de Aço", "💰 Tabela Oficial"])
        
        with tab_a:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Cimento (50kg)", f"{total_cimento_sacos} sacos")
            col2.metric("Cal (20kg)", f"{total_cal_sacos} sacos")
            col3.metric("Areia", f"{total_areia_m3:.2f} m³")
            col4.metric("Brita", f"{total_brita_m3:.2f} m³")
            st.markdown("---")
            if calc_alvenaria:
                st.write(f"🧱 **Tijolos de 1 Vez:** {qtd_tij_1v} unidades")
                st.write(f"🧱 **Tijolos de Meia Vez:** {qtd_tij_mv} unidades")
            if tipo_concreto != "Virado na Obra" and vol_concreto_total > 0:
                st.info(f"🚚 **Betão Usinado a pedir:** {vol_concreto_total:.2f} m³")
                
        with tab_b:
            st.write(f"**Armadura Transversal (Estribos) - Metragem: {comp_total_estribos:.2f} m lineares**")
            st.success(f"Comprar: **{barras_fino} Varões de {comp_barra}m**")
            st.write(f"**Armadura Longitudinal (Estrutural) - Metragem: {comp_total_longit:.2f} m lineares**")
            st.success(f"Comprar: **{barras_grosso} Varões de {comp_barra}m**")
            
        with tab_c:
            itens_orcamento = [
                {"Material": "Tijolo 1 Vez", "Quantidade": f"{qtd_tij_1v} un", "Custo (R$)": custo_tij_1v},
                {"Material": "Tijolo Meia Vez", "Quantidade": f"{qtd_tij_mv} un", "Custo (R$)": custo_tij_mv},
                {"Material": "Cimento (50kg)", "Quantidade": f"{total_cimento_sacos} sacos", "Custo (R$)": custo_cimento},
                {"Material": "Cal (20kg)", "Quantidade": f"{total_cal_sacos} sacos", "Custo (R$)": custo_cal},
                {"Material": "Areia", "Quantidade": f"{total_areia_m3:.2f} m³", "Custo (R$)": custo_areia},
                {"Material": "Brita", "Quantidade": f"{total_brita_m3:.2f} m³", "Custo (R$)": custo_brita},
                {"Material": f"Aço Fino ({comp_barra}m)", "Quantidade": f"{barras_fino} brs", "Custo (R$)": custo_aco_fino},
                {"Material": f"Aço Grosso ({comp_barra}m)", "Quantidade": f"{barras_grosso} brs", "Custo (R$)": custo_aco_grosso}
            ]
            if tipo_concreto != "Virado na Obra":
                itens_orcamento.append({"Material": "Betão Usinado", "Quantidade": f"{vol_concreto_total:.2f} m³", "Custo (R$)": custo_conc_usinado})
                
            df = pd.DataFrame(itens_orcamento)
            df = df[df["Custo (R$)"] > 0]
            st.dataframe(df.style.format({"Custo (R$)": "R$ {:.2f}"}), use_container_width=True)
            st.success(f"### Custo Total Estimado: R$ {custo_total_geral:,.2f}")

# ==========================================
# BARRA LATERAL E NAVEGAÇÃO HFF
# ==========================================
try:
    if os.path.exists("image_d804c5.png"):
        st.sidebar.image("image_d804c5.png", use_column_width=True)
    else:
        st.sidebar.markdown("<h1 style='text-align: center; color: white;'>HFF</h1>", unsafe_allow_html=True)
except:
    st.sidebar.markdown("<h1 style='text-align: center; color: white;'>HFF</h1>", unsafe_allow_html=True)

st.sidebar.markdown("---")
modulo = st.sidebar.radio("Navegação do Sistema:", [
    "6. Materiais ERP (Orçamento)",
    "0. Cargas (NBR 6120)", 
    "1. Vigas CA (Gráficos)", 
    "2. Pilares CA", 
    "3. Lajes Maciças", 
    "4. Lajes Treliçadas",
    "5. Estruturas Metálicas"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📐 Referências Normativas\n- **NBR 6118**\n- **NBR 6120**\n- **NBR 8800**")

# ROTAS
if "6" in modulo: modulo_materiais_avancado()
elif "0" in modulo: modulo_cargas()
elif "1" in modulo: modulo_vigas()
elif "2" in modulo: modulo_pilares()
elif "3" in modulo: modulo_lajes()
elif "4" in modulo: modulo_laje_trelicada()
elif "5" in modulo: modulo_metalicas_mistas()