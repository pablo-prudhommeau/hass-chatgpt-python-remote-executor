import logging
import json
import requests
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.helpers import config_validation as cv, entity_platform, service
from homeassistant.util.json import JsonObjectType

DOMAIN = "python_remote_executor"
SERVICE_RUN_SCRIPT = "run_python_script"

SERVICE_RUN_SCRIPT_SCHEMA = vol.Schema({
    vol.Required("script"): cv.string,
    vol.Required('requirements'): cv.string
})

_LOGGER = logging.getLogger(__package__)

def setup(hass, config):
    def handle_run_script_service(call):
        script = call.data.get("script")
        requirements = call.data.get("requirements")
        url = "http://<REMOTE_EXECUTOR_HOST>:6000/run_script"
        try:
            response = requests.post(url, json={"script": script, "requirements": requirements})
            return {"response" : response.text}
        except requests.RequestException as e:
            _LOGGER.error(f"Error executing script: {e}")

    hass.services.register(
        DOMAIN,
        SERVICE_RUN_SCRIPT,
        handle_run_script_service,
        schema=SERVICE_RUN_SCRIPT_SCHEMA,
        supports_response=SupportsResponse.OPTIONAL
    )
    
    return True