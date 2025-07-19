# 🚀 Szybkie Wdrożenie Przykładów AI

Przewodnik krok po kroku do uruchomienia przykładów Gemini, GPT-4 i Claude-3 w środowisku Langflow + Open WebUI.

## 📋 Wymagania

- Docker i Docker Compose
- Klucze API dla wybranych modeli:
  - **Gemini**: Google AI Studio API Key
  - **GPT-4o**: OpenAI API Key  
  - **Claude-3.5**: Anthropic API Key

## 🎯 Instalacja i Uruchomienie

### 1. Uruchom Środowisko

```bash
# Sklonuj repozytorium (jeśli nie masz jeszcze)
git clone <repo-url>
cd langflow-ui

# Uruchom wszystkie serwisy
./setup-openwebui.sh
```

Poczekaj aż wszystkie serwisy będą gotowe. Sprawdź dostępność:
- 🌐 Open WebUI: http://localhost:3000
- 🔧 Langflow: http://localhost:7860

### 2. Zaimportuj Przykład do Langflow

**Opcja A: Import z pliku JSON**
1. Otwórz http://localhost:7860
2. Kliknij **"New Flow"** → **"Upload"**
3. Wybierz plik z katalogu `catalog/flows/`:
   - `gemini-chat-basic.json` - dla Gemini
   - `gpt4-chat-basic.json` - dla GPT-4o
   - `claude3-chat-basic.json` - dla Claude-3.5

**Opcja B: Kopiowanie pipeline**
1. Skopiuj odpowiedni pipeline z `catalog/pipelines/` do głównego katalogu `pipelines/`
2. Zrestartuj serwis pipelines: `docker-compose restart pipelines`

### 3. Skonfiguruj Klucze API

Po zaimportowaniu przepływu w Langflow:

1. Kliknij na komponent AI (Gemini/GPT/Claude)
2. W panelu po prawej znajdź pole **"API Key"**
3. Wpisz swój klucz API
4. Kliknij **"Save"** lub **Ctrl+S**

### 4. Przetestuj Przepływ

**W Langflow:**
1. Kliknij **"Playground"** w prawym dolnym rogu
2. Napisz wiadomość testową, np. "Cześć, jak się masz?"
3. Kliknij **"Run"** i sprawdź czy otrzymujesz odpowiedź

**W Open WebUI:**
1. Otwórz http://localhost:3000
2. Napisz: `@flow:nazwa-endpoint-u Twoja wiadomość`
   - Przykład: `@flow:gemini-chat-basic Opowiedz mi o AI`

## 🔧 Dostosowywanie

### Zmiana Modelu AI

**Gemini:**
- `gemini-pro` - podstawowy model
- `gemini-1.5-pro-latest` - najnowszy (domyślny)
- `gemini-1.5-flash-latest` - szybszy model

**GPT-4o:**
- `gpt-4o` - najnowszy (domyślny)
- `gpt-4-turbo` - alternatywa
- `gpt-4o-mini` - tańsza wersja

**Claude-3.5:**
- `claude-3-5-sonnet-20240620` - najnowszy (domyślny)
- `claude-3-opus-20240229` - najinteligentniejszy
- `claude-3-haiku-20240307` - najszybszy

### Dostosowanie System Message

W każdym przepływie można zmienić wiadomość systemową:
1. Kliknij na komponent AI
2. Znajdź pole **"System Message"**
3. Zmień na swoją instrukcję, np.:
   ```
   Jesteś ekspertem od programowania. 
   Odpowiadaj konkretnie z przykładami kodu.
   ```

### Zmiana Parametrów

**Temperature (0.0-1.0):**
- `0.1` - bardzo konserwatywne odpowiedzi
- `0.7` - bardziej kreatywne (domyślne)
- `1.0` - bardzo kreatywne

**Max Tokens:**
- `512` - krótkie odpowiedzi
- `1024` - średnie odpowiedzi (domyślne)
- `2048` - długie odpowiedzi

## 🐛 Rozwiązywanie Problemów

### Błąd "API Key not found"
1. Sprawdź czy wprowadziłeś poprawny klucz API
2. Sprawdź czy klucz ma odpowiednie uprawnienia
3. Upewnij się, że zapisałeś przepływ po wprowadzeniu klucza

### Błąd "Connection Error"
1. Sprawdź czy wszystkie serwisy działają: `docker-compose ps`
2. Sprawdź logi: `docker-compose logs langflow`
3. Zrestartuj serwisy: `docker-compose restart`

### Brak odpowiedzi z modelu
1. Sprawdź logi Langflow: `docker-compose logs -f langflow`
2. Przetestuj bezpośrednio w Langflow Playground
3. Sprawdź czy model jest dostępny w danym regionie

### Pipeline nie działa w Open WebUI
1. Sprawdź czy pipeline jest w katalogu `pipelines/`
2. Zrestartuj pipelines: `docker-compose restart pipelines`
3. Sprawdź logi: `docker-compose logs -f pipelines`

## 💡 Wskazówki Pro

1. **Kopiuj ID przepływu** z Langflow URL po zapisaniu
2. **Używaj różnych endpoint_name** dla różnych wersji
3. **Testuj zawsze w Playground** przed użyciem w Open WebUI
4. **Monitoruj logi** podczas pierwszego uruchomienia
5. **Używaj Docker volumes** do zachowania danych

## 🔄 Aktualizacje

Aby zaktualizować obrazy Docker:
```bash
docker-compose pull
docker-compose up -d
```

## 📞 Pomoc

- **Logi serwisów**: `docker-compose logs -f [service-name]`
- **Status serwisów**: `docker-compose ps`
- **Restart wszystkich**: `docker-compose restart`
- **Reset danych**: `./setup-openwebui.sh --clean`

---

**Potrzebujesz pomocy?** Sprawdź główny [README.md](../../README.md) lub logi serwisów.