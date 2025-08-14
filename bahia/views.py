import requests
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import pprint


API_KEY = '2c74310bac17e58a82cf4970c9afbcd9'

CIDADES_BA = [
    'Salvador', 'Feira de Santana', 'Vitoria da Conquista', 'Itabuna', 'Juazeiro', 'Ilhéus', 'Barreiras'
]


def _pegar_clima():
    dados = []
    for cidade in CIDADES_BA:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={cidade},BR&appid={'2c74310bac17e58a82cf4970c9afbcd9'}&units=metric&lang=pt_br"
        )
        try:
            r = requests.get(url, timeout=6)
            if r.status_code == 200:
                info = r.json()
                dados.append({
                    "cidade": cidade,
                    "temp": round(info['main']['temp']),
                    "descricao": info['weather'][0]['description'].capitalize(),
                    "umidade": info['main']['humidity'],
                    "icone": info['weather'][0]['icon'],
                })
            else:
                dados.append({
                    "cidade": cidade, "temp": "--", "descricao": "Erro API", "umidade": "--", "icone": "50d"
                })
        except requests.RequestException:
            dados.append({
                "cidade": cidade, "temp": "—", "descricao": "Sem conexão",
                "umidade": "—", "icone": "50d"
            })

    return {
        "itens": dados,
        "atualizado_em": datetime.now().isoformat(),
    }


def pagina_clima(request):
    # Renderiza HTML inicial (server-side)
    dados = _pegar_clima()
    pprint.pprint(dados)  # imprime no terminal pra ver
    return render(request, "clima.html", dados)
    return render(request, "clima.html", _pegar_clima())


def api_clima(request):
    # Endpoint JSON para o JavaScript atualizar sem recarregar
    return JsonResponse(_pegar_clima())
