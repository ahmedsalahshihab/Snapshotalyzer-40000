import boto3
import click
import botocore		#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html

session = boto3.Session(profile_name='shotty')
ec2sr = session.resource('ec2')

def filter_instances(project):
	filters = [{'Name': 'tag:Project', 'Values': [project]}]
	if project:
		return ec2sr.instances.filter(Filters=filters)
	else:
		return ec2sr.instances.all()

def has_pending_snapshot(volume):
	all_snapshots = volume.snapshots.all()
	for s in all_snapshots:
		if (s.state == "pending"):
			return True
			break
	else:
		return False

####################################################################

@click.group()
def cli():
	"Snapshot manager"

####################################################################

@cli.group('instances')		#Check https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands for nesting commands
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
		try:
			print("Starting EC2 instance " + str(i.instance_id))
			i.start()
		except botocore.exceptions.ClientError as e:
			print(" Could not start instance {0}. ".format(i.id) + str(e))


@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def stop_instances(project):
	"Stops EC2 instances"

	instances_list = filter_instances(project)
	for i in instances_list:
		try:
			print("Stopping EC2 instance " + str(i.instance_id))
			i.stop()
		except botocore.exceptions.ClientError as e:
			print(" Could not stop instance {0}. ".format(i.id) + str(e))

@instances.command('snapshot')
@click.option('--project', default=None, help='Only instances for project (tag Project:<name>)')
def create_snapshot(project):
	"Create snapshots of all volumes"

	instances_list = filter_instances(project)
	for i in instances_list:
		print("Stopping instance {0}".format(i.id))
		i.stop()
		i.wait_until_stopped()
		for v in i.volumes.all():
			if (has_pending_snapshot(v)):
				print(" Skipping {0}, snapshot already in progress".format(v.id))
			else:
				print(" Creating snapshot of {0}".format(v.id))
				v.create_snapshot(Description='Created by SnapshotAlyzer 40000')
		print("Starting instance {0}".format(i.id))
		i.start()
		i.wait_until_running()
	print("Job's done!")

####################################################################

@cli.group('volumes')
def volumes():
	"Commands for EC2 volumes"

@volumes.command('list')
@click.option('--project', default=None, help='Only volumes for project (tag Project:<name>)')
def list_volumes(project):
	"Lists EC2 volumes"

	instances_list = filter_instances(project)
	for i in instances_list:
		for v in i.volumes.all():
			print(', '.join([i.instance_id, v.volume_id, v.snapshot_id, v.availability_zone, str(v.tags)]))

####################################################################

@cli.group('snapshots')
def snapshots():
	"Commands for snapshots"

@snapshots.command('list')
@click.option('--project', default=None, help='Only snapshots for project (tag Project:<name>)')
@click.option('--all', default=False, is_flag=True, help="List all snapshots for each volume, not just the most recent")
def list_snapshots(project, all):
	"Lists snapshots"

	instances_list = filter_instances(project)
	for i in instances_list:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(', '.join((i.id, s.id, s.volume_id, s.start_time.strftime("%c"), s.state, s.progress)))
				if ((s.state == "completed") and (all==False)):		
					break	 

####################################################################

if __name__ == '__main__':
	cli() 