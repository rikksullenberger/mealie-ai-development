import { defineNuxtPlugin } from "#app";

export default defineNuxtPlugin((nuxtApp) => {
    const RELOAD_KEY = "chunk_load_error_reload";

    nuxtApp.hook("app:error", (error) => {
        // Check if the error is a ChunkLoadError
        if (isChunkLoadError(error)) {
            handleChunkError();
        }
    });

    // Also catch window errors that might sneak past Nuxt
    if (import.meta.client) {
        window.addEventListener("error", (event) => {
            if (isChunkLoadError(event.error)) {
                handleChunkError();
            }
        });
    }

    function isChunkLoadError(error: any): boolean {
        if (!error) return false;
        const message = error.message || "";
        return (
            message.includes("Failed to fetch dynamically imported module") ||
            message.includes("Importing a module script failed") ||
            error.name === "ChunkLoadError"
        );
    }

    function handleChunkError() {
        const isReloaded = sessionStorage.getItem(RELOAD_KEY);

        if (!isReloaded) {
            // Set the flag so we don't reload indefinitely if the error persists
            sessionStorage.setItem(RELOAD_KEY, "true");
            console.warn("Chunk load error detected. Reloading page...");
            window.location.reload();
        } else {
            console.error(
                "Chunk load error detected, but page was already reloaded. Stopping loop."
            );
            // Optional: Clear the flag after a delay or let the user manually refresh
            // For now, let's clear it after a decent interval so if they come back later it works
            setTimeout(() => {
                sessionStorage.removeItem(RELOAD_KEY);
            }, 60000); // 1 minute
        }
    }

    // Clear the flag on successful navigation to reset the safety mechanism
    const router = useRouter();
    router.afterEach(() => {
        sessionStorage.removeItem(RELOAD_KEY);
    });
});
