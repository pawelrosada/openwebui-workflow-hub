# 📚 Katalog Przykładów Langflow

Ten katalog zawiera gotowe przykłady przepływów Langflow, które można zaimportować i używać bezpośrednio w środowisku Langflow + Open WebUI.

## 🤖 Dostępne Przykłady AI

### 1. **Gemini Pro Chat** (`gemini-chat-basic.json`)
- **Model**: Google Gemini Pro (najnowsza wersja)
- **Architektura**: Chat Input → Gemini → Chat Output
- **Użycie**: Podstawowy chat z Google Gemini
- **Pipeline**: `gemini_chat_pipeline.py`

### 2. **GPT-4 Chat** (`gpt4-chat-basic.json`)
- **Model**: OpenAI GPT-4 (najnowsza wersja)
- **Architektura**: Chat Input → OpenAI GPT → Chat Output
- **Użycie**: Podstawowy chat z GPT-4
- **Pipeline**: `gpt4_chat_pipeline.py`

### 3. **Claude-3 Chat** (`claude3-chat-basic.json`)
- **Model**: Anthropic Claude-3 (najnowsza wersja)
- **Architektura**: Chat Input → Claude → Chat Output
- **Użycie**: Podstawowy chat z Claude-3
- **Pipeline**: `claude_chat_pipeline.py`

## 🚀 Jak Używać Przykładów

### Import do Langflow
1. Uruchom środowisko: `./setup-openwebui.sh`
2. Otwórz Langflow: http://localhost:7860
3. Kliknij "Import" lub "Load Flow"
4. Wybierz plik JSON z katalogu `flows/`
5. Skonfiguruj klucze API dla wybranego modelu
6. Zapisz i uruchom przepływ

### Użycie w Open WebUI
1. Skopiuj ID przepływu z Langflow
2. W Open WebUI napisz: `@flow:your-flow-id Twoja wiadomość`
3. Pipeline automatycznie przekieruje do odpowiedniego modelu AI

### Konfiguracja Pipeline
1. Skopiuj odpowiedni plik pipeline z `pipelines/`
2. Zaktualizuj `WORKFLOW_ID` w pliku pipeline
3. Zrestartuj serwis pipelines: `docker-compose restart pipelines`

## 🔧 Struktura Kataloga

```
catalog/
├── README.md                          # Ten plik
├── flows/                            # Pliki JSON do importu
│   ├── gemini-chat-basic.json       # Przykład Gemini
│   ├── gpt4-chat-basic.json         # Przykład GPT-4
│   └── claude3-chat-basic.json      # Przykład Claude-3
└── pipelines/                       # Skrypty integracyjne
    ├── gemini_chat_pipeline.py      # Pipeline dla Gemini
    ├── gpt4_chat_pipeline.py        # Pipeline dla GPT-4
    └── claude_chat_pipeline.py      # Pipeline dla Claude
```

## 🔑 Wymagane Klucze API

Aby używać przykładów, potrzebujesz kluczy API:

- **Gemini**: Google AI Studio API Key
- **GPT-4**: OpenAI API Key
- **Claude-3**: Anthropic API Key

Skonfiguruj je w zmiennych środowiskowych lub bezpośrednio w Langflow.

## 💡 Wskazówki

- **Każdy przykład** to kompletny, funkcjonalny przepływ
- **Pojedyncze użycie AI** - jeden model na przepływ
- **Najnowsze modele** - używamy najnowszych wersji każdego AI
- **Proste integracje** - skupiamy się na podstawowym chat flow

## 🛠️ Rozszerzanie

Możesz łatwo rozszerzyć te przykłady:
- Dodać preprocessing tekstu
- Zintegrować z bazami danych
- Dodać memory/historię konwersacji  
- Połączyć z zewnętrznymi API

---

*Więcej dokumentacji: [README główny](../README.md)*