"""Config flow for TCM Body Clock integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_OPENAI_API_KEY,
    CONF_OPENAI_BASE_URL,
    CONF_OPENAI_MODEL,
    CONF_PROMPT_HEADER,
    CONF_WEATHER_ENTITY_ID,
    DEFAULT_PROMPT_HEADER,
    DOMAIN,
)


class TCMBodyClockConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TCM Body Clock."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # 检查是否已经配置过
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors = {}
        weather_entities = self.hass.states.async_entity_ids("weather")
        has_weather = bool(weather_entities)
        weather_selector = selector.EntitySelector(
            selector.EntitySelectorConfig(domain=["weather"])
        )

        defaults = user_input or {}
        base_url_default = defaults.get(CONF_OPENAI_BASE_URL, "")
        api_key_default = defaults.get(CONF_OPENAI_API_KEY, "")
        model_default = defaults.get(CONF_OPENAI_MODEL, "")
        prompt_default = defaults.get(
            CONF_PROMPT_HEADER,
            DEFAULT_PROMPT_HEADER,
        )

        weather_default = defaults.get(CONF_WEATHER_ENTITY_ID)
        if weather_default is None and weather_entities:
            weather_default = weather_entities[0]

        if not has_weather:
            errors[CONF_WEATHER_ENTITY_ID] = "no_weather_options"

        if user_input is not None and not errors:
            return self.async_create_entry(title="中医养生表", data=user_input)

        weather_field = (
            vol.Required(CONF_WEATHER_ENTITY_ID, default=weather_default)
            if weather_default is not None
            else vol.Required(CONF_WEATHER_ENTITY_ID)
        )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_OPENAI_BASE_URL,
                    default=base_url_default,
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=False)
                ),
                vol.Required(
                    CONF_OPENAI_API_KEY,
                    default=api_key_default,
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=False)
                ),
                vol.Required(
                    CONF_OPENAI_MODEL,
                    default=model_default,
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=False)
                ),
                weather_field: weather_selector,
                vol.Optional(
                    CONF_PROMPT_HEADER,
                    default=prompt_default,
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=True)
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "message": "我会结合时辰和天气，给你一句贴心的养生提醒，陪你更好地照顾自己。",
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return TCMBodyClockOptionsFlow(config_entry)


class TCMBodyClockOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for TCM Body Clock."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""

        errors: dict[str, str] = {}
        weather_entities = self.hass.states.async_entity_ids("weather")
        has_weather = bool(weather_entities)
        weather_selector = selector.EntitySelector(
            selector.EntitySelectorConfig(domain=["weather"])
        )

        # Current values (options take precedence over data)
        current_base_url = self.config_entry.options.get(
            CONF_OPENAI_BASE_URL
        ) or self.config_entry.data.get(CONF_OPENAI_BASE_URL, "")
        current_api_key = self.config_entry.options.get(
            CONF_OPENAI_API_KEY
        ) or self.config_entry.data.get(CONF_OPENAI_API_KEY, "")
        current_model = self.config_entry.options.get(
            CONF_OPENAI_MODEL
        ) or self.config_entry.data.get(CONF_OPENAI_MODEL, "")
        current_weather = self.config_entry.options.get(
            CONF_WEATHER_ENTITY_ID
        ) or self.config_entry.data.get(CONF_WEATHER_ENTITY_ID)
        current_prompt_header = self.config_entry.options.get(CONF_PROMPT_HEADER) or self.config_entry.data.get(
            CONF_PROMPT_HEADER
        ) or DEFAULT_PROMPT_HEADER
        current_prompt = current_prompt_header

        defaults = user_input.copy() if user_input is not None else {}
        if CONF_OPENAI_BASE_URL not in defaults:
            defaults[CONF_OPENAI_BASE_URL] = current_base_url
        if CONF_OPENAI_API_KEY not in defaults:
            defaults[CONF_OPENAI_API_KEY] = current_api_key
        if CONF_OPENAI_MODEL not in defaults:
            defaults[CONF_OPENAI_MODEL] = current_model
        if current_weather is not None and CONF_WEATHER_ENTITY_ID not in defaults:
            defaults[CONF_WEATHER_ENTITY_ID] = current_weather
        if CONF_PROMPT_HEADER not in defaults:
            defaults[CONF_PROMPT_HEADER] = current_prompt
        base_url_default = defaults.get(CONF_OPENAI_BASE_URL, "")
        api_key_default = defaults.get(CONF_OPENAI_API_KEY, "")
        model_default = defaults.get(CONF_OPENAI_MODEL, "")

        weather_default = defaults.get(CONF_WEATHER_ENTITY_ID)
        if weather_default is None and weather_entities:
            weather_default = weather_entities[0]

        if not has_weather:
            errors[CONF_WEATHER_ENTITY_ID] = "no_weather_options"

        if user_input is not None and not errors:
            # Save selections into options so they can be changed later
            return self.async_create_entry(title="", data=user_input)

        weather_field = (
            vol.Required(CONF_WEATHER_ENTITY_ID, default=weather_default)
            if weather_default is not None
            else vol.Required(CONF_WEATHER_ENTITY_ID)
        )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_OPENAI_BASE_URL,
                    default=base_url_default,
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=False)
                ),
                vol.Required(
                    CONF_OPENAI_API_KEY,
                    default=api_key_default,
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=False)
                ),
                vol.Required(
                    CONF_OPENAI_MODEL,
                    default=model_default,
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=False)
                ),
                weather_field: weather_selector,
                vol.Optional(
                    CONF_PROMPT_HEADER,
                    default=defaults.get(CONF_PROMPT_HEADER, DEFAULT_PROMPT_HEADER),
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=True)
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "message": "你可以在这里修改 OpenAI 接口、模型、天气实体和系统提示词，让养生提醒更贴合现在的需要。",
            },
        )
