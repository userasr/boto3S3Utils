import boto3
import datetime
import argparse

parser = argparse.ArgumentParser("Enter one argument either 'snapshot' or 'export'. 'snapshot' creates a snapshot of whole RDS instance. 'export' pushes the DB data to S3 bucket.")
parser.add_argument("dbtask", type=str, help="Enter either 'snapshot' or 'export'. 'snapshot' creates a snapshot of whole RDS instance. 'export' pushes the DB data to S3 bucket.")
args = parser.parse_args()

client = boto3.client('rds')

if args.dbtask == 'snapshot' :
	print('Creating DB Snapshot : MYDB-snapshot-monthly-%s' % datetime.datetime.now().strftime("%b%Y"))
	client.create_db_snapshot(
        	DBInstanceIdentifier='MYDB',
        	DBSnapshotIdentifier='MYDB-snapshot-monthly-%s' % datetime.datetime.now().strftime("%b%Y"),
        	Tags=[
            	   {
                	'Key': 'MYDBBKP',
                	'Value': 'MYDB'
             	   },
        	]
    	)
elif args.dbtask == 'export' :
	print('Exporting DB data to S3 bucket MYDB-snapshot/ENV/MYDB-snapshot-monthly-%s' % datetime.datetime.now().strftime("%b%Y"))
	client.start_export_task(
                ExportTaskIdentifier='MYDB-snapshot-monthly-%s' % datetime.datetime.now().strftime("%b%Y"),
                SourceArn='arn:aws:rds:us-west-2:MYACCOUNT:snapshot:MYDB-snapshot-monthly-%s' % datetime.datetime.now().strftime("%b%Y"),
                S3BucketName='MYDB-snapshot',
		S3Prefix='ENV/MYDB-snapshot-monthly-%s' % datetime.datetime.now().strftime("%b%Y"),
                IamRoleArn='arn:aws:iam::MYACCOUNT:role/service-role/S3WriteTemporary',
                KmsKeyId='arn:aws:kms:us-west-2:MYACCOUNT:key/KEYKEY',
                ExportOnly=['database','MYDB']
        )
else :
        print("Enter one argument either 'snapshot' or 'export'. 'snapshot' creates a snapshot of whole RDS instance. 'export' pushes the DB data to S3 bucket.")
