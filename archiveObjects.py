import boto3
from datetime import datetime

# CONFIGURATIONS
bucketName = 'BUCKETNAME'  # Enter the bucket name
prefix = 'ANYPREFIX'  # Enter the prefix name
threshold = 30  # Enter the Threshold value, number of days after which the Storage Class of the objects to be changed to Glacier Deep Archive

s3 = boto3.client('s3')
curDate = datetime.today()

for key in s3.list_objects(Bucket=bucketName, Prefix=prefix)['Contents']:
    if key['Key'] != prefix:
        # print(key['Key'].split('/')[1])
        strDate = key['Key'].split('/')[1]
        oldDate = datetime.strptime(strDate, '%Y%m%d')
        if (curDate - oldDate).days >= threshold:
            if key['StorageClass'] != 'DEEP_ARCHIVE':
                print("Changing Storage Class for Object : " + key['Key'])
                copy_source = {
                    'Bucket': bucketName,
                    'Key': key['Key']
                }
                s3.copy(
                    copy_source, bucketName, key['Key'],
                    ExtraArgs={
                        'StorageClass': 'DEEP_ARCHIVE',
                        'MetadataDirective': 'COPY'
                    }
                )

