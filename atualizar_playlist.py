import requests

def gerar_playlist():
    # Lista de domínios conhecidos da API devido às constantes migrações
    urls_para_testar = [
        "https://reidoscanais.cam",
        "https://reidoscanais.st",
        "https://reidoscanais.my"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    dados = None
    url_funcional = None

    # Tenta cada uma das URLs até uma responder com JSON válido
    for url in urls_para_testar:
        print(f"Tentando conectar em: {url}")
        try:
            resposta = requests.get(url, headers=headers, timeout=10)
            if resposta.status_code == 200:
                dados = resposta.json()
                url_funcional = url
                print(f"Sucesso ao conectar em: {url}")
                break
        except Exception as e:
            print(f"Falha no domínio {url}: {e}")
            continue

    conteudo_m3u = "#EXTM3U\n"
    
    if dados and dados.get("success") and "data" in dados:
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
        print(f"Total de canais adicionados: {canais_adicionados}")
    else:
        print("Nenhum dos domínios da API retornou dados válidos.")
        conteudo_m3u += "# Erro: Todos os servidores da API falharam ou retornaram blocos vazios\n"

    # Salva o arquivo final
    with open("playlist.m3u", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_m3u)
    print("Concluído!")

if __name__ == "__main__":
    gerar_playlist()
