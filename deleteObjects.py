import boto3
from datetime import datetime

# CONFIGURATIONS
bucketName = 'BUCKETNAME'  # Enter the bucket name
prefix = 'ANYPREFIX'  # Enter the prefix name
threshold = 21  # Enter the Threshold value, number of days after which the objects will get deleted from the Glacier Deep Archive

s3 = boto3.client('s3')
curDate = datetime.today()
delete_key_list = []

s3Resource = boto3.resource('s3')

bucket = s3Resource.Bucket(bucketName)
for key in s3.list_objects(Bucket=bucketName, Prefix=prefix)['Contents']:
    if key['Key'] != prefix:
        # print(key['Key'].split('/')[1])
        strDate = key['Key'].split('/')[1]
        oldDate = datetime.strptime(strDate, '%Y%m%d')
        if (curDate - oldDate).days >= threshold:
            if key['StorageClass'] == 'DEEP_ARCHIVE':
                print("Deleting Object : " + prefix + strDate)
                newPrefix = prefix + strDate
                bucket.objects.filter(Prefix=newPrefix).delete()

