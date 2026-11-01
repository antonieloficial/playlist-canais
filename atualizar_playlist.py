import requests

def gerar_playlist():
    url_api = "https://reidoscanais.my"
    print("Buscando canais da API...")
    
    try:
        resposta = requests.get(url_api)
        resposta.raise_for_status()
        dados = resposta.json()
    except Exception as e:
        print(f"Erro ao acessar a API: {e}")
        return

    if not dados.get("success") or "data" not in dados:
        print("API retornou uma estrutura inválida.")
        return

    # Início do arquivo de playlist M3U
    conteudo_m3u = "#EXTM3U\n"

    for canal in dados["data"]:
        nome = canal.get("name", "Canal Sem Nome")
        categoria = canal.get("category", "Geral")
        logo = canal.get("logo_url", "")
        
        # Filtra os links de transmissão (embeds)
        embeds = canal.get("embeds", [])
        if not embeds:
            continue
            
        # Pega a primeira opção de transmissão disponível
        url_transmissao = embeds[0].get("embed_url", "")
        
        if url_transmissao:
            # Estrutura padrão M3U com metadados de logo e grupo
            conteudo_m3u += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{categoria}",{nome}\n'
            conteudo_m3u += f'{url_transmissao}\n'

    # Salva o arquivo localmente no ambiente do GitHub
    with open("playlist.m3u", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_m3u)
    print("Playlist (.m3u) gerada com sucesso!")

if __name__ == "__main__":
    gerar_playlist()
  
