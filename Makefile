add_user:
	ansible-playbook add_user.yaml --extra-vars '{"user":["user1","user2"], docker: "yes"}' --limit lambdagpu2
# 	ansible-playbook add_user.yaml --extra-vars '{"user":["user1","user2"], docker: "yes"}' --limit aciworker --list-hosts

packagesinstall:
	ansible-playbook packagesinstall.yaml --limit lambdagpu2

set_files:
	ansible-playbook set_files.yaml --limit lambdagpu2

mount:
	ansible-playbook mount.yaml --tags "packages,configuration,mount"

#==================HACKS==================#


# make_history:
# 	ansible-playbook all add_user.yaml --extra-vars '{"user":["user1","user2"]}'

accept_keys:
	ANSIBLE_HOST_KEY_CHECKING=false ansible-playbook keys_accept.yaml 

image_docker:
	ansible -m shell -a "docker pull mrphys/mfsimage:coMagnetAzure" 

list:
	ansible-playbook joinkube.yaml --limit cern-mc39h.ydf.yandex.net -f 25 --list-hosts

limit:
	ansible-playbook -l victim  iptables.yaml --tags "docker" --list-hosts

disable-aa:
	ansible victim -i hosts.yaml -m shell -a "/etc/init.d/apparmor stop" --become
	ansible victim -i hosts.yaml -m shell -a "/etc/init.d/apparmor teardown" --become

ad_hoc:
	ansible -m ping 
	ansible -m shell -a "echo ok, boomer"