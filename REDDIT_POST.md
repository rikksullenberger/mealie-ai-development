# Reddit Post Draft for /r/Cooking

**Title:** I added AI Recipe & Image Generation to Mealie (Self-Hosted Recipe Manager) 🤖👨‍🍳

**Body:**

Hi everyone!

I've been a huge fan of [Mealie](https://mealie.io), the open-source self-hosted recipe manager. It's fantastic for planning meals and organizing recipes. However, I really wanted to integrate some modern AI features to make adding new ideas easier and to make my collection look better.

So, I built **Mealie AI** – an enhanced version of Mealie that integrates OpenAI (GPT-4o and DALL-E 3) to supercharge your recipe book.

### What’s New?

*   **✨ AI Recipe Generation:** Have an idea for a "Spicy Thai Basil Chicken" but don't have a recipe? Just type the name, and it will generate the full ingredients, steps, and description for you.
*   **🎨 AI Image Generation:** Missing photos for your imported recipes? One click (or a batch job) uses DALL-E 3 to create beautiful, appetizing images that match your recipe perfectly.
*   **🔒 Enhanced Security:** I've hardened the Docker image, patching several recent security vulnerabilities (in `urllib3`, system libraries, and Go) to keep your self-hosted setup safe.
*   **🛠️ Simple Setup:** It's packaged as a single Docker container. Just pop in your OpenAI API key and go.

### Is it free?
Yes and no. The software itself is **100% free and open-source** (AGPL-3.0). However, it uses your own OpenAI API key, so you pay OpenAI directly for what you use (usually pennies per recipe).

### Where can I get it?
*   **GitHub (Docs & Code):** [https://github.com/rikksullenberger/mealie-ai](https://github.com/rikksullenberger/mealie-ai)
*   **Docker Hub:** `rikksullenber/mealie-ai:latest`

### Massive Thanks
Huge credit goes to the original [Mealie team](https://github.com/mealie-recipes/mealie). This project is built on top of their incredible work. I just added the AI "sprinkles" on top of their delicious cake.

Let me know what you think or if you have any feature requests! Happy cooking! 🥘
