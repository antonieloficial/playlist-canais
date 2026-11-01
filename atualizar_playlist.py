import requests

def gerar_playlist():
    # URL oficial atualizada e limpa para requisições assíncronas
    url_api = "https://reidoscanais.cam"
    print("Buscando canais através do bypass de emulação de navegador...")
    
    # Conjunto de cabeçalhos de alta fidelidade para contornar o bloqueio de raspagem da Cloudflare
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://reidoscanais.cam/",
        "Origin": "https://reidoscanais.cam",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }
    
    conteudo_m3u = "#EXTM3U\n"
    
    try:
        # Abre a sessão simulada
        sessao = requests.Session()
        resposta = sessao.get(url_api, headers=headers, timeout=25)
        
        # Se retornar HTML de bloqueio, tentamos o espelho secundário estável
        if "<html>" in resposta.text or "<script>" in resposta.text:
            print("Bloqueio detectado no domínio .cam, tentando espelho secundário (.st)...")
            url_api_backup = "https://reidoscanais.st"
            headers["Referer"] = "https://reidoscanais.st"
            headers["Origin"] = "https://reidoscanais.st"
            resposta = sessao.get(url_api_backup, headers=headers, timeout=25)
            
        resposta.raise_for_status()
        dados = resposta.json()
        
        if dados.get("success") and "data" in dados:
            canais_adicionados = 0
            for canal in dados["data"]:
                nome = canal.get("name", "Canal Sem Nome")
                categoria = canal.get("category", "Geral")
                logo = canal.get("logo_url", "")
                
                embeds = canal.get("embeds", [])
                if embeds and isinstance(embeds, list):
                    primeiro_embed = embeds[0]
                    url_transmissao = primeiro_embed.get("embed_url", "")
                    
                    if url_transmissao:
                        conteudo_m3u += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{categoria}",{nome}\n'
                        conteudo_m3u += f'{url_transmissao}\n'
                        canais_adicionados += 1
            print(f"Sucesso! Total de canais adicionados: {canais_adicionados}")
        else:
            conteudo_m3u += "# Erro: API respondeu com bloco de dados inválido ou vazio\n"
            
    except Exception as e:
        print(f"Falha na conexão: {e}")
        conteudo_m3u += f"# Erro de comunicacao com o servidor: {e}\n"

    # Salva o arquivo final estruturado
    with open("playlist.m3u", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_m3u)
    print("Processamento da lista concluído.")

if __name__ == "__main__":
    gerar_playlist()
