# Copyright 2017 The Forseti Security Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrapper for AppEngine API client."""
from httplib2 import HttpLib2Error

from googleapiclient import errors

from google.cloud.security.common.gcp_api import _base_repository
from google.cloud.security.common.gcp_api import api_helpers
from google.cloud.security.common.gcp_api import errors as api_errors
from google.cloud.security.common.gcp_api import repository_mixins


class AppEngineRepositoryClient(_base_repository.BaseRepositoryClient):
    """AppEngine API Respository."""

    def __init__(self,
                 quota_max_calls=None,
                 quota_period=1.0,
                 use_rate_limiter=True):
        """Constructor.

        Args:
            quota_max_calls (int): Allowed requests per <quota_period> for the
                API.
            quota_period (float): The time period to track requests over.
            use_rate_limiter (bool): Set to false to disable the use of a rate
                limiter for this service.
        """
        if not quota_max_calls:
            use_rate_limiter = False

        self._apps = None
        self._app_services = None
        self._service_versions = None
        self._version_instances = None

        super(AppEngineRepositoryClient, self).__init__(
            'appengine', versions=['v1'],
            quota_max_calls=quota_max_calls,
            quota_period=quota_period,
            use_rate_limiter=use_rate_limiter)

    # Turn off docstrings for properties.
    # pylint: disable=missing-return-doc, missing-return-type-doc
    @property
    def apps(self):
        """Returns an _AppEngineAppsRepository instance."""
        if not self._apps:
            self._apps = self._init_repository(
                _AppEngineAppsRepository)
        return self._apps

    @property
    def app_services(self):
        """Returns an _AppEngineAppsServicesRepository instance."""
        if not self._app_services:
            self._app_services = self._init_repository(
                _AppEngineAppsServicesRepository)
        return self._app_services

    @property
    def service_versions(self):
        """Returns an _AppEngineAppsServicesVersionsRepository instance."""
        if not self._service_versions:
            self._service_versions = self._init_repository(
                _AppEngineAppsServicesVersionsRepository)
        return self._service_versions

    @property
    def version_instances(self):
        """Returns an _AppEngineAppsServicesVersionsInstancesRepository."""
        if not self._version_instances:
            self._version_instances = self._init_repository(
                _AppEngineAppsServicesVersionsInstancesRepository)
        return self._version_instances
    # pylint: enable=missing-return-doc, missing-return-type-doc


class _AppEngineAppsRepository(
        repository_mixins.GetQueryMixin,
        _base_repository.GCPRepository):
    """Implementation of AppEngine Apps repository."""

    def __init__(self, **kwargs):
        """Constructor.

        Args:
            **kwargs (dict): The args to pass into GCPRepository.__init__()
        """
        super(_AppEngineAppsRepository, self).__init__(
            component='apps', key_field='appsId', **kwargs)


class _AppEngineAppsServicesRepository(
        repository_mixins.GetQueryMixin,
        repository_mixins.ListQueryMixin,
        _base_repository.GCPRepository):
    """Implementation of AppEngine Apps Services repository."""

    def __init__(self, **kwargs):
        """Constructor.

        Args:
            **kwargs (dict): The args to pass into GCPRepository.__init__()
        """
        super(_AppEngineAppsServicesRepository, self).__init__(
            component='apps.services', key_field='appsId',
            entity_field='servicesId', max_results_field='pageSize', **kwargs)


# pylint: disable=arguments-differ
class _AppEngineAppsServicesVersionsRepository(
        repository_mixins.GetQueryMixin,
        repository_mixins.ListQueryMixin,
        _base_repository.GCPRepository):
    """Implementation of AppEngine Apps Services Versions repository."""

    def __init__(self, **kwargs):
        """Constructor.

        Args:
            **kwargs (dict): The args to pass into GCPRepository.__init__()
        """
        super(_AppEngineAppsServicesVersionsRepository, self).__init__(
            component='apps.services.versions', key_field='appsId',
            entity_field='versionsId', max_results_field='pageSize', **kwargs)

    def get(self, resource, target, services_id, **kwargs):
        """Get specific entity of a given resource.

        Args:
            resource (str): The id of the resource to query.
            target (str):  Name of the entity to fetch.
            services_id (str): The id of the service to query.
            **kwargs (dict): Optional additional arguments to pass to the query.

        Returns:
            dict: An API response containing the entity resource.
        """
        return repository_mixins.GetQueryMixin.get(
            self, resource, target, servicesId=services_id, **kwargs)

    def list(self, resource, services_id, **kwargs):
        """List subresources of a given resource.

        Args:
            resource (str): The id of the resource to query.
            services_id (str): The id of the service to query.
            **kwargs (dict): Optional additional arguments to pass to the query.

        Returns:
            iterator: An iterator over each page of results from the API.
        """
        return repository_mixins.ListQueryMixin.list(
            self, resource, servicesId=services_id, **kwargs)


class _AppEngineAppsServicesVersionsInstancesRepository(
        repository_mixins.GetQueryMixin,
        repository_mixins.ListQueryMixin,
        _base_repository.GCPRepository):
    """Implementation of AppEngine Apps Services Versions Instances repo."""

    def __init__(self, **kwargs):
        """Constructor.

        Args:
            **kwargs (dict): The args to pass into GCPRepository.__init__()
        """
        super(_AppEngineAppsServicesVersionsInstancesRepository, self).__init__(
            component='apps.services.versions.instances', key_field='appsId',
            entity_field='instancesId', max_results_field='pageSize', **kwargs)

    def get(self, resource, target, services_id, versions_id, **kwargs):
        """Get specific entity of a given resource.

        Args:
            resource (str): The id of the resource to query.
            target (str):  Name of the entity to fetch.
            services_id (str): The id of the service to query.
            versions_id (str): The id of the version to query.
            **kwargs (dict): Optional additional arguments to pass to the query.

        Returns:
            dict: An API response containing the entity resource.
        """
        return repository_mixins.GetQueryMixin.get(
            self, resource, target, servicesId=services_id,
            versionsId=versions_id, **kwargs)

    def list(self, resource, services_id, versions_id, **kwargs):
        """List subresources of a given resource.

        Args:
            resource (str): The id of the resource to query.
            services_id (str): The id of the service to query.
            versions_id (str): The id of the version to query.
            **kwargs (dict): Optional additional arguments to pass to the query.

        Returns:
            iterator: An iterator over each page of results from the API.
        """
        return repository_mixins.ListQueryMixin.list(
            self, resource, servicesId=services_id, versionsId=versions_id,
            **kwargs)
# pylint: enable=arguments-differ


class AppEngineClient(object):
    """AppEngine Client.

    https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps
    """
    DEFAULT_QUOTA_PERIOD = 1.0

    def __init__(self, global_configs, **kwargs):
        """Initialize.

        Args:
            global_configs (dict): Forseti config.
            **kwargs (dict): The kwargs.
        """
        max_calls = global_configs.get('max_appengine_api_calls_per_second')
        self.repository = AppEngineRepositoryClient(
            quota_max_calls=max_calls,
            quota_period=self.DEFAULT_QUOTA_PERIOD,
            use_rate_limiter=kwargs.get('use_rate_limiter', True))

    def get_app(self, project_id):
        """Gets information about an application.

        Args:
            project_id (str): The id of the project.

        Returns:
            dict: The response of retrieving the AppEngine app.
        """
        try:
            return self.repository.apps.get(project_id)
        except (errors.HttpError, HttpLib2Error) as e:
            if isinstance(e, errors.HttpError) and e.resp.status == 404:
                # TODO: handle error more gracefully
                # application not found
                return {}
            raise api_errors.ApiExecutionError(project_id, e)

    def get_service(self, project_id, service_id):
        """Gets information about a specific service.

        Args:
            project_id (str): The id of the project.
            service_id (str): The id of the service to query.

        Returns:
            dict: A Service resource dict for a given project_id and
                service_id.
        """
        try:
            return self.repository.app_services.get(
                project_id, target=service_id)
        except (errors.HttpError, HttpLib2Error) as e:
            if isinstance(e, errors.HttpError) and e.resp.status == 404:
                return {}
            raise api_errors.ApiExecutionError(project_id, e)

    def list_services(self, project_id):
        """Lists services of a project.

        Args:
            project_id (str): The id of the project.

        Returns:
            list: A list of Service resource dicts for a project_id.
        """
        try:
            paged_results = self.repository.app_services.list(project_id)
            return api_helpers.flatten_list_results(paged_results, 'services')
        except (errors.HttpError, HttpLib2Error) as e:
            if isinstance(e, errors.HttpError) and e.resp.status == 404:
                return []
            raise api_errors.ApiExecutionError(project_id, e)

    def get_version(self, project_id, service_id, version_id):
        """Gets information about a specific version of a service.

        Args:
            project_id (str): The id of the project.
            service_id (str): The id of the service to query.
            version_id (str): The id of the version to query.

        Returns:
            dict: A Version resource dict for a given project_id and
                service_id.
        """
        try:
            return self.repository.service_versions.get(
                project_id, target=version_id, services_id=service_id)
        except (errors.HttpError, HttpLib2Error) as e:
            if isinstance(e, errors.HttpError) and e.resp.status == 404:
                return {}
            raise api_errors.ApiExecutionError(project_id, e)

    def list_versions(self, project_id, service_id):
        """Lists versions of a given service.

        Args:
            project_id (str): The id of the project.
            service_id (str): The id of the service to query.

        Returns:
            list: A list of Version resource dicts for a given Service.
        """
        try:
            paged_results = self.repository.service_versions.list(
                project_id, services_id=service_id)
            return api_helpers.flatten_list_results(paged_results, 'versions')
        except (errors.HttpError, HttpLib2Error) as e:
            if isinstance(e, errors.HttpError) and e.resp.status == 404:
                return []
            raise api_errors.ApiExecutionError(project_id, e)

    def get_instance(self, project_id, service_id, version_id, instances_id):
        """Gets information about a specific instance of a service.

        Args:
            project_id (str): The id of the project.
            service_id (str): The id of the service to query.
            version_id (str): The id of the version to query.
            instances_id (str): The id of the instance to query.

        Returns:
            dict: An Instance resource dict for a given project_id,
                service_id and version_id.
        """
        try:
            return self.repository.version_instances.get(
                project_id, target=instances_id, services_id=service_id,
                versions_id=version_id)
        except (errors.HttpError, HttpLib2Error) as e:
            if isinstance(e, errors.HttpError) and e.resp.status == 404:
                return {}
            raise api_errors.ApiExecutionError(project_id, e)

    def list_instances(self, project_id, service_id, version_id):
        """Lists instances of a given service and version.

        Args:
            project_id (str): The id of the project.
            service_id (str): The id of the service to query.
            version_id (str): The id of the version to query.

        Returns:
            list: A list of Instance resource dicts for a given Version.
        """
        try:
            paged_results = self.repository.version_instances.list(
                project_id, services_id=service_id, versions_id=version_id)
            return api_helpers.flatten_list_results(paged_results, 'instances')
        except (errors.HttpError, HttpLib2Error) as e:
            if isinstance(e, errors.HttpError) and e.resp.status == 404:
                return []
            raise api_errors.ApiExecutionError(project_id, e)
