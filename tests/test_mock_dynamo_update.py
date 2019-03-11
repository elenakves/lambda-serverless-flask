import sys
import unittest
import boto3
import json

from moto import mock_dynamodb2
sys.path.append("..")
import custom_platform.app as app

BASE_URL = "http://127.0.0.1:5000/users"
GOOD_ITEM_URL = "{}/1".format(BASE_URL)

USERS_TABLE = "users-table-test-update"

class TestDynamoUpdate(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    @mock_dynamodb2
    def test_update_user(self):
        client = boto3.client("dynamodb")

        # create mimic table - it will be intercepted by the moto framework
        table = client.create_table(
            TableName=USERS_TABLE,
            KeySchema=[
                {
                    "AttributeName": "user_id",
                    "KeyType": "HASH"
                },
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "user_id",
                    "AttributeType": "S"
                },

            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
            }
        )
        # populate table with data
        item = {}
        item["user_id"] = {"S": "1"}
        item["name"] = {"S": "test name"}
        item["access"] = {"S": "user"}
        client.put_item(TableName=USERS_TABLE, Item=item)

        new_item = {}
        new_item["user_id"] = {"S": "1"}
        new_item["name"] = {"S": "updated test name"}
        new_item["access"] = {"S": "admin"}

        response = self.app.put(BASE_URL,
                                data=json.dumps(new_item),
                                content_type='application/json')
        print(response)

        self.assertEqual(response.status_code, 200)
        #self.assertEquals(result.get("name").get("S"), "updated test name")
        #self.assertEquals(result.get("access").get("S"), "admin")


if __name__ == "__main__":
    unittest.main()