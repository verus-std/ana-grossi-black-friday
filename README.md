# Protótipo — Black Friday Ana Grossi

Página estática em HTML/CSS/JavaScript. `index.html` é a página de captura; `obrigado.html` apresenta a etapa do WhatsApp e a biografia da Ana, sem vídeo. O formulário não envia nem armazena dados. A integração de captação depende da plataforma final.

O convite do WhatsApp deve ser preenchido na constante `whatsappGroupUrl` em `obrigado.js`. Enquanto o link não estiver disponível, os botões abrem um aviso de que o grupo será liberado em breve.

## Conteúdo provisório

- A hero usa a montagem enviada em `assets/hero-ana.jpg`. A seção “Quem é Ana” usa os dois retratos enviados, em `assets/ana-retrato.jpg` e `assets/ana-costura.jpg`.
- O ano de 2026 foi usado no contador para a data de 04 de novembro, às 20h (horário de Brasília).
- O preço especial permanece oculto, conforme a copy recebida.

Para visualizar localmente: `python3 -m http.server 8000` e acesse `http://localhost:8000`.

## Primeira versão

A primeira versão publicada (commit `368be0a`) está preservada em `/versao-antiga/`, com seus próprios estilos, scripts, imagens e página de obrigado.
