# Printer AR — Vídeo em Realidade Aumentada via QR Code

Experiência WebAR: a pessoa abre a página no navegador do celular (sem instalar app),
aponta a câmera para um **QR code impresso** e o conteúdo **aparece grudado no papel**,
acompanhando posição, escala e rotação.

Stack: [jsQR](https://github.com/cozmo/jsQR) + CSS transforms (100% web, sem dependência
de engine 3D). O QR faz dois papéis ao mesmo tempo: **identifica** o conteúdo e serve de
**âncora** para posicionar o overlay.

Há duas experiências nesta pasta:

| Página | O que faz |
|---|---|
| `index.html` | Catálogo de um produto (FLOW): vídeo, funcionalidades, plataforma, contato. |
| `ecossistema.html` | Backdrop 2026 "Ecossistema da Informação": 14 itens, um QR por bolinha. |

---

## Estrutura dos arquivos

```
printer-ar/
├── index.html          → a página AR (o que o QR code abre)
├── qr-generator.html   → gera o QR code a partir da sua URL
├── assets/
│   ├── target.mind     → (VOCÊ GERA) a imagem-alvo compilada
│   └── video.mp4       → (VOCÊ COLOCA) o vídeo que vai tocar
└── README.md
```

---

## Passo a passo

### 1. Prepare a imagem-alvo (a que será impressa)
Escolha a imagem que a pessoa vai apontar a câmera. Boas imagens-alvo têm:
- Muitos detalhes e contraste (fotos, ilustrações ricas).
- **Evite** imagens muito lisas, repetitivas ou com pouco contraste (ruins para rastrear).
- Proporção retangular clara.

### 2. Compile a imagem em um arquivo `.mind`
1. Acesse o compilador oficial: **https://hiukim.github.io/mind-ar-js-doc/tools/compile**
2. Arraste sua imagem, clique em **Start**, e depois **Download**.
3. Renomeie o arquivo baixado para **`target.mind`** e coloque em `assets/`.

> Dica: dá para ter várias imagens no mesmo `.mind`. Se usar mais de uma, ajuste
> `targetIndex` no `index.html` (0 = primeira imagem, 1 = segunda, etc.).

### 3. Adicione o vídeo
- Coloque seu vídeo em `assets/video.mp4`.
- Formato recomendado: **MP4 (H.264 + AAC)**, que toca em iOS e Android.
- Se o vídeo **não for 16:9**, ajuste `width` e `height` do `<a-video>` no `index.html`.
  A proporção é `height = width × (altura_video / largura_video)`.
  Ex.: vídeo quadrado 1:1 → `width="1" height="1"`. Vídeo 9:16 (vertical) → `width="1" height="1.777"`.

### 4. Publique no seu servidor (HTTPS obrigatório)
Suba a pasta `printer-ar/` para o seu servidor, sob uma URL **https://**.
A câmera **não funciona** em `http://` (só em `https://` ou `localhost`).
Ex.: `https://seudominio.com.br/ar/`

### 5. Gere o QR code
- Abra `qr-generator.html` no navegador.
- Cole a URL pública da página AR (a mesma do passo 4).
- Clique em **Gerar QR Code** → **Baixar PNG**.
- Use esse PNG na arte impressa da Printer.

---

## Detalhes de comportamento

- **Tela inicial "Iniciar experiência":** necessária porque navegadores exigem um toque do
  usuário antes de liberar câmera e áudio.
- **Som:** o vídeo começa **mudo** (exigência de autoplay no mobile). O botão 🔇 no canto
  superior direito ativa o áudio.
- **Play/Pause automático:** o vídeo toca quando a imagem é detectada e pausa quando some do enquadramento.

## Compatibilidade
- ✅ Android (Chrome), iOS 11+ (Safari).
- No iOS, o usuário **precisa abrir no Safari** (a câmera é bloqueada em alguns navegadores in-app,
  como o do Instagram/Facebook). Vale colocar um aviso "abra no Safari/Chrome" na arte.

---

## Ecossistema da Informação (`ecossistema.html`)

O ciclo de vida da informação do backdrop 2026, percorrido a pé. O padrão é sempre o
mesmo, em toda bolinha:

1. **Vídeo acima da bolinha** — e só isso ancorado ali;
2. **Os caminhos possíveis ficam animados**, irradiando da bolinha.

A pessoa então **segue um dos caminhos até o QR seguinte**. Chegando lá, o novo QR abre o
novo vídeo e anima os caminhos possíveis dali. E assim por diante, percorrendo o ciclo.

### Os caminhos apontam para o lugar certo do painel

Cada raio é desenhado na **direção real** que aquele caminho tem na arte impressa, não numa
posição decorativa. A constante `POS` no `ecossistema.html` guarda a coordenada de cada
bolinha em pontos do `backdrop.pdf`; a direção de cada seta sai da diferença entre as duas
coordenadas. Como o overlay já herda a rotação do QR, a seta acompanha o painel mesmo com
o celular torto.

- **Setas cheias, na cor do produto, apontando para fora** = caminhos de saída. É por aí
  que se segue.
- **Setas tracejadas, cinza, apontando para dentro** = de onde a informação veio.
- Cada seta traz o **nome do destino e a distância em cm** até ele.

> A distância vem de `BACKDROP_CM` (padrão: 300 cm de largura). Se o painel for impresso
> em outra medida, ajuste só essa constante — as **direções continuam certas** de qualquer
> jeito, muda apenas o número em cm.

### Sem autoplay

O vídeo **nunca começa sozinho**. Ele só toca quando um QR é reconhecido pela câmera, e
**pausa assim que o QR sai de quadro**. Abrir a página não dispara nada.

A única outra forma de tocar é o seletor de itens no rodapé, que exige um toque explícito
— é o modo de demonstração, para apresentar a experiência **sem o backdrop impresso em
mãos**. Junto dele fica a **ficha do item** (descrição e capacidades), fixa na tela e não
ancorada, porque texto que treme junto com o rastreio fica ilegível.

### Os 14 itens

`doc` · `scanner` · `multi` · `computador` · `airsafe` · `air` · `flow` · `cidadao` ·
`siga` · `descarte` · `rdc` · `nfc` · `impressora` · `print3d`

### Vídeos

Coloque cada vídeo em **`assets/eco/video/<id>.mp4`** — por exemplo `assets/eco/video/siga.mp4`.
Formato: **MP4 (H.264 + AAC)**, que toca em iOS e Android.

Se o arquivo de um item ainda não existir, **o player some sozinho** e a experiência segue
mostrando só o nome, o mini-diagrama e a ficha. Dá para publicar com uma parte dos vídeos
e ir completando depois, sem tocar no código.

### Ícones

Já estão em `assets/eco/icons/<id>.png`, recortados direto do PDF do backdrop — são
exatamente as mesmas bolinhas da arte impressa.

### Gerar os QR codes

```bash
python gen_qr_eco.py
```

Gera 14 PNGs em `qrcodes/eco/`, cada um já rotulado com o nome do item e com a barra
superior na cor do produto. **Antes de rodar, confira a constante `BASE`** no topo do
arquivo — ela precisa apontar para a URL pública onde o `ecossistema.html` foi publicado.

A página aceita três formatos de conteúdo no QR, então QRs antigos ou feitos à mão
também funcionam:

- `https://…/ecossistema.html?i=siga`
- `printer:eco:siga`
- `siga`

### Dicas para o impresso

- Um QR de **3 a 4 cm** já é lido com folga a um braço de distância.
- Deixe uma **margem branca** ao redor do QR (o gerador já inclui `border=3`).
- **Use sempre o mesmo deslocamento em relação à bolinha** — o QR logo abaixo dela, na
  mesma distância, em todos os 14 itens. Os caminhos animados nascem do centro do QR; se
  o QR estiver deslocado de um jeito diferente em cada item, as setas apontam torto.
- O vídeo nasce acima do QR. Evite encostar o QR no topo do painel, ou o vídeo fica alto
  demais para quem estiver de pé na frente dele.

---

## Auto-hospedar as bibliotecas (opcional, recomendado para produção)
O `index.html` carrega A-Frame e MindAR de CDN. Para não depender de CDN, baixe:
- `https://cdn.jsdelivr.net/npm/aframe@1.5.0/dist/aframe.min.js`
- `https://cdn.jsdelivr.net/npm/mind-ar@1.2.5/dist/mindar-image-aframe.prod.js`

Coloque em `assets/lib/` e troque os `src` no `<head>` para os caminhos locais.
