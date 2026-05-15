# Improvements

## Content appropriate characteristics for images

Now if it is an image, model will mark pacing and time of the hook as none.

## PostCTA

Now if CTA is none, then CTA_type is also none.

## Body logic

Sometimes model will mark body logic as none and at first I thought it is some kind of an error:

```json
{
    ...,
    "post_product_value_type": "hyper_personalization",
    "post_body_logic_type": null,
    ...,
    "post_text": "Hai intenzione di iniziare il digiuno intermittente? Ottieni un piano di allenamento e alimentare personalizzato! \ud83c\udf4e\ud83e\udd51"
}
```

But if you look closely at the text:
```txt
(original)
Hai intenzione di iniziare il digiuno intermittente? Ottieni un piano di allenamento e alimentare personalizzato! \ud83c\udf4e\ud83e\udd51

(translation)
Are you planning to start intermittent fasting? Get a personalized workout and nutrition plan! \ud83c\udf4e\ud83e\udd51
```

It really does not have any body logic. It does not deponstrate anything, or even educate viewer. Before prompt improvement model did't catch this, but now it can see where in posts body logic is missing.

# Downsides

## Video pacing
Since I said that image pacing is `none` it now can even set video pacing as `none`:

```json
{
    "post_cta": "Ottieni un piano di allenamento e alimentare personalizzato! \ud83c\udf4e\ud83e\udd51",
    "post_cta_type": "assessment_entry",
    "post_product_value_type": "hyper_personalization",
    "post_body_logic_type": null,
    "post_hook": "Hai intenzione di iniziare il digiuno intermittente?",
    "post_hook_type": "question",
    "post_hook_emotional_valence": "diagnostic_authority",
    "content_cta": "TOCCA LO SCHERMO PER PARTECIPARE!",
    "content_cta_type": "community_engagement",
    "content_product_value_type": "transformation_outcome",
    "content_body_logic_type": "demonstration",
    "content_hook": "Ok, ragazze! Luned\u00ec 16 marzo sta per iniziare la nostra Sfida di Digiuno Intermittente",
    "content_hook_length_seconds": null,
    "content_hook_visual_format": "motion_graphics",
    "content_hook_type": "call_to_action",
    "content_hook_emotional_valence": "aspirational_relief",
    "pacing": null,
    "published": true,
    "content_id": 1007763421578293,
    "content_type": "video",
    "content_format": "9:16",
    "product": "BetterMe",
    "date_published": "2026-03-13",
    "reach": 455945,
    "post_text": "Hai intenzione di iniziare il digiuno intermittente? Ottieni un piano di allenamento e alimentare personalizzato! \ud83c\udf4e\ud83e\udd51"
}
```

Upon closer inspection it turns out that video is a dynamic image, so I guess model decided to put pacing to none just because content resembles image, and the instructions were *to set pacing to none if the content is image*.

I do not think it is a big problem, considering that it really hard to apply pacing to the dynamic images.


# Result
Given enough time some things can be improved, but prompt is good as is on a test set, so we move to the annotating all dataset.