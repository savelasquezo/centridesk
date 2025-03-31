from io import StringIO

from pandas import DataFrame

from shared.email.infrastructure.async_email_sender import EmailSender
from src.agents.infrastructure.agents_mysql import AgentsMysql
from src.comments.infrastructure.comments_mysql import CommentsMysql
from src.configurations.infrastructure.transcriptions_mysql import TranscriptionsMysql
from src.customers.infrastructure.customers_mysql import CustomersMysql
from src.tickets.infrastructure.tickets_mysql import TicketsMysql


class EpSendTicketTranscription:

    def __init__(self, account_id, ticket_id, subject) -> None:
        self.account_id = account_id
        self.ticket_id = ticket_id
        self.subject = subject

        self.__agents = {}

    def run(self):
        tickets = TicketsMysql(account_id=self.account_id, ticket_id=self.ticket_id)
        ticket = tickets.get_by_id()

        agents = AgentsMysql()

        if not ticket['is_agent']:
            customers = CustomersMysql(account_id=self.account_id, customer_id=ticket['author_id'])
            author = customers.get_by_id()

        else:
            agents.agent_id = ticket['author_id']
            author = agents.get_by_id()

        comments = CommentsMysql(account_id=self.account_id, ticket_id=self.ticket_id)
        comm = comments.get_by_ticket()

        attachments = []
        transcription = []

        for __c in comm:
            if __c['text_json']:
                for __i in __c['text_json']['interactions']:
                    transcription.append({
                        "created_at": __i['created_at'],
                        "author": 'Bot' if __i['is_bot'] else author['name'],
                        "text": __i['text'],
                        "attachment": __i.get('url')
                    })

                    if __i.get('url'):
                        attachments.append({'url': __i['url']})

            else:
                if __c['is_agent']:
                    agent = self.__agents.get(__c['author_id'])

                    if not agent:
                        agents.agent_id = __c['author_id']
                        agent = agents.get_by_id()

                transcription.append({
                    "created_at": __c['created_at'],
                    "author": agent['name'] if __c['is_agent'] else author['name'],
                    "text": __c['text'] if __c['text'] != 'only_attachment' else '',
                    "attachment": __c['attachments'][0]['url'] if __c['text'] == 'only_attachment' else None
                })

            if __c['attachments']:
                attachments.extend(__c['attachments'])

        _df = DataFrame(transcription)

        buf = StringIO()
        _df.to_csv(buf, index=False)
        csv = buf.getvalue()
        buf.close()

        attachments.append({
            'type': 'text',
            'content': csv,
            'name': 'transcription.csv'
        })

        # todo get email from transcription configuration
        transcriptions_obj = TranscriptionsMysql(account_id=self.account_id)
        config = transcriptions_obj.get_by_key()

        if not config:
            raise Exception('Transcription not found')

        __s = EmailSender(
            email=config['info']['email'],
            language='en',
            template='desk_send_ticket_transcription',
            attachments=attachments,
            subject=self.subject,
        )
        __s.send()
