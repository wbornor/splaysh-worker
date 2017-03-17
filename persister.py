__author__ = 'wesbornor'

import boto.dynamodb

import creds

# put record to DynamoDB
def put(json):
    conn = boto.dynamodb.connect_to_region(
        'us-east-1',
        aws_access_key_id=creds.aws["aws_access_key_id"],
        aws_secret_access_key=creds.aws["aws_secret_access_key"])
    print "itemsTable: " + creds.aws['itemsTable']
    table = conn.get_table(creds.aws['itemsTable'])

    for entry in json:
        item = table.new_item(
            hash_key=entry["id"],
            range_key=entry["create_date"],
            attrs=entry
        )
        item.put()
        print 'put: ' + str(item)
        time.sleep(2)