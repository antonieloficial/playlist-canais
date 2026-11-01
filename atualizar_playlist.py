import requests

def gerar_playlist():
    url_api = "https://reidoscanais.my"
    print("Buscando canais da API...")
    
    conteudo_m3u = "#EXTM3U\n"
    canais_adicionados = 0
    
    # Cabeçalhos para simular um navegador real e evitar bloqueios da API
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        # Adicionado o parâmetro headers na requisição
        resposta = requests.get(url_api, headers=headers, timeout=15)
        resposta.raise_for_status()
        dados = resposta.json()
        
        if dados.get("success") and "data" in dados:
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
            print(f"Total de canais processados com link: {canais_adicionados}")
        else:
            print("API retornou uma estrutura inválida ou success=False.")
            conteudo_m3u += "# Erro: API retornou estrutura inválida ou vazia\n"
            
    except Exception as e:
        print(f"Erro ao acessar a API: {e}")
        conteudo_m3u += f"# Erro ao conectar na API: {e}\n"

    with open("playlist.m3u", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_m3u)
    print("Arquivo playlist.m3u gerado!")

if __name__ == "__main__":
    gerar_playlist()
