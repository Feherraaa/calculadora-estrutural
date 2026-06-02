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
        angulos = np.linspace(0, 2*np.pi, num_barras, endpoint=False)
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

def plot_secao_mista(d, bf, tw, tf, tc, beff, pna_y):
    """Gera o desenho da Viga Mista Aço-Concreto com a Linha Neutra Plástica"""
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Perfil de Aço I
    ax.add_patch(patches.Rectangle((-tw/2, 0), tw, d, fill=True, color='slategray', label='Perfil de Aço')) # Alma
    ax.add_patch(patches.Rectangle((-bf/2, 0), bf, tf, fill=True, color='slategray')) # Mesa Inferior
    ax.add_patch(patches.Rectangle((-bf/2, d-tf), bf, tf, fill=True, color='slategray')) # Mesa Superior
    
    # Laje de Concreto
    ax.add_patch(patches.Rectangle((-beff/2, d), beff, tc, fill=True, color='lightgray', hatch='//', label='Laje de Concreto Colaborante'))
    
    # Linha Neutra Plástica (PNA)
    ax.axhline(pna_y, color='red', linestyle='--', lw=2.5, label=rf'L.N. Plástica (y={pna_y:.1f} cm)')
    
    # Zonas de Compressão/Tração Visuais
    if pna_y > d: # PNA na laje
        ax.add_patch(patches.Rectangle((-beff/2, pna_y), beff, (d+tc)-pna_y, color='red', alpha=0.2, label='Zona Comprimida'))
    else: # PNA no perfil de aço
        ax.add_patch(patches.Rectangle((-beff/2, d), beff, tc, color='red', alpha=0.2, label='Zona Comprimida'))
        ax.add_patch(patches.Rectangle((-bf/2, pna_y), bf, d-pna_y, color='red', alpha=0.2))
        
    ax.set_xlim(-beff/2 - 5, beff/2 + 5)
    ax.set_ylim(-5, d + tc + 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Seção Transversal - Viga Mista (Eurocode 4)", fontsize=10)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=8)
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
            st.success(rf"Aço Inferior (Tração): **{num_inf} barras de $\phi$ {phi_inf} mm**")
            if tem_dupla:
                num_sup, phi_sup, a_sup = otimizar_bitola(As_sup, bw, min_barras=2)
                st.warning(rf"🚨 Armadura Dupla Requerida! Aço Superior: **{num_sup} barras de $\phi$ {phi_sup} mm**")
            
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
            if a_real > As_max: st.error("🚨 Seção Subdimensionada! O aço estrapolou os 8% permitidos.")
            else: st.success(rf"✅ Adotar: **{num_b} barras de $\phi$ {phi_b} mm** (Área: {a_real:.2f} cm²)")
            st.pyplot(plot_pilar_detalhe(formato, b, h_p, num_b))

def modulo_metalicas_mistas():
    st.header("Módulo 5: Estruturas Metálicas e Vigas Mistas")
    st.markdown("---")
    st.info("💡 **Referências Normativas:** ABNT NBR 8800, NBR 5884, Manuais CBCA e Eurocode 4.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Geometria do Perfil de Aço (Catálogo)")
        tipo_perfil = st.selectbox("Tipo de Perfil", ["Perfil I Laminado/Soldado", "Perfil U Laminado"])
        d_aco = st.number_input("Altura do Perfil d (cm)", min_value=5.0, value=25.0)
        bf_aco = st.number_input("Largura da Mesa bf (cm)", min_value=5.0, value=12.5)
        tw_aco = st.number_input("Espessura da Alma tw (mm)", min_value=2.0, value=6.3) / 10 # Convertido para cm
        tf_aco = st.number_input("Espessura da Mesa tf (mm)", min_value=2.0, value=9.5) / 10 # Convertido para cm
        
        aco_fy = st.selectbox("Tensão de Escoamento do Aço fy", ["ASTM A36 (250 MPa)", "ASTM A572 (345 MPa)"])
        fy = 25.0 if "250" in aco_fy else 34.5 # kN/cm²
        
        st.subheader("Integração com Laje de Concreto (Viga Mista)")
        viga_mista = st.checkbox("Considerar trabalho conjunto com a Laje (Viga Mista)?")
        
        if viga_mista:
            tc_concreto = st.number_input("Espessura da Laje tc (cm)", min_value=5.0, value=10.0)
            beff_concreto = st.number_input("Largura Efetiva da Laje beff (cm)", min_value=30.0, value=150.0)
            fck_misto = st.number_input("fck do Concreto da Laje (MPa)", min_value=20.0, value=25.0)

    with col2:
        st.subheader("Propriedades e Momentos Resistentes")
        if st.button("Calcular Resistência Metálica / Mista"):
            # 1. Propriedades Geométricas do Perfil de Aço Nu
            Area_aco = 2 * (bf_aco * tf_aco) + (d_aco - 2*tf_aco) * tw_aco
            
            st.write(rf"- Área da Seção de Aço ($A_a$): **{Area_aco:.2f} cm²**")
            
            # Resistência à Tração / Compressão do perfil
            Rs = Area_aco * (fy / 1.10) # kN (Força plástica do aço)
            
            if not viga_mista:
                # Perfil Isolado (Apenas Aço)
                # Cálculo do Módulo Plástico Zx (Simplificado para Perfil I simétrico)
                Zx = (bf_aco * tf_aco) * (d_aco - tf_aco) + (tw_aco * (d_aco - 2*tf_aco)**2) / 4
                Mpl_Rd = (Zx * fy) / 1.10 # kN.cm
                
                st.success(rf"Momento Fletor Plástico Resistente ($M_{{pl,Rd}}$): **{Mpl_Rd/100:.2f} kN.m**")
                st.caption("Nota: Cálculo base para perfil 100% contido lateralmente (sem flambagem lateral com torção - FLT).")
                
            else:
                # Viga Mista (Aço + Concreto) - Análise Plástica (Eurocode 4 / CBCA)
                fcd = (fck_misto / 1.4) / 10 # kN/cm²
                
                # Capacidade Máxima de Compressão da Laje
                Rc = 0.85 * fcd * beff_concreto * tc_concreto # kN
                
                st.write(rf"- Força Plástica do Aço ($R_s$): **{Rs:.2f} kN**")
                st.write(rf"- Capacidade da Laje de Concreto ($R_c$): **{Rc:.2f} kN**")
                
                # Posição da Linha Neutra Plástica (PNA)
                if Rc >= Rs:
                    # Linha neutra está dentro da laje de concreto
                    a_comp = Rs / (0.85 * fcd * beff_concreto) # Profundidade comprimida do concreto
                    pna_y = d_aco + tc_concreto - a_comp # Y a partir da base do perfil
                    
                    z = (d_aco / 2) + tc_concreto - (a_comp / 2) # Braço de alavanca
                    M_misto_Rd = Rs * z # kN.cm
                    
                    st.info("PNA (Linha Neutra Plástica) localizada na **Laje de Concreto**.")
                else:
                    # Linha neutra está no perfil de aço (Laje 100% comprimida)
                    # Força que precisa ser equilibrada pelo aço comprimido
                    Ra_comp = (Rs - Rc) / 2
                    
                    # Verifica se o PNA está na mesa superior do aço ou na alma
                    R_mesa_sup = (bf_aco * tf_aco) * (fy / 1.10)
                    if Ra_comp <= R_mesa_sup:
                        st.info("PNA (Linha Neutra Plástica) localizada na **Mesa Superior de Aço**.")
                        y_pna_from_top = Ra_comp / (bf_aco * (fy/1.10))
                        pna_y = d_aco - y_pna_from_top
                    else:
                        st.info("PNA (Linha Neutra Plástica) localizada na **Alma de Aço**.")
                        R_alma = Ra_comp - R_mesa_sup
                        y_alma_from_top = R_alma / (tw_aco * (fy/1.10))
                        pna_y = d_aco - tf_aco - y_alma_from_top
                        
                    # Para simplificação robusta na calculadora, usamos limite conservador de momento misto
                    z_approx = (d_aco / 2) + (tc_concreto / 2)
                    M_misto_Rd = Rc * z_approx + (Rs - Rc) * (d_aco/4) # Estimativa segura
                    
                st.success(rf"Momento Plástico Resistente da Viga Mista ($M_{{pl,Rd}}$): **{M_misto_Rd/100:.2f} kN.m**")
                st.pyplot(plot_secao_mista(d_aco, bf_aco, tw_aco, tf_aco, tc_concreto, beff_concreto, pna_y))

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

# ==========================================
# MENU LATERAL E NAVEGAÇÃO
# ==========================================
st.sidebar.title("Navegação do Edifício")
modulo = st.sidebar.radio("Selecione o Componente:", [
    "0. Cargas (NBR 6120)", 
    "1. Vigas CA (Flexão/Cortante)", 
    "2. Pilares CA (Variantes)", 
    "3. Lajes Maciças", 
    "4. Lajes Treliçadas",
    "5. Metálicas e Vigas Mistas"
])

if "0." in modulo: modulo_cargas()
elif "1." in modulo: modulo_vigas()
elif "2." in modulo: modulo_pilares()
elif "3." in modulo: modulo_lajes()
elif "4." in modulo: modulo_laje_trelicada()
else: modulo_metalicas_mistas()