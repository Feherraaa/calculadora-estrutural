<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Godoy & Prado - Plataforma de Engenharia</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .hidden { display: none; }
        .nav-btn { cursor: pointer; transition: all 0.2s ease-in-out; }
        .nav-btn:hover { background-color: #112240; color: #C5A059; }
        /* Cores baseadas na Logo Godoy & Prado: Azul Marinho #0A192F e Dourado #C5A059 */
        .active-nav { background-color: #112240; color: #C5A059; border-left: 4px solid #C5A059; font-weight: 600; }
        
        details > summary { list-style: none; cursor: pointer; }
        details > summary::-webkit-details-marker { display: none; }
        
        .tab-btn { cursor: pointer; transition: all 0.2s; }
        .active-tab { border-bottom: 2px solid #C5A059; color: #0A192F; font-weight: bold; }
        
        /* Custom scrollbar para o menu lateral */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #1A2E4C; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #C5A059; }
    </style>
</head>
<body class="bg-slate-50 font-sans flex h-screen overflow-hidden text-slate-800">

    <aside class="w-64 bg-[#0A192F] border-r border-[#1A2E4C] flex flex-col h-full z-10 shadow-2xl">
        
        <div class="p-6 border-b border-[#1A2E4C] flex flex-col items-center justify-center bg-[#071324]">
            <img src="image_d8ed05.png" alt="Logo Godoy & Prado" class="w-40 mb-2 drop-shadow-lg">
        </div>

        <nav class="flex-1 mt-4 overflow-y-auto">
            <ul class="space-y-1">
                <li onclick="showModule('mod-materiais', this)" class="nav-btn active-nav block px-6 py-3 text-sm text-slate-300">Orçamentação (ERP)</li>
                <li onclick="showModule('mod-cargas', this)" class="nav-btn block px-6 py-3 text-sm text-slate-400">Descida de Cargas</li>
                <li onclick="showModule('mod-vigas', this)" class="nav-btn block px-6 py-3 text-sm text-slate-400">Vigas (Gráficos)</li>
            </ul>
        </nav>

        <div class="p-5 bg-[#071324] border-t border-[#1A2E4C]">
            <h4 class="text-[#C5A059] text-xs font-bold uppercase tracking-wider mb-3 flex items-center">
                <span class="mr-2">📚</span> Referências
            </h4>
            <ul class="text-[11px] text-slate-400 space-y-2 leading-tight">
                <li>• <strong class="text-slate-300">NBR 6118:</strong> Proj. Estruturas de Concreto</li>
                <li>• <strong class="text-slate-300">NBR 6120:</strong> Cargas para Cálculo</li>
                <li>• <strong class="text-slate-300">NBR 8800:</strong> Estruturas de Aço / FLT</li>
                <li>• <strong class="text-slate-300">Eurocode 4 / CBCA:</strong> Vigas Mistas</li>
                <li>• <strong class="text-slate-300">Catálogos Gerdau:</strong> Perfis W e U</li>
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
                        <input type="checkbox" id="chk_alv" checked onchange="toggleSection('sec_alv', this.checked)" class="form-checkbox h-5 w-5 text-[#C5A059] rounded border-slate-300 focus:ring-[#C5A059]">
                        <span class="ml-2 text-slate-700 font-medium">Alvenaria</span>
                    </label>
                    <label class="flex items-center cursor-pointer">
                        <input type="checkbox" id="chk_fund" checked onchange="toggleSection('sec_fund', this.checked)" class="form-checkbox h-5 w-5 text-[#C5A059] rounded border-slate-300 focus:ring-[#C5A059]">
                        <span class="ml-2 text-slate-700 font-medium">Fundações</span>
                    </label>
                    <label class="flex items-center cursor-pointer">
                        <input type="checkbox" id="chk_sup" checked onchange="toggleSection('sec_sup', this.checked)" class="form-checkbox h-5 w-5 text-[#C5A059] rounded border-slate-300 focus:ring-[#C5A059]">
                        <span class="ml-2 text-slate-700 font-medium">Pilares e Vigas</span>
                    </label>
                </div>

                <div class="p-6 space-y-8">
                    
                    <div id="sec_alv" class="space-y-4">
                        <h3 class="text-lg font-bold text-[#0A192F] flex items-center"><span class="text-xl mr-2">🧱</span> Dimensões da Alvenaria</h3>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div><label class="block text-xs font-semibold text-slate-500 mb-1">Pé-direito (m)</label><input type="number" id="m_pd" value="2.8" class="w-full bg-slate-50 border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-[#C5A059] outline-none transition"></div>
                            <div><label class="block text-xs font-semibold text-slate-500 mb-1">Parede 1 Vez (Metro Linear)</label><input type="number" id="m_ml_1v" value="20.0" class="w-full bg-slate-50 border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-[#C5A059] outline-none transition"></div>
                            <div><label class="block text-xs font-semibold text-slate-500 mb-1">Parede Meia Vez (Metro Linear)</label><input type="number" id="m_ml_mv" value="50.0" class="w-full bg-slate-50 border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-[#C5A059] outline-none transition"></div>
                        </div>
                    </div>

                    <div id="sec_fund" class="space-y-4 border-t border-slate-100 pt-6">
                        <h3 class="text-lg font-bold text-[#0A192F] flex items-center"><span class="text-xl mr-2">🕳️</span> Geometria das Estacas</h3>
                        <div class="grid grid-cols-2 md:grid-cols-6 gap-4">
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Quantidade</label><input type="number" id="e_qtd" value="20" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-[#C5A059]"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Diâmetro (cm)</label><input type="number" id="e_diam" value="25.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-[#C5A059]"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Profund. (m)</label><input type="number" id="e_prof" value="6.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-[#C5A059]"></div>
                            
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Qtd Aço Long.</label><input type="number" id="e_qtd_long" value="4" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-[#C5A059]"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Esp. Estribo (cm)</label><input type="number" id="e_esp_est" value="15.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-[#C5A059]"></div>
                            <div class="col-span-2 md:col-span-1"><label class="block text-xs font-semibold text-slate-500 mb-1">Cobrimento (cm)</label><input type="number" id="e_cob" value="4.0" class="w-full bg-slate-50 border border-slate-200 p-2 rounded-lg outline-none focus:border-[#C5A059]"></div>
                            <input type="hidden" id="e_transp" value="40.0">
                        </div>
                    </div>

                    <div id="sec_sup" class="space-y-6 border-t border-slate-100 pt-6">
                        <h3 class="text-lg font-bold text-[#0A192F] flex items-center"><span class="text-xl mr-2">🏛️</span> Superestrutura</h3>
                        
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            <div class="bg-white border-l-4 border-[#0A192F] rounded-r-xl p-5 shadow-sm bg-slate-50/50">
                                <h4 class="font-bold text-[#0A192F] mb-3">Pilares</h4>
                                <div class="grid grid-cols-3 gap-3 mb-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd</label><input type="number" id="p_qtd" value="12" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Comp. (m)</label><input type="number" id="p_comp" value="3.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Seção (cm)</label>
                                        <div class="flex items-center space-x-1">
                                            <input type="number" id="p_b" value="15" class="w-full bg-white border border-slate-200 p-2 rounded-lg text-center" title="Base">
                                            <span class="text-slate-400">x</span>
                                            <input type="number" id="p_h" value="30" class="w-full bg-white border border-slate-200 p-2 rounded-lg text-center" title="Altura">
                                        </div>
                                    </div>
                                </div>
                                <div class="grid grid-cols-3 gap-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd Aço Long.</label><input type="number" id="p_qtd_long" value="4" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Esp. Estribo (cm)</label><input type="number" id="p_esp_est" value="15.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Cobrimento (cm)</label><input type="number" id="p_cob" value="3.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#C5A059] outline-none"></div>
                                    <input type="hidden" id="p_transp" value="40.0">
                                </div>
                            </div>

                            <div class="bg-white border-l-4 border-[#C5A059] rounded-r-xl p-5 shadow-sm bg-slate-50/50">
                                <h4 class="font-bold text-[#C5A059] mb-3">Vigas</h4>
                                <div class="grid grid-cols-3 gap-3 mb-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd</label><input type="number" id="v_qtd" value="15" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#0A192F] outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Comp. Médio (m)</label><input type="number" id="v_comp" value="4.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#0A192F] outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Seção (cm)</label>
                                        <div class="flex items-center space-x-1">
                                            <input type="number" id="v_bw" value="15" class="w-full bg-white border border-slate-200 p-2 rounded-lg text-center" title="Base">
                                            <span class="text-slate-400">x</span>
                                            <input type="number" id="v_h" value="40" class="w-full bg-white border border-slate-200 p-2 rounded-lg text-center" title="Altura">
                                        </div>
                                    </div>
                                </div>
                                <div class="grid grid-cols-3 gap-3">
                                    <div><label class="block text-xs text-slate-500 mb-1">Qtd Aço Long.</label><input type="number" id="v_qtd_long" value="4" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#0A192F] outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Esp. Estribo (cm)</label><input type="number" id="v_esp_est" value="15.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#0A192F] outline-none"></div>
                                    <div><label class="block text-xs text-slate-500 mb-1">Cobrimento (cm)</label><input type="number" id="v_cob" value="3.0" class="w-full bg-white border border-slate-200 p-2 rounded-lg focus:border-[#0A192F] outline-none"></div>
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
                                    <select id="cfg_barra" class="bg-white border border-slate-300 p-2 rounded text-sm focus:border-[#C5A059] outline-none">
                                        <option value="12">Barras de 12 metros</option>
                                        <option value="6">Barras de 6 metros</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-bold text-slate-500 mb-2 uppercase">Preparo do Concreto</label>
                                    <select id="tipo_concreto" onchange="toggleConcreto(this.value)" class="bg-white border border-slate-300 p-2 rounded text-sm focus:border-[#C5A059] outline-none">
                                        <option value="virado">Virado na Obra</option>
                                        <option value="usinado">Usinado (Concreteira)</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <h4 class="text-sm font-bold text-[#0A192F] mb-3">Traços Volumétricos (Cimento : Cal : Areia)</h4>
                                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                                    <div class="bg-white p-3 rounded border border-slate-200">
                                        <span class="text-xs text-slate-400 block mb-2 font-bold">Assentamento</span>
                                        <div class="flex space-x-1"><input type="number" id="a_cim" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="a_cal" value="0.5" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="a_ar" value="6.0" class="w-full text-center border rounded p-1 text-sm"></div>
                                    </div>
                                    <div class="bg-white p-3 rounded border border-slate-200">
                                        <span class="text-xs text-slate-400 block mb-2 font-bold">Reboco</span>
                                        <div class="flex space-x-1"><input type="number" id="r_cim" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="r_cal" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="r_ar" value="6.0" class="w-full text-center border rounded p-1 text-sm"></div>
                                    </div>
                                    <div class="bg-white p-3 rounded border border-slate-200">
                                        <span class="text-xs text-slate-400 block mb-2 font-bold">Chapisco</span>
                                        <div class="flex space-x-1"><input type="number" id="c_cim" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="c_cal" value="0.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="c_ar" value="3.0" class="w-full text-center border rounded p-1 text-sm"></div>
                                    </div>
                                    <div id="box-concreto-obra" class="bg-white p-3 rounded border border-slate-200 border-l-2 border-l-[#C5A059]">
                                        <span class="text-xs text-[#0A192F] block mb-2 font-bold">Concreto (Cim : Ar : Br)</span>
                                        <div class="flex space-x-1"><input type="number" id="co_cim" value="1.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="co_ar" value="2.0" class="w-full text-center border rounded p-1 text-sm"><input type="number" id="co_br" value="3.0" class="w-full text-center border rounded p-1 text-sm"></div>
                                    </div>
                                    <div id="box-concreto-usinado" class="hidden bg-white p-3 rounded border border-slate-200 col-span-1 border-l-2 border-l-[#C5A059]">
                                        <span class="text-xs text-[#0A192F] block mb-2 font-bold">Concreto Usinado</span>
                                        <select id="cfg_fck" class="w-full border rounded p-1.5 text-sm"><option value="20">FCK 20 MPa</option><option value="25" selected>FCK 25 MPa</option><option value="30">FCK 30 MPa</option></select>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <h4 class="text-sm font-bold text-[#0A192F] mb-3">Tabela de Preços Unitários (R$)</h4>
                                <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
                                    <div><label class="text-[10px] text-slate-500">Tijolo 1Vz</label><input type="number" id="pr_t1v" value="1.20" step="0.1" class="w-full border p-1 rounded text-sm text-center focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Tijolo MVz</label><input type="number" id="pr_tmv" value="0.80" step="0.1" class="w-full border p-1 rounded text-sm text-center focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Cim 50kg</label><input type="number" id="pr_cim" value="35.00" class="w-full border p-1 rounded text-sm text-center focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Cal 20kg</label><input type="number" id="pr_cal" value="15.00" class="w-full border p-1 rounded text-sm text-center focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Areia m³</label><input type="number" id="pr_ar" value="120.00" class="w-full border p-1 rounded text-sm text-center focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Brita m³</label><input type="number" id="pr_br" value="110.00" class="w-full border p-1 rounded text-sm text-center focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Aço Fino/Br</label><input type="number" id="pr_af" value="25.00" class="w-full border p-1 rounded text-sm text-center focus:border-[#C5A059] outline-none"></div>
                                    <div><label class="text-[10px] text-slate-500">Aço Gros/Br</label><input type="number" id="pr_ag" value="60.00" class="w-full border p-1 rounded text-sm text-center focus:border-[#C5A059] outline-none"></div>
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
                        <span class="mr-2">📄</span> Gerar Relatório e Orçamento
                    </button>
                </div>
            </div>

            <div id="res-erp" class="hidden">
                <h3 class="text-2xl font-bold text-[#0A192F] mb-6">Orçamento Godoy & Prado</h3>
                
                <div class="bg-white rounded-xl shadow-sm border border-[#C5A059] overflow-hidden">
                    <table class="min-w-full divide-y divide-slate-200">
                        <thead class="bg-[#0A192F] text-[#C5A059]">
                            <tr>
                                <th class="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">Item / Material</th>
                                <th class="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider">Qtd Necessária</th>
                                <th class="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider">Custo (R$)</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-slate-100 text-sm text-slate-700" id="tabela-orcamento">
                            </tbody>
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
                <input type="number" id="c_area" value="100" class="w-full border p-2.5 rounded-lg mb-4 bg-slate-50 outline-none focus:border-[#C5A059]">
                <label class="block text-sm text-slate-600 mb-1">Qtd Pilares</label>
                <input type="number" id="c_pilares" value="8" class="w-full border p-2.5 rounded-lg mb-6 bg-slate-50 outline-none focus:border-[#C5A059]">
                <button onclick="calcCargas()" class="w-full bg-[#0A192F] text-[#C5A059] hover:bg-[#112240] font-bold py-3 rounded-lg transition border border-[#C5A059]">Calcular</button>
                <div id="res-cargas" class="mt-6 p-4 bg-[#0A192F] border border-[#C5A059] rounded-lg hidden">
                    <p class="text-sm text-slate-300">Carga Axial de Serviço (Nk) p/ Pilar:</p>
                    <p class="text-3xl font-bold text-[#C5A059]" id="out-nk"></p>
                </div>
            </div>
        </section>

        <section id="mod-vigas" class="module-section hidden max-w-3xl mx-auto text-center py-20">
            <h2 class="text-3xl font-extrabold text-[#0A192F] mb-4">Módulo de Vigas</h2>
            <p class="text-slate-500">Para a versão local completa com os gráficos de flexão (Chart.js), implemente as rotas visuais conforme o módulo anterior Python/JS.</p>
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
            if(tipo === 'usinado') {
                document.getElementById('box-concreto-obra').classList.add('hidden');
                document.getElementById('box-concreto-usinado').classList.remove('hidden');
                document.getElementById('preco_usinado_box').classList.remove('hidden');
            } else {
                document.getElementById('box-concreto-obra').classList.remove('hidden');
                document.getElementById('box-concreto-usinado').classList.add('hidden');
                document.getElementById('preco_usinado_box').classList.add('hidden');
            }
        }

        function processarERP() {
            const c_alv = document.getElementById('chk_alv').checked;
            const c_fund = document.getElementById('chk_fund').checked;
            const c_sup = document.getElementById('chk_sup').checked;
            const t_conc = document.getElementById('tipo_concreto').value;
            const comp_barra = parseFloat(document.getElementById('cfg_barra').value);

            let tot_cim_sacos = 0, tot_cal_sacos = 0, tot_ar_m3 = 0, tot_br_m3 = 0;
            let qtd_1v = 0, qtd_mv = 0, vol_conc = 0, m_estribos = 0, m_longit = 0;

            function calcTraco(vol, cim, cal, ar) {
                if(vol<=0 || ar==0) return {c:0, k:0, a:0};
                let vp = vol / ar;
                return { c: Math.ceil((vp*cim)/0.036), k: Math.ceil((vp*cal)/0.036), a: vol };
            }

            if(c_alv) {
                let pd = parseFloat(document.getElementById('m_pd').value);
                let ml_1v = parseFloat(document.getElementById('m_ml_1v').value);
                let ml_mv = parseFloat(document.getElementById('m_ml_mv').value);
                let area_1v = ml_1v * pd;
                let area_mv = ml_mv * pd;
                qtd_1v = Math.ceil(area_1v * 38.45);
                qtd_mv = Math.ceil(area_mv * 25.0);

                let v_ass = (area_1v * 0.03) + (area_mv * 0.015);
                let v_chap = (area_1v + area_mv) * 2 * 0.005;
                let v_rev = (area_1v + area_mv) * 2 * 0.02;

                let rA = calcTraco(v_ass, parseFloat(document.getElementById('a_cim').value), parseFloat(document.getElementById('a_cal').value), parseFloat(document.getElementById('a_ar').value));
                let rC = calcTraco(v_chap, parseFloat(document.getElementById('c_cim').value), parseFloat(document.getElementById('c_cal').value), parseFloat(document.getElementById('c_ar').value));
                let rR = calcTraco(v_rev, parseFloat(document.getElementById('r_cim').value), parseFloat(document.getElementById('r_cal').value), parseFloat(document.getElementById('r_ar').value));

                tot_cim_sacos += rA.c + rC.c + rR.c;
                tot_cal_sacos += rA.k + rC.k + rR.k;
                tot_ar_m3 += rA.a + rC.a + rR.a;
            }

            if(c_fund) {
                let q = parseFloat(document.getElementById('e_qtd').value);
                let prof = parseFloat(document.getElementById('e_prof').value);
                let d = parseFloat(document.getElementById('e_diam').value)/100;
                let cob = parseFloat(document.getElementById('e_cob').value)/100;
                let esp = parseFloat(document.getElementById('e_esp_est').value)/100;
                let ql = parseFloat(document.getElementById('e_qtd_long').value);
                let tr = 0.4;
                vol_conc += q * (Math.PI * Math.pow(d/2, 2)) * prof;
                m_estribos += ((Math.PI * (d - 2*cob)) + (2*tr)) * Math.ceil(prof/esp) * q;
                m_longit += (prof + tr) * ql * q;
            }

            if(c_sup) {
                let pq = parseFloat(document.getElementById('p_qtd').value);
                let pc = parseFloat(document.getElementById('p_comp').value);
                let pb = parseFloat(document.getElementById('p_b').value)/100;
                let ph = parseFloat(document.getElementById('p_h').value)/100;
                let pco = parseFloat(document.getElementById('p_cob').value)/100;
                let pes = parseFloat(document.getElementById('p_esp_est').value)/100;
                let pql = parseFloat(document.getElementById('p_qtd_long').value);
                let ptr = 0.4;
                vol_conc += pq * pb * ph * pc;
                m_estribos += (2*(pb-2*pco) + 2*(ph-2*pco) + 2*ptr) * Math.ceil(pc/pes) * pq;
                m_longit += (pc + ptr) * pql * pq;

                let vq = parseFloat(document.getElementById('v_qtd').value);
                let vc = parseFloat(document.getElementById('v_comp').value);
                let vb = parseFloat(document.getElementById('v_bw').value)/100;
                let vh = parseFloat(document.getElementById('v_h').value)/100;
                let vco = parseFloat(document.getElementById('v_cob').value)/100;
                let ves = parseFloat(document.getElementById('v_esp_est').value)/100;
                let vql = parseFloat(document.getElementById('v_qtd_long').value);
                let vtr = 0.2;
                vol_conc += vq * vb * vh * vc;
                m_estribos += (2*(vb-2*vco) + 2*(vh-2*vco) + 2*vtr) * Math.ceil(vc/ves) * vq;
                m_longit += (vc + vtr) * vql * vq;
            }

            let br_fin = Math.ceil(m_estribos / comp_barra) || 0;
            let br_gro = Math.ceil(m_longit / comp_barra) || 0;

            if(t_conc === 'virado' && vol_conc > 0) {
                let v_seco = vol_conc * 1.5;
                let tc = parseFloat(document.getElementById('co_cim').value);
                let ta = parseFloat(document.getElementById('co_ar').value);
                let tb = parseFloat(document.getElementById('co_br').value);
                let vp = v_seco / (tc + ta + tb);
                tot_cim_sacos += Math.ceil((vp*tc)/0.036);
                tot_ar_m3 += vp * ta;
                tot_br_m3 += vp * tb;
            }

            let custo_total = 0;
            let tb = document.getElementById('tabela-orcamento');
            tb.innerHTML = '';
            
            function addRow(nome, qtd, unid, preco) {
                if(qtd > 0) {
                    let cst = qtd * preco;
                    custo_total += cst;
                    tb.innerHTML += `<tr class="hover:bg-slate-50 transition"><td class="px-6 py-3 font-medium">${nome}</td><td class="px-6 py-3 text-right">${qtd.toLocaleString('pt-BR', {maximumFractionDigits:2})} ${unid}</td><td class="px-6 py-3 text-right font-semibold text-slate-600">R$ ${cst.toLocaleString('pt-BR', {minimumFractionDigits:2, maximumFractionDigits:2})}</td></tr>`;
                }
            }

            addRow('Tijolo 1 Vez', qtd_1v, 'unid', parseFloat(document.getElementById('pr_t1v').value));
            addRow('Tijolo Meia Vez', qtd_mv, 'unid', parseFloat(document.getElementById('pr_tmv').value));
            addRow('Cimento (50kg)', tot_cim_sacos, 'sacos', parseFloat(document.getElementById('pr_cim').value));
            addRow('Cal (20kg)', tot_cal_sacos, 'sacos', parseFloat(document.getElementById('pr_cal').value));
            addRow('Areia', tot_ar_m3, 'm³', parseFloat(document.getElementById('pr_ar').value));
            addRow('Brita', tot_br_m3, 'm³', parseFloat(document.getElementById('pr_br').value));
            addRow(`Aço Fino (${comp_barra}m)`, br_fin, 'barras', parseFloat(document.getElementById('pr_af').value));
            addRow(`Aço Grosso (${comp_barra}m)`, br_gro, 'barras', parseFloat(document.getElementById('pr_ag').value));
            
            if(t_conc === 'usinado' && vol_conc > 0) {
                addRow('Concreto Usinado', vol_conc, 'm³', parseFloat(document.getElementById('pr_conc').value));
            }

            document.getElementById('out-custo-total').innerText = `R$ ${custo_total.toLocaleString('pt-BR', {minimumFractionDigits:2, maximumFractionDigits:2})}`;
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