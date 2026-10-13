import os

def procesar_y_actualizar():
    archivo_partidos = "partidos.txt"
    archivo_html = "index.html"
    
    if not os.path.exists(archivo_partidos):
        print(f"❌ No encuentro el archivo {archivo_partidos}.")
        return
    
    if not os.path.exists(archivo_html):
        print(f"❌ No encuentro el archivo {archivo_html}.")
        return

    with open(archivo_partidos, "r", encoding="utf-8") as f:
        lineas_partidos = f.readlines()

    print("🔄 Leyendo próximos partidos...")

    # Generamos únicamente la rejilla con las tarjetas de los partidos
    bloque_partidos_html = '<div class="grid grid-cols-1 gap-8">\n'
    
    for linea in lineas_partidos:
        linea = linea.strip()
        if not linea:
            continue
        
        partes = [p.strip() for p in linea.split('|')]
        
        match_info = partes[0] if len(partes) > 0 else "Partido Oficial"
        horario = partes[1] if len(partes) > 1 else "Horario por confirmar"
        lugar = partes[2] if len(partes) > 2 else "Sede por confirmar"
        imagen = partes[3] if len(partes) > 3 else ""
        
        if imagen:
            bloque_partidos_html += f"""
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center bg-gradient-to-br from-gray-900/90 via-black to-gray-900/90 border-2 border-interBlue/50 p-6 sm:p-8 rounded-3xl shadow-neon-blue backdrop-blur-md">
                <div class="lg:col-span-7 space-y-4">
                    <span class="bg-interBlue text-white text-xs font-black px-3.5 py-1.5 rounded-md uppercase tracking-wider shadow-neon-blue">PRÓXIMO ENCUENTRO</span>
                    <h4 class="text-xl sm:text-2xl font-black text-white italic uppercase">{match_info}</h4>
                    <p class="text-sm text-amber-400 font-bold">🕒 {horario}</p>
                    <p class="text-xs text-gray-300">📍 {lugar}</p>
                </div>
                <div class="lg:col-span-5 flex flex-col items-center justify-center">
                    <div class="relative group w-full max-w-xs rounded-2xl overflow-hidden border-2 border-interBlue/60 shadow-neon-blue bg-black p-2">
                        <a href="{imagen}" target="_blank" rel="noopener noreferrer">
                            <img src="{imagen}" alt="Cartel del partido" class="w-full h-auto object-contain rounded-xl transform group-hover:scale-105 transition duration-500">
                            <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition duration-300 flex items-center justify-center rounded-xl pointer-events-none">
                                <span class="bg-interBlue text-white text-xs font-black px-4 py-2 rounded-xl shadow-lg uppercase tracking-wider">
                                    <i class="fa-solid fa-expand mr-1"></i> Ampliar Imagen
                                </span>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
            """
        else:
            bloque_partidos_html += f"""
            <div class="bg-black/80 border border-gray-800 p-5 rounded-2xl space-y-2">
                <span class="text-xs text-amber-400 font-black uppercase tracking-wider block">⚽ {match_info}</span>
                <p class="text-sm text-white font-bold">🕒 {horario}</p>
                <p class="text-xs text-gray-400">📍 {lugar}</p>
            </div>
            """
    
    bloque_partidos_html += '</div>'

    with open(archivo_html, "r", encoding="utf-8") as f:
        contenido_html = f.read()

    inicio_marca = "<!-- INICIO_ACTUALIZACION_SEMANAL -->"
    fin_marca = "<!-- FIN_ACTUALIZACION_SEMANAL -->"

    if inicio_marca not in contenido_html or fin_marca not in contenido_html:
        print("❌ Error: No encuentro las marcas en index.html.")
        return

    partes_html = contenido_html.split(inicio_marca)
    preambulo = partes_html[0]
    resto = partes_html[1].split(fin_marca)[1]

    nuevo_bloque_semanal = f"{inicio_marca}\n{bloque_partidos_html}\n{fin_marca}"

    contenido_final = preambulo + nuevo_bloque_semanal + resto

    with open(archivo_html, "w", encoding="utf-8") as f:
        f.write(contenido_final)

    print("✅ ¡'index.html' actualizado correctamente sin duplicar títulos!")

if __name__ == "__main__":
    procesar_y_actualizar()