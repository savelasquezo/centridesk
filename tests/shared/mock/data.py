from shared.infrastructure.b64 import encode_obj
from shared.infrastructure.timestamps import from_timestamp_to_date


class MockData:

    def __init__(self):
        self.created_at = 1653458400
        self.updated_at = 1653458600
        self.closed_at = 1653458800

        # Dicts
        self.status_dict = {1: 'new', 2: 'open', 3: 'pending', 4: 'hold', 5: 'solved', 6: 'closed'}
        self.priorities_dict = {1: 'low', 2: 'medium', 3: 'high', 4: 'urgent'}
        self.chat_web_channel_id = '49646b17a76042fcbc4d40efdd2ebc30'
        self.whatsapp_channel_id = 'b7aa1136b454448d8ccaeaff6f9450fc'
        self.messenger_channel_id = '05c8c4b6c74241158fa4f00e3a5e0525'
        self.telegram_channel_id = 'c221ea086c4141ccb48f7e38cc1ac9d4'
        self.instagram_channel_id = 'ba14400e2259406bbd136fa602bb8c0d'
        self.channels_dict = {
            self.chat_web_channel_id: 'Chat Web',
            self.whatsapp_channel_id: 'Whatsapp',
            self.messenger_channel_id: 'Messenger',
            self.telegram_channel_id: 'Telegram',
            self.instagram_channel_id: 'Instagram'
        }

        # Channels
        self.channel_id_not_exist = '85f2ee7f60e24a2bb272a2684183a864'
        self.channel_platform_not_exist = 'platform_not_exist'

        self.channels = [
            {
                "unique_id": self.chat_web_channel_id,
                "name": self.channels_dict[self.chat_web_channel_id],
                "platform": "chatweb",
                "active": 1,
                "created_at": self.created_at,
            },
            {
                "unique_id": self.whatsapp_channel_id,
                "name": self.channels_dict[self.whatsapp_channel_id],
                "platform": "whatsapp",
                "active": 1,
                "created_at": self.created_at,
            },
            {
                "unique_id": self.messenger_channel_id,
                "name": self.channels_dict[self.messenger_channel_id],
                "platform": "messenger",
                "active": 1,
                "created_at": self.created_at,
            },
            {
                "unique_id": self.telegram_channel_id,
                "name": self.channels_dict[self.telegram_channel_id],
                "platform": "telegram",
                "active": 1,
                "created_at": self.created_at,
            },
            {
                "unique_id": self.instagram_channel_id,
                "name": self.channels_dict[self.instagram_channel_id],
                "platform": "instagram",
                "active": 1,
                "created_at": self.created_at,
            }
        ]

        # Accounts
        self.account_id_not_exist = "account_not_exist"
        self.account_id1 = "7e24c64985994a78a36b5f4b8e9bf69d"
        self.account_id2 = "4bde76ad380142d68167f09302c18009"
        self.account_id3 = "efaf32c172b841f3bbdb73be2a537a6a"

        self.accounts = [
            self.account_id1,
            self.account_id2,
            self.account_id3
        ]

        # Accounts platform products
        self.accounts_platform_products = [
            {
                "account_id": self.account_id1,
                "centridesk": True,
                "centripush": True
            },
            {
                "account_id": self.account_id2,
                "centridesk": True,
                "centripush": False
            }
        ]

        # Account webhook
        self.webhook_token1 = 'gewhrEF9dWabpGNWTWMSZNxbGUKhFWs3PYsa7FMSvmc'

        self.account_webhooks = [
            {
                'account_id': self.account_id1,
                'token': self.webhook_token1
            }
        ]

        # Projects
        self.project_id_not_exist = "project_not_exist"
        self.project_unique_id1 = "185a82a010a84f6aa32d1a11fdf35d5e"
        self.project_unique_id2 = "3f8349bb1d324adebd7eb7922c4ecd25"
        self.project_unique_id3 = "6fb8a0692b8f4b598284cc9c0bbe6e4c"

        self.projects = [
            {
                "id": self.project_unique_id1,
                "account_id": self.account_id1
            },
            {
                "id": self.project_unique_id2,
                "account_id": self.account_id1
            },
            {
                "id": self.project_unique_id3,
                "account_id": self.account_id2
            }
        ]

        # Templates
        self.template_category_account_update = "account_update"
        self.template_language_es = "es"
        self.template_status_approved = "approved"
        self.template_status_pending = "pending"
        self.template_status_rejected = "rejected"
        self.template_requested_at = 1655189538
        self.template_approved_at = 1655209538
        self.template_rejected_at = 1655209538

        self.template_unique_id1 = "7c9859919e35477cba5f34ccce6d0f7b"
        self.template_project_id1 = self.project_unique_id1
        self.template_name1 = "template_1"
        self.template_header1 = {"type": "text", "text": "template header 1"}
        self.template_body1 = "template body 1"
        self.template_footer1 = "template footer 1"
        self.template_buttons1 = {"type": None, "buttons": []}

        self.template_unique_id2 = "38559faf4d4d40b8843ff3a18a5321a0"
        self.template_project_id2 = self.project_unique_id1
        self.template_name2 = "template_2"
        self.template_header2 = {"type": "text", "text": "template header 2"}
        self.template_body2 = "template body 2"
        self.template_footer2 = "template footer 2"
        self.template_buttons2 = {"type": None, "buttons": []}

        self.template_unique_id3 = "f6d4276a733148fe963ada5da51a8a41"
        self.template_project_id3 = self.project_unique_id2
        self.template_name3 = "template_3"
        self.template_header3 = {"type": "text", "text": "template header 3"}
        self.template_body3 = "template body 3"
        self.template_footer3 = "template footer 3"
        self.template_buttons3 = {"type": None, "buttons": []}

        self.template_unique_id4 = "50a1f76d88a24456b5d850f0fbc06092"
        self.template_project_id4 = self.project_unique_id3
        self.template_name4 = "template_4"
        self.template_header4 = {"type": "text", "text": "template header 4"}
        self.template_body4 = "template body 4"
        self.template_footer4 = "template footer 4"
        self.template_buttons4 = {"type": None, "buttons": []}

        self.templates = [
            {
                "unique_id": self.template_unique_id1,
                "project_id": self.template_project_id1,
                "category": self.template_category_account_update,
                "name": self.template_name1,
                "language": self.template_language_es,
                "header": self.template_header1,
                "body": self.template_body1,
                "footer": self.template_footer1,
                "buttons": self.template_buttons1,
                "status": self.template_status_approved,
                "parameters_count": 0,
                "created_at": self.created_at,
                "requested_at": self.template_requested_at,
                "approved_at": self.template_approved_at,
                "rejected_at": None
            },
            {
                "unique_id": self.template_unique_id2,
                "project_id": self.template_project_id2,
                "category": self.template_category_account_update,
                "name": self.template_name2,
                "language": self.template_language_es,
                "header": self.template_header2,
                "body": self.template_body2,
                "footer": self.template_footer2,
                "buttons": self.template_buttons2,
                "status": self.template_status_rejected,
                "parameters_count": 0,
                "created_at": self.created_at,
                "requested_at": self.template_requested_at,
                "approved_at": None,
                "rejected_at": self.template_rejected_at
            },
            {
                "unique_id": self.template_unique_id3,
                "project_id": self.template_project_id3,
                "category": self.template_category_account_update,
                "name": self.template_name3,
                "language": self.template_language_es,
                "header": self.template_header3,
                "body": self.template_body3,
                "footer": self.template_footer3,
                "buttons": self.template_buttons3,
                "status": self.template_status_approved,
                "parameters_count": 0,
                "created_at": self.created_at,
                "requested_at": self.template_requested_at,
                "approved_at": self.template_approved_at,
                "rejected_at": None
            },
            {
                "unique_id": self.template_unique_id4,
                "project_id": self.template_project_id4,
                "category": self.template_category_account_update,
                "name": self.template_name4,
                "language": self.template_language_es,
                "header": self.template_header4,
                "body": self.template_body4,
                "footer": self.template_footer4,
                "buttons": self.template_buttons4,
                "status": self.template_status_approved,
                "parameters_count": 0,
                "created_at": self.created_at,
                "requested_at": self.template_requested_at,
                "approved_at": self.template_approved_at,
                "rejected_at": None
            }
        ]

        # Users and Roles
        self.role_trainer_id = 'd1b82f5bf1c3491d8cfe7b77fda06d4b'
        self.role_admin_id = 'dfa856ce88104968a7010b9a5e31fb58'
        self.role_superadmin_id = "c35851102cab49ff9d31e71c4a82b4e1"
        self.role_agent_id = "55f20c232859401da884b95bbd6535a4"
        self.role_supervisor_id = '115f18b805a14946824cb1fcfcf2e72d'

        self.roles = [
            {'unique_id': self.role_trainer_id, 'name': 'Entrenador', 'bot': 1, 'desk': 0},
            {'unique_id': self.role_admin_id, 'name': 'Administrador', 'bot': 1, 'desk': 1},
            {'unique_id': self.role_superadmin_id, 'name': 'SuperAdmin', 'bot': 1, 'desk': 1},
            {'unique_id': self.role_agent_id, 'name': 'Agent', 'bot': 0, 'desk': 1},
            {'unique_id': self.role_supervisor_id, 'name': 'Supervisor', 'bot': 0, 'desk': 1}
        ]

        self.user_id1 = 'b20997c0cfdd4e7fa902ad7b89afd2ff'
        self.user_id2 = 'c40453c0cfdd4e7fa902ad7b89afd2aa'
        self.user_id3 = 'bc38f14bc203433e98ac56de5cf69c98'
        self.user_id4 = '075cff15aaee4b83a052bd129113eb42'

        self.users_accounts = [
            {'id': 1, 'user_id': self.user_id1, 'account_id': self.account_id1},
            {'id': 2, 'user_id': self.user_id3, 'account_id': self.account_id1},
            {'id': 3, 'user_id': self.user_id4, 'account_id': self.account_id1}
        ]

        self.user_roles = [
            {'user_id': self.user_id1, 'role_id': self.role_superadmin_id},
            {'user_id': self.user_id4, 'role_id': self.role_trainer_id}
        ]

        # Agents (Centribot users)
        self.agent_unique_id1 = self.user_id1
        self.agent_first_name1 = "Superadmin1"
        self.agent_last_name1 = "Superadmin1"
        self.agent_email1 = "superadmin1@centribal.com"

        self.agent_unique_id2 = self.user_id3
        self.agent_first_name2 = "Agent2"
        self.agent_last_name2 = "Agent2"
        self.agent_email2 = "agent2@centribal.com"

        self.agents = [
            {
                'unique_id': self.agent_unique_id1,
                'first_name': self.agent_first_name1,
                'last_name': self.agent_last_name1,
                'email': self.agent_email1,
                'lang': 'es',
                'is_active': 1,
                'role_id': self.role_superadmin_id,
                'created_at': self.created_at,
                'updated_at': None,
                'deactivated_at': None
            },
            {
                'unique_id': self.agent_unique_id2,
                'first_name': self.agent_first_name2,
                'last_name': self.agent_last_name2,
                'email': self.agent_email2,
                'lang': 'es',
                'active': 1,
                'role_id': self.role_agent_id,
                'created_at': self.created_at,
                'updated_at': None,
                'deactivated_at': None
            }
        ]

        # Users tokens
        self.user_token_centribot_user_id1 = self.agent_unique_id1
        self.user_token_mobile_id1 = 'mobile_id_agent1'
        self.user_token_key1 = 'user_agent1_key'

        self.user_token_centribot_user_id2 = self.agent_unique_id2
        self.user_token_key2 = 'user_agent2_key'

        self.users_tokens = [
            {
                'centribot_user_id': self.user_token_centribot_user_id1,
                'mobile_id': encode_obj([self.user_token_mobile_id1]),
                'key': self.user_token_key1,
                'created_at': self.created_at,
                'updated_at': None
            },
            {
                'centribot_user_id': self.user_token_centribot_user_id2,
                'mobile_id': None,
                'key': self.user_token_key2,
                'created_at': self.created_at,
                'updated_at': None
            }
        ]

        # Customers
        self.customer_id_not_exist = '743ef7f8bf9243f594700ab88f950cd5'
        self.centribot_external_id_not_exist = 'a45a905edd7b422b93654e265fb3f895'
        self.email_not_exist = 'email_not_exit@mail.com'
        self.phone_not_exist = '+34678456456'

        self.customer_unique_id1 = "9177f1af705d46acb4e85afaf3cef30b"
        self.customer_display_name1 = "Centribot User 1"
        self.customer_centribot_external_id1 = "30b33bdea83d4fb9be46a499a3dd3176"

        self.customer_unique_id2 = '9f716d467f2e4918a179a4647cb2d7d5'
        self.customer_display_name2 = "Centribot User 2"
        self.customer_email2 = 'customer2@mail.com'
        self.customer_phone2 = '+34698543245'
        self.customer_centribot_external_id2 = '836dgah17k9ac70208fa14ea7d75c791hayqu87d'
        self.customer_created_at2 = 1654094955
        self.customer_updated_at2 = 1654094999
        self.customer_created_date2 = from_timestamp_to_date(self.customer_created_at2)
        self.customer_updated_date2 = from_timestamp_to_date(self.customer_updated_at2)

        self.customer_unique_id3 = '6a8db7c42b9ac70208fa14ea7d75c7d11317d462'
        self.customer_display_name3 = "Centribot User 3"
        self.customer_email3 = 'customer3@mail.com'
        self.customer_phone3 = '+34678678678'
        self.customer_centribot_external_id3 = '6a8db7c42b9ac70208fa14ea7d75c7d11317d462'
        self.customer_created_at3 = 1654094907
        self.customer_updated_at3 = 1654094915
        self.customer_created_date3 = from_timestamp_to_date(self.customer_created_at3)
        self.customer_updated_date3 = from_timestamp_to_date(self.customer_updated_at3)
        self.customer_company = 'Compañía'
        self.customer_delegation = 'Develop'
        self.external_id = 'ID-123456'
        self.external_id2 = 'ID-654321'

        self.customers = {
            self.account_id1: [
                {
                    "id": 1,
                    "unique_id": self.customer_unique_id1,
                    'agent_id': None,
                    "display_name": self.customer_display_name1,
                    "email": None,
                    "phone": None,
                    "centribot_external_id": self.customer_centribot_external_id1,
                    'company': None,
                    'delegation': None,
                    'last_comment_at': None,
                    'external_id': None,
                    'gdpr': 1,
                    'gdpr_updated_at': self.created_at,
                    "created_at": self.created_at,
                    "updated_at": None,
                    "active": True
                },
                {
                    'id': 2,
                    'unique_id': self.customer_unique_id2,
                    'agent_id': self.agent_unique_id1,
                    'display_name': self.customer_display_name2,
                    'email': self.customer_email2,
                    'phone': self.customer_phone2,
                    'centribot_external_id': self.customer_centribot_external_id2,
                    'company': encode_obj(self.customer_company),
                    'delegation': None,
                    'external_id': encode_obj(self.external_id),
                    'gdpr': 0,
                    'gdpr_updated_at': self.customer_created_at2,
                    'last_comment_at': None,
                    'created_at': self.customer_created_at2,
                    'updated_at': None,
                    'active': True
                },
                {
                    'id': 3,
                    'unique_id': self.customer_unique_id3,
                    'agent_id': self.agent_unique_id1,
                    'display_name': self.customer_display_name3,
                    'email': self.customer_email3,
                    'phone': self.customer_phone3,
                    'centribot_external_id': self.customer_centribot_external_id3,
                    'company': encode_obj(self.customer_company),
                    'delegation': encode_obj(self.customer_delegation),
                    'external_id': encode_obj(self.external_id2),
                    'gdpr': 1,
                    'gdpr_updated_at': self.customer_created_at3,
                    'last_comment_at': None,
                    'created_at': self.customer_created_at3,
                    'updated_at': None,
                    'active': True
                }
            ]
        }

        # Tickets
        self.ticket_title = "Centridesk tickets"
        self.tags_open = ["test", "platform_centribot", "centribot_intent_desk", "centribot_chatweb"]
        self.tags_solved = self.tags_open.copy() + ["platform_centribot_solved"]

        self.centribot_channel_id1 = "5e0814d23ec74e57a09184a5d2f166c0"
        self.centribot_project_id1 = self.project_unique_id1

        self.ticket_unique_id1 = "9102302ea0a945bfa6c02439adcdbbef"
        self.ticket_unique_id2 = "5b294f24b16a4a7794adb9ae775ef828"
        self.ticket_unique_id3 = "ac14494fb9174aeb8e6a4d6e0a3a8199"
        self.ticket_unique_id4 = "yu93889fb9174aeb8e6a4d6e0a3a0945"

        self.tickets = {
            self.account_id1: [
                {
                    "id": 1,
                    "unique_id": self.ticket_unique_id1,
                    "title": encode_obj(self.ticket_title),
                    "assignee_id": None,
                    "author_id": self.customer_unique_id1,
                    "is_agent": 0,
                    "priority_id": 1,
                    "status_id": 2,
                    "external_id": self.customer_centribot_external_id1,
                    "channel_id": self.chat_web_channel_id,
                    "centribot_channel_id": self.centribot_channel_id1,
                    "centribot_project_id": self.centribot_project_id1,
                    "tags": encode_obj(self.tags_open),
                    "active": 1,
                    "created_at": self.created_at,
                    "updated_at": None,
                    "closed_at": None
                },
                {
                    "id": 2,
                    "unique_id": self.ticket_unique_id2,
                    "title": encode_obj(self.ticket_title),
                    "assignee_id": None,
                    "author_id": self.customer_unique_id1,
                    "is_agent": 0,
                    "priority_id": 2,
                    "status_id": 2,
                    "external_id": self.customer_centribot_external_id1,
                    "channel_id": self.chat_web_channel_id,
                    "centribot_channel_id": self.centribot_channel_id1,
                    "centribot_project_id": self.centribot_project_id1,
                    "tags": encode_obj(self.tags_open),
                    "active": 1,
                    "created_at": self.created_at + 10,
                    "updated_at": self.updated_at,
                    "closed_at": None
                },
                {
                    "id": 3,
                    "unique_id": self.ticket_unique_id3,
                    "title": encode_obj(self.ticket_title),
                    "assignee_id": None,
                    "author_id": self.customer_unique_id1,
                    "is_agent": 0,
                    "priority_id": 3,
                    "status_id": 5,
                    "external_id": self.customer_centribot_external_id1,
                    "channel_id": self.chat_web_channel_id,
                    "centribot_channel_id": self.centribot_channel_id1,
                    "centribot_project_id": self.centribot_project_id1,
                    "tags": encode_obj(self.tags_solved),
                    "active": 1,
                    "created_at": self.created_at + 20,
                    "updated_at": self.updated_at,
                    "closed_at": None
                },
                {
                    "id": 3,
                    "unique_id": self.ticket_unique_id4,
                    "title": encode_obj(self.ticket_title),
                    "assignee_id": None,
                    "author_id": self.customer_unique_id3,
                    "is_agent": 0,
                    "priority_id": 3,
                    "status_id": 5,
                    "external_id": self.customer_centribot_external_id1,
                    "channel_id": self.chat_web_channel_id,
                    "centribot_channel_id": self.centribot_channel_id1,
                    "centribot_project_id": self.centribot_project_id1,
                    "tags": encode_obj(self.tags_solved),
                    "active": 1,
                    "created_at": self.created_at + 30,
                    "updated_at": self.updated_at,
                    "closed_at": None
                }
            ]
        }

        # Tickets filters, sorts and order
        self.filter_by_author_id1_status2 = {
            "author_id": self.customer_unique_id1,
            "status_id": 2
        }

        self.filter_by_invalid_field = {
            "invalid_field": "no_value"
        }

        self.sort_created_at = "created_at"
        self.sort_invalid = "invalid_field"

        self.order_desc = "desc"
        self.order_invalid = "invalid_order"

        # Comments
        self.comment_unique_id1 = "ca82123116b24267b5f1caaa784af6e4"
        self.comment_text1 = "Comment 1 text"
        self.comment_attachments1 = [
            {
                "type": "image",
                "mediatype": "image/jpg",
                "url": "http://url.example.com/s3bucketresource.jpg",
                "mediasize": "1234"
            }
        ]

        self.comments = {
            self.account_id1: [
                {
                    'unique_id': self.comment_unique_id1,
                    'text': encode_obj(self.comment_text1),
                    'text_json': None,
                    'attachments': encode_obj(self.comment_attachments1),
                    'author_id': self.customer_unique_id1,
                    'is_agent': 0,
                    'public': 1,
                    'ticket_id': self.ticket_unique_id1,
                    'created_at': self.created_at
                }
            ]
        }

        # Actions
        self.action_id1 = '55c2ea2d-5c89-4ea6-b27c-099cc298d791'
        self.action_id2 = '94934460-4d62-4397-a4ad-55248e5d0df9'
        self.action_id3 = '94934460-4d62-4397-a4ad-55248e5d0df9'
        self.actions = {
            self.account_id1: [
                {
                    "id": self.action_id1,
                    "action": "desk_download_users",
                    "requester_id": self.user_id1,
                    "pending": False,
                    "in_progress": False,
                    "info": encode_obj({"filter": {"name": "lala"}}),
                    "result": 0,
                    "error": None,
                    "created_at": self.created_at,
                    "initiated_at": None,
                    "finished_at": None
                },
            ],
            self.account_id2: [
                {
                    "id": self.action_id2,
                    "action": "desk_download_users",
                    "requester_id": self.user_id1,
                    "pending": False,
                    "in_progress": True,
                    "info": encode_obj({"filter": {"name": "lala"}}),
                    "result": 0,
                    "error": None,
                    "created_at": self.created_at,
                    "initiated_at": None,
                    "finished_at": None
                },
            ],
            self.account_id3: [
                {
                    "id": self.action_id3,
                    "action": "desk_download_users",
                    "requester_id": self.user_id1,
                    "pending": True,
                    "in_progress": False,
                    "info": encode_obj({"filter": {"name": "lala"}}),
                    "result": 0,
                    "error": None,
                    "created_at": self.created_at,
                    "initiated_at": None,
                    "finished_at": None
                },
            ]
        }
