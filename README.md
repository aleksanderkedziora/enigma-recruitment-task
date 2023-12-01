# ECOMERCE TASK

1. **Uruchomienie:**

- Ze względu na zaimplementowaną, asynchroniczną obsługę maili, a co za tym idzie również instancji bazy Redis, zaleca
się uruchomienie aplikacji przy wykorzystaniu konteneryzacji Docker.

- W tym celu na maszynie na, której odbędzie się uruchomienie programu, uprzednio należy zainstalować Docker desktop,
chyba, że maszyna operuje na jądrze linuxa, wówczas krok ten można pominąć.

    ```bash
    https://www.docker.com/products/docker-desktop/
    ```

- Po zainstalowaniu Docker Desktop, środowisko budujemy za pomocą komendy
    
    ```bash
    docker-compose up
    ```
  lub
    ```bash
  docker-compose up -d
  ```
  
  jeśli chcemy by kontenery nie były przypięte do terminala

2. **Obsługa aplikacji:**

  - Przechodzimy do:

      ```bash
      localhost:80/api/docs/
      ```

  - W celu demonstacyjnym utworzono konto admin@example.com z hasłem admin
  - Konta utworzone przez niezalogowanego użytkownika to konta klienta
  - Konta utworzone przez admina to konta pracowników
  - Gdy jesteśmy zalogowani jako pracownik i dodamy nowe konto to utworzony zostanie nowe konto pracownika

3. **Alternatywne uruchomienie aplikacji:**

    Twórca niniejszej aplikacji nie zaleca opisywanego tu sposobu uruchomienia aplikcji, gdyż w zależności od systemu,
proces ten będzie się różnić.

- W niniejszym podejściu zalecane jest uruchomienie aplikcaji w IDE.
- Wymagane jest posiadanie zainstalowanego Redisa na maszynie, na której będzie uruchomiona aplikacja.
  - Należy uruchomić wirtualne środowisko, a następnie zainstlować wymagane biblioteki za pomocą komendy:
      ```bash
      pip install -r requirements.txt
      ```

      Następnie wykonać migracje:

      ```bash
      python manage.py migrate
      ```
     lub
     ```bash
      python3 manage.py migrate
      ```
      dalej w celu utworzenia konta administracyjnego

     ```bash
      python manage.py add_admin
      ```
  
      serwer uruchamiamy za pomocą:

      ```bash
      python manage.py runserver 8000
      ```
  
      należy również obsłużyć celery:
 
      ```bash
      celery -A config worker -l INFO
      celery -A config  beat -l INFO
      ```
    
4. **Dokumentacja:**
 - Dokumentacja została wykonana przy pomocy biblioteki drf-spectacular (Swagger). Dokumentacja pozwala na 
interaktywne przetestowanie wystawionych endpointów API.
