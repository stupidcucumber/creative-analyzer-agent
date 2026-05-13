import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import numpy as np
from pathlib import Path


async def extract_facebook_ad_text(url: str) -> None | str:
    async with async_playwright() as p:
        # Launching browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print(f"Loading page: {url}")
        await page.goto(url, wait_until="networkidle")

        # 1. Wait for the content to hydrate (the 5-second rule)
        print("\tWaiting for dynamic content to render...")
        await page.wait_for_timeout(10000)

        # 2. Execute the extraction script in the browser context
        # This script filters for spans that:
        # - Are NOT inside the 'mount' container
        # - Contain ONLY text nodes or <br> tags
        # - Are not empty strings
        extraction_logic = """
        () => {
            // Target the mount container using a partial ID match for stability
            const forbiddenContainer = document.querySelector('[id^="mount_0_0_"]');
            const spans = Array.from(document.querySelectorAll('span'));
            
            return spans
                .filter(span => {
                    // Rule 1: Omit if inside the specific mount div
                    if (forbiddenContainer && forbiddenContainer.contains(span)) {
                        return false;
                    }

                    // Rule 2: Ensure it has child nodes
                    const children = Array.from(span.childNodes);
                    if (children.length === 0) return false;
                    
                    // Rule 3: Every child MUST be a Text Node (3) or a BR element (1 + tagName BR)
                    const onlyTextOrBr = children.every(node => 
                        node.nodeType === 3 || (node.nodeType === 1 && node.tagName === 'BR')
                    );

                    // Rule 4: Clean up whitespace and ensure it's not an empty string
                    const textContent = span.innerText.trim();
                    const hasActualContent = textContent.length > 0;
                    
                    return onlyTextOrBr && hasActualContent;
                })
                .map(span => span.innerText.trim());
        }
        """

        results = await page.evaluate(extraction_logic)

        # 3. Output results
        print(f"\tSuccessfully extracted {len(results)} elements:")
        
        # Using a set to remove potential duplicates if the same span is nested
        unique_results = list(dict.fromkeys(results))
        text_of_interest = None
        
        for i, text in enumerate(unique_results, 1):

            if len(text) > 50:

                print(f"\t--- Element {i} ---")
                print("\t", text.replace("\n", " "))
                print("\t-" * 30)

                text_of_interest = text

        await browser.close()

    return text_of_interest 


async def extract_creatives_of_interest() -> pd.DataFrame:
    creatives_folder = Path("data/BetterMe Creatives")
    data = pd.read_csv("data/BetterMe Creatives.csv")

    creatives_ids = []

    for creative_path in creatives_folder.glob("*"):
        creative_id = int(creative_path.stem)
        creatives_ids.append(creative_id)

    return data[[creative_id in creatives_ids for creative_id in data["id"]]]


async def main() -> None:

    creatives_data = await extract_creatives_of_interest()
    creatives_data["ad_text"] = [None] * len(creatives_data)

    for row_id, ad_id, product, ad_creation_time, reach, ad_link, _ in creatives_data.itertuples(index=True, name=None):

        try:
            ad_text = await extract_facebook_ad_text(url=ad_link)
        
        except Exception as e:
            print(f"Caught an error: {e}")
            ad_text = f"ERROR: {e}"
        
        creatives_data.loc[row_id, "ad_text"] = ad_text

        await asyncio.sleep((np.random.random() + 1) * 2)
    
    creatives_data.to_csv("data/BetterMe Creatives_clean+text.csv", index=False)
    

if __name__ == "__main__":
    asyncio.run(main())