import os

def actualizar_cronicas():
    archivo_cronicas = "cronicas.txt"
    archivo_html = "index.html"
    
    if not os.path.exists(archivo_cronicas):
        print(f"❌ No encuentro el archivo {archivo_cronicas}. Créalo para meter las crónicas semanalmente.")
        return
    
    if not os.path.exists(archivo_html):
        print(f"❌ No encuentro el archivo {archivo_html}.")
        return

    with open(archivo_cronicas, "r", encoding="utf-8") as f:
        lineas_cronicas = f.readlines()

    print("🔄 Generando sección de crónicas y resultados...")

    bloque_cronicas_html = '<div class="space-y-8">\n'
    
    for linea in lineas_cronicas:
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        
        partes = [p.strip() for p in linea.split('|')]
        
        equipo = partes[0] if len(partes) > 0 else "INTER DE MORATALAZ"
        rival = partes[1] if len(partes) > 1 else "Rival"
        resultado = partes[2] if len(partes) > 2 else "0 - 0"
        goleadores = partes[3] if len(partes) > 3 else "Sin detalles de goles"
        sede = partes[4] if len(partes) > 4 else "Sede por confirmar"
        imagen = partes[5] if len(partes) > 5 else ""

        # Formateamos la lista de goleadores
        items_goles = ""
        if goleadores and goleadores != "Sin detalles de goles":
            goles_lista = [g.strip() for g in goleadores.split(',')]
            for gol in goles_lista:
                items_goles += f"""
                <div class="bg-black/60 p-2.5 rounded-xl border border-gray-800 flex justify-between items-center text-xs">
                    <span class="text-amber-400 font-bold"><i class="fa-solid fa-futbol mr-1.5"></i> GOL</span>
                    <span class="text-gray-200 font-medium text-right">{gol}</span>
                </div>
                """
        else:
            items_goles = '<p class="text-xs text-gray-400 italic">No hay detalles registrados de los goles.</p>'

        # Columna del cartel (si existe)
        columna_cartel = ""
        if imagen and os.path.exists(imagen):
            columna_cartel = f"""
            <div class="lg:col-span-5 flex flex-col items-center justify-center">
                <div class="relative group w-full max-w-xs rounded-2xl overflow-hidden border-2 border-interBlue/60 shadow-neon-blue bg-black p-2">
                    <a href="{imagen}" target="_blank" rel="noopener noreferrer">
                        <img src="{imagen}" alt="Cartel del partido" class="w-full h-auto object-contain rounded-xl transform group-hover:scale-105 transition duration-500">
                        <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition duration-300 flex items-center justify-center rounded-xl pointer-events-none">
                            <span class="bg-interBlue text-white text-xs font-black px-4 py-2 rounded-xl shadow-lg uppercase tracking-wider">
                                <i class="fa-solid fa-expand mr-1"></i> Ampliar Cartel
                            </span>
                        </div>
                    </a>
                </div>
            </div>
            """
            col_span_info = "lg:col-span-7"
        else:
            col_span_info = "lg:col-span-12"

        # Tarjeta completa del partido
        bloque_cronicas_html += f"""
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center bg-gradient-to-br from-gray-900/90 via-black to-gray-900/90 border-2 border-green-500/50 p-6 sm:p-8 rounded-3xl shadow-[0_0_30px_rgba(34,197,94,0.25)] backdrop-blur-md">
            <div class="{col_span_info} space-y-5">
                <div class="flex flex-wrap items-center gap-3">
                    <span class="bg-interBlue text-white text-xs font-black px-3.5 py-1.5 rounded-md uppercase tracking-wider shadow-neon-blue">{equipo}</span>
                    <span class="bg-green-500 text-black text-xs font-black px-3.5 py-1.5 rounded-md uppercase tracking-wider">RESULTADO FINAL: {resultado}</span>
                </div>

                <h3 class="text-xl sm:text-2xl font-black text-white italic uppercase tracking-tight">
                    {rival} <span class="text-green-400">{resultado}</span> INTER DE MORATALAZ ({equipo})
                </h3>

                <div class="bg-black/80 border border-gray-800 p-5 rounded-2xl space-y-3">
                    <span class="text-xs text-green-400 uppercase font-black tracking-wider block"><i class="fa-solid fa-trophy mr-1.5"></i> Resumen / Goleadores</span>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {items_goles}
                    </div>
                </div>

                <div class="bg-black/80 border border-gray-800 p-4 rounded-2xl flex items-start space-x-3.5">
                    <i class="fa-solid fa-map-location-dot text-red-500 text-lg mt-0.5"></i>
                    <div>
                        <span class="text-xs text-gray-400 uppercase font-bold block">Sede / Campo:</span>
                        <span class="text-sm font-black text-white uppercase block">{sede}</span>
                    </div>
                </div>
            </div>

            {columna_cartel}
        </div>
        """
    
    bloque_cronicas_html += '</div>'

    with open(archivo_html, "r", encoding="utf-8") as f:
        contenido_html = f.read()

    inicio_marca = "<!-- INICIO_CRONICAS_SEMANALES -->"
    fin_marca = "<!-- FIN_CRONICAS_SEMANALES -->"

    if inicio_marca not in contenido_html or fin_marca not in contenido_html:
        print("❌ Error: No encuentro las marcas <!-- INICIO_CRONICAS_SEMANALES --> y <!-- FIN_CRONICAS_SEMANALES --> en index.html.")
        return

    partes_html = contenido_html.split(inicio_marca)
    preambulo = partes_html[0]
    resto = partes_html[1].split(fin_marca)[1]

    nuevo_bloque = f"{inicio_marca}\n{bloque_cronicas_html}\n{fin_marca}"
    contenido_final = preambulo + nuevo_bloque + resto

    with open(archivo_html, "w", encoding="utf-8") as f:
        f.write(contenido_final)

    print("✅ ¡'index.html' actualizado con las crónicas y resultados de la jornada!")

if __name__ == "__main__":
    actualizar_cronicas()