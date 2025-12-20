<template>
  <v-container
    fluid
    class="narrow-container"
  >
    <!-- Image -->
    <BasePageTitle divider>
      <template #header>
        <v-img
          width="100%"
          max-height="200"
          max-width="150"
          src="/svgs/admin-site-settings.svg"
        />
      </template>
      <template #title>
        {{ $t("settings.site-settings") }}
      </template>
    </BasePageTitle>

    <!-- Bug Report -->
    <BaseDialog
      v-model="bugReportDialog"
      :title="$t('settings.bug-report')"
      :width="800"
      :icon="$globals.icons.github"
    >
      <v-card-text>
        <div class="pb-4">
          {{ $t('settings.bug-report-information') }}
        </div>
        <v-textarea
          v-model="bugReportText"
          variant="outlined"
          rows="18"
          readonly
        />
        <div
          class="d-flex justify-end"
          style="gap: 5px"
        >
          <BaseButton
            color="gray"
            secondary
            target="_blank"
            href="https://github.com/mealie-recipes/mealie/issues/new/choose"
          >
            <template #icon>
              {{ $globals.icons.github }}
            </template>
            {{ $t('settings.tracker') }}
          </BaseButton>
          <AppButtonCopy
            :copy-text="bugReportText"
            color="info"
            :icon="false"
          />
        </div>
      </v-card-text>
    </BaseDialog>

    <div class="d-flex justify-end">
      <BaseButton
        color="info"
        @click="
          bugReportDialog = true;
        "
      >
        <template #icon>
          {{ $globals.icons.github }}
        </template>
        {{ $t('settings.bug-report') }}
      </BaseButton>
    </div>

    <!-- Configuration -->
    <section>
      <BaseCardSectionTitle
        class="pb-0"
        :icon="$globals.icons.cog"
        :title="$t('settings.configuration')"
      />
      <v-card class="mb-4">
        <template
          v-for="(check, idx) in simpleChecks"
          :key="`list-item-${idx}`"
        >
          <v-list-item :title="check.text">
            <template #prepend>
              <v-icon :color="check.color" class="opacity-100">
                {{ check.icon }}
              </v-icon>
            </template>
            <v-list-item-subtitle class="wrap-word">
              {{ check.status ? check.successText : check.errorText }}
            </v-list-item-subtitle>
          </v-list-item>
          <v-divider />
        </template>
      </v-card>
    </section>

    <!-- SMTP Settings -->
    <section>
      <BaseCardSectionTitle
        class="pt-2"
        :icon="$globals.icons.email"
        :title="$t('user.email')"
      />
      <v-card class="mb-4 pa-4">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="siteSettings.smtp_host"
              label="SMTP Host"
              variant="outlined"
              hide-details="auto"
            />
          </v-col>
          <v-col cols="12" md="6">
             <v-text-field
              v-model="siteSettings.smtp_port"
              label="SMTP Port"
              type="number"
              variant="outlined"
              hide-details="auto"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="siteSettings.smtp_user"
              label="SMTP User"
              variant="outlined"
              hide-details="auto"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="siteSettings.smtp_password"
              label="SMTP Password"
              type="password"
              variant="outlined"
              hide-details="auto"
              placeholder="*****"
            />
          </v-col>
           <v-col cols="12" md="6">
            <v-text-field
              v-model="siteSettings.smtp_from_name"
              label="From Name"
              variant="outlined"
              hide-details="auto"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="siteSettings.smtp_from_email"
              label="From Email"
              variant="outlined"
              hide-details="auto"
            />
          </v-col>
           <v-col cols="12" md="6">
             <v-select
              v-model="siteSettings.smtp_auth_strategy"
              :items="['TLS', 'SSL', 'None']"
              label="Auth Strategy"
              variant="outlined"
              hide-details="auto"
              clearable
            />
          </v-col>
        </v-row>
        
        <div class="mt-4">
            <v-divider class="mb-4" />
             <div class="d-flex align-center">
             <v-text-field
                v-model="address"
                class="mr-4"
                :label="$t('user.email')"
                :rules="[validators.email]"
                density="compact"
                hide-details
                style="max-width: 300px"
              />
              <BaseButton
                color="info"
                variant="elevated"
                :loading="loading"
                :disabled="!validEmail"
                @click="testEmail"
              >
                <template #icon>
                  {{ $globals.icons.email }}
                </template>
                {{ $t("general.test") }}
              </BaseButton>
             </div>
             <template v-if="tested">
                <div class="mt-2">
                  <span :class="success ? 'text-success' : 'text-error'">
                    {{ success ? $t('settings.succeeded') : $t('settings.failed') + ': ' + error }}
                  </span>
                </div>
              </template>
        </div>
      </v-card>
    </section>

    <!-- AI Settings -->
    <section>
      <BaseCardSectionTitle
        class="pt-2"
        :icon="$globals.icons.autoFix"
        title="AI Services"
      />
      <v-card class="mb-4 pa-4">
        <v-alert
          type="info"
          variant="tonal"
          class="mb-4"
          text="Configure OpenAI settings. These will override environment variables if set."
        />
        <v-row>
          <v-col cols="12">
             <v-select
              v-model="siteSettings.ai_provider"
              :items="[{ title: 'OpenAI', value: 'openai' }, { title: 'Google (Gemini)', value: 'google' }]"
              label="AI Provider"
              variant="outlined"
              hide-details="auto"
            />
          </v-col>
        </v-row>

        <v-row v-if="siteSettings.ai_provider === 'openai' || !siteSettings.ai_provider">
          <v-col cols="12">
            <v-text-field
              v-model="siteSettings.openai_api_key"
              label="OpenAI API Key"
              type="password"
              variant="outlined"
              hide-details="auto"
              placeholder="sk-..."
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="siteSettings.openai_model"
              label="OpenAI Model"
              variant="outlined"
              hide-details="auto"
              placeholder="gpt-3.5-turbo"
            />
          </v-col>
           <v-col cols="12" md="6">
            <v-text-field
              v-model="siteSettings.openai_base_url"
              label="OpenAI Base URL"
              variant="outlined"
              hide-details="auto"
              placeholder="https://api.openai.com/v1"
            />
          </v-col>
        </v-row>

        <v-row v-if="siteSettings.ai_provider === 'google'">
          <v-col cols="12">
            <v-text-field
              v-model="siteSettings.google_api_key"
              label="Google API Key"
              type="password"
              variant="outlined"
              hide-details="auto"
              placeholder="AIza..."
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="siteSettings.google_model"
              label="Google Model"
              variant="outlined"
              hide-details="auto"
              placeholder="gemini-pro"
            />
          </v-col>
        </v-row>
      </v-card>
    </section>

    <!-- Save Actions -->
    <div class="d-flex justify-end mb-4">
        <BaseButton
        color="success"
        size="large"
        :loading="loading"
        @click="saveSettings"
        >
        <template #icon>
            {{ $globals.icons.contentSave }}
        </template>
        {{ $t("general.save") }}
        </BaseButton>
    </div>

    <!-- General App Info -->
    <section class="mt-4">
      <BaseCardSectionTitle
        class="pb-0"
        :icon="$globals.icons.cog"
        :title="$t('settings.general-about')"
      />
      <v-card class="mb-4">
        <template v-if="appInfo && appInfo.length">
          <template
            v-for="(property, idx) in appInfo"
            :key="property.name"
          >
            <v-list-item
              :title="property.name"
              :prepend-icon="property.icon || $globals.icons.user"
            >
              <template v-if="property.slot === 'recipe-scraper'">
                <v-list-item-subtitle>
                  <a
                    target="_blank"
                    :href="`https://github.com/hhursev/recipe-scrapers/releases/tag/${property.value}`"
                  >
                    {{ property.value }}
                  </a>
                </v-list-item-subtitle>
              </template>
              <template v-else-if="property.slot === 'build'">
                <v-list-item-subtitle>
                  <a
                    target="_blank"
                    :href="`https://github.com/mealie-recipes/mealie/commit/${property.value}`"
                  >
                    {{ property.value }}
                  </a>
                </v-list-item-subtitle>
              </template>
              <template v-else-if="property.slot === 'version' && property.value !== 'develop' && property.value !== 'nightly'">
                <v-list-item-subtitle>
                  <a
                    target="_blank"
                    :href="`https://github.com/mealie-recipes/mealie/releases/tag/${property.value}`"
                  >
                    {{ property.value }}
                  </a>
                </v-list-item-subtitle>
              </template>
              <template v-else>
                <v-list-item-subtitle>
                  {{ property.value }}
                </v-list-item-subtitle>
              </template>
            </v-list-item>
            <v-divider
              v-if="appInfo && idx !== appInfo.length - 1"
              :key="`divider-${property.name}`"
            />
          </template>
        </template>
        <template v-else>
          <div class="mb-3 text-center">
            <AppLoader :waiting-text="$t('general.loading')" />
          </div>
        </template>
      </v-card>
    </section>
  </v-container>
</template>

<script lang="ts">
import type { TranslateResult } from "vue-i18n";
import { useAdminApi, useUserApi } from "~/composables/api";
import { validators } from "~/composables/use-validators";
import { useAsyncKey } from "~/composables/use-utils";
import type { CheckAppConfig } from "~/lib/api/types/admin";
import type { SiteSettings } from "~/lib/api/types/admin/detailed-settings";
import AppLoader from "~/components/global/AppLoader.vue";
import { useToast } from "~/composables/use-toast";

enum DockerVolumeState {
  Unknown = "unknown",
  Success = "success",
  Error = "error",
}

interface SimpleCheck {
  id: string;
  text: TranslateResult;
  status: boolean | undefined;
  successText: TranslateResult;
  errorText: TranslateResult;
  color: string;
  icon: string;
}

interface CheckApp extends CheckAppConfig {
  isSiteSecure?: boolean;
}

export default defineNuxtComponent({
  components: { AppLoader },
  setup() {
    definePageMeta({
      layout: "admin",
    });

    // For some reason the layout is not set automatically, so we set it here,
    // even though it's defined above in the page meta.
    onMounted(() => {
      setPageLayout("admin");
    });

    const { $globals } = useNuxtApp();
    const i18n = useI18n();

    const state = reactive({
      loading: false,
      address: "",
      success: false,
      error: "",
      tested: false,
    });

    // Set page title
    useSeoMeta({
      title: i18n.t("settings.site-settings"),
    });

    const appConfig = ref<CheckApp>({
      emailReady: true,
      baseUrlSet: true,
      isSiteSecure: true,
      isUpToDate: false,
      ldapReady: false,
      oidcReady: false,
      enableOpenai: false,
    });
    function isLocalHostOrHttps() {
      return window.location.hostname === "localhost" || window.location.protocol === "https:";
    }
    const api = useUserApi();
    const adminApi = useAdminApi();
    const toast = useToast();
    
    const siteSettings = ref<SiteSettings>({});

    async function saveSettings() {
      state.loading = true;
      try {
        const { data } = await adminApi.settings.update(siteSettings.value);
        if (data) {
          siteSettings.value = data;
          toast.success(i18n.t("general.saved"));
          
          // Refresh checks
          const { data: checks } = await adminApi.about.checkApp();
          if (checks) {
             appConfig.value = { ...checks, isSiteSecure: isLocalHostOrHttps() };
          }
        }
      } catch (e) {
        // Error handling handled by interceptors usually, or we show toast
      }
      state.loading = false;
    }

    onMounted(async () => {
      adminApi.settings.get().then(({ data }) => {
        if (data) siteSettings.value = data;
      });

      const { data } = await adminApi.about.checkApp();
      if (data) {
        appConfig.value = { ...data, isSiteSecure: false };
      }
      appConfig.value.isSiteSecure = isLocalHostOrHttps();
    });
    const simpleChecks = computed<SimpleCheck[]>(() => {
      const goodIcon = $globals.icons.checkboxMarkedCircle;
      const badIcon = $globals.icons.alert;
      const warningIcon = $globals.icons.alertCircle;
      const goodColor = "success";
      const badColor = "error";
      const warningColor = "warning";
      const data: SimpleCheck[] = [
        {
          id: "application-version",
          text: i18n.t("settings.application-version"),
          status: appConfig.value.isUpToDate,
          errorText: i18n.t("settings.application-version-error-text", [rawAppInfo.value.version, rawAppInfo.value.versionLatest]),
          successText: i18n.t("settings.mealie-is-up-to-date"),
          color: appConfig.value.isUpToDate ? goodColor : warningColor,
          icon: appConfig.value.isUpToDate ? goodIcon : warningIcon,
        },
        {
          id: "secure-site",
          text: i18n.t("settings.secure-site"),
          status: appConfig.value.isSiteSecure,
          errorText: i18n.t("settings.secure-site-error-text"),
          successText: i18n.t("settings.secure-site-success-text"),
          color: appConfig.value.isSiteSecure ? goodColor : badColor,
          icon: appConfig.value.isSiteSecure ? goodIcon : badIcon,
        },
        {
          id: "server-side-base-url",
          text: i18n.t("settings.server-side-base-url"),
          status: appConfig.value.baseUrlSet,
          errorText: i18n.t("settings.server-side-base-url-error-text"),
          successText: i18n.t("settings.server-side-base-url-success-text"),
          color: appConfig.value.baseUrlSet ? goodColor : badColor,
          icon: appConfig.value.baseUrlSet ? goodIcon : badIcon,
        },
        {
          id: "ldap-ready",
          text: i18n.t("settings.ldap-ready"),
          status: appConfig.value.ldapReady,
          errorText: i18n.t("settings.ldap-ready-error-text"),
          successText: i18n.t("settings.ldap-ready-success-text"),
          color: appConfig.value.ldapReady ? goodColor : warningColor,
          icon: appConfig.value.ldapReady ? goodIcon : warningIcon,
        },
        {
          id: "oidc-ready",
          text: i18n.t("settings.oidc-ready"),
          status: appConfig.value.oidcReady,
          errorText: i18n.t("settings.oidc-ready-error-text"),
          successText: i18n.t("settings.oidc-ready-success-text"),
          color: appConfig.value.oidcReady ? goodColor : warningColor,
          icon: appConfig.value.oidcReady ? goodIcon : warningIcon,
        },
        {
          id: "openai-ready",
          text: i18n.t("settings.openai-ready"),
          status: appConfig.value.enableOpenai,
          errorText: i18n.t("settings.openai-ready-error-text"),
          successText: i18n.t("settings.openai-ready-success-text"),
          color: appConfig.value.enableOpenai ? goodColor : warningColor,
          icon: appConfig.value.enableOpenai ? goodIcon : warningIcon,
        },
      ];
      return data;
    });
    async function testEmail() {
      state.loading = true;
      state.tested = false;
      const { data } = await api.email.test({ email: state.address });
      if (data) {
        if (data.success) {
          state.success = true;
        }
        else {
          state.error = data.error ?? "";
          state.success = false;
        }
      }
      state.loading = false;
      state.tested = true;
    }
    const validEmail = computed(() => {
      if (state.address === "") {
        return false;
      }
      const valid = validators.email(state.address);
      // Explicit bool check because validators.email sometimes returns a string
      if (valid === true) {
        return true;
      }
      return false;
    });
    // ============================================================
    // General About Info
    const rawAppInfo = ref({
      version: "null",
      versionLatest: "null",
    });
    function getAppInfo() {
      const { data: statistics } = useAsyncData(useAsyncKey(), async () => {
        const { data } = await adminApi.about.about();
        if (data) {
          rawAppInfo.value.version = data.version;
          rawAppInfo.value.versionLatest = data.versionLatest;
          const prettyInfo = [
            {
              slot: "version",
              name: i18n.t("about.version"),
              icon: $globals.icons.information,
              value: data.version,
            },
            {
              slot: "build",
              name: i18n.t("settings.build"),
              icon: $globals.icons.information,
              value: data.buildId,
            },
            {
              name: i18n.t("about.application-mode"),
              icon: $globals.icons.devTo,
              value: data.production ? i18n.t("about.production") : i18n.t("about.development"),
            },
            {
              name: i18n.t("about.demo-status"),
              icon: $globals.icons.testTube,
              value: data.demoStatus ? i18n.t("about.demo") : i18n.t("about.not-demo"),
            },
            {
              name: i18n.t("about.api-port"),
              icon: $globals.icons.api,
              value: data.apiPort,
            },
            {
              name: i18n.t("about.api-docs"),
              icon: $globals.icons.file,
              value: data.apiDocs ? i18n.t("general.enabled") : i18n.t("general.disabled"),
            },
            {
              name: i18n.t("about.database-type"),
              icon: $globals.icons.database,
              value: data.dbType,
            },
            {
              name: i18n.t("about.database-url"),
              icon: $globals.icons.database,
              value: data.dbUrl,
            },
            {
              name: i18n.t("about.default-group"),
              icon: $globals.icons.group,
              value: data.defaultGroup,
            },
            {
              name: i18n.t("about.default-household"),
              icon: $globals.icons.household,
              value: data.defaultHousehold,
            },
            {
              slot: "recipe-scraper",
              name: i18n.t("settings.recipe-scraper-version"),
              icon: $globals.icons.primary,
              value: data.recipeScraperVersion,
            },
          ];
          return prettyInfo;
        }
        return data;
      });
      return statistics;
    }
    const appInfo = getAppInfo();
    const bugReportDialog = ref(false);
    const bugReportText = computed(() => {
      const ignore = {
        [i18n.t("about.database-url")]: true,
        [i18n.t("about.default-group")]: true,
      };
      let text = "**Details**\n";
      appInfo.value?.forEach((item) => {
        if (ignore[item.name as string]) {
          return;
        }
        text += `${item.name as string}: ${item.value as string}\n`;
      });
      const ignoreChecks: {
        [key: string]: boolean;
      } = {
        "application-version": true,
      };
      text += "\n**Checks**\n";
      simpleChecks.value.forEach((item) => {
        if (ignoreChecks[item.id]) {
          return;
        }
        const status = item.status ? i18n.t("general.yes") : i18n.t("general.no");
        text += `${item.text.toString()}: ${status}\n`;
      });
      text += `${i18n.t("settings.email-configured")}: ${appConfig.value.emailReady ? i18n.t("general.yes") : i18n.t("general.no")}\n`;
      return text;
    });
    return {
      bugReportDialog,
      bugReportText,
      DockerVolumeState,
      simpleChecks,
      appConfig,
      validEmail,
      validators,
      ...toRefs(state),
      appInfo,
      siteSettings,
      saveSettings,
    };
  },
});
</script>

<style scoped>
.wrap-word {
  white-space: normal;
  word-wrap: break-word;
}
</style>
