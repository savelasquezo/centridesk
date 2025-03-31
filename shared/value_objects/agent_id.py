from shared.exceptions.type_error import TypeErrorValue
from shared.value_objects.unique_id import UniqueID


class AgentID:
    def __init__(self, agent_id):
        self.__name = 'Agent ID'
        self.agent_id = agent_id

    @property
    def agent_id(self):
        return self.__agent_id

    @agent_id.setter
    def agent_id(self, agent_id):
        value = None
        if agent_id:
            try:
                agent_id = UniqueID(agent_id)
            except Exception:
                raise TypeErrorValue('agent ID')
            value = agent_id.value

        self.__agent_id = value
