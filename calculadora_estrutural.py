import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Configuração da página
st.set_page_config(page_title="Plataforma de Cálculo Estrutural - NBR 6118/6120", layout="wide")

# ==========================================
# FUNÇÕES GRÁFICAS DE COMPORTAMENTO MECÂNICO
# ==========================================

def plot_viga_esforcos(L, q):
    x = np.linspace(0, L, 200)
    V = q * (L / 2 - x)
    M = (q * x / 2) * (L - x)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5))
    ax1.plot(x, V, color='teal', lw=2)
    ax1.fill_between(x, V, color='teal', alpha=0.1)
    ax1.axhline(0, color='black', lw=0.8)
    ax1.set_title("Diagrama de Força Cortante - DEC (kN)", fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    ax2.plot(x, M, color='crimson', lw=2)
    ax2.fill_between(x, M, color='crimson', alpha=0.1)
    ax2.axhline(0, color='black', lw=0.8)
    ax2.set_title("Diagrama de Momento Fletor - DMF (kN.m)", fontsize=10)
    ax2.invert_yaxis()
    ax2.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    return fig

def plot_viga_dominios(bw, h, d, x_ln):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), gridspec_kw={'width_ratios': [1, 1.5]})
    
    ax1.add_patch(patches.Rectangle((0, 0), bw, h, fill=False, lw=2, color='black'))
    ax1.axhline(h - x_ln, color='red', linestyle='--', label='L.N.')
    ax1.add_patch(patches.Rectangle((0, h - 0.8*x_ln), bw, 0.8*x_ln, color='red', alpha=0.2, label='0.8x Comprimido'))
    ax1.scatter([bw*0.25, bw*0.5, bw*0.75], [h - d, h - d, h - d], color='blue', s=80, label='Aço (As)')
    ax1.set_xlim(-5, bw+5)
    ax1.set_ylim(-5, h+5)
    ax1.set_title("Seção Transversal", fontsize=10)
    ax1.axis('off')
    ax1.legend(loc='lower center', fontsize=7)
    
    ax2.plot([0, 0], [0, h], color='black', lw=1.5)
    ax2.axhline(h - x_ln, color='red', linestyle='--')
    
    x_d = x_ln / d
    if x_d <= 0.259:
        eps_s = 10.0
        eps_c = (x_ln * eps_s) / (d - x_ln)
    else:
        eps_c = 3.5
        eps_s = (eps_c * (d - x_ln)) / x_ln
        
    ax2.plot([-eps_c, eps_s], [h, h - d], color='purple', lw=2, marker='o')
    ax2.fill_betweenx([h - x_ln, h], 0, [-eps_c*0.0, -eps_c], color='red', alpha=0.1)
    ax2.fill_betweenx([h - d, h - x_ln], 0, [eps_s, eps_s*0.0], color='blue', alpha=0.1)
    
    ax2.set_title("Diagrama de Deformações (Domínios)", fontsize=10)
    ax2.set_xlabel(r"Deformação ($\perthousand$)")
    ax2.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig

def plot_viga_elevacao(L, h):
    """Gera o desenho de elevação longitudinal da viga com armaduras"""
    L_cm = L * 100
    fig, ax = plt.subplots(figsize=(10, 2.5))
    
    # Contorno de Concreto
    ax.add_patch(patches.Rectangle((0, 0), L_cm, h, fill=False, lw=2, color='gray', label='Face de Concreto'))
    
    c = 3.0 # Cobrimento visual
    # Armadura Longitudinal Inferior (Tração)
    ax.plot([c, L_cm-c], [c, c], color='blue', lw=3.5, label='Armadura Longitudinal (Tração)')
    # Armadura Construtiva Superior (Porta-estribos)
    ax.plot([c, L_cm-c], [h-c, h-c], color='blue', lw=1.5, linestyle='--', label='Armadura Superior (Construtiva)')
    
    # Armadura Transversal (Estribos) - Distribuídos visualmente ao longo do vão
    s_visual = max(15.0, L_cm / 40) # Espaçamento apenas para não poluir o desenho
    x_estribos = np.arange(c, L_cm-c, s_visual)
    for x in x_estribos:
        ax.plot([x, x], [c, h-c], color='darkred', lw=1.5)
    ax.plot([], [], color='darkred', lw=1.5, label='Armadura Transversal (Estribos)')
    
    ax.set_xlim(-10, L_cm + 10)
    ax.set_ylim(-10, h + 10)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(rf"Elevação Longitudinal da Viga (Vão = {L}m)", fontsize=10)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.4), ncol=4, fontsize=8)
    return fig

def plot_secao_T(bf, bw, h, hf, d, x_ln):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.add_patch(patches.Rectangle((-bw/2, 0), bw, h - hf, fill=False, lw=2, color='black'))
    ax.add_patch(patches.Rectangle((-bf/2, h - hf), bf, hf, fill=False, lw=2, color='black'))
    ax.axhline(h - x_ln, color='red', linestyle='--', label=rf'L.N. (x={x_ln:.2f}cm)')
    
    y_comp = 0.8 * x_ln
    if y_comp <= hf:
        ax.add_patch(patches.Rectangle((-bf/2, h - y_comp), bf, y_comp, color='red', alpha=0.3, label='Zona Comprimida'))
    else:
        ax.add_patch(patches.Rectangle((-bf/2, h - hf), bf, hf, color='red', alpha=0.3))
        ax.add_patch(patches.Rectangle((-bw/2, h - y_comp), bw, y_comp - hf, color='red', alpha=0.3, label='Zona Comprimida'))
    
    ax.scatter([-bw/4, bw/4], [h - d, h - d], color='blue', s=80, label='Aço Longitudinal')
    ax.set_xlim(-bf/2 - 5, bf/2 + 5)
    ax.set_ylim(-5, h + 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='lower center', fontsize=8)
    return fig

def plot_pilar_secao(b, h, num_barras):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.add_patch(patches.Rectangle((0, 0), b, h, fill=False, lw=3, color='grey', label='Concreto'))
    ax.add_patch(patches.Rectangle((2.5, 2.5), b-5, h-5, fill=False, lw=1.5, color='darkred', linestyle='-', label='Estribo Transversal'))
    xs = [3.5, b-3.5]
    ys = [3.5, h-3.5]
    barras_x, barras_y = [], []
    
    if num_barras == 4:
        for x in xs:
            for y in ys:
                barras_x.append(x); barras_y.append(y)
    elif num_barras == 6:
        for x in xs:
            for y in ys:
                barras_x.append(x); barras_y.append(y)
        if h >= b:
            barras_x.extend([3.5, b-3.5]); barras_y.extend([h/2, h/2])
        else:
            barras_x.extend([b/2, b/2]); barras_y.extend([3.5, h-3.5])
            
    ax.scatter(barras_x, barras_y, color='black', s=150, zorder=3, label='Barras')
    ax.set_xlim(-5, b+5)
    ax.set_ylim(-5, h+5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='upper right', fontsize=8)
    return fig

def plot_laje_ruptura(lx, ly):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.add_patch(patches.Rectangle((0, 0), lx, ly, fill=False, lw=2, color='black'))
    
    if lx <= ly:
        x1, y1 = lx/2, lx/2
        x2, y2 = lx/2, ly - lx/2
        ax.plot([0, x1], [0, y1], color='orange', lw=2, linestyle='--')
        ax.plot([lx, x1], [0, y1], color='orange', lw=2, linestyle='--')
        ax.plot([0, x2], [ly, y2], color='orange', lw=2, linestyle='--')
        ax.plot([lx, x2], [ly, y2], color='orange', lw=2, linestyle='--')
        ax.plot([x1, x2], [y1, y2], color='orange', lw=2, linestyle='--')
    else:
        x1, y1 = ly/2, ly/2
        x2, y2 = lx - ly/2, ly/2
        ax.plot([0, x1], [0, y1], color='orange', lw=2, linestyle='--')
        ax.plot([0, x2], [ly, y2], color='orange', lw=2, linestyle='--')
        ax.plot([lx, x1], [0, y1], color='orange', lw=2, linestyle='--')
        ax.plot([lx, x2], [ly, y2], color='orange', lw=2, linestyle='--')
        ax.plot([x1, x2], [y1, y2], color='orange', lw=2, linestyle='--')
        
    ax.set_xlim(-0.5, lx+0.5)
    ax.set_ylim(-0.5, ly+0.5)
    ax.set_title("Quinhões de Carga (Linhas de Ruptura)", fontsize=10)
    ax.grid(True, alpha=0.3)
    return fig

# ==========================================
# MÓDULOS DA APLICAÇÃO
# ==========================================

def modulo_cargas():
    st.header("Módulo 0: Estimativa e Descida de Cargas (NBR 6120)")
    st.markdown("---")
    st.info("💡 **Objetivo:** Estimar a carga total da edificação baseada na área construída e distribuir o peso de forma aproximada pela quantidade de pilares (Áreas de Influência).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dados Arquitetônicos")
        area_planta = st.number_input("Área da Planta por Pavimento (m²)", min_value=10.0, value=100.0)
        uso = st.selectbox("Tipo de Uso (Carga Acidental NBR 6120)", ["Residencial", "Comercial / Escritórios", "Garagem / Depósito"])
        num_pilares = st.number_input("Quantidade estimada de Pilares", min_value=4, value=9)
        
        pavimentos_tipo = st.radio("Tipologia da Edificação:", ["Térrea (1 Laje)", "Sobrado / Múltiplos Andares"])
        
        andares = 1
        if pavimentos_tipo == "Sobrado / Múltiplos Andares":
            andares = st.number_input("Número de Lajes (Andares/Pavimentos)", min_value=2, value=2)

    with col2:
        st.subheader("Análise de Cargas")
        if st.button("Gerar Descida de Cargas"):
            # Estimativas por m² (Peso Próprio + Revestimento + Alvenaria + Acidental)
            carga_acidental = 1.5 if uso == "Residencial" else (2.5 if "Comercial" in uso else 3.0)
            carga_permanente = 5.5 # Estimativa média: 2.5(laje) + 1.0(rev) + 2.0(alvenaria)
            
            carga_por_m2 = carga_permanente + carga_acidental
            carga_total_pavimento = area_planta * carga_por_m2
            carga_total_edificacao = carga_total_pavimento * andares
            
            # Carga média por pilar (Descida de carga simplificada)
            # Adicionamos 10% a mais para compensar o peso próprio do próprio pilar e da viga
            carga_pilar_media = (carga_total_edificacao / num_pilares) * 1.10
            
            st.write(rf"- Carga Média Estimada: **{carga_por_m2:.2f} kN/m²**")
            st.write(rf"- Peso Total da Edificação: **{carga_total_edificacao:.2f} kN** (Aprox. {carga_total_edificacao/10:.1f} Toneladas)")
            st.markdown("### 🎯 Descarga nos Pilares (Nk)")
            st.success(rf"Carga Axial Média por Pilar ($N_k$): **{carga_pilar_media:.2f} kN**")
            st.caption("Nota: Pilares centrais costumam receber até 30% mais carga do que a média, e os de canto recebem menos. Use este valor médio de Nk para iniciar o dimensionamento no 'Módulo de Pilares'.")

def modulo_vigas():
    st.header("Módulo 1: Vigas - Flexão, Cortante e Detalhamento")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("Vão Livre da Viga L (m)", min_value=1.0, value=5.0)
        q_reg = st.number_input("Carga Distribuída q (kN/m)", min_value=1.0, value=15.0)
        bw = st.number_input("Largura bw (cm)", min_value=10.0, value=20.0)
        h = st.number_input("Altura h (cm)", min_value=20.0, value=50.0)
        caa = st.selectbox("Agressividade Ambiental", ["I - Fraca", "II - Moderada", "III - Forte"])
        fck = st.number_input("fck (MPa)", min_value=20.0, value=25.0)

    with col2:
        if st.button("Executar Análise"):
            c_nom = 2.5 if "I -" in caa else 3.0 if "II -" in caa else 4.0
            q_d = q_reg * 1.4
            M_sd = (q_d * (L**2)) / 8
            V_sd = (q_d * L) / 2
            
            d = h - c_nom - 1.2
            fcd = (fck / 1.4) / 10
            fyd = (500 / 1.15) / 10
            
            a_eq = 0.272 * bw * fcd
            b_eq = -0.68 * bw * fcd * d
            c_eq = M_sd * 100
            delta = b_eq**2 - 4 * a_eq * c_eq
            
            if delta < 0:
                st.error("Seção Superarmada. Aumente 'h'.")
            else:
                x_ln = (-b_eq - math.sqrt(delta)) / (2 * a_eq)
                As_calc = (M_sd * 100) / (fyd * (d - 0.4 * x_ln))
                rho_min = 0.15 / 100 if fck <= 30 else (0.15 + (fck-30)*0.002)/100
                As_min = rho_min * bw * h
                As_final = max(As_calc, As_min)
                
                st.success(rf"Área de Aço (As): **{As_final:.2f} cm²**")
                
                # Cortante
                fctm = 0.3 * (fck**(2/3))
                fctd = (0.7 * fctm) / 1.4 / 10
                V_c = 0.6 * fctd * bw * d
                V_sw = max(0, V_sd - V_c)
                Asw_s_calc = (V_sw / (0.9 * d * fyd)) * 100
                Asw_s_min = (0.2 * (fctm / 500)) * bw * 100
                Asw_s_final = max(Asw_s_calc, Asw_s_min)
                st.success(rf"Estribos (Asw/s): **{Asw_s_final:.2f} cm²/m**")
                
                # Gráficos
                st.pyplot(plot_viga_dominios(bw, h, d, x_ln))
                st.markdown("### 🏗️ Detalhamento Longitudinal da Armadura")
                st.pyplot(plot_viga_elevacao(L, h))

def modulo_pilares():
    st.header("Módulo 2: Pilares")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        b = st.number_input("Dimensão b (cm)", min_value=14.0, value=20.0)
        h_p = st.number_input("Dimensão h (cm)", min_value=14.0, value=30.0)
        N_k = st.number_input("Força Normal Nk (kN)", min_value=10.0, value=600.0, help="Utilize o Nk gerado no Módulo 0 (Cargas).")
        phi_l = st.selectbox("Bitola Longitudinal (mm)", [10.0, 12.5, 16.0, 20.0, 25.0])
        num_barras = st.selectbox("Quantidade de Barras", [4, 6])

    with col2:
        if st.button("Analisar Pilar"):
            N_sd = N_k * 1.4
            Ac = b * h_p
            fyd = (500 / 1.15) / 10
            As_real = num_barras * ((math.pi * (phi_l/10)**2) / 4)
            As_min = max(0.15 * (N_sd / fyd), 0.004 * Ac)
            As_max = 0.08 * Ac
            
            if As_real < As_min: st.error("Pilar Subarmado!")
            elif As_real > As_max: st.error("Pilar Superarmado!")
            else: st.success("Armadura Longitudinal OK!")
            
            phi_t = max(5.0, phi_l / 4)
            s_max = min(20.0, b, h_p, 12 * (phi_l / 10))
            st.write(rf"Estribos: $\phi$ **{phi_t:.1f} mm** a cada **{math.floor(s_max)} cm**")
            st.pyplot(plot_pilar_secao(b, h_p, num_barras))

def modulo_lajes():
    st.header("Módulo 3: Lajes Maciças")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        lx = st.number_input("Vão Menor lx (m)", min_value=1.0, value=3.5)
        ly = st.number_input("Vão Maior ly (m)", min_value=1.0, value=4.5)
        p_total = st.number_input("Carga Total q (kN/m²)", min_value=1.0, value=6.0)
        h_laje = st.number_input("Espessura h (cm)", min_value=5.0, value=9.0)
        fck = st.number_input("fck (MPa)", value=25.0)

    with col2:
        if st.button("Dimensionar Laje"):
            lam = ly / lx
            is_unidirecional = lam > 2.0
            M_x_k = (p_total * (lx**2)) / 8 if is_unidirecional else (((ly**4) / (lx**4 + ly**4)) * p_total * (lx**2)) / 8
            
            M_xd = M_x_k * 1.4
            d = h_laje - 2.0
            fcd = (fck / 1.4) / 10
            fyd = (500 / 1.15) / 10
            
            a_eq = 0.272 * 100 * fcd
            b_eq = -0.68 * 100 * fcd * d
            c_eq = M_xd * 100
            delta = b_eq**2 - 4 * a_eq * c_eq
            
            if delta < 0:
                st.error("Espessura insuficiente.")
            else:
                x_ln = (-b_eq - math.sqrt(delta)) / (2 * a_eq)
                As_calc = (M_xd * 100) / (fyd * (d - 0.4 * x_ln))
                As_min = (0.15 / 100) * 100 * h_laje
                As_final = max(As_calc, As_min)
                
                st.success(rf"Área de Aço ($A_{{s,x}}$): **{As_final:.2f} cm²/m**")
                st.pyplot(plot_laje_ruptura(lx, ly))

def modulo_laje_trelicada():
    st.header("Módulo 4: Lajes Treliçadas / Nervuradas")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("Vão Livre da Laje L (m)", min_value=1.0, value=4.0)
        q_laje = st.number_input("Carga Distribuída na Laje (kN/m²)", min_value=1.0, value=4.0)
        bf = st.number_input("Intereixo bf (cm)", min_value=30.0, value=40.0)
        bw = st.number_input("Largura da Sapata bw (cm)", min_value=9.0, value=12.0)
        h = st.number_input("Altura Total h (cm)", min_value=10.0, value=16.0)
        hf = st.number_input("Capa de Concreto hf (cm)", min_value=4.0, value=4.0)
        fck = st.number_input("fck (MPa) ", min_value=20.0, value=25.0)

    with col2:
        if st.button("Dimensionar Nervura"):
            q_nervura = q_laje * (bf / 100)
            M_sd = (q_nervura * 1.4 * (L**2)) / 8
            
            d = h - 2.5
            fcd = (fck / 1.4) / 10
            fyd = (500 / 1.15) / 10
            
            a_eq = 0.272 * bf * fcd
            b_eq = -0.68 * bf * fcd * d
            c_eq = M_sd * 100
            delta = b_eq**2 - 4 * a_eq * c_eq
            
            if delta < 0:
                st.error("Aumente a altura da laje.")
            else:
                x_ln = (-b_eq - math.sqrt(delta)) / (2 * a_eq)
                As_calc = (M_sd * 100) / (fyd * (d - 0.4 * x_ln))
                st.success(rf"Área de Aço por vigota (As): **{As_calc:.2f} cm²**")
                st.pyplot(plot_secao_T(bf, bw, h, hf, d, x_ln))

# ==========================================
# MENU LATERAL E NAVEGAÇÃO
# ==========================================

st.sidebar.title("Navegação")
modulo = st.sidebar.radio("Selecione o Componente:", [
    "0. Cargas (NBR 6120)", 
    "1. Vigas (Flexão/Cortante)", 
    "2. Pilares (Travamento)", 
    "3. Lajes Maciças", 
    "4. Lajes Treliçadas"
])

if "0." in modulo: modulo_cargas()
elif "1." in modulo: modulo_vigas()
elif "2." in modulo: modulo_pilares()
elif "3." in modulo: modulo_lajes()
else: modulo_laje_trelicada()