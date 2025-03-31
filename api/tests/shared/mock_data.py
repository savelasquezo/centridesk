from shared.infrastructure.b64 import encode_obj


class MockData:

    def __init__(self):
        # Accounts
        self.account_id1 = 'a96af04e2230436c83bc1c57540d2a4a'
        self.account_id2 = '71cbe8a8bac74065b1964ac2ff2ae9d7'

        self.account_not_found = '2d954a3be6ff4a5f90b5715d5227fa43'

        self.accounts = [
            {'unique_id': self.account_id1, 'name': self.account_id1, 'active': True},
            {'unique_id': self.account_id2, 'name': self.account_id2, 'active': True}
        ]

        self.accounts_databases = [self.account_id1]

        # Tokens
        self.token1 = 'd75c7d11317d4626a8db7c42b9ac70208fa14ea7'
        self.token2 = 'a74fc2351fe83644ae808f02a280df829175fe23'
        self.token3 = '98uidrtsbTrD35Es68u89oT5rrPer57Yt72sxdr8'
        self.new_token = '6a8db7c42b9ac70208fa14ea7d75c7d11317d462'  # do not relate with account!

        self.my_tokens = [
            {'name': 'centribot', 'key': self.token1, 'account_id': self.account_id1},
            {'name': 'centribot', 'key': self.token2, 'account_id': self.account_id2}
        ]

        # dates
        self.created_at = 1609341795
        self.created_date = '2020-12-30 16:23:15'

        self.updated_at = 1609419210
        self.updated_date = "2020-12-31 13:53:30"

        self.username = 'test@centribal.com'
        self.password = 'Centribal.Password123!'

        self.centribot_user_id1 = 'dc3b229281894b069d8582d7708c1bd5'
        self.centribot_user_id2 = '8uk265ts81894b069d8582d7poy67drt'
        self.centribot_user_id3 = '9ie6tyeYr9IO98u79d85828II0ongrE3'

        self.mobile_id1 = '1925484eff3a441dbef6c744d3ebecf8'

        # Static users token
        self.no_expired_user1 = {
            'key': self.token1,
            'centribot_user_id': self.centribot_user_id1,
            'mobile_id': None,
            'created_at': self.created_at,
            'updated_at': None
        }

        self.no_expired_user2 = {
            'key': self.token2,
            'centribot_user_id': self.centribot_user_id2,
            'mobile_id': None,
            'created_at': self.created_at,
            'updated_at': None
        }
        self.no_expired_user3 = {
            'key': self.token3,
            'centribot_user_id': self.centribot_user_id3,
            'mobile_id': encode_obj([self.mobile_id1]),
            'created_at': self.created_at,
            'updated_at': self.created_at
        }

        self.users_token = [self.no_expired_user1, self.no_expired_user2, self.no_expired_user3]
