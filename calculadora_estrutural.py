import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(page_title="Plataforma de Cálculo Estrutural - NBR 6118/6120", layout="wide")

# ==========================================
# FUNÇÕES DE ENGENHARIA E OTIMIZAÇÃO
# ==========================================
def otimizar_bitola(As_req, bw):
    """Testa bitolas comerciais e escolhe a combinação com menor desperdício de aço"""
    bitolas = [8.0, 10.0, 12.5, 16.0, 20.0, 25.0]
    melhor_opcao = None
    menor_excesso = float('inf')
    
    for phi in bitolas:
        area_barra = (math.pi * (phi/10)**2) / 4
        # Mínimo de 2 barras para montar a gaiola da viga
        num_barras = max(2, math.ceil(As_req / area_barra))
        area_total = num_barras * area_barra
        
        # Otimização: Achar o menor excesso de área (mais econômico)
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

def plot_viga_dominios(bw, h, d, x_ln, As_sup_req):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), gridspec_kw={'width_ratios': [1, 1.5]})
    
    # Seção Transversal
    ax1.add_patch(patches.Rectangle((0, 0), bw, h, fill=False, lw=2, color='black'))
    ax1.axhline(h - x_ln, color='red', linestyle='--', label='L.N.')
    ax1.add_patch(patches.Rectangle((0, h - 0.8*x_ln), bw, 0.8*x_ln, color='red', alpha=0.2, label='0.8x Comprimido'))
    
    # Armadura Inferior (Tração)
    ax1.scatter([bw*0.25, bw*0.5, bw*0.75], [h - d, h - d, h - d], color='blue', s=80, label='Aço Tração (As)')
    
    # Armadura Superior (Compressão / Dupla) se existir
    if As_sup_req > 0:
        d_linha = h - d
        ax1.scatter([bw*0.25, bw*0.75], [h - d_linha, h - d_linha], color='orange', s=80, label="Aço Compressão (As')")
    
    ax1.set_xlim(-5, bw+5)
    ax1.set_ylim(-5, h+5)
    ax1.set_title("Seção Transversal", fontsize=10)
    ax1.axis('off')
    ax1.legend(loc='lower center', fontsize=7)
    
    # Diagrama de Domínios
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
    
    ax2.set_title("Diagrama de Deformações", fontsize=10)
    ax2.set_xlabel(r"Deformação ($\perthousand$)")
    ax2.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig

def plot_viga_elevacao(L, h, tem_armadura_dupla):
    L_cm = L * 100
    fig, ax = plt.subplots(figsize=(10, 2.5))
    
    ax.add_patch(patches.Rectangle((0, 0), L_cm, h, fill=False, lw=2, color='gray', label='Concreto'))
    c = 3.0
    
    # Tração
    ax.plot([c, L_cm-c], [c, c], color='blue', lw=3.5, label='Tração (Inferior)')
    
    # Compressão
    if tem_armadura_dupla:
        ax.plot([c, L_cm-c], [h-c, h-c], color='orange', lw=3.5, label='Compressão (Superior - Estrutural)')
    else:
        ax.plot([c, L_cm-c], [h-c, h-c], color='blue', lw=1.5, linestyle='--', label='Construtiva (Porta-estribo)')
    
    s_visual = max(15.0, L_cm / 40)
    x_estribos = np.arange(c, L_cm-c, s_visual)
    for x in x_estribos:
        ax.plot([x, x], [c, h-c], color='darkred', lw=1.5)
    ax.plot([], [], color='darkred', lw=1.5, label='Estribos')
    
    ax.set_xlim(-10, L_cm + 10)
    ax.set_ylim(-10, h + 10)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(rf"Elevação Longitudinal (Vão = {L}m)", fontsize=10)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.4), ncol=4, fontsize=8)
    return fig

# ==========================================
# MÓDULOS DA APLICAÇÃO
# ==========================================
def modulo_vigas():
    st.header("Módulo 1: Vigas - Flexão Inteligente e Armadura Dupla (NBR 6118)")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Entrada de Projeto Mecânico")
        L = st.number_input("Vão Livre da Viga L (m)", min_value=1.0, value=5.0)
        q_reg = st.number_input("Carga Distribuída q (kN/m)", min_value=1.0, value=25.0)
        bw = st.number_input("Largura bw (cm)", min_value=10.0, value=15.0)
        h = st.number_input("Altura h (cm)", min_value=20.0, value=40.0)
        caa = st.selectbox("Agressividade Ambiental", ["I - Fraca", "II - Moderada", "III - Forte"])
        fck = st.number_input("fck (MPa)", min_value=20.0, value=25.0)

    with col2:
        st.subheader("Dimensionamento e Otimização")
        if st.button("Calcular Viga"):
            c_nom = 2.5 if "I -" in caa else 3.0 if "II -" in caa else 4.0
            q_d = q_reg * 1.4
            M_sd = (q_d * (L**2)) / 8
            V_sd = (q_d * L) / 2
            
            d = h - c_nom - 1.2
            d_linha = c_nom + 1.2
            fcd = (fck / 1.4) / 10
            fyd = (500 / 1.15) / 10
            M_sd_cm = M_sd * 100
            
            # Limite do Concreto - Domínio 3 (x_lim = 0.45d para fck <= 50)
            x_lim = 0.45 * d
            M_sd_lim = 0.68 * bw * x_lim * fcd * (d - 0.4 * x_lim)
            
            As_inf = 0
            As_sup = 0
            tem_armadura_dupla = False
            
            if M_sd_cm <= M_sd_lim:
                # ARMADURA SIMPLES (Só aço inferior)
                a_eq = 0.272 * bw * fcd
                b_eq = -0.68 * bw * fcd * d
                c_eq = M_sd_cm
                delta = b_eq**2 - 4 * a_eq * c_eq
                x_ln = (-b_eq - math.sqrt(delta)) / (2 * a_eq)
                As_calc = M_sd_cm / (fyd * (d - 0.4 * x_ln))
                
                rho_min = 0.15 / 100 if fck <= 30 else (0.15 + (fck-30)*0.002)/100
                As_min = rho_min * bw * h
                As_inf = max(As_calc, As_min)
                
                st.success(rf"✅ **Armadura Simples é suficiente.** O concreto suporta a compressão sozinho. (x = {x_ln:.2f} cm)")
            
            else:
                # ARMADURA DUPLA (Aço inferior + Aço superior)
                tem_armadura_dupla = True
                x_ln = x_lim
                delta_M = M_sd_cm - M_sd_lim
                
                As1 = M_sd_lim / (fyd * (d - 0.4 * x_lim))
                As2 = delta_M / (fyd * (d - d_linha))
                As_inf = As1 + As2
                As_sup = delta_M / (fyd * (d - d_linha)) # Simplificado fsc = fyd
                
                st.error(rf"🚨 **Limite do Concreto Excedido!** Momento muito alto para a seção {bw}x{h}.")
                st.warning(r"⚠️ Aplicando **Armadura Dupla** (Aço de Compressão) para evitar ruptura frágil. *Dica de Otimização: Aumentar a altura 'h' reduzirá severamente o custo da obra.*")
            
            # Escolha Otimizada de Bitolas
            st.markdown("### 🎯 Otimização de Bitolas (Menor Custo)")
            num_inf, phi_inf, area_inf = otimizar_bitola(As_inf, bw)
            st.write(rf"**Armadura Inferior (Tração):** Requerido {As_inf:.2f} cm²")
            st.success(rf"👉 Adotar: **{num_inf} barras de $\phi$ {phi_inf} mm** (Área real: {area_inf:.2f} cm²)")
            
            if tem_armadura_dupla:
                num_sup, phi_sup, area_sup = otimizar_bitola(As_sup, bw)
                st.write(rf"**Armadura Superior (Compressão):** Requerido {As_sup:.2f} cm²")
                st.success(rf"👉 Adotar: **{num_sup} barras de $\phi$ {phi_sup} mm** (Área real: {area_sup:.2f} cm²)")
                
            st.pyplot(plot_viga_dominios(bw, h, d, x_ln, As_sup))
            st.pyplot(plot_viga_elevacao(L, h, tem_armadura_dupla))

st.sidebar.title("Navegação")
modulo = st.sidebar.radio("Selecione:", ["1. Vigas Otimizadas"])
if "1." in modulo: modulo_vigas()