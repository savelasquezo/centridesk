import unittest


from shared.infrastructure.timestamps import from_timestamp_to_date
from src.agents.domain.agent_out import AgentOut
from tests.shared.mock.data import MockData


class TestAgentOut(unittest.TestCase):

    def setUp(self) -> None:
        self.mock = MockData()

    def test_all_values_ok(self):
        expected = {
            'id': self.mock.agent_unique_id1,
            'name': f"{self.mock.agent_first_name1} {self.mock.agent_last_name1}",
            'email': self.mock.agent_email1,
            'lang': 'es',
            'active': True,
            'created_at': from_timestamp_to_date(self.mock.created_at),
            'updated_at': None,
            'deactivated_at': None
        }

        self.assertEqual(AgentOut(self.mock.agents[0]).data, expected)
