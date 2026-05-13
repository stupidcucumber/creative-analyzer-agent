# creative-analyzer-agent
RAG + ChatBOT that analyzes performance of various creatives.

## How to run this?


## General Information

### Key Characteristics of the Creative
Let's derive our key characteristics of a creative more abstractly.

|Name|Description|
|----|-----------|
|Hook|What was used to stop user from scrolling further?|
|Value|How creative shows value to its viewers?|
|Call to action|How creative makes user to do something?|

Now what will constitute an entry in our database?
1. Hook:
    1) Hook Type (Call-Out, Pattern Interrupt, Negative, Social Proof, Specific Result)
    2) Hook Text (I will use Gemini STT model to extract subtitles from the video)
    3) Hook Emotional Valence (Positive, Negative, Neutral, Educational)
    4) Hook Length (If applicable)
    5) Hook POV (First-person, Direct address, Third-person)
    6) Hook Visual Format (UGC, Studio/Cinematic, Motion Graphics)
2. Value:
    1) Value Type (Educational/Informational, Entertainment, Transformational, Economic)
    2) Proof Of Value (Demonstration, Social Proof, Authority/Credentials, Before vs. After)
    3) Barrier Reduction
    4) Value POV (First-person, Direct address, Third-person)
4. Call to Action:
    1) CTA Urgency/Scarcity (Time-Bound, Quantity-Bound) 
    2) CTA Text
    3) CTA Type (Direct, Soft/Low-Friction, Instructional)
5. Other metadata:
    1) Date of publication
    2) Reach
    3) Content Type (Video, Image)
    4) Content format (9:16, 1:1, 4:5, etc.)
    5) Content language
    6) Ad text

Other columns that might be helpful:
1. Hook-Body Bridge Type. How do you transition from Hook to Body?
2. Value Barrier Reduction. Why is it so easy about the product that it is valuable?


### Чат-бот повинен відповідати на запитання, спираючись на базу даних проаналізованих креативів. Обов'язкові запитання:
1. "Сформуй список найкращих хуків за останній тиждень" — топ хуки за reach серед креативів, завантажених за останні 7 днів.
2. "Сформуй список нових хуків за останній тиждень, яких не було до цього" — хуки, які вперше з'явились у нових креативах і не зустрічались раніше.
3. "Сформуй ідеальний креатив на основі даних" — агент аналізує кореляцію між атрибутами та reach і генерує опис найефективнішого можливого креативу.
4. "Які формати показують найкращий reach цього місяця?" — порівняння відео vs зображення, 9:16 vs 1:1 тощо.
5. "Покажи тренди: що змінилось у підходах за останні 2 тижні порівняно з попередніми?"
6. (Custom question) "Які емоції отримали найвищий reach за останні 2 тижні?"
7. (Custom question) "Який proof-of-value має найгірший reach?"
(Власне питання кандидата — заохочується додати 1–2 власних)


### Methodology & testing
1. Separate 15 samples from the data (make it so ratio of images/videos will be the same as in the training data, and the same as in the whole dataset).
2. Semi-manually annotate those 15 samples by first annotating them with a simple prompt, and then correct any errors in the data. At this point Database scheme must be ready.
3. Define metrics that are crucial for prompt quality. Then test prompt and save results in the database.


## Technical Information

### Database

### Prompt evolution

1. prompt_v0.txt included only basic instructions like persona and task.
2. prompt_v1.txt added "CRITICAL INSTRUCTIONS FOR OUTPUT", which helps LLM to structure output better. Like in what format it must provide and what to put if there is no CTA in the post/content.

## Improvements


### Prompt


### Access to more in-depth analytics


### Storage
Change from Google Drive to S3 storage. Right now to analyze anything you need to download creatives first to your local machine, and then upload to Google Gemini, or any other neural network through FileAPI. Which is slow, and can be a speed bottleneck in the future.

S3 storage, for example, allows flagship Google Models like Gemini access files right away without the need of spending minutes to upload a sequence of creatives.
