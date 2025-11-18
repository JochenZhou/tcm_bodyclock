"""Sensor for TCM Body Clock integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NARRATIVE_KEY


@dataclass
class TCMDetailSensorDescription(SensorEntityDescription):
    """Class describing a TCM detail sensor."""


DETAIL_SENSOR_DESCRIPTIONS: tuple[TCMDetailSensorDescription, ...] = (
    TCMDetailSensorDescription(
        key="meridian",
        name="经络值班",
        icon="mdi:yin-yang",
    ),
    TCMDetailSensorDescription(
        key="health_tip",
        name="养生重点",
        icon="mdi:heart-pulse",
    ),
    TCMDetailSensorDescription(
        key="recommend",
        name="推荐事项",
        icon="mdi:lightbulb-on",
    ),
    TCMDetailSensorDescription(
        key="avoid",
        name="注意事项",
        icon="mdi:alert-circle",
    ),
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    # 从 hass.data 中获取 coordinator
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = [
        TCMBodyClockSensor(coordinator),
        TCMBodyClockNarrativeSensor(coordinator),
    ]
    entities.extend(
        TCMBodyClockDetailSensor(coordinator, description)
        for description in DETAIL_SENSOR_DESCRIPTIONS
    )
    async_add_entities(entities)

class TCMBodyClockSensor(CoordinatorEntity, SensorEntity):
    """Representation of the main TCM Body Clock sensor."""

    _attr_icon = "mdi:clock-outline"

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "时辰"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_tcm_bodyclock"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": "中医养生表",
            "manufacturer": "Enmy&AI",
            "model": "Body Clock",
            "entry_type": "service",
        }

    @property
    def native_value(self):
        """Return the current TCM hour (the state)."""
        if self.coordinator.data:
            return self.coordinator.data.get("name")
        return None


class TCMBodyClockDetailSensor(CoordinatorEntity, SensorEntity):
    """Representation of individual attribute sensors."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, description: TCMDetailSensorDescription):
        """Initialize the attribute sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"中医养生表 {description.name}"
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_tcm_bodyclock_{description.key}"
        )
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": "中医养生表",
            "manufacturer": "Enmy&AI",
            "model": "Body Clock",
            "entry_type": "service",
        }

    @property
    def native_value(self):
        """Return the attribute value for this sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self.entity_description.key)


class TCMBodyClockNarrativeSensor(CoordinatorEntity, SensorEntity):
    """Sensor that shows AI generated natural tips."""

    _attr_icon = "mdi:robot"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "中医养生表 AI提醒"
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_tcm_bodyclock_narrative"
        )
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": "中医养生表",
            "manufacturer": "Enmy&AI",
            "model": "Body Clock",
            "entry_type": "service",
        }

    @property
    def native_value(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(NARRATIVE_KEY)
