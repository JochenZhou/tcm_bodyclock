"""Config flow for TCM Body Clock integration."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN


class TCMBodyClockConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TCM Body Clock."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # 检查是否已经配置过
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="中医十二时辰养生", data={})

        return self.async_show_form(
            step_id="user",
            # data_schema=None, # 因为没有字段，所以不需要
            description_placeholders={"description": "点击“提交”即可添加中医养生表组件。此集成无需额外配置。"},
        )

    # Options Flow (可选功能)
    # 你原来的代码有一个 alert_enabled 选项，但在其他地方并未使用。
    # 如果你未来想添加配置选项（例如“开启/关闭某个时辰的通知”），可以启用下面的代码。
    # 目前为了保持代码简洁，我暂时将其注释掉。
    # @staticmethod
    # @callback
    # def async_get_options_flow(config_entry):
    #     """Get the options flow for this handler."""
    #     return TCMBodyClockOptionsFlow(config_entry)

# class TCMBodyClockOptionsFlow(config_entries.OptionsFlow):
#     """Handle options flow for TCM Body Clock."""
#
#     def __init__(self, config_entry):
#         """Initialize options flow."""
#         self.config_entry = config_entry
#
#     async def async_step_init(self, user_input=None):
#         """Manage the options."""
#         if user_input is not None:
#             return self.async_create_entry(title="", data=user_input)
#
#         return self.async_show_form(
#             step_id="init",
#             data_schema=vol.Schema({
#                 # 这里获取已有的值作为默认值
#                 vol.Optional(
#                     "alert_enabled",
#                     default=self.config_entry.options.get("alert_enabled", True)
#                 ): bool
#             })
#         )