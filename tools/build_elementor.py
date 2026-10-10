"""Build paste-ready Elementor HTML widgets from the current static pages."""
from pathlib import Path
import re
import shutil
import zipfile
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'elementor'
ASSETS = 'https://verus-std.github.io/ana-grossi-black-friday/assets/'
CSS = (ROOT / 'styles.css').read_text()
CSS = re.sub(r'/\*.*?\*/', '', CSS, flags=re.S)
CSS = CSS.replace('body.modal-open{overflow:hidden}', '')
DIVIDER = 'data:image/svg+xml,' + quote((ROOT / 'assets/divisor.svg').read_text(), safe='')
CSS = CSS.replace("url('assets/divisor.svg')", f'url("{DIVIDER}")')
CSS = CSS.replace('assets/', ASSETS)


def scope_css(text, root):
    """Scope this project's simple rules and nested media queries without dependencies."""
    result = []
    pos = 0
    while pos < len(text):
        opening = text.find('{', pos)
        if opening == -1:
            assert not text[pos:].strip()
            break
        selector = text[pos:opening].strip()
        depth, end = 1, opening + 1
        while depth:
            if text[end] == '{':
                depth += 1
            elif text[end] == '}':
                depth -= 1
            end += 1
        content = text[opening + 1:end - 1]
        if selector.startswith('@media'):
            result.append(selector + '{\n' + scope_css(content, root) + '}\n')
        else:
            assert not selector.startswith('@'), selector
            selectors = []
            for item in selector.split(','):
                item = item.strip()
                if item in (':root', 'body', 'html'):
                    item = root
                elif item.startswith(('.capture-page', '.thanks-page')):
                    item = root + item
                else:
                    item = root + ' ' + item
                selectors.append(item)
            result.append(','.join(selectors) + '{' + content.strip() + '}\n')
        pos = end
    return ''.join(result)


BASE_RESET = '''
ROOT{display:block;position:relative;width:100%;max-width:none;margin:0;padding:0;text-align:left;font:400 16px/normal 'DM Sans',sans-serif;letter-spacing:normal;text-transform:none;isolation:isolate}
ROOT,ROOT *,ROOT *::before,ROOT *::after{box-sizing:border-box}
ROOT :where(h1,h2,h3,h4,p,ol,ul,figure){margin:0 0 1em;padding:0;color:inherit;font-family:inherit;letter-spacing:normal;text-transform:none}
ROOT :where(h1,h2,h3,h4){font-weight:700;line-height:1.2}
ROOT :where(button,input){font:inherit;box-shadow:none;text-shadow:none}
ROOT button{border-radius:0;text-decoration:none}
ROOT a{text-decoration:none;color:inherit}
ROOT img{max-width:100%;height:auto;border:0;box-shadow:none;border-radius:0}
ROOT svg{max-width:100%;flex-shrink:0}
ROOT strong{font-weight:700}
ROOT small{font-size:80%}
ROOT [hidden]{display:none!important}
'''

CAPTURE_JS = r'''
(() => {
  const root = document.currentScript.closest('.ag-widget');
  if (!root || root.dataset.agReady) return;
  root.dataset.agReady = 'true';
  const controller = new AbortController();
  const on = (node, event, handler) => node.addEventListener(event, handler, {signal: controller.signal});
  const $ = selector => root.querySelector(selector);
  const target = new Date(root.dataset.eventDate).getTime();
  const units = ['days', 'hours', 'minutes', 'seconds'].map(id => $('#ag-captura-' + id));
  const countdown = () => {
    const seconds = Math.max(0, Math.floor((target - Date.now()) / 1000));
    [Math.floor(seconds / 86400), Math.floor(seconds / 3600) % 24, Math.floor(seconds / 60) % 60, seconds % 60]
      .forEach((value, index) => { units[index].textContent = String(value).padStart(2, '0'); });
  };
  countdown();
  const timer = setInterval(countdown, 1000);
  const modal = $('#ag-captura-signup-modal');
  let previousFocus, savedOverflow;
  const unlock = () => {
    if (savedOverflow !== undefined) {
      document.body.style.overflow = savedOverflow;
      savedOverflow = undefined;
    }
  };
  const close = () => {
    modal.close();
    modal.hidden = true;
    unlock();
    if (previousFocus?.isConnected) previousFocus.focus();
  };
  root.querySelectorAll('[data-open-form]').forEach(button => on(button, 'click', () => {
    previousFocus = document.activeElement;
    savedOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    modal.hidden = false;
    modal.showModal();
    $('#ag-captura-name').focus();
  }));
  root.querySelectorAll('[data-close-form]').forEach(button => on(button, 'click', close));
  on(modal, 'cancel', event => { event.preventDefault(); close(); });
  on(modal, 'close', () => { modal.hidden = true; unlock(); });
  on($('#ag-captura-signup-form'), 'submit', event => {
    event.preventDefault();
    // Etapa visual: não envia nem armazena os dados. Integrar a captação antes do lançamento.
    window.location.assign(root.dataset.thankYouUrl);
  });
  // Impede envio nativo de dados caso scripts sejam removidos pelo WordPress.
  $('#ag-captura-signup-form button[type="submit"]').disabled = false;
  root.querySelectorAll('a[href^="#ag-captura-"]').forEach(link => on(link, 'click', event => {
    const target = $(link.getAttribute('href'));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
  }));
  // Libera listeners e contador se o Elementor reconstruir o widget no editor.
  const observer = new MutationObserver(() => {
    if (root.isConnected) return;
    clearInterval(timer); controller.abort(); unlock(); observer.disconnect();
  });
  observer.observe(document.body, {childList: true, subtree: true});
})();
'''

THANKS_JS = r'''
(() => {
  const root = document.currentScript.closest('.ag-widget');
  if (!root || root.dataset.agReady) return;
  root.dataset.agReady = 'true';
  root.querySelectorAll('[data-capture-link]').forEach(link => { link.href = root.dataset.captureUrl; });
  root.querySelectorAll('[data-whatsapp-group]').forEach(button => {
    button.addEventListener('click', () => {
      if (root.dataset.whatsappUrl.trim()) {
        window.location.assign(root.dataset.whatsappUrl.trim());
      } else {
        root.querySelector('#ag-obrigado-group-dialog').showModal();
      }
    });
  });
})();
'''


def build(source, name, page_class, config, script):
    prefix = 'ag-' + name
    root = '#' + prefix
    html = (ROOT / source).read_text()
    fonts = re.search(r'<link href="https://fonts.googleapis.com/[^>]+>', html).group()
    body = re.search(r'<body[^>]*>(.*?)</body>', html, re.S).group(1).strip()
    for old in re.findall(r'\bid="([^"]+)"', body):
        body = body.replace(f'id="{old}"', f'id="{prefix}-{old}"')
        body = body.replace(f'for="{old}"', f'for="{prefix}-{old}"')
        body = body.replace(f'aria-labelledby="{old}"', f'aria-labelledby="{prefix}-{old}"')
        body = body.replace(f'href="#{old}"', f'href="#{prefix}-{old}"')
    body = body.replace('src="assets/', f'src="{ASSETS}')
    if name == 'captura':
        body = body.replace('<div class="modal"', '<dialog aria-labelledby="ag-captura-modal-title" class="modal"')
        body = re.sub(r'</div>\s*$', '</dialog>', body)
        body = body.replace(' role="dialog" aria-modal="true" aria-labelledby="ag-captura-modal-title"', '')
        body = body.replace('action="obrigado.html"', 'action="/obrigado/"')
        body = body.replace('type="submit"', 'type="submit" disabled')
    else:
        body = body.replace('href="index.html"', 'href="/black-friday/" data-capture-link')
    css = BASE_RESET.replace('ROOT', root) + scope_css(CSS, root)
    if name == 'captura':
        css += f'{root} .modal{{width:100%;max-width:none;height:100%;max-height:none;margin:0;border:0;background:transparent;color:var(--ink)}}\n'
        css += f'{root} .modal::backdrop{{background:transparent}}\n'
    widget = f'''<!-- ANA GROSSI — Cole TODO este arquivo em um único widget HTML do Elementor.
Configuração: altere somente os endereços abaixo conforme o seu WordPress.
Imagens hospedadas no GitHub Pages; podem ser substituídas pelas URLs da Biblioteca de Mídia.
-->
<div id="{prefix}" class="ag-widget {page_class}" lang="pt-BR"
  {config}>
{fonts}
<style>
{css}</style>
{body}
<script>
{script}</script>
</div>
'''
    (OUT / f'{name}-widget.txt').write_text(widget)
    # Local preview has typical broad theme styles, to check widget style isolation.
    preview = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Ana Grossi — prévia {name} Elementor</title><style>body{{margin:0;font-family:serif}}h1,h2,h3{{color:blue;font-family:serif}}button{{background:purple;border-radius:99px}}img{{border-radius:40px}}.elementor-widget-container{{width:100%;padding:0}}</style></head><body><div class="elementor-widget-container">{widget}</div></body></html>'''
    preview = preview.replace('data-thank-you-url="/obrigado/"', 'data-thank-you-url="previa-obrigado.html"').replace('data-capture-url="/black-friday/"', 'data-capture-url="previa-captura.html"')
    (OUT / f'previa-{name}.html').write_text(preview)


OUT.mkdir(exist_ok=True)
build('index.html', 'captura', 'capture-page', 'data-thank-you-url="/obrigado/"\n  data-event-date="2026-11-04T20:00:00-03:00"', CAPTURE_JS)
build('obrigado.html', 'obrigado', 'thanks-page', 'data-capture-url="/black-friday/"\n  data-whatsapp-url=""', THANKS_JS)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
with zipfile.ZipFile(OUT / 'ana-grossi-elementor.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.suffix != '.zip':
            archive.write(path, path.relative_to(OUT))
print('Widgets gerados em', OUT)
