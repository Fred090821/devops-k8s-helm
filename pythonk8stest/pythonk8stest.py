import os
import subprocess
import unittest
from unittest import TestCase
import pytest
import requests
import logging


# Post a new user data to the REST API using POST method.
# Submit a GET request to make sure status code is 200 and data equals to the
# posted data.
# Check posted data was stored inside DB (users table).
class IntegrationTests(TestCase):
    user_name = None
    k8s_url = os.environ['k8s_url']

    def setUpClass(cls):
        cls.user_name = 'john'
        cls.api_url = cls.k8s_url + '/users/'
        print(cls.api_url)
        cls.post_data = {"user_name": cls.user_name}

    def test_step_1_post_john_status_200(self):
        logging.debug("Test creation of user john with POST")

        post_response = requests.post(self.api_url, json={"user_name": self.user_name})
        pytest.last_added_user_id = post_response.json().get("added_user_id")
        assert post_response.status_code == 200

    def test_step_2_get_john_status_200(self):
        logging.debug(" Test retrieving of user john with GET")
        logging.debug(" str(pytest.last_added_user_id) = %s", str(pytest.last_added_user_id))
        logging.debug(" self.api_url = %s", self.api_url)
        get_response = requests.get(self.api_url + str(pytest.last_added_user_id))
        self.assertEqual(get_response.status_code, 200)

        logging.debug(" Test Extract User Name")
        extract_user_name = get_response.json().get("user_name")
        logging.debug(" extract_user_name = %s", extract_user_name)
        self.assertEqual(extract_user_name, self.user_name, f"Unexpected JSON content: {extract_user_name}")

        logging.debug(" Test assert extract_user_name == self.user_name")
        # Assert the actual JSON content matches the expected JSON content
        assert extract_user_name == self.user_name, f"Unexpected JSON content: {extract_user_name}"


if __name__ == "__main__":
    unittest.main()
