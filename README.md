### API EndPoints

Messages Management API (Root: http://themessengertask.herokuapp.com/api/). 


| HTTP Method | Endpoint | Params | Payload |Output Example| Description
| ------ | ------ | ------ | ------ | ------ | ------ |
| POST | /message/ | |{"receiver": "Receiver user name.", "subject": "Message subject."}|{"sender": "admin", "receiver": "Test", "subject": "Test Message", "creation_date": "2019-07-10T02:41:18.708000Z", "is_read": false}| Create Message.
| DELETE | //message/{message_id}/ | | | | Delete Message.
| POST | /message/{message_id}/read_message/ | | |{"sender": "Test", "receiver": "admin", "subject": "Hi there", "creation_date": "2019-07-10T02:41:17Z", "is_read": true}| Fetch message and mark it as read.
| GET | /message/received_messages/ | | |[{"sender": "admin", "receiver": "Test", "subject": "Hi", "creation_date": "2019-07-10T02:41:17Z", "is_read": false}]| Fetch all received messages by logged user.
| GET | /message/unread_messages/ | | |[{"sender": "admin", "receiver": "Test", "subject": "Hi", "creation_date": "2019-07-10T02:41:17Z", "is_read": false}]| Fetch all the unread messages which received by logged user.


