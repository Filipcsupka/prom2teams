import unittest
import json

from tests.context import MessageSchema, compose_all, map_prom_alerts_to_teams_alarms


class TestJSONFields(unittest.TestCase):

    TEST_CONFIG_FILES_PATH = 'data/jsons/'

    def test_json_with_all_fields(self):
        with open(self.TEST_CONFIG_FILES_PATH + 'all_ok.json') as json_data:
            json_received = json.load(json_data)
            message_schema = MessageSchema()
            alerts = message_schema.load(json_received).data
            alarm = map_prom_alerts_to_teams_alarms(alerts)[0]
            self.assertNotIn('unknown', str(alarm))

    def test_json_without_mandatory_field(self):
        with open(self.TEST_CONFIG_FILES_PATH + 'without_mandatory_field.json') as json_data:
            json_received = json.load(json_data)
            message_schema = MessageSchema()
            alerts = message_schema.load(json_received).data
            alarm = map_prom_alerts_to_teams_alarms(alerts)[0]
            self.assertIn('unknown', str(alarm))

    def test_json_without_optional_field(self):
        with open(self.TEST_CONFIG_FILES_PATH + 'without_optional_field.json') as json_data:
            json_received = json.load(json_data)
            message_schema = MessageSchema()
            alerts = message_schema.load(json_received).data
            alarm = map_prom_alerts_to_teams_alarms(alerts)[0]
            self.assertNotIn('unknown', str(alarm))

    def test_json_without_instance_field(self):
        with open(self.TEST_CONFIG_FILES_PATH + 'without_instance_field.json') as json_data:
            json_received = json.load(json_data)
            message_schema = MessageSchema()
            alerts = message_schema.load(json_received).data
            alarm = map_prom_alerts_to_teams_alarms(alerts)[0]
            self.assertEqual('unknown', str(alarm['instance']))

    def test_compose_all(self):
        with open(self.TEST_CONFIG_FILES_PATH + 'all_ok.json') as json_data:
            with open(self.TEST_CONFIG_FILES_PATH + 'teams_alarm_all_ok.json') as expected_data:
                json_received = json.load(json_data)
                json_expected = json.load(expected_data)

                message_schema = MessageSchema()
                alerts = message_schema.load(json_received).data
                alarms = map_prom_alerts_to_teams_alarms(alerts)
                rendered_data = compose_all(alarms)[0]
                json_rendered = json.loads(rendered_data)

                self.assertDictEqual(json_rendered, json_expected)


if __name__ == '__main__':
    unittest.main()
