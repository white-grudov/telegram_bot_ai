# Кодова частина курсової роботи Даніїла Білогрудова на тему "Розробка Telegram чат-боту з використанням штучного інтелекту"

Цей бот розроблений на мові Python з використанням фреймворку для розробки Telegram-ботів - `aiogram`. Чат-бот використовує різні методи обробки природньої мови (NLP) для виконання запитів користувачів. 

### Поточні можливості боту:

- **Розпізнавання намірів (Intent classification)**: бот визначає намір повідомлення за допомогою класифікатора намірів, який використовує пайплайн з двох кроків — `TfidfVectorizer` та `LinearSVC`. Наразі класифікатор намірів розпізнає чотири наміри: "weather request", "image search", "summarize" та "unknown".

- **Розпізнавання мови (Language classification)**: бот використовує класифікатор мов, який використовує пайплайн з двох кроків — `TfidfVectorizer` та `MultinomialNB`, щоб розпізнати мову, якою написаний запит. Класифікатор розпізнає 6 мов (англійська, українська, польська, іспанська, німецька, французька) та визначає, коли запит наданий мовою не вказаною вище.

- **Переклад запитів за допомогою DeepL API**: початкове повідомлення перекладається на англійську мову (якщо воно початково не було англійською), і далі обробка запиту виконується з перекладеним текстом англійською мовою. Коли відповідь готова, вона перекладається назад на мову початкового повідомлення. Переклад виконується за допомогою бібліотеки для використання DeepL API мовою Python.

- **Прогноз погоди**: користувач вводить запит на прогноз погоди природньою мовою ("Яка погода в Гельсінкі завтра?"), потім бот обробляє запит і витягує місце розташування ("Гельсінкі") за допомогою NER (Named Entity Recognition) і бібліотеки `flashgeotext`, дату прогнозу ("завтра") за допомогою бібліотеки dateparser, бот отримує прогноз за допомогою OpenWeatherAPI і повертає його користувачеві.

- **Пошук зображень**: користувач вводить запит на пошук зображень природньою мовою ("Знайти фото сплячого кота"), потім бот витягує тему пошуку ("сплячий кіт") за допомогою бібліотек `NLTK` і `SpaCy`, бот отримує зображення за допомогою Google Image Search API і надсилає зображення користувачеві.

- **Короткий переказ тексту**: користувач вводить повідомлення типу "Надай мені короткий переказ тексту", бот розпізнає намір "короткий переказ", скорочує текст за допомогою моделі, яка використовує бібліотеку `NLTK` і `TfidfVectorizer` з `scikit-learn` і повертає скорочений текст користувачеві.
