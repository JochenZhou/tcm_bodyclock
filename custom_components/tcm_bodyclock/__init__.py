"""The TCM Body Clock integration."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_OPENAI_API_KEY,
    CONF_OPENAI_BASE_URL,
    CONF_OPENAI_MODEL,
    CONF_PROMPT_HEADER,
    CONF_WEATHER_ENTITY_ID,
    DOMAIN,
    DEFAULT_PROMPT_HEADER,
    NARRATIVE_KEY,
    TCM_HOURS,
)

_LOGGER = logging.getLogger(__name__)

# 定义更新的时间间隔，每分钟检查一次，确保时间切换的及时性
SCAN_INTERVAL = timedelta(minutes=1)


def _entry_value(entry: ConfigEntry, key: str):
    """Return a config value, preferring options over data."""

    if key in entry.options and entry.options.get(key) is not None:
        return entry.options.get(key)
    return entry.data.get(key)

def get_current_tcm_hour(now_hour: int):
    """Find the current TCM hour details from the TCM_HOURS list."""
    for hour_data in TCM_HOURS:
        start, end = hour_data["start"], hour_data["end"]
        # 处理跨午夜的情况 (e.g., 23:00-01:00)
        if start > end:
            if now_hour >= start or now_hour < end:
                return hour_data
        # 处理当天内的情况 (e.g., 01:00-03:00)
        else:
            if start <= now_hour < end:
                return hour_data
    return None # 理论上不会发生

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TCM Body Clock from a config entry."""
    await _async_populate_missing_config(hass, entry)
    # 创建一个 Coordinator
    async def _async_update_data():
        """Fetch data from API."""
        try:
            from homeassistant.util import dt as dt_util
            current_hour = dt_util.now().hour
            tcm_hour = get_current_tcm_hour(current_hour)
            if not tcm_hour:
                raise UpdateFailed("Unable to determine current TCM hour")

            weather_entity_id = _entry_value(entry, CONF_WEATHER_ENTITY_ID)
            base_url = _entry_value(entry, CONF_OPENAI_BASE_URL)
            api_key = _entry_value(entry, CONF_OPENAI_API_KEY)
            model = _entry_value(entry, CONF_OPENAI_MODEL)
            system_prompt = _entry_value(entry, CONF_PROMPT_HEADER) or DEFAULT_PROMPT_HEADER

            if not weather_entity_id or not base_url or not api_key or not model:
                raise UpdateFailed("Integration not configured with API/Weather selections")

            weather_state = hass.states.get(weather_entity_id)
            if not weather_state:
                raise UpdateFailed(
                    f"Weather entity {weather_entity_id} is unavailable"
                )

            weather_attributes = weather_state.attributes
            temperature = weather_attributes.get("temperature")
            apparent_temperature = weather_attributes.get("apparent_temperature")
            humidity = weather_attributes.get("humidity")

            comfort_phrase = _describe_comfort(apparent_temperature or temperature, humidity)

            weather_info = {
                "entity_id": weather_entity_id,
                "condition": weather_state.state,
                "temperature": temperature,
                "apparent_temperature": apparent_temperature,
                "humidity": humidity,
                "pressure": weather_attributes.get("pressure"),
                "wind_speed": weather_attributes.get("wind_speed"),
                "comfort": comfort_phrase,
            }

            # 控制 AI 调用频率：仅在启动、时辰变化、天气状况或温度变化时重新生成
            previous_data = coordinator.data
            previous_narrative: Optional[str] = None
            regenerate_narrative = True

            if previous_data:
                previous_narrative = previous_data.get(NARRATIVE_KEY)
                prev_hour_name = previous_data.get("name")
                prev_weather = previous_data.get("weather") or {}
                prev_condition = prev_weather.get("condition")
                prev_temp = prev_weather.get("temperature")
                prev_apparent = prev_weather.get("apparent_temperature")

                if (
                    prev_hour_name == tcm_hour.get("name")
                    and prev_condition == weather_info["condition"]
                    and prev_temp == weather_info["temperature"]
                    and prev_apparent == weather_info["apparent_temperature"]
                ):
                    regenerate_narrative = False

            if regenerate_narrative or not previous_narrative:
                narrative = await _async_generate_narrative(
                    hass,
                    base_url,
                    api_key,
                    model,
                    tcm_hour,
                    weather_info,
                    system_prompt,
                )
            else:
                narrative = previous_narrative

            return {
                **tcm_hour,
                "weather": weather_info,
                NARRATIVE_KEY: narrative,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="中医养生表",
        update_method=_async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    # 首次刷新数据
    await coordinator.async_config_entry_first_refresh()

    # 将 coordinator 存储在 hass.data 中，以便 sensor 平台可以访问
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # 转发到 sensor 平台进行设置
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # 从 sensor 平台卸载
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def _async_generate_narrative(
    hass: HomeAssistant,
    base_url: str,
    api_key: str,
    model: str,
    tcm_hour: dict[str, Any],
    weather_info: dict[str, Any],
    system_prompt: str,
) -> str:
    """Generate a natural language tip via the configured AI agent."""

    meridian = tcm_hour.get("meridian")
    tip = tcm_hour.get("health_tip")
    recommend = tcm_hour.get("recommend")
    avoid = tcm_hour.get("avoid")

    condition = weather_info.get("condition")
    apparent_temp = weather_info.get("apparent_temperature")
    temp = weather_info.get("temperature")
    humidity = weather_info.get("humidity")
    comfort_phrase = weather_info.get("comfort")

    prompt_parts: list[str] = []
    prompt_parts.append(
        f"当前时辰：{tcm_hour.get('name')}，经络：{meridian}。"
    )
    prompt_parts.append(
        f"养生重点：{tip}，推荐事项：{recommend}，注意事项：{avoid}。"
    )
    weather_sentence = f"天气状况：{condition}"
    temp_to_use = apparent_temp if apparent_temp is not None else temp
    if temp_to_use is not None:
        weather_sentence += f"，体感温度 {temp_to_use}°C"
    if humidity is not None:
        weather_sentence += f"，湿度 {humidity}%"
    if comfort_phrase:
        weather_sentence += f"，舒适度：{comfort_phrase}"
    prompt_parts.append(weather_sentence + "。")

    user_prompt = "\n".join(prompt_parts)

    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    try:
        session = aiohttp_client.async_get_clientsession(hass)
        async with session.post(url, json=payload, headers=headers, timeout=30) as resp:
            data = await resp.json()
            if resp.status >= 400:
                _LOGGER.warning("OpenAI-compatible API error %s: %s", resp.status, data)
            else:
                choices = data.get("choices") or []
                if choices:
                    message = choices[0].get("message") or {}
                    content = message.get("content")
                    if isinstance(content, str) and content.strip():
                        return content.strip()
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.warning("AI generation failed: %s", err)

    # 兜底提示
    fallback = f"{tcm_hour.get('name')} {meridian or ''}，{tip or ''}，{recommend or ''}"
    return fallback.strip()


async def _async_populate_missing_config(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Attempt to auto-fill config data for legacy entries."""

    data = dict(entry.data)
    changed = False

    if not data.get(CONF_WEATHER_ENTITY_ID):
        weather_entity = _async_first_weather_entity(hass)
        if weather_entity:
            data[CONF_WEATHER_ENTITY_ID] = weather_entity
            changed = True

    if CONF_PROMPT_HEADER not in data or not data.get(CONF_PROMPT_HEADER):
        data[CONF_PROMPT_HEADER] = DEFAULT_PROMPT_HEADER
        changed = True

    if changed:
        hass.config_entries.async_update_entry(entry, data=data)


def _async_first_weather_entity(hass: HomeAssistant) -> str | None:
    entity_ids = hass.states.async_entity_ids("weather")
    if entity_ids:
        return entity_ids[0]
    return None


def _describe_comfort(
    temp: Optional[float],
    humidity: Optional[float],
) -> Optional[str]:
    """Return a simple textual comfort assessment."""

    if temp is None:
        return None

    comfort = "舒适"
    if temp < 0:
        comfort = "严寒"
    elif temp < 10:
        comfort = "寒冷"
    elif temp < 18:
        comfort = "偏凉"
    elif temp <= 26:
        comfort = "宜人"
    elif temp <= 32:
        comfort = "偏热"
    else:
        comfort = "闷热"

    if humidity is not None:
        if humidity > 80 and temp >= 26:
            comfort += "、潮湿"
        elif humidity < 40 and temp > 20:
            comfort += "、干燥"

    return comfort


def _render_intent_response(response) -> Optional[str]:
    """Deprecated helper kept for backward compatibility; no longer used."""

    if response is None:
        return None
    if isinstance(response, str):
        return response.strip() or None
    return None
