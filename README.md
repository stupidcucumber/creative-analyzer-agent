# Характеристики креативів

## Характеристики відео/зображень (AgentOutputContentCharacteristics)
Ця група полів аналізує структуру та психологічні тригери самого відео або зобреження.

1. Хук

`content_hook (Текст/концепція зачіпки)`: Перший елемент, що змушує користувача зупинити гортання стрічки (scroll-stopper). Зазвичай апелює до конкретної проблеми (наприклад, «соматичні вправи проти жиру на животі») або створює інтригу.

`content_hook_length_seconds (Тривалість зачіпки)`: Точний хронометраж початкового хука. Для утримання уваги це зазвичай короткий інтервал від 1 до 5 секунд, де чітко артикулюється головна цінність.

`content_hook_visual_format (Візуальний формат)`: Естетична подача хука. Визначає, що саме використовується: порівняння на розділеному екрані (split-screen), «живі» UGC-кадри (контент від звичайних користувачів) чи графічні інформаційні шари (overlays).

`content_hook_type (Тип хука)`: Психологічний механізм початку відео. Це може бути діагностичне питання про тіло користувача, парадоксальний/шокуючий факт або демонстрація швидкої трансформації «до/після».

`content_hook_emotional_valence (Емоційне забарвлення)`: Початковий емоційний настрій відео. Визначає, чи починається ролик з нагнітання проблеми («Біль/Роздратування»), чи одразу пропонує натхненне рішення («Прагнення до полегшення»).


2. Ціннісна пропозиція (Value)

`content_product_value_type (Тип цінності продукту)`: Головна обіцянка реклами («навіщо це мені?»). Фокусується на кінцевому результаті (трансформація) або на зручності стилю життя (наприклад, легкість виконання вправ без спортзалу).

`content_body_logic_type (Логіка викладу)`: Риторична стратегія для побудови довіри та подолання скепсису. Може використовувати освітній розбір (пояснення науки про кортизол/соматику) або соціальний доказ (результати реальних користувачів).

3. Заклик до дії (CTA)

`content_cta (Текст заклику до дії)`: Фінальна пряма вказівка чи команда наприкінці відео. Базується на терміновості або цікавості, наприклад: «Пройди тест», «Забери свій план на 28 днів» чи «Почни пробний період за $1».

`content_cta_type (Тип заклику до дії)`: Стратегічна класифікація цілі конверсії: переспрямування користувача на інтерактивну діагностику (квіз) чи на миттєве оформлення підписки/тріалу.

4. Загальні параметри

`pacing (Темп/Динаміка)`: Швидкість, з якою відео взаємодіє з користувачем і подає інформацію.

## Характеристики тексту публікації (AgentOutputPostTextCharacteristics)
Ця група аналізує копірайтинг — текст (caption), який супроводжує відео у публікації. Структура дублює логіку відео, але націлена на текстове сприйняття.

1. Текстовий хук (Post Hook)

`post_hook (Перший рядок)`: Текст-зачіпка на початку опису. Зазвичай це смілива заява або опис знайомої користувачу проблеми (наприклад, «Досить боротися зі своїм тілом»), мета якої — змусити натиснути кнопку «Читати далі» (See More).

`post_hook_type (Тип текстового хука)`: Риторична структура початку тексту. Наприклад, шокуючий факт про метаболізм або запитання, таргетоване на конкретний архетип (наприклад, «Для зайнятих професіоналів»).

`post_hook_emotional_valence (Емоційне забарвлення тексту)`: Точка емоційного входу. Часто починається з емпатичного опису болю чи втоми, щоб вибудувати зв'язок із читачем перед пропозицією рішення.

2. Цінність у тексті (Post Value)

`post_product_value_type (Тип цінності в тексті)`: Обіцянка, закладена в тілі тексту (наприклад, акцент на трансформації або на тому, що вправи можна робити «прямо в піжамі»).

`post_body_logic_type (Логіка текстового викладу)`: Аргументація та докази в тексті. Часто реалізується через списки (bullet points), що пояснюють фізіологічні чи психологічні переваги застосунку (наприклад, регуляція кортизолу).

4. Текстовий заклик до дії (Post CTA)

`post_cta (Текст фінальної інструкції)`: Фінальний заклик у тексті, часто підсилений емодзі та дедлайном, наприклад: «Тисни нижче, щоб дізнатися свій метаболічний вік ⬇️».

`post_cta_type (Тип текстового CTA)`: Категорія конверсії для тексту — перехід на проходження тесту (квізу) чи пряма конверсія на обмежену в часі пропозицію.

## Алгоритмічні метадані (AlgorithmicMetadata)
Технічні та статистичні параметри публікації, необхідні для системної аналітики та збереження в БД:

`published (Статус публікації)`: Чи було оголошення опубліковано (True/False).

`content_id (Ідентифікатор контенту)`: Унікальний числовий ID креативу.

`content_type (Тип контенту)`: Категорія контенту за внутрішньою класифікацією.

`content_format (Формат контенту)`: Опис формату (наприклад, розміри, співвідношення сторін або платформа).

`product (Продукт)`: Назва продукту або застосунку, який рекламується.

`date_published (Дата публікації)`: Дата, коли креатив став активним.

`reach (Охоплення)`: Кількість унікальних користувачів, які побачили цю рекламу.

`post_text (Повний текст)`: Весь текст публікації (копілефт) в оригінальному вигляді.

# Яку модель було обрано і чому?
Для цього демо я обрав Google (а не OpenAI, чи Claude) за його невисоку собівартість, а також різноманіття моделей, з якими можна попрацювати.

Я протестував декілька моделей від Google:

1. **Gemma 4 31B**. Повільний API, контексту як раз вистачає на промпт + зображення або промпт + відео, але не вистачає складності моделі для побудови закономірностей між заданими характеристиками та креативами. В результаті модель часто брала не ті частини тексту з посту, чи неправильно записувала, що було сказано у відео.
2. **Gemini 2.5 Flash Lite**. Швидка, багато контексту, що дозволяє аналізувати відео довжиною більше ніж 60 секунд. Має достатню складність для аналізу закономірностей між характеристиками та креативами. Модель себе гарно показала, працювала швидко, але були проблеми з Content Value Type, та розумінням коли і де треба поставити null.
3. **Gemini 2.5 Flash**. Все те саме, що і flash lite, але вона може будувати складніші логічні зв'язки. Показала себе найкраще, бо тепер є мінімальні проблеми з Content Value Type, а також модель на достатньо гарному рівні розуміє куди поставити null.

Отже я обрав `Gemini 2.5 Flash` за швидкодію, вартість та точність.

# Prompts для отримання характеристик креативів

## З чого складається промпт?

Промпт складається з двох головних частин:
1. Преамбула. Містить в собі загальні інструкції, як, наприклад, структура відповіді, роль, рекомендації по аналізу.
2. Функціональна частина. Вона дуже тісно пов'язана з самою структурою даних, яку ми записуємо в базу даних. Тут описується, що кожна колонка в таблиці означає, які значення вона може приймати і, що кожне з цих значень у свою чергу означає.

Чому так? Ця структура дозволяє бути гнучкою в інструкціях ЯК обробляти даних, але в той самий час вона строго описує те, ЩО ми хочемо отримати від моделі, чітко описуючи значення та приклади.  

## Як відбувалось покращення промтів?

Я відібрав 10 рандомних креативів (3 зображення та 7 відео), і запускав на кожному промпті LLM для аналізу. Далі я вручну перевіряв те, наскільки гарні були відповіді та будував гіпотези, далі я робив покращення та перевіряв, чи не стало краще.

### Відбір тестового датасету

Було відібрано 10% усього датасету як "тренування". Важливо було врахувати співвідношення зображень до відео, бо відео у нас набагато більше, тож треба і приділяти більше уваги. В результаті отримано 3 зображення та 7 відео.

### Версіонування промптів

Версіювання промптів відбувається за допомогою `prompt_{prompt_version}_{commit_hash}`. При цьому створюється окрема папка з назвою "prompts". 

Чому включати в це хеш коміту? Річ у тім, що функціональна частина промпту є частиною коду, що в даному випадку забезпечує `inheritent versioning` та дозволяє не хвилюватись, що десь лежить якийсь txt файл.

### Тестування промптів

Я спочатку думав, що передивлюсь вручну всі 10 відео, але після декількох ітерацій я зрозумів, що без експертної думки моя оцінка така ж сама, що й в LLM.

Якщо коротко, то я:
1. Проганяв модель на 10 рандомних креативах
2. Дивився де, як я думав вона помилилась
3. Будував гіпотези, чому так вийшло
4. Перевіряв гіпотезу, змінюючи щось

## Підсумування промптів

### Гарні сторони

1. Агент правильно ідентифікує CTA та Value в постах. Гарно витягує текст (Hook) з контенту.
2. Агент розуміє емоційне спрямування поста

### Негативні сторони

1. Агент іноді помиляється при визначенні довжини хуку. Мабуть це те, як всередині воно працює, LLM просто важко визначати довжину чогось.
2. Іноді агент неправильно визначає `pacing`. Наприклад відео '870873419302426.mp4' та '1433361945187888.mp4' мають одну і ту саму основну частину, але при цьому мають `repetitive_rhythmic` та `calm_mindful` відповідно. Мені здається, що проблема в промпті, і що можна замінити на якісь інші категорії, чи підтюнити скрипт.

## Приклади аналізу

### Нульовий приклад

```json
{
    "post_cta": "Tap today.",
    "post_cta_type": "direct_conversion",
    "post_product_value_type": "frictionless_ease",
    "post_body_logic_type": "objection_handling",
    "post_hook": "⏳ I kept waiting for the “right moment” — more time, more energy, maybe a gym. It never came.",
    "post_hook_type": "transformation",
    "post_hook_emotional_valence": "pain_agitation",
    "content_cta": "Tap now to start your transformation",
    "content_cta_type": "direct_conversion",
    "content_product_value_type": "transformation_outcome",
    "content_body_logic_type": "demonstration",
    "content_hook": "THE EASIEST WAY TO SHOCK EVERYONE WHO HASN'T SEEN YOU IN MONTHS.",
    "content_hook_length_seconds": 3,
    "content_hook_visual_format": "ugc",
    "content_hook_type": "transformation",
    "content_hook_emotional_valence": "aspirational_relief",
    "pacing": "high_energy_fast",
    "published": true,
    "content_id": 951064930588755,
    "content_type": "video",
    "content_format": "9:16",
    "product": "BetterMe",
    "date_published": "2026-03-07",
    "reach": 538897,
    "post_text": "⏳ I kept waiting for the “right moment” — more time, more energy, maybe a gym. It never came. \nWhat worked was BetterMe Calisthenics 👣 \n15 min I could actually keep up with 👉 \nBig change starts small 🚀 Tap today."
}
```

Все ідеально ідентифіковано.


### Перший приклад

```json
{
    "post_cta": "Rozwiąż 1-minutowy quiz 📊",
    "post_cta_type": "assessment_entry",
    "post_product_value_type": "hyper_personalization",
    "post_body_logic_type": "educational_teardown",
    "post_hook": "Osiągnij cele związane z mięśniami💪",
    "post_hook_type": "transformation",
    "post_hook_emotional_valence": "aspirational_relief",
    "content_cta": "KLIKNIJ EKRAN, ABY DOŁĄCZYĆ!",
    "content_cta_type": "'direct_conversion'",
    "content_product_value_type": "transformation_outcome",
    "content_body_logic_type": "objection_handling",
    "content_hook": "SZUKAMY DZIEWCZYN KTÓRE NIE ĆWICZYŁY REGULARNIE i chcą osiągnąć wymarzoną sylwetkę w 2026 roku",
    "content_hook_length_seconds": null,
    "content_hook_visual_format": null,
    "content_hook_type": "transformation",
    "content_hook_emotional_valence": "aspirational_relief",
    "pacing": null,
    "published": true,
    "content_id": 2099857124146357,
    "content_type": "image",
    "content_format": "9:16",
    "product": "BetterMe",
    "date_published": "2026-03-06",
    "reach": 734709,
    "post_text": "\"Osiągnij cele związane z mięśniami💪 \nTrzymaj się tego prostego planu, aby odnieść sukces: \n1. Rozwiąż 1-minutowy quiz 📊 \n2. Uzyskaj plan ćwiczeń i posiłków oparty na wadze, wzroście, wieku, codziennej aktywności i kondycji fizycznej📲 \n3. Postępuj zgodnie z programem 😎\""
}
```

Тут правильно було ідентифіковано все. 
1. Агент правильно проаналізував текст посту, ідентифікував `Rozwiąż 1-minutowy quiz 📊` як `assessment_entry` тип CTA.
2. Агент правильно визначив CTA контенту: `KLIKNIJ EKRAN, ABY DOŁĄCZYĆ!` та `direct_conversion` тип.
3. Агент правильно ідентифікував Hook `SZUKAMY DZIEWCZYN KTÓRE NIE ĆWICZYŁY REGULARNIE i chcą osiągnąć wymarzoną sylwetkę w 2026 roku` та тип хуку `transformation`.
4. Агент неправильно ідентифікував `content_hook_visual_format`. На мою думку воно має бути `cinematic`, бо це найближче серед усіх типів. Мабуть би я додав ще тип `photorealistic`. 

### Другий приклад

```json
{
    "post_cta": null,
    "post_cta_type": null,
    "post_product_value_type": "transformation_outcome",
    "post_body_logic_type": "educational_teardown",
    "post_hook": "Your body can become the equipment. Try Calisthenics.",
    "post_hook_type": "call_to_action",
    "post_hook_emotional_valence": "diagnostic_authority",
    "content_cta": "TAP THE SCREEN TO JOIN US",
    "content_cta_type": "direct_conversion",
    "content_product_value_type": "transformation_outcome",
    "content_body_logic_type": "demonstration",
    "content_hook": "IF YOU START CALISTHENICS ON MARCH 16TH YOU'LL BE UNRECOGNIZABLE BY MAY",
    "content_hook_length_seconds": 3,
    "content_hook_visual_format": "ugc",
    "content_hook_type": "transformation",
    "content_hook_emotional_valence": "aspirational_relief",
    "pacing": "high_energy_fast",
    "published": true,
    "content_id": 1888741965847477,
    "content_type": "video",
    "content_format": "9:16",
    "product": "BetterMe",
    "date_published": "2026-03-16",
    "reach": 1107501,
    "post_text": "Your body can become the equipment. Try Calisthenics.\n\nInstead of machines and weights, this 28-day plan teaches your body to move, hold, and build strength using its own resistance.\nYou’ll develop:\n💪 Stronger arms and shoulders\n🔥 A tight, active core\n🦵 Powerful legs and glutes\n⚡ Better balance and control\n\nYour 28-Day Calisthenics Plan\n🟢 Week 1: Learn foundational bodyweight moves\n🟢 Week 2: Build control and core stability\n🟢 Week 3: Increase strength and endurance\n🟢 Week 4: Move with power and confidence\n\n🏠 No equipment needed\n⏱ Short daily sessions\n💪 Strength built with your own body\n\n✨ When your body becomes the resistance, strength feels different."
}
```

1. Правильно ідентифіковано `ugc`, `pacing`, `content_product_value_type`, `content_body_logic_type`, `content_cta`, `content_cta_type` etc.
2. Є деяка проблема з `content_hook_length_seconds`, так як Агент сказав, що воно протягом 3 seconds, однак насправді вого протягом 5 seconds.

### Третій приклад

```json
{
    "post_cta": "Inizia la trasformazione ora!",
    "post_cta_type": "assessment_entry",
    "post_product_value_type": "hyper_personalization",
    "post_body_logic_type": "demonstration",
    "post_hook": "Raggiungi i tuoi obiettivi facilmente 💪",
    "post_hook_type": "transformation",
    "post_hook_emotional_valence": "aspirational_relief",
    "content_cta": "TOCCA PER PARTECIPARE",
    "content_cta_type": "direct_conversion",
    "content_product_value_type": "transformation_outcome",
    "content_body_logic_type": "objection_handling",
    "content_hook": "CERCHIAMO UOMINI che non si allenano da anni e vogliono diventare irriconoscibili nel 2026",
    "content_hook_length_seconds": null,
    "content_hook_visual_format": "cinematic",
    "content_hook_type": "transformation",
    "content_hook_emotional_valence": "aspirational_relief",
    "pacing": null,
    "published": true,
    "content_id": 1612214663311424,
    "content_type": "image",
    "content_format": "9:16",
    "product": "BetterMe",
    "date_published": "2026-03-06",
    "reach": 661560,
    "post_text": "Raggiungi i tuoi obiettivi facilmente 💪\n\n1️⃣ Fai un quiz di 1 minuto\n2️⃣ Ottieni un programma personalizzato\n3️⃣ Traccia i progressi e tieniti motivato\n4️⃣  Vedi risultati visibili in 4 settimane!\nInizia la trasformazione ora!"
}
```

1. Правильно ідентифіковано `content_hook_emotional_valence`, `content_hook_visual_format`, CTA, Value.

# Chat-bot Agent

## З чого складається?

Чат бот є `Directed Graph`, з наступними етапами:

0. Отримання питання від користувача через Телеграм (aiogram).
1. Аналіз поставленої задачі та генерація SQL.
2. Виконання SQL для отримання даних з БД.
3. Аналіз отриманих даних та співставлення з питанням користувача, та формування відповіді.
4. Відповідь через Телеграм (aiogram).

Для побудови агента було використано:

1. `LangChain` та `LangGraph`. Побудова графу та виклик `LLM`.
2. `aiogram`. Зручна бібліотека для написання інтерфейсу з телеграмом. 

## Приклади відповідей на обов'язкові питання

## Приклади відповідей на додаткові питання

# Які покращення можна зробити?

## Golden Set для автоматизованого тестування промпту

Як завжди відбувається в продукті, а це по-суті внутрішній продукт, де наші користувачі – маркетологи та аналітики, треба слухати кінцевого користувача. Найкраща порада так це витратити певний час, щоб зрозуміти:

1. Яка структура креативу? (Для розкриття моєї думки, я буду вважати, що будь-який креатив має "Хук", "Цінність", та "Заклик до дії").
2. Що може описувати "Хук"? Чи є якісь чіткі категорії, на які можна поділити "Хуки"?
3. Чи є якісь характеристики креативу, які не можна поділити на категорії?
4. Які питання найбільш поширені?

Я намагався відповісти на ці питання самотужки, запитуючи в Gemini та читаючи маркетингові пости, але як на мене у мене вийшли не такі гарні описи категорій, та їхніх значень. Однак маючи відповіді на ці питання від експертів ми можемо побудувати гарну функціональну частину нашого промпту. 

Далі треба продивитись мевні креативи та вручну розмітити їх за допомогою експертної оцінки. В подальшому цю розмітку можна використовувати як для дотренування якоїсь `SLM` (маленької Language Model), так і для тестування преамбули як `golden set`.

Намагатись підлаштувати преамбулу, щоб воно якомога краще відповідало `golden set`.

## Dagster для обробки та збереження даних

Я витратив час на побудову пайплайну для витягування метаданих та обробку відео. Я би для цього рекомендував використовувати `Dagster`, чи щось подібне. Використовуючи цей оркестратор можна буде розбити обробку, збереження та аналіз даних на окремі кроки, і повноцінно автоматизувати весь процес ще більше:

1. Завантаження креативу на `Google Drive` чи `Google S3`. Сенсор буде слідкувати, як тільки сенсор бачить, що було додано новий креатив, то ми його скачуємо на якийсь `Compute Service`.
2. На цьому Compute Service ми робимо аналіз креативу.
3. Аналіз креативу записуємо в `Elastic Search`, чи `BigQuery`.

Код стає простіше, обробка даних прозоріша, одразу можна побачити де і що іде не так.

## Logical Guardrails

Зазвичай промпт не є якимось законом для моделі, а скоріше він є "наставленням". Модель не зобов'язана його слухати і робить як заманеться. Поки я покращував промпти, то у мене ідея: додати якісь правила вже на структуровану відповідь, які ми називатимемо `logical guardrails`.

Наприклад, часто модель каже, що `post_cta=none`, водночас каже `post_cta_type="assessment_entry"`. Якщо вкінці ми додамо правило:
```py
analysis_object = llm.analyze(post)

if analysis_object.post_cta = None:
    analysis_object.post_cta_type = None
```

То це забезпечуватиме 100% того, що у нас CTA буде всюди Null, тож дані будуть "чистіше".
