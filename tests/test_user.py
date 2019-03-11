import sys
import unittest
import boto3
import json

from moto import mock_dynamodb2
sys.path.append("..")
import custom_platform.app as app

BASE_URL = "http://127.0.0.1:5000/users"
GOOD_ITEM_URL = "{}/1".format(BASE_URL)
BAD_ITEM_URL = "{}/2".format(BASE_URL)
USERS_TABLE = "users-table-test"


class TestDynamoDB(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()


    @mock_dynamodb2
    def create_table(self):

        dynamodb = boto3.client("dynamodb")

        # create mimic table - it will be intercepted by the moto framework
        table = dynamodb.create_table(
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
        item["name"] = {"S": "TEST NAME"}
        item["password"] = {"S": "PASSWORD1"}
        item["access"] = {"S": "user"}

        response_from_mock = dynamodb.put_item(TableName=USERS_TABLE, Item=item)
        print(response_from_mock["Attributes"])

        return table

    def test_create_user(self):

        item = {}
        item["user_id"] = {"S": "2"}
        item["name"] = {"S": "TEST NAME"}
        item["password"] = {"S": "PASSWORD1"}
        item["access"] = {"S": "user"}

        response = self.app.post(BASE_URL,
                                 data=json.dumps(item),
                                 content_type='application/json')
        print(response)

        self.assertEqual(response.status_code, 200)
        #self.assertTrue("user_id" in response.get_data())
        #self.assertEquals(item.get("userID").get("S"), "2")

    def test_delete_user(self):

        response = self.app.delete(BAD_ITEM_URL)

        self.assertEqual(response.status_code, 200)

    def test_get_user(self):

        response = self.app.get(GOOD_ITEM_URL)
        print(response)
        self.assertEqual(response.status_code, 200)
        response = self.app.get(BAD_ITEM_URL)
        self.assertEqual(response.status_code, 404)
        #self.assertTrue("user_id" in response.get_data())

    def test_update_user(self):

        updated_item = {}
        updated_item["user_id"] = {"S": "1"}
        updated_item["name"] = {"S": "updated test name"}
        updated_item["access"] = {"S": "admin"}

        response = self.app.put(BASE_URL,
                                data=json.dumps(updated_item),
                                content_type='application/json')
        print(response)

        self.assertEqual(response.status_code, 200)
        # self.assertEquals(response.get("name").get("S"), "updated test name")
        # self.assertEquals(response.get("access").get("S"), "admin")

    @mock_dynamodb2
    def tearDown(self):
        dynamodb = boto3.client("dynamodb")
        dynamodb.delete_table(
            TableName=USERS_TABLE
        )


if __name__ == "__main__":
    unittest.main()