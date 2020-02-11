import os
import random
import string
import argparse
from pathlib import Path
from passlib.hash import sha512_crypt



passwd_folder = Path("jupyterhub/passwords")


def get_users(file):
	user_file: str = file
	user_list = []
	with open(user_file, 'r') as f:
		for line in f:
			user = line.strip('\n')
			user_list.append(user)
	return user_list

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def generate_list(user_list):
	wrapped_user_list = []
	for user in user_list:
		wrapped_user_list.append(f"\"{user}\"")
	user_str = ", ".join(wrapped_user_list)
	print(user_str)

def generate_passwd(user_list, force=False):
	passwd_dict = {}
	for user in user_list:
		passwd_dict[user] = randomString(20)
		pass_file = f"{user}.password"
		if force or (not os.path.isfile(passwd_folder / pass_file)) :
			with open(passwd_folder / pass_file, 'w') as f:
				f.write(passwd_dict[user])
				print(f"password for {user} was created in the {passwd_folder/pass_file}")
			with open(passwd_folder / f"{pass_file}_hashed", 'w') as f:
				f.write(sha512_crypt.using(rounds=5000).hash(passwd_dict[user]))
		else:
			print(f"Pass for {user} exists in the {passwd_folder / pass_file}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Give me files with users")
	parser.add_argument('--file', help='Specify file with users')
	parser.add_argument('--passwd', help='generate pass', action="store_true")
	parser.add_argument('--force', help='Force generate pass', action="store_true")
	args = parser.parse_args()

	user_list = get_users(args.file)
	if args.file:
		generate_list(user_list)
	if args.passwd:
		generate_passwd(user_list, args.force)
