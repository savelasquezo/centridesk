from django.test import SimpleTestCase

from shared.value_objects.agent_id import AgentID


class TestAgentId(SimpleTestCase):

    def test_agent_id_correct_format(self):

        unique_id = "b20997c0-cfdd-4e7f-a902-ad7b89afd2ff"

        try:
            result = AgentID(unique_id)
        except Exception as e:
            result = str(e)

        self.assertEqual(result.agent_id, unique_id)

    def test_agent_id_wrong_format(self):

        unique_id = "b20997c0cfdd4e7fa902ad7b89a"
        expected_result = "Agent id has an invalid type."

        try:
            result = AgentID(unique_id)
        except Exception as e:
            result = str(e)

        self.assertEqual(result, expected_result)
