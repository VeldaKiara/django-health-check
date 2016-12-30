# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

from health_check.backends import BaseHealthCheckBackend
from health_check.plugins import plugin_dir


class TestHomeView(object):
    url = reverse_lazy('health_check_home')

    def test_success(self, client):
        response = client.get(self.url)
        assert response.status_code == 200, response.content.decode('utf-8')

    def test_error(self, client):
        class MyBackend(BaseHealthCheckBackend):
            def run_check(self):
                self.add_error('Super Fail!')

        plugin_dir.register(MyBackend)
        response = client.get(self.url)
        assert response.status_code == 500, response.content.decode('utf-8')
        assert b'Super Fail!' in response.content