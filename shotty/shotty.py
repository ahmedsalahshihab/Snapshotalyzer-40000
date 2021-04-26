import boto3

if __name__ == '__main__':

	session = boto3.Session(profile_name='shotty')
	ec2sr = session.resource('ec2')

	for i in ec2sr.instances.all():
		print(i)