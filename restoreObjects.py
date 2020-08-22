import boto3
from botocore.exceptions import ClientError

bucketName = 'BUCKETNAME'
prefix = 'ANYPREFIX'
restore_days = 2	#Change it as per the need
recallTier = 'Standard'	#Change it as per the need
result = ''

s3 = boto3.client('s3')
s3Resource = boto3.resource('s3')
bucket = s3Resource.Bucket(bucketName)

for key in s3.list_objects(Bucket=bucketName, Prefix=prefix)['Contents']:
    if key['Key'] != prefix and key['StorageClass'] == 'DEEP_ARCHIVE':
        #print key['Key']
        s3_object = s3Resource.Object(bucketName, key['Key'])
        print("Restoring object : "+ key['Key'])
        try:
            result = s3_object.restore_object(
                RestoreRequest={'Days': restore_days, 'GlacierJobParameters': {'Tier': recallTier}})
        except ClientError as e:
            if e.response['Error']['Code'] == 'RestoreAlreadyInProgress':
                print(e.response['Error']['Code'])
            else:
                print("Unexpected Error whilst attempting to recall object")
        print (result)


