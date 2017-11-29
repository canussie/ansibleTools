# ansibleTools

Tools to use with ansible


hosts.py

Pull hostgroups and hosts from satellite 6, use as ansible dynamic inventory utility.

Configure satellite server and credentials. Run the python script and a json dump containing all host groups and hosts within each group will be returned.

Run with ansible like so:

$ ansible <HOSTGROUP or HOSTNAME> -i hosts.py <ARG>
