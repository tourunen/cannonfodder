#!/usr/bin/env python

import os
import random
import string
import time
import argparse

import jinja2

import yaml
import htpasswd
import names

USER_DB_FILE = 'users.yaml'

NAME_ADJECTIVES = (
    'happy',
    'sad',
    'bright',
    'dark',
    'blue',
    'yellow',
    'red',
    'green',
    'white',
    'black',
    'clever',
    'witty',
    'smiley',
)


class UserDatabase:
    def __init__(self):
        self.users = {}

    def add(self, username, password, **kwargs):
        self.users[username] = dict(username=username, password=password, **kwargs)

    def load(self):
        if os.path.isfile(USER_DB_FILE):
            self.users = yaml.load(open(USER_DB_FILE))
        if not self.users:
            self.users = {}

    def save(self):
        yaml.dump(self.users, open(USER_DB_FILE, 'w'))


def create_username(user_database):
    username = None
    while not username:
        username = '{name}-the-{adjective}'.format(
            name=names.get_first_name().lower(),
            adjective=random.choice(NAME_ADJECTIVES),
        )
        if username in user_database.users.keys():
            username = None

    return username


def create_password(length=8):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    password = ''
    for i in range(length):
        password += chars[ord(os.urandom(1)) % len(chars)]
    return password


def update_htpasswd(filename, username, password):
    with htpasswd.Basic(filename, mode='md5') as ht:
        if username not in ht.users:
            ht.add(username, password)
        else:
            ht.change_password(username, password)


def create_user(user_database):
    username = create_username(user_database)
    password = create_password()

    user_database.add(username, password)

    print(username, password)


def sync_htpasswd(user_database, filename):
    with open(filename, 'a'):
        os.utime(filename, None)

    users = user_database.users
    for username in users:
        update_htpasswd(filename, username, users[username]['password'])


def process_template(user_data, template_file, output_file=None):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
    template = env.get_template(template_file)
    return template.render(**user_data)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    sp = subparsers.add_parser('add')
    sp.add_argument(
        '-n', '--num_users', type=int, required=True, help='number of users'
    )

    sp = subparsers.add_parser('update')
    sp.add_argument(
        '-f', '--filename', type=str, required=True, help='htpasswd file to update'
    )

    sp = subparsers.add_parser('yaml')
    sp.add_argument(
        '-f', '--filename', type=str, required=True, help='htpasswd file to update'
    )

    sp = subparsers.add_parser('process')
    sp.add_argument(
        '-t', '--template', type=str, required=True, help='jinja2 template to process'
    )
    sp.add_argument(
        '-u', '--user', type=str, help='only process given user'
    )
    sp.add_argument(
        '-s', '--suffix', type=str, help='suffix for output files'
    )

    user_database = UserDatabase()
    user_database.load()

    args = parser.parse_args()
    command = args.command

    if command == 'add':
        print('Adding {num_users} users'.format(num_users=args.num_users))
        num_generated = 0
        while num_generated < args.num_users:
            try:
                create_user(user_database)
                num_generated += 1
            except RuntimeWarning:
                pass

        user_database.save()
        print('User database now has {} users'.format(len(user_database.users)))

    elif command == 'update':
        print('Updating htpasswd file {}'.format(args.filename))
        sync_htpasswd(user_database, args.filename)

    elif command == 'yaml':
        print('htpasswd:')
        users = user_database.users
        with htpasswd.Basic(args.filename, mode='md5') as ht:
            for username in users:
                print('  {}: "{}"'.format(username, ht._encrypt_password(users[username]['password'])))

    elif command == 'process':
        print('Processing template {}'.format(args.template))

        if args.user:
            # filter only given user
            users = dict()
            users[args.user]=user_database.users[args.user]
        else:
            # process all users
            users = user_database.users

        for username in users:
            user_data=users[username]
            process_template(user_database.users[username], args.template)
            rendered_data = process_template(user_data, args.template)
            if args.suffix:
                print('processing user {}'.format(username))
                with open('{}-{}'.format(user_data['username'], args.suffix), 'w') as outfile:
                    outfile.write(rendered_data)
            else:
                print('=' * 4, 'BEGIN ', user_data['username'])
                print(rendered_data)
                print('=' * 4, 'END ', user_data['username'])


if __name__ == '__main__':
    start_ts = time.time()

    try:
        main()
    finally:
        end_ts = time.time()
        print("Run took %d seconds" % int(end_ts - start_ts))
