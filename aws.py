# coding=utf8
import csv
import random
import string

import boto3


def get_token():
    n = 16
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])


def list_emails():
    with open('foo.md', 'r') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]


def get_user_name(email):
    return email[: email.find('@aktsk.jp')]


def register(client, email):
    user_name = get_user_name(email)
    client.create_user(UserName=user_name)
    password = get_token()
    client.create_login_profile(UserName=user_name, Password=password, PasswordResetRequired=True)
    client.add_user_to_group(GroupName='aktsk-member', UserName=user_name)
    with open('out', 'a') as f:
        f.write('{},{}\n'.format(user_name, password))
        print('{}'.format(user_name))


def main():
    client = boto3.client('iam')
    emails = list_emails()
    for email in emails:
        register(client, email)


if __name__ == '__main__':
    main()
