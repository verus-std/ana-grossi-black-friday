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

## Elementor

`elementor/ana-grossi-elementor.zip` reúne os widgets de captura e obrigado, prévias e imagens. Copie o conteúdo de cada `*-widget.txt` em um único widget HTML. As instruções e configurações dos links estão em `elementor/LEIA-ME.txt`. Os formulários continuam sem integração de captação.

Para atualizar o pacote a partir das páginas atuais, execute `python3 tools/build_elementor.py`. Os estilos são limitados ao widget, os IDs recebem prefixos, o divisor fica incorporado e as imagens usam URLs completas. As prévias simulam regras globais de tema; a instalação real no Elementor ainda deve ser conferida.
