import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2sr = session.resource('ec2')

def filter_instances(project):
	filters = [{'Name': 'tag:Project', 'Values': [project]}]
	if project:
		return ec2sr.instances.filter(Filters=filters)
	else:
		return ec2sr.instances.all()

####################################################################

@click.group()		#Check https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands for nesting commands
def instances():
	"Commands for EC2 instances"

@instances.command('list')		#'list' --> this is the command name now
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def list_instances(project):
	"Lists EC2 instances"

	instances_list = filter_instances(project)
	for i in instances_list:
		print(', '.join([i.instance_id, i.instance_type, i.public_dns_name, i.placement['AvailabilityZone'], i.state['Name'], str(i.tags)]))

@instances.command('start')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def start_instances(project):
	"Starts EC2 instances"

	instances_list = filter_instances(project)
	for i in instances_list:
			i.start()
			print("Starting EC2 instance " + str(i.instance_id))

@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def stop_instances(project):
	"Stops EC2 instances"

	instances_list = filter_instances(project)
	for i in instances_list:
			i.stop()
			print("Stopping EC2 instance " + str(i.instance_id))

####################################################################

if __name__ == '__main__':
	instances() 