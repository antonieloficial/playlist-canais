import requests

def gerar_playlist():
    # Passando a requisição por um espelho/proxy aberto para burlar o bloqueio de bot da Cloudflare
    url_api = "https://corsproxy.io"
    print("Buscando canais via Proxy estruturado...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    conteudo_m3u = "#EXTM3U\n"
    
    try:
        resposta = requests.get(url_api, headers=headers, timeout=20)
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
            print("API respondeu, mas os dados vieram vazios.")
            conteudo_m3u += "# Erro: API retornou estrutura sem canais ativos\n"
            
    except Exception as e:
        print(f"Falha na conexão: {e}")
        conteudo_m3u += f"# Erro de comunicacao com o servidor: {e}\n"

    # Força a escrita correta no repositório
    with open("playlist.m3u", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_m3u)
    print("Processamento concluído.")

if __name__ == "__main__":
    gerar_playlist()
