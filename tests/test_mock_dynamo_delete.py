import sys
import unittest
import boto3

from moto import mock_dynamodb2
sys.path.append("..")
import custom_platform.app as app

BASE_URL = "http://127.0.0.1:5000/users"
GOOD_ITEM_URL = "{}/1".format(BASE_URL)
BAD_ITEM_URL = "{}/3".format(BASE_URL)

class TestDynamoDelete(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()


    @mock_dynamodb2
    def test_delete_user(self):
        self.table_name = "users-table-test-delete"
        self.client = boto3.client("dynamodb")
        # create mimic table - it will be intercepted by the moto framework
        table = self.client.create_table(
            TableName=self.table_name,
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

        response_from_mock = self.client.put_item(TableName=self.table_name, Item=item)
        print(response_from_mock["Attributes"])

        response = self.app.delete(GOOD_ITEM_URL)
        self.assertEqual(response.status_code, 204)

        response = self.app.delete(BAD_ITEM_URL)
        self.assertEqual(response.status_code, 404)

    # @mock_dynamodb2
    # def tearDown(self):
    #     self.client.delete_table(
    #         TableName=self.table_name
    #     )

if __name__ == "__main__":
    unittest.main()
