# Printer AR — Vídeo em Realidade Aumentada via QR Code

Experiência WebAR de **image tracking**: a pessoa escaneia o QR code, abre a página no
navegador do celular (sem instalar app), aponta a câmera para uma **imagem impressa** e o
**vídeo aparece grudado na imagem**, acompanhando o papel.

Stack: [MindAR](https://hiukim.github.io/mind-ar-js-doc/) + [A-Frame](https://aframe.io/) (100% web).

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

## Auto-hospedar as bibliotecas (opcional, recomendado para produção)
O `index.html` carrega A-Frame e MindAR de CDN. Para não depender de CDN, baixe:
- `https://cdn.jsdelivr.net/npm/aframe@1.5.0/dist/aframe.min.js`
- `https://cdn.jsdelivr.net/npm/mind-ar@1.2.5/dist/mindar-image-aframe.prod.js`

Coloque em `assets/lib/` e troque os `src` no `<head>` para os caminhos locais.
