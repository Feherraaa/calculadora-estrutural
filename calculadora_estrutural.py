import streamlit as st
import streamlit.components.v1 as components

# Configuração da página para ocupar a tela toda
st.set_page_config(page_title="HFF - Plataforma Estrutural", layout="wide", initial_sidebar_state="collapsed")

# Aqui "embrulhamos" o nosso site HTML dentro do Python
codigo_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HFF - Plataforma de Engenharia</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .hidden { display: none; }
        .nav-btn { cursor: pointer; transition: all 0.2s ease-in-out; }
        .nav-btn:hover { background-color: #112240; color: #C5A059; }
        .active-nav { background-color: #112240; color: #C5A059; border-left: 4px solid #C5A059; font-weight: 600; }
        details > summary { list-style: none; cursor: pointer; }
        details > summary::-webkit-details-marker { display: none; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #1A2E4C; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #C5A059; }
    </style>
</head>
<body class="bg-slate-50 font-sans flex h-screen overflow-hidden text-slate-800">

    <aside class="w-64 bg-[#0A192F] border-r border-[#1A2E4C] flex flex-col h-full z-10 shadow-2xl">
        <div class="p-6 border-b border-[#1A2E4C] flex flex-col items-center justify-center bg-[#071324] min-h-[120px]">
            <img src="image_d8ed05.png" alt="Logo HFF" class="w-40 drop-shadow-lg" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
            <h1 style="display:none;" class="text-3xl font-black tracking-widest text-[#C5A059] text-center">HFF</h1>
        </div>

        <nav class="flex-1 mt-4 overflow-y-auto">
            <ul class="space-y-1">
                <li onclick="showModule('mod-materiais', this)" class="nav-btn active-nav block px-6 py-3 text-sm text-slate-300">Orçamentação (ERP)</li>
                <li onclick="showModule('mod-cargas', this)" class="nav-btn block px-6 py-3 text-sm text-slate-400">Descida de Cargas</li>
            </ul>
        </nav>

        <div class="p-5 bg-[#071324] border-t border-[#1A2E4C]">
            <h4 class="text-[#C5A059] text-xs font-bold uppercase tracking-wider mb-3 flex items-center"><span class="mr-2">📚</span> Referências</h4>
            <ul class="text-[11px] text-slate-400 space-y-2 leading-tight">
                <li>• <strong class="text-slate-300">NBR 6118:</strong> Estruturas de Concreto</li>
                <li>• <strong class="text-slate-300">NBR 6120:</strong> Cargas para Cálculo</li>
                <li>• <strong class="text-slate-300">NBR 8800:</strong> Estruturas de Aço / FLT</li>
                <li>• <strong class="text-slate-300">Eurocode 4:</strong> Vigas Mistas</li>
            </ul>
        </div>
    </aside>

    <main class="flex-1 h-full overflow-y-auto p-8 lg:px-12 xl:px-20">

        <section id="mod-materiais" class="module-section max-w-5xl mx-auto">
            <div class="mb-8 border-b-2 border-[#C5A059] pb-4">
                <h2 class="text-3xl font-extrabold text-[#0A192F] tracking-tight">Levantamento de Materiais</h2>
                <p class="text-slate-500 mt-2">Selecione as etapas da obra e preencha a geometria para gerar o orçamento.</p>
            </div>
            
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 mb-8 overflow-hidden">
                <div class="bg-slate-50 p-6 border-b border-slate-200 flex flex-wrap gap-6 items-center">
                    <span class="text-sm font-semibold text-[#0A192F] uppercase tracking-wider">Calcular:</span>
                    <label class="flex items-center cursor-pointer">
                        <input type="checkbox" id="chk_alv" checked onchange="toggleSection('sec_alv', this.checked)" class="form-checkbox h-5 w-5 text-[#C5A059] rounded border-slate-300">
                        <span class="ml-2 text-slate-700 font-medium">Alvenaria</span>
                    </label>
                    <label class="flex items-center cursor-pointer">
                        <input type="checkbox" id="chk_fund" checked onchange="toggleSection('sec_fund', this.checked)" class="form-checkbox h-5 w-5 text-[#C5A059] rounded border-slate-300">
                        <span class="ml-2 text-slate-700 font-medium">Fundações</span>
                    </label>
                    <label class="flex items-center cursor-pointer">
                        <input type="checkbox" id="chk_sup" checked onchange="toggleSection('sec_sup', this.checked)" class="form-checkbox h-5 w-5 text-[#C5A059] rounded border-slate-300">
                        <span class="ml-2 text-slate-700 font-medium">Pilares e Vigas</span>
                    </label>
                </div>

                <div class="p-6 space-y-8">
                    <div id="sec_alv" class="space-y-4">
                        <h3 class="text-lg font-bold text-[#0A192F] flex items-center"><span class="text-xl mr-2">🧱</span> Dimensões da Alvenaria</h3>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div><label class="block text-xs font-semibold text-slate-500 mb-1">Pé-direito (m)</label><input type="number" id="m_pd" value="2.8" class="w-full bg-slate-50 border border-slate-200 p-2.5 rounded-lg outline-none"></div>
                            <div><label class="block text-xs font-semibold text-slate-500 mb-1">Parede 1 Vez (Metro Linear)</label><input type="number" id="m_ml_1v" value="20.0" class="w-full bg-slate-50 border border-slate-200 p-2.5 rounded-lg outline-none"></div>
                            <div><label class="block text-xs font-semibold text-slate-500 mb-1">Parede Meia Vez (Metro Linear)</label><input type="number" id="m_ml_mv" value="50.0" class="w-full bg-slate-50 border border-slate-200 p-2.5 rounded-lg outline-none"></div>
                        </div>
                    </div>

                    <div id="sec_fund" class="space-y-4 border-t border-slate-100 pt-6">
                        <h3 class="text-lg font-bold text-[#0A192F] flex items-center"><span class="text-xl mr-2">🕳️</span> Geometria das Estacas</h3>
                        <div class="grid grid-cols-2 md:grid-cols-6 gap-4">
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Quantidade</label><input type="number" id="e_qtd" value="20" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Diâmetro (cm)</label><input type="number" id="e_diam" value="25.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Profund. (m)</label><input type="number" id="e_prof" value="6.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Qtd Aço Long.</label><input type="number" id="e_qtd_long" value="4" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Esp. Estribo (cm)</label><input type="number" id="e_esp_est" value="15.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Cobrimento (cm)</label><input type="number" id="e_cob" value="4.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none"></div>
                            <input type="hidden" id="e_transp" value="40.0">
                        </div>
                    </div>

                    <div id="sec_sup" class="space-y-6 border-t border-slate-100 pt-6">
                        <h3 class="text-lg font-bold text-[#0A192F] flex items-center"><span class="text-xl mr-2">🏛️</span> Superestrutura</h3>
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            <div class="bg-white border-l-4 border-[#0A192F] rounded-r-xl p-5 shadow-sm bg-slate-50/50">
                                <h4 class="font-bold text-[#0A192F] mb-3">Pilares</h4>
                                <div class="grid grid-cols-3 gap-3 mb-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd</label><input type="number" id="p_qtd" value="12" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Comp. (m)</label><input type="number" id="p_comp" value="3.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Seção b x h(cm)</label><input type="text" id="p_sec" value="15,30" class="w-full bg-white border border-slate-200 p-2 rounded-lg text-center" title="ex: 15,30"></div>
                                </div>
                                <div class="grid grid-cols-3 gap-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd Aço Long.</label><input type="number" id="p_qtd_long" value="4" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Esp. Estribo (cm)</label><input type="number" id="p_esp_est" value="15.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Cobrimento (cm)</label><input type="number" id="p_cob" value="3.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <input type="hidden" id="p_transp" value="40.0">
                                </div>
                            </div>

                            <div class="bg-white border-l-4 border-[#C5A059] rounded-r-xl p-5 shadow-sm bg-slate-50/50">
                                <h4 class="font-bold text-[#C5A059] mb-3">Vigas</h4>
                                <div class="grid grid-cols-3 gap-3 mb-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd</label><input type="number" id="v_qtd" value="15" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Comp. Médio (m)</label><input type="number" id="v_comp" value="4.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Seção bw x h(cm)</label><input type="text" id="v_sec" value="15,40" class="w-full bg-white border border-slate-200 p-2 rounded-lg text-center" title="ex: 15,40"></div>
                                </div>
                                <div class="grid grid-cols-3 gap-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd Aço Long.</label><input type="number" id="v_qtd_long" value="4" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Esp. Estribo (cm)</label><input type="number" id="v_esp_est" value="15.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Cobrimento (cm)</label><input type="number" id="v_cob" value="3.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg outline-none"></div>
                                    <input type="hidden" id="v_transp" value="20.0">
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <details class="bg-slate-50 rounded-xl border border-slate-200 group transition-all">
                        <summary class="flex justify-between items-center font-semibold p-4 text-[#0A192F] hover:text-[#C5A059] cursor-pointer">
                            <span class="flex items-center"><span class="text-xl mr-2">⚙️</span> Configurações Avançadas (Preços e Traços)</span>
                            <span class="transition group-open:rotate-180">▼</span>
                        </summary>
                        <div class="p-6 border-t border-slate-200 space-y-6">
                            
                            <div class="flex gap-8 border-b pb-4 border-slate-200">
                                <div>
                                    <label class="block text-xs font-bold text-slate-500 mb-2 uppercase">Aço Comercial</label>
                                    <select id="cfg_barra" class="bg-white border border-slate-300 p-2 rounded text-sm outline-none">
                                        <option value="12">Barras de 12 metros</option>
                                        <option value="6">Barras de 6 metros</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-bold text-slate-500 mb-2 uppercase">Preparo do Concreto</label>
                                    <select id="tipo_concreto" onchange="toggleConcreto(this.value)" class="bg-white border border-slate-300 p-2 rounded text-sm outline-none">
                                        <option value="virado">Virado na Obra</option>
                                        <option value="usinado">Usinado (Concreteira)</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <h4 class="text-sm font-bold text-[#0A192F] mb-3">Traços Volumétricos (Cim : Cal : Ar)</h4>
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
                                    <div id="box-concreto-obra" class="bg-white p-3 rounded border border-slate-200 border-l-2 border-l-[#C5A059]">
                                        <span class="text-[11px] text-[#0A192F] block mb-2 font-bold">Concreto (Cim : Ar : Br)</span>
                                        <div class="flex space-x-1"><input type="number" id="co_cim" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="co_ar" value="2.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="co_br" value="3.0" class="w-full text-center border rounded p-1 text-sm"></div>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <h4 class="text-sm font-bold text-[#0A192F] mb-3">Tabela de Preços Unitários (R$)</h4>
                                <div class="grid grid-cols-4 lg:grid-cols-8 gap-3">
                                    <div><label class="text-[10px] text-slate-500">Tijolo 1V</label><input type="number" id="pr_t1v" value="1.20" step="0.1" class="w-full border p-1 rounded text-sm text-center"></div>
                                    <div><label class="text-[10px] text-slate-500">Tijolo MV</label><input type="number" id="pr_tmv" value="0.80" step="0.1" class="w-full border p-1 rounded text-sm text-center"></div>
                                    <div><label class="text-[10px] text-slate-500">Cim 50kg</label><input type="number" id="pr_cim" value="35.00" class="w-full border p-1 rounded text-sm text-center"></div>
                                    <div><label class="text-[10px] text-slate-500">Cal 20kg</label><input type="number" id="pr_cal" value="15.00" class="w-full border p-1 rounded text-sm text-center"></div>
                                    <div><label class="text-[10px] text-slate-500">Areia m³</label><input type="number" id="pr_ar" value="120.00" class="w-full border p-1 rounded text-sm text-center"></div>
                                    <div><label class="text-[10px] text-slate-500">Brita m³</label><input type="number" id="pr_br" value="110.00" class="w-full border p-1 rounded text-sm text-center"></div>
                                    <div><label class="text-[10px] text-slate-500">Aço Fino</label><input type="number" id="pr_af" value="25.00" class="w-full border p-1 rounded text-sm text-center"></div>
                                    <div><label class="text-[10px] text-slate-500">Aço Gros</label><input type="number" id="pr_ag" value="60.00" class="w-full border p-1 rounded text-sm text-center"></div>
                                </div>
                                <div id="preco_usinado_box" class="hidden mt-3 w-1/4">
                                    <label class="text-[10px] text-[#C5A059] font-bold">Preço Concreto Usinado (m³)</label>
                                    <input type="number" id="pr_conc" value="450.00" class="w-full border p-1 rounded text-sm text-center border-[#C5A059] outline-none">
                                </div>
                            </div>
                        </div>
                    </details>
                </div>
                
                <div class="bg-slate-50 p-6 border-t border-slate-200">
                    <button onclick="processarERP()" class="w-full md:w-auto px-10 py-4 bg-[#0A192F] hover:bg-[#112240] text-[#C5A059] border border-[#C5A059] font-bold rounded-xl shadow-md transition-all text-lg flex items-center justify-center mx-auto">
                        📄 Gerar Relatório e Orçamento
                    </button>
                </div>
            </div>

            <div id="res-erp" class="hidden">
                <h3 class="text-2xl font-bold text-[#0A192F] mb-6">Orçamento HFF</h3>
                <div class="bg-white rounded-xl shadow-sm border border-[#C5A059] overflow-hidden">
                    <table class="min-w-full divide-y divide-slate-200">
                        <thead class="bg-[#0A192F] text-[#C5A059]">
                            <tr>
                                <th class="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">Material</th>
                                <th class="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider">Qtd Necessária</th>
                                <th class="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider">Custo (R$)</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-slate-100 text-sm text-slate-700" id="tabela-orcamento"></tbody>
                        <tfoot class="bg-[#0A192F] text-white">
                            <tr>
                                <td colspan="2" class="px-6 py-5 text-right font-semibold">Custo Total Estimado:</td>
                                <td class="px-6 py-5 text-right font-black text-2xl text-[#C5A059]" id="out-custo-total">R$ 0,00</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>

                <details class="mt-6 text-sm text-slate-500">
                    <summary class="cursor-pointer hover:text-[#C5A059]">Ver detalhamento de cálculo (Metragens e Volumes)</summary>
                    <div class="p-4 bg-white border rounded mt-2 grid grid-cols-2 md:grid-cols-4 gap-4" id="detalhes_finais"></div>
                </details>
            </div>
        </section>

        <section id="mod-cargas" class="module-section hidden max-w-3xl mx-auto">
            <h2 class="text-3xl font-extrabold text-[#0A192F] mb-8 border-b-2 border-[#C5A059] pb-2">Descida de Cargas</h2>
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <label class="block text-sm text-slate-600 mb-1">Área da Planta (m²)</label>
                <input type="number" id="c_area" value="100" class="w-full border p-2.5 rounded-lg mb-4 bg-slate-50 outline-none">
                <label class="block text-sm text-slate-600 mb-1">Qtd Pilares</label>
                <input type="number" id="c_pilares" value="8" class="w-full border p-2.5 rounded-lg mb-6 bg-slate-50 outline-none">
                <button onclick="calcCargas()" class="w-full bg-[#0A192F] text-[#C5A059] font-bold py-3 rounded-lg border border-[#C5A059]">Calcular</button>
                <div id="res-cargas" class="mt-6 p-4 bg-[#0A192F] border border-[#C5A059] rounded-lg hidden">
                    <p class="text-sm text-slate-300">Carga Axial (Nk) p/ Pilar:</p>
                    <p class="text-3xl font-bold text-[#C5A059]" id="out-nk"></p>
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