import type { ApiRequestInstance } from "../types/non-generated";

export interface SiteSettings {
    ai_provider?: string | null;

    openai_api_key?: string | null;
    openai_model?: string | null;
    openai_base_url?: string | null;

    google_api_key?: string | null;
    google_model?: string | null;

    smtp_host?: string | null;
    smtp_port?: number | null;
    smtp_user?: string | null;
    smtp_password?: string | null;
    smtp_from_name?: string | null;
    smtp_from_email?: string | null;
    smtp_auth_strategy?: string | null;
}

export class DetailedSettingsApi {
    constructor(private requests: ApiRequestInstance) { }

    public get() {
        return this.requests.get<SiteSettings>("/api/admin/detailed-settings");
    }

    public update(data: SiteSettings) {
        return this.requests.put<SiteSettings>("/api/admin/detailed-settings", data);
    }
}
