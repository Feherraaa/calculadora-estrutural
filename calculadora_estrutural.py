import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# CONFIGURAÇÃO DE PÁGINA E ESTÉTICA (HFF)
# ==========================================
st.set_page_config(page_title="HFF - Arquitetura e Urbanismo", layout="wide", initial_sidebar_state="collapsed")

# 🎨 PALETA DE CORES (Minimalismo Arquitetônico)
# Se quiser adicionar uma cor da sua logo, troque o #555555 (Cinza) pelo HEX da sua cor!
st.markdown("""
<style>
    /* Cor de Fundo da Barra Lateral (Grafite Escuro) */
    [data-testid="stSidebar"] {
        background-color: #111111;
    }
    /* Cor dos Textos da Barra Lateral (Branco/Gelo) */
    [data-testid="stSidebar"] * {
        color: #E5E5E5 !important;
    }
    /* Estilização dos Botões Principais */
    .stButton>button {
        background-color: #111111;
        color: #FFFFFF;
        border: 1px solid #555555;
        border-radius: 4px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #333333;
        color: #FFFFFF;
        border: 1px solid #FFFFFF;
    }
    /* Títulos Principais */
    h1, h2 { color: #111111 !important; }
    h3 { color: #555555 !important; }
</style>
""", unsafe_allow_html=True)

codigo_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HFF - Arquitetura e Urbanismo</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .hidden { display: none; }
        .nav-btn { cursor: pointer; transition: all 0.2s ease-in-out; }
        .nav-btn:hover { background-color: #222222; color: #FFFFFF; }
        .active-nav { background-color: #222222; color: #FFFFFF; border-left: 4px solid #888888; font-weight: 600; }
        details > summary { list-style: none; cursor: pointer; }
        details > summary::-webkit-details-marker { display: none; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #333333; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #888888; }
    </style>
</head>
<body class="bg-slate-50 font-sans flex h-screen overflow-hidden text-slate-800">

    <aside class="w-64 bg-[#111111] border-r border-[#222222] flex flex-col h-full z-10 shadow-2xl">
        <div class="p-6 border-b border-[#222222] flex flex-col items-center justify-center bg-[#0A0A0A] min-h-[120px]">
            <img src="image_d804c5.png" alt="Logo HFF" class="w-32 drop-shadow-md mb-2" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
            <h1 style="display:none;" class="text-3xl font-black tracking-widest text-white text-center">HFF</h1>
            <p class="text-[10px] text-gray-400 tracking-widest uppercase mt-2">Arquitetura & Urbanismo</p>
        </div>

        <nav class="flex-1 mt-4 overflow-y-auto">
            <ul class="space-y-1">
                <li onclick="showModule('mod-materiais', this)" class="nav-btn active-nav block px-6 py-3 text-sm text-slate-300">Orçamentação (ERP)</li>
                <li onclick="showModule('mod-cargas', this)" class="nav-btn block px-6 py-3 text-sm text-slate-400">Descida de Cargas</li>
            </ul>
        </nav>

        <div class="p-5 bg-[#0A0A0A] border-t border-[#222222]">
            <h4 class="text-gray-300 text-xs font-bold uppercase tracking-wider mb-3 flex items-center"><span class="mr-2">📐</span> Normas & Ref</h4>
            <ul class="text-[11px] text-slate-500 space-y-2 leading-tight">
                <li>• <strong class="text-slate-400">NBR 6118:</strong> Estruturas de Concreto</li>
                <li>• <strong class="text-slate-400">NBR 6120:</strong> Cargas para Cálculo</li>
                <li>• <strong class="text-slate-400">NBR 8800:</strong> Estruturas de Aço / FLT</li>
                <li>• <strong class="text-slate-400">Eurocode 4:</strong> Vigas Mistas</li>
            </ul>
        </div>
    </aside>

    <main class="flex-1 h-full overflow-y-auto p-8 lg:px-12 xl:px-20">

        <section id="mod-materiais" class="module-section max-w-5xl mx-auto">
            <div class="mb-8 border-b-2 border-gray-300 pb-4">
                <h2 class="text-3xl font-extrabold text-[#111111] tracking-tight">Levantamento de Materiais</h2>
                <p class="text-slate-500 mt-2">Gestão de insumos e quantitativos precisos para o canteiro de obras.</p>
            </div>
            
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 mb-8 overflow-hidden">
                <div class="bg-slate-50 p-6 border-b border-slate-200 flex flex-wrap gap-6 items-center">
                    <span class="text-sm font-semibold text-[#111111] uppercase tracking-wider">Calcular:</span>
                    <label class="flex items-center cursor-pointer">
                        <input type="checkbox" id="chk_alv" checked onchange="toggleSection('sec_alv', this.checked)" class="form-checkbox h-5 w-5 text-gray-800 rounded border-slate-300">
                        <span class="ml-2 text-slate-700 font-medium">Alvenaria</span>
                    </label>
                    <label class="flex items-center cursor-pointer">
                        <input type="checkbox" id="chk_fund" checked onchange="toggleSection('sec_fund', this.checked)" class="form-checkbox h-5 w-5 text-gray-800 rounded border-slate-300">
                        <span class="ml-2 text-slate-700 font-medium">Fundações</span>
                    </label>
                    <label class="flex items-center cursor-pointer">
                        <input type="checkbox" id="chk_sup" checked onchange="toggleSection('sec_sup', this.checked)" class="form-checkbox h-5 w-5 text-gray-800 rounded border-slate-300">
                        <span class="ml-2 text-slate-700 font-medium">Pilares e Vigas</span>
                    </label>
                </div>

                <div class="p-6 space-y-8">
                    <div id="sec_alv" class="space-y-4">
                        <h3 class="text-lg font-bold text-[#111111] flex items-center"><span class="text-xl mr-2">🧱</span> Dimensões da Alvenaria</h3>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div><label class="block text-xs font-semibold text-slate-500 mb-1">Pé-direito (m)</label><input type="number" id="m_pd" value="2.8" class="w-full bg-slate-50 border border-slate-200 p-2.5 rounded-lg outline-none focus:border-gray-500"></div>
                            <div><label class="block text-xs font-semibold text-slate-500 mb-1">Parede 1 Vez (Metro Linear)</label><input type="number" id="m_ml_1v" value="20.0" class="w-full bg-slate-50 border border-slate-200 p-2.5 rounded-lg outline-none focus:border-gray-500"></div>
                            <div><label class="block text-xs font-semibold text-slate-500 mb-1">Parede Meia Vez (Metro Linear)</label><input type="number" id="m_ml_mv" value="50.0" class="w-full bg-slate-50 border border-slate-200 p-2.5 rounded-lg outline-none focus:border-gray-500"></div>
                        </div>
                    </div>

                    <div id="sec_fund" class="space-y-4 border-t border-slate-100 pt-6">
                        <h3 class="text-lg font-bold text-[#111111] flex items-center"><span class="text-xl mr-2">🕳️</span> Geometria das Estacas</h3>
                        <div class="grid grid-cols-2 md:grid-cols-6 gap-4">
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Quantidade</label><input type="number" id="e_qtd" value="20" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Diâmetro (cm)</label><input type="number" id="e_diam" value="25.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Profund. (m)</label><input type="number" id="e_prof" value="6.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Qtd Aço Long.</label><input type="number" id="e_qtd_long" value="4" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Esp. Estribo (cm)</label><input type="number" id="e_esp_est" value="15.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Cobrimento (cm)</label><input type="number" id="e_cob" value="4.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                            <input type="hidden" id="e_transp" value="40.0">
                        </div>
                    </div>

                    <div id="sec_sup" class="space-y-6 border-t border-slate-100 pt-6">
                        <h3 class="text-lg font-bold text-[#111111] flex items-center"><span class="text-xl mr-2">🏛️</span> Superestrutura</h3>
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            <div class="bg-white border-l-4 border-[#111111] rounded-r-xl p-5 shadow-sm bg-slate-50/50">
                                <h4 class="font-bold text-[#111111] mb-3">Pilares</h4>
                                <div class="grid grid-cols-3 gap-3 mb-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd</label><input type="number" id="p_qtd" value="12" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Comp. (m)</label><input type="number" id="p_comp" value="3.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Seção b x h(cm)</label><input type="text" id="p_sec" value="15,30" class="w-full bg-white border border-slate-200 p-2 rounded-lg text-center" title="ex: 15,30"></div>
                                </div>
                                <div class="grid grid-cols-3 gap-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd Aço Long.</label><input type="number" id="p_qtd_long" value="4" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Esp. Estribo (cm)</label><input type="number" id="p_esp_est" value="15.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Cobrimento (cm)</label><input type="number" id="p_cob" value="3.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <input type="hidden" id="p_transp" value="40.0">
                                </div>
                            </div>
                            <div class="bg-white border-l-4 border-gray-400 rounded-r-xl p-5 shadow-sm bg-slate-50/50">
                                <h4 class="font-bold text-gray-700 mb-3">Vigas</h4>
                                <div class="grid grid-cols-3 gap-3 mb-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd</label><input type="number" id="v_qtd" value="15" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Comp. Médio (m)</label><input type="number" id="v_comp" value="4.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Seção bw x h(cm)</label><input type="text" id="v_sec" value="15,40" class="w-full bg-white border border-slate-200 p-2 rounded-lg text-center" title="ex: 15,40"></div>
                                </div>
                                <div class="grid grid-cols-3 gap-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd Aço Long.</label><input type="number" id="v_qtd_long" value="4" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Esp. Estribo (cm)</label><input type="number" id="v_esp_est" value="15.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Cobrimento (cm)</label><input type="number" id="v_cob" value="3.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none focus:border-gray-500"></div>
                                    <input type="hidden" id="v_transp" value="20.0">
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <details class="bg-slate-50 rounded-xl border border-slate-200 group transition-all">
                        <summary class="flex justify-between items-center font-semibold p-4 text-[#111111] hover:text-gray-500 cursor-pointer">
                            <span class="flex items-center"><span class="text-xl mr-2">⚙️</span> Configurações Avançadas (Preços e Traços)</span>
                            <span class="transition group-open:rotate-180">▼</span>
                        </summary>
                        <div class="p-6 border-t border-slate-200 space-y-6">
                            
                            <div class="flex gap-8 border-b pb-4 border-slate-200">
                                <div>
                                    <label class="block text-xs font-bold text-slate-500 mb-2 uppercase">Aço Comercial</label>
                                    <select id="cfg_barra" class="bg-white border border-slate-300 p-2 rounded text-sm outline-none focus:border-gray-500">
                                        <option value="12">Barras de 12 metros</option>
                                        <option value="6">Barras de 6 metros</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-bold text-slate-500 mb-2 uppercase">Preparo do Concreto</label>
                                    <select id="tipo_concreto" onchange="toggleConcreto(this.value)" class="bg-white border border-slate-300 p-2 rounded text-sm outline-none focus:border-gray-500">
                                        <option value="virado">Virado na Obra</option>
                                        <option value="usinado">Usinado (Concreteira)</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <h4 class="text-sm font-bold text-[#111111] mb-3">Traços Volumétricos (Cim : Cal : Ar)</h4>
                                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                                    <div class="bg-white p-3 rounded border border-slate-200">
                                        <span class="text-[11px] text-slate-400 block mb-2 font-bold">Assentamento</span>
                                        <div class="flex space-x-1"><input type="number" id="a_cim" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="a_cal" value="0.5" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="a_ar" value="6.0" class="w-full text-center border rounded p-1 text-sm"></div>
                                    </div>
                                    <div class="bg-white p-3 rounded border border-slate-200">
                                        <span class="text-[11px] text-slate-400 block mb-2 font-bold">Reboco</span>
                                        <div class="flex space-x-1"><input type="number" id="r_cim" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="r_cal" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="r_ar" value="6.0" class="w-full text-center border rounded p-1 text-sm"></div>
                                    </div>
                                    <div class="bg-white p-3 rounded border border-slate-200">
                                        <span class="text-[11px] text-slate-400 block mb-2 font-bold">Chapisco</span>
                                        <div class="flex space-x-1"><input type="number" id="c_cim" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="c_cal" value="0.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="c_ar" value="3.0" class="w-full text-center border rounded p-1 text-sm"></div>
                                    </div>
                                    <div id="box-concreto-obra" class="bg-white p-3 rounded border border-slate-200 border-l-2 border-l-gray-800">
                                        <span class="text-[11px] text-[#111111] block mb-2 font-bold">Concreto (Cim : Ar : Br)</span>
                                        <div class="flex space-x-1"><input type="number" id="co_cim" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="co_ar" value="2.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="co_br" value="3.0" class="w-full text-center border rounded p-1 text-sm"></div>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <h4 class="text-sm font-bold text-[#111111] mb-3">Tabela de Preços Unitários (R$)</h4>
                                <div class="grid grid-cols-4 lg:grid-cols-8 gap-3">
                                    <div><label class="text-[10px] text-slate-500">Tijolo 1V</label><input type="number" id="pr_t1v" value="1.20" step="0.1" class="w-full border p-1 rounded text-sm text-center focus:border-gray-500 outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Tijolo MV</label><input type="number" id="pr_tmv" value="0.80" step="0.1" class="w-full border p-1 rounded text-sm text-center focus:border-gray-500 outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Cim 50kg</label><input type="number" id="pr_cim" value="35.00" class="w-full border p-1 rounded text-sm text-center focus:border-gray-500 outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Cal 20kg</label><input type="number" id="pr_cal" value="15.00" class="w-full border p-1 rounded text-sm text-center focus:border-gray-500 outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Areia m³</label><input type="number" id="pr_ar" value="120.00" class="w-full border p-1 rounded text-sm text-center focus:border-gray-500 outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Brita m³</label><input type="number" id="pr_br" value="110.00" class="w-full border p-1 rounded text-sm text-center focus:border-gray-500 outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Aço Fino</label><input type="number" id="pr_af" value="25.00" class="w-full border p-1 rounded text-sm text-center focus:border-gray-500 outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Aço Gros</label><input type="number" id="pr_ag" value="60.00" class="w-full border p-1 rounded text-sm text-center focus:border-gray-500 outline-none"></div>
                                </div>
                                <div id="preco_usinado_box" class="hidden mt-3 w-1/4">
                                    <label class="text-[10px] text-gray-800 font-bold">Preço Concreto Usinado (m³)</label>
                                    <input type="number" id="pr_conc" value="450.00" class="w-full border p-1 rounded text-sm text-center border-gray-400 outline-none">
                                </div>
                            </div>
                        </div>
                    </details>
                </div>
                
                <div class="bg-slate-50 p-6 border-t border-slate-200">
                    <button onclick="processarERP()" class="w-full md:w-auto px-10 py-4 bg-[#111111] hover:bg-[#333333] text-white border border-[#555555] font-bold rounded-xl shadow-md transition-all text-lg flex items-center justify-center mx-auto">
                        📄 Gerar Relatório e Orçamento
                    </button>
                </div>
            </div>

            <div id="res-erp" class="hidden">
                <h3 class="text-2xl font-bold text-[#111111] mb-6">Orçamento - HFF Arquitetura e Urbanismo</h3>
                <div class="bg-white rounded-xl shadow-sm border border-gray-300 overflow-hidden">
                    <table class="min-w-full divide-y divide-slate-200">
                        <thead class="bg-[#111111] text-gray-200">
                            <tr>
                                <th class="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">Material</th>
                                <th class="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider">Qtd Necessária</th>
                                <th class="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider">Custo (R$)</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-slate-100 text-sm text-slate-700" id="tabela-orcamento"></tbody>
                        <tfoot class="bg-[#f3f4f6] text-gray-800 border-t-2 border-gray-300">
                            <tr>
                                <td colspan="2" class="px-6 py-5 text-right font-semibold">Custo Total Estimado:</td>
                                <td class="px-6 py-5 text-right font-black text-2xl text-[#111111]" id="out-custo-total">R$ 0,00</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>

                <details class="mt-6 text-sm text-slate-500">
                    <summary class="cursor-pointer hover:text-gray-800">Ver detalhamento de cálculo (Metragens e Volumes)</summary>
                    <div class="p-4 bg-white border rounded mt-2 grid grid-cols-2 md:grid-cols-4 gap-4" id="detalhes_finais"></div>
                </details>
            </div>
        </section>

        <section id="mod-cargas" class="module-section hidden max-w-3xl mx-auto">
            <h2 class="text-3xl font-extrabold text-[#111111] mb-8 border-b-2 border-gray-300 pb-2">Descida de Cargas</h2>
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <label class="block text-sm text-slate-600 mb-1">Área da Planta (m²)</label>
                <input type="number" id="c_area" value="100" class="w-full border p-2.5 rounded-lg mb-4 bg-slate-50 outline-none">
                <label class="block text-sm text-slate-600 mb-1">Qtd Pilares</label>
                <input type="number" id="c_pilares" value="8" class="w-full border p-2.5 rounded-lg mb-6 bg-slate-50 outline-none">
                <button onclick="calcCargas()" class="w-full bg-[#111111] text-white font-bold py-3 rounded-lg border border-[#555555] hover:bg-[#333333] transition">Calcular</button>
                <div id="res-cargas" class="mt-6 p-4 bg-[#111111] border border-[#555555] rounded-lg hidden">
                    <p class="text-sm text-slate-300">Carga Axial (Nk) p/ Pilar:</p>
                    <p class="text-3xl font-bold text-white" id="out-nk"></p>
                </div>
            </div>
        </section>

    </main>

    <script>
        function showModule(moduleId, element) {
            document.querySelectorAll('.module-section').forEach(el => el.classList.add('hidden'));
            document.getElementById(moduleId).classList.remove('hidden');
            document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active-nav'));
            element.classList.add('active-nav');
        }

        function toggleSection(secId, isChecked) {
            const el = document.getElementById(secId);
            if(isChecked) { el.classList.remove('hidden'); } else { el.classList.add('hidden'); }
        }

        function toggleConcreto(tipo) {
            if(tipo === 'usinado') { document.getElementById('box-concreto-obra').classList.add('opacity-50'); } 
            else { document.getElementById('box-concreto-obra').classList.remove('opacity-50'); }
        }

        function processarERP() {
            const c_alv = document.getElementById('chk_alv').checked;
            const c_fund = document.getElementById('chk_fund').checked;
            const c_sup = document.getElementById('chk_sup').checked;
            const t_conc = document.getElementById('tipo_concreto').value;
            const comp_barra = parseFloat(document.getElementById('cfg_barra').value);

            let tot_cim = 0, tot_cal = 0, tot_ar = 0, tot_br = 0;
            let qtd_1v = 0, qtd_mv = 0, vol_conc = 0, m_est = 0, m_long = 0;

            function calcTraco(vol, cim, cal, ar) {
                if(vol<=0 || ar==0) return {c:0, k:0, a:0};
                let vp = vol / ar;
                return { c: Math.ceil((vp*cim)/0.036), k: Math.ceil((vp*cal)/0.036), a: vol };
            }

            if(c_alv) {
                let a1 = parseFloat(document.getElementById('m_ml_1v').value) * parseFloat(document.getElementById('m_pd').value);
                let am = parseFloat(document.getElementById('m_ml_mv').value) * parseFloat(document.getElementById('m_pd').value);
                qtd_1v = Math.ceil(a1 * 38.45);
                qtd_mv = Math.ceil(am * 25.0);
                let rA = calcTraco((a1*0.03)+(am*0.015), parseFloat(document.getElementById('a_cim').value), parseFloat(document.getElementById('a_cal').value), parseFloat(document.getElementById('a_ar').value));
                let rC = calcTraco((a1+am)*2*0.005, parseFloat(document.getElementById('c_cim').value), parseFloat(document.getElementById('c_cal').value), parseFloat(document.getElementById('c_ar').value));
                let rR = calcTraco((a1+am)*2*0.02, parseFloat(document.getElementById('r_cim').value), parseFloat(document.getElementById('r_cal').value), parseFloat(document.getElementById('r_ar').value));
                tot_cim += rA.c + rC.c + rR.c; tot_cal += rA.k + rC.k + rR.k; tot_ar += rA.a + rC.a + rR.a;
            }

            if(c_fund) {
                let q = parseFloat(document.getElementById('e_qtd').value), d = parseFloat(document.getElementById('e_diam').value)/100, prof = parseFloat(document.getElementById('e_prof').value);
                let cob = parseFloat(document.getElementById('e_cob').value)/100, esp = parseFloat(document.getElementById('e_esp_est').value)/100;
                vol_conc += q * (Math.PI * Math.pow(d/2, 2)) * prof;
                m_est += ((Math.PI * (d - 2*cob)) + 0.8) * Math.ceil(prof/esp) * q;
                m_long += (prof + 0.4) * parseFloat(document.getElementById('e_qtd_long').value) * q;
            }

            if(c_sup) {
                let pq = parseFloat(document.getElementById('p_qtd').value), pc = parseFloat(document.getElementById('p_comp').value);
                let [pb, ph] = document.getElementById('p_sec').value.split(',').map(x => parseFloat(x)/100);
                vol_conc += pq * pb * ph * pc;
                m_est += (2*(pb-0.06) + 2*(ph-0.06) + 0.8) * Math.ceil(pc/0.15) * pq;
                m_long += (pc + 0.4) * parseFloat(document.getElementById('p_qtd_long').value) * pq;

                let vq = parseFloat(document.getElementById('v_qtd').value), vc = parseFloat(document.getElementById('v_comp').value);
                let [vb, vh] = document.getElementById('v_sec').value.split(',').map(x => parseFloat(x)/100);
                vol_conc += vq * vb * vh * vc;
                m_est += (2*(vb-0.06) + 2*(vh-0.06) + 0.4) * Math.ceil(vc/0.15) * vq;
                m_long += (vc + 0.2) * parseFloat(document.getElementById('v_qtd_long').value) * vq;
            }

            let b_f = Math.ceil(m_est/comp_barra) || 0;
            let b_g = Math.ceil(m_long/comp_barra) || 0;

            if(t_conc === 'virado' && vol_conc > 0) {
                let vs = vol_conc * 1.5;
                let c = parseFloat(document.getElementById('co_cim').value), a = parseFloat(document.getElementById('co_ar').value), b = parseFloat(document.getElementById('co_br').value);
                let vp = vs / (c + a + b);
                tot_cim += Math.ceil((vp*c)/0.036); tot_ar += vp*a; tot_br += vp*b;
            }

            let custo = 0; let tb = document.getElementById('tabela-orcamento'); tb.innerHTML = '';
            function addR(nome, qtd, un, preco) {
                if(qtd > 0) {
                    let cst = qtd * preco; custo += cst;
                    tb.innerHTML += `<tr class="border-b border-slate-100"><td class="px-6 py-3 font-medium">${nome}</td><td class="px-6 py-3 text-right">${qtd.toLocaleString('pt-BR',{maximumFractionDigits:2})} ${un}</td><td class="px-6 py-3 text-right font-semibold">R$ ${cst.toLocaleString('pt-BR',{minimumFractionDigits:2})}</td></tr>`;
                }
            }

            addR('Tijolo 1 Vez', qtd_1v, 'un', parseFloat(document.getElementById('pr_t1v').value));
            addR('Tijolo Meia Vez', qtd_mv, 'un', parseFloat(document.getElementById('pr_tmv').value));
            addR('Cimento (50kg)', tot_cim, 'sacos', parseFloat(document.getElementById('pr_cim').value));
            addR('Cal (20kg)', tot_cal, 'sacos', parseFloat(document.getElementById('pr_cal').value));
            addR('Areia', tot_ar, 'm³', parseFloat(document.getElementById('pr_ar').value));
            addR('Brita', tot_br, 'm³', parseFloat(document.getElementById('pr_br').value));
            addR(`Aço Fino (${comp_barra}m)`, b_f, 'barras', parseFloat(document.getElementById('pr_af').value));
            addR(`Aço Grosso (${comp_barra}m)`, b_g, 'barras', parseFloat(document.getElementById('pr_ag').value));

            if(t_conc === 'usinado' && vol_conc > 0) {
                addR('Concreto Usinado', vol_conc, 'm³', parseFloat(document.getElementById('pr_conc').value));
            }

            document.getElementById('out-custo-total').innerText = `R$ ${custo.toLocaleString('pt-BR',{minimumFractionDigits:2})}`;
            document.getElementById('detalhes_finais').innerHTML = `
                <div><span class="block text-xs">Vol Concreto Total</span><strong>${vol_conc.toFixed(2)} m³</strong></div>
                <div><span class="block text-xs">Metragem Estribos</span><strong>${m_estribos.toFixed(2)} m</strong></div>
                <div><span class="block text-xs">Metragem Longit.</span><strong>${m_longit.toFixed(2)} m</strong></div>
            `;
            document.getElementById('res-erp').classList.remove('hidden');
        }

        function calcCargas() {
            let a = parseFloat(document.getElementById('c_area').value);
            let p = parseInt(document.getElementById('c_pilares').value);
            document.getElementById('out-nk').innerText = (((a * 7) / p) * 1.15).toFixed(2) + ' kN';
            document.getElementById('res-cargas').classList.remove('hidden');
        }
    </script>
</body>
</html>
"""

# Renderiza o HTML no Streamlit ocupando a altura total
components.html(codigo_html, height=900, scrolling=True)

# Restaura as funções analíticas completas para quem desejar usar no backend:
st.sidebar.markdown("---")
modulo_backend = st.sidebar.selectbox("Funções Avançadas (Módulos 1 a 5)", ["Selecione...", "Módulo 1: Vigas", "Módulo 2: Pilares", "Módulo 3: Lajes Maciças", "Módulo 4: Lajes Nervuradas", "Módulo 5: Estruturas Metálicas (FLT)"])

if modulo_backend == "Módulo 1: Vigas":
    st.markdown("---")
    st.title("Módulo 1: Vigas CA")
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

elif modulo_backend == "Módulo 2: Pilares":
    st.markdown("---")
    st.title("Módulo 2: Pilares CA")
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

elif modulo_backend == "Módulo 5: Estruturas Metálicas (FLT)":
    st.markdown("---")
    st.title("Módulo 5: Metálicas (FLT)")
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
        if st.button("Calcular Resistência Aço"):
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