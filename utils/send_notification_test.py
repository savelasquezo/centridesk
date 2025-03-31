from os import path as os_path
from sys import path as sys_path

sys_path.append(f"{os_path.dirname(os_path.abspath(__file__))}/..")

from shared.firebase.infrastructure.firebase_connector import FirebaseConnector

if __name__ == '__main__':

    print("entro al main")

    firebase_connector = FirebaseConnector()

    user_token = "elccJpIvSyq1MBiCQpdWW1:APA91bEE4-TMtU0k2XULz9rRsosmpuP8rZuoaQbKwOfsk6mbx05WckAjpjLSjho9XYjLZj1-FNK4_ZdVLHs5O3kPfbv5bqnCs_a2a_uQkeVp1v02mEU-YKOFj5WpplfmeOTpJ1Lsh-m_"

    notification = {
        "title": "Title de test",
        "body": "Body de test"
    }

    data = {
        "customer_id": "123456",
        "customer_name": "Carlos test"
    }

    print(firebase_connector.send_notification(notification, data, user_token))
