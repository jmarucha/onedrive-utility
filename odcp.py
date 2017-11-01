#!/usr/bin/python3

import onedrivesdk
from onedrivesdk.version_bridge.fragment_upload import ItemUploadFragmentBuilder
import os
import argparse

client = None;

def add_slash(path):
    return path if path[0] == '/' else '/' + path

def parse_args():
    parser = argparse.ArgumentParser(description="Copy files to remote server.")
    parser.add_argument('source', type=str, help="Begin with od: to copy from one-drive")
    parser.add_argument('destination', type=str, help="Begin with  od: to copy to one-drive")
    return parser.parse_args()

def auth_client():
    redirect_uri = 'http://localhost:8080/'
    client_secret = r'yjdWQS35{&({ofdcZWMM742'
    client_id='576bca9f-5e74-440e-85fb-9025c984b5f6'
    api_base_url='https://api.onedrive.com/v1.0/'
    scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(
        http_provider=http_provider,
        client_id=client_id,
        scopes=scopes)
    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
    try: 
        auth_provider.load_session()
        auth_provider.refresh_token()

    except:
        auth_url = client.auth_provider.get_auth_url(redirect_uri)
        # Ask for the code
        print('Paste this URL into your browser, approve the app\'s access.')
        print('Copy everything in the address bar after "code=", and paste it below.')
        print(auth_url)
        code = input('Paste code here: ')
        auth_provider.authenticate(code, redirect_uri, client_secret)
        auth_provider.save_session()
    return client


def pull(client, src, dest):
    src = add_slash(src)
    if os.path.isdir(dest):
        dest = dest + '/' + src.split('/')[-1]
    client.item(path = src).download(dest)

def push(client, src, dest):
    dest, filename = dest.rsplit('/', 1)
    if filename == "":
        filename = src.split('/')[-1]
    c = client.item(path = dest).children[filename]
    c.upload_async(src)

def main():
    args = parse_args();
    client = auth_client();

    if args.source.startswith('od:') and args.destination.startswith('od:'): 
        drive_to_drive(args.source[3:], args.destination[3:])
    elif args.source.startswith('od:'):
        pull(client, args.source[3:], args.destination)
    elif args.destination.startswith('od:'):
        push(client,args.source, args.destination[3:])
    else:
        print("LOL, use 'cp' instead")

if __name__ == "__main__":
    main()
