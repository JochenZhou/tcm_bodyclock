"""Sensor for TCM Body Clock integration."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    # 从 hass.data 中获取 coordinator
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([TCMBodyClockSensor(coordinator)])

class TCMBodyClockSensor(CoordinatorEntity, SensorEntity):
    """Representation of a TCM Body Clock sensor."""

    # _attr_has_entity_name = True  # 如果你想让HA自动在设备名前加上实体名，可以设为True
    _attr_icon = "mdi:clock-outline" # 使用一个更通用的时钟图标

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        # 从 manifest.json 和 config_flow 获取设备信息
        self._attr_name = "中医养生表" # 实体名称
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_tcm_bodyclock"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": "中医十二时辰养生", # 设备名称
            "manufacturer": "TCM Theory",
            "model": "Body Clock",
            "entry_type": "service",
        }


    @property
    def state(self):
        """Return the current TCM hour (the state)."""
        if self.coordinator.data:
            return self.coordinator.data.get("name")
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data:
            return {
                "经络值班": self.coordinator.data.get("meridian"),
                "养生重点": self.coordinator.data.get("health_tip"),
                "推荐事项": self.coordinator.data.get("recommend"),
                "注意事项": self.coordinator.data.get("avoid")
            }
        return {}

    # 无需 async_update 方法，CoordinatorEntity 会自动处理