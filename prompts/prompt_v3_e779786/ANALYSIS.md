# How it changed from the previous one?

1. Removed CTA Urgency types. It was mostly rerdundant for this stage, and required quite a lot of research and refinement.
2. Changed CTA types (removed LEAD_GENERATION) and tuned descriptions a little bit.
3. Tuned Emotional Valence to be more in sync with BetterMe products.
4. Made descriptions of all characteristics to match the vibe of BetterMe.
5. Changed from `gemini-2.5-flash-lite` to `gemini-2.5-flash`.

# Improvements

## Content & Post Value
Model correctly marks most of the cases as "transformation_outcome" for values.

## Content & Post Hooks
All hooks is about transformation, so model was able to identify them as such. And also it was able to extract almost all hooks.

## Content & Post CTA
It correctly identified all "Call-to-Action" sequences for DIRECT_CONVERSION, like "Inizia la trasformazione ora!", "Tap now, your mat is waiting", "ESSAYEZ D\u00c8S MAINTENANT!", and even found ASSESMENT_ENTRY "Fai un quiz di 1 minuto". With almost all creatives being DIRECT_CONVERSION, which is what creatives must do.

## Valence
It correctly identified all valences.

# Downsides

## Content Value

Model still consideres creative to carry "transformation_outcome" rather than "frictionless_ease". For example, in `1575327530928091.jpg` model said it is "transformation_outcome", however:
1. *Removal of Location/Cost Barriers*: image explicitly states "Keine Fitnessstudio-Mitgliedschaft" (No gym membership), positioning the offer as a low-barrier alternative to traditional gyms.
2. *Minimal Time Commitment*: The ad highlights "15-minütige Home-Workouts" (15-minute home workouts), emphasizing that the program requires very little time and no travel.
3. *Psychological Ease*: By stating "kein Druck" (no pressure), the content targets individuals who find the intensity or social environment of a gym intimidating, promising a stress-free experience.
4. *Convenience*: The directive "zu Hause erreichen" (reach [goals] at home) reinforces the idea that the user can achieve results without changing their daily environment or buying specialized equipment.

## Content & Post CTA
Sometimes it says that there is no CTA (e.g. None), but at the same time assigns CTA Type.

## Content Inapplicable characteristics for images

Model outputs 3 seconds of hook, but the content is image. Same with pacing.

# Result

1. Tell model that if cta_type if none, then everything else connected to CTA is also none.
2. As for the inapplicable characteristics I do not think it is such a big problem, as we have "content_type" field in our database, so if we to know average time length for hooks we will just filter out all images. 
3. Since it is still struggling with `Content Value` type I would suggest model to pay closer attention to it in a preambula.