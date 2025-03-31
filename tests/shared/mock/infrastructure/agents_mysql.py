from src.agents.domain.agent_out import AgentOut
from tests.shared.mock.data import MockData


class AgentsMysql:

    def __init__(self, agent_id=None, account_id=None, mock=None):
        self.agent_id = agent_id
        self.account_id = account_id
        self.mock = mock or MockData()

    def get_by_id(self):
        for agent in self.mock.agents:
            if agent['unique_id'] == self.agent_id:
                return AgentOut(agent).data

    def get_account(self):
        pass

    def get_user_account_by_user_and_account(self):
        user_account = None
        for ua in self.mock.users_accounts:
            if ua['user_id'] == self.agent_id and ua['account_id'] == self.account_id:
                user_account = ua
        return user_account

    def get_user_rol_by_user(self):
        user_role = None
        for ur in self.mock.user_roles:
            if ur['user_id'] == self.agent_id:
                user_role = ur
        return user_role

    def get_role(self, role_id):
        role = None
        for r in self.mock.roles:
            if r['unique_id'] == role_id:
                role = r
        return role

    def get_rol_by_user(self):
        user_role = {}
        for ur in self.mock.user_roles:
            if ur['user_id'] == self.agent_id:
                for r in self.mock.roles:
                    if r['unique_id'] == ur['role_id']:
                        user_role['user_id'] = ur['user_id']
                        user_role['role_id'] = ur['role_id']
                        user_role['name'] = r['name']
                        user_role['bot'] = r['bot']
                        user_role['desk'] = r['desk']

        return user_role
