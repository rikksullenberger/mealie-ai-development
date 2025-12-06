# OpenAI Integration

:octicons-tag-24: v1.7.0

Mealie's OpenAI integration enables several features and enhancements throughout the application. To enable OpenAI features, you must have an account with OpenAI and configure Mealie to use the OpenAI API key (for more information, check out the [backend configuration](./backend-config.md#openai)).

## Configuration

For most users, supplying the OpenAI API key is all you need to do; you will use the regular OpenAI service with the default language model. Note that while OpenAI has a free tier, it's not sufficiently capable for Mealie (or most other production use cases). For more information, check out [OpenAI's rate limits](https://platform.openai.com/docs/guides/rate-limits). If you deposit $5 into your OpenAI account, you will be permanently bumped up to Tier 1, which is sufficient for Mealie. Cost per-request is dependant on many factors, but Mealie tries to keep token counts conservative.

Alternatively, if you have another service you'd like to use in-place of OpenAI, you can configure Mealie to use that instead, as long as it has an OpenAI-compatible API. For instance, a common self-hosted alternative to OpenAI is [Ollama](https://ollama.com/). To use Ollama with Mealie, change your `OPENAI_BASE_URL` to `http://localhost:11434/v1` (where `http://localhost:11434` is wherever you're hosting Ollama, and `/v1` enables the OpenAI-compatible endpoints). Note that you *must* provide an API key, even though it is ultimately ignored by Ollama.

If you wish to disable image recognition features (to save costs, or because your custom model doesn't support them) you can set `OPENAI_ENABLE_IMAGE_SERVICES` to `False`. For more information on what configuration options are available, check out the [backend configuration](./backend-config.md#openai).

## OpenAI Features

Mealie AI includes powerful new features powered by OpenAI:

### 1. AI Recipe Generation
Generate complete recipes from just a name or description.
- **How to use**: Go to **Recipe > New Recipe**, select **Generate with AI**, enter a name (e.g., "Spicy Thai Basil Chicken"), and watch Mealie create the full recipe with ingredients and steps.

### 2. AI Image Generation
Automatically generate missing images for your recipes.
- **Single Recipe**: In the recipe editor, click the "Generate Image" button.
- **Batch Generation**: Go to **Maintenance > AI Tools** to scan your library for recipes without images and generate them in bulk.

### 3. Smart Import & Parsing
- **URL Import**: If standard scraping fails, OpenAI attempts to parse the page content.
- **Image Import**: Upload a photo of a cookbook page or handwritten card, and OpenAI will transcribe it.
- **Ingredient Parsing**: Use the "OpenAI Parser" to intelligently interpret complex ingredient strings.
