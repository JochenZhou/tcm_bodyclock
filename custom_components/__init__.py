"""The TCM Body Clock integration."""
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, TCM_HOURS

_LOGGER = logging.getLogger(__name__)

# 定义更新的时间间隔，每分钟检查一次，确保时间切换的及时性
SCAN_INTERVAL = timedelta(minutes=1)

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
    # 创建一个 Coordinator
    async def _async_update_data():
        """Fetch data from API."""
        try:
            from homeassistant.util import dt as dt_util
            current_hour = dt_util.now().hour
            return get_current_tcm_hour(current_hour)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="TCM Body Clock Sensor",
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