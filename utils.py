# utils.py
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import IamIdentityV1, UsageReportsV4, ResourceControllerV2, GlobalTaggingV1, GlobalSearchV2, ResourceManagerV2
from ibm_cloud_sdk_core import ApiException
import logging
from ibm_code_engine_sdk.code_engine_v2 import *


class SDKConnector:
    def __init__(self, IBMCLOUD_API_KEY):
        self.IBMCLOUD_API_KEY = IBMCLOUD_API_KEY

    def create_authenticator(self):
        try:
            return IAMAuthenticator(self.IBMCLOUD_API_KEY)
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()

    def create_iam_identity_service(self):
        authenticator = self.create_authenticator()
        try:
            return IamIdentityV1(authenticator=authenticator)
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()

    def create_usage_reports_service(self):
        authenticator = self.create_authenticator()
        try:
            return UsageReportsV4(authenticator=authenticator)
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()

    def create_resource_controller_service(self):
        authenticator = self.create_authenticator()
        try:
            return ResourceControllerV2(authenticator=authenticator)
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()

    def create_resource_manager_service(self):
        authenticator = self.create_authenticator()
        try:
            return ResourceManagerV2(authenticator=authenticator)
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()

    def create_global_tagging_service(self):
        authenticator = self.create_authenticator()
        try:
            global_tagging_service = GlobalTaggingV1(authenticator=authenticator)
            global_tagging_service.enable_retries(max_retries=5, retry_interval=1.0)
            global_tagging_service.set_http_config({'timeout': 120})
            return global_tagging_service
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()

    def create_global_search_service(self):
        authenticator = self.create_authenticator()
        try:
            return GlobalSearchV2(authenticator=authenticator)
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()

    def create_code_engine_service(self):
        authenticator = self.create_authenticator()
        try:
            code_engine_service = CodeEngineV2(authenticator=authenticator)
            return code_engine_service
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()

