from brownie import network
import requests
import json
import os


def convert_card_name(card_name):
    return card_name.lower().replace(' ', '-')


def upload_img_to_local_ipfs(card_name, index):
    ipfs_url = 'http://127.0.0.1:5001'
    endpoint = '/api/v0/add'
    card_img_path = f"{os.getcwd()}\metadata\img\\{index}.png"
    img_binary = open(card_img_path, 'rb')
    response = requests.post(ipfs_url + endpoint, files={"file": (convert_card_name(card_name), img_binary)})
    ipfs_hash = response.json()['Hash']
    image_uri = f"ipfs://{ipfs_hash}"
    return image_uri


def upload_img_to_pinata(card_name, index):
    pinata_img_path = 'ipfs://{}'
    pinata_base_url = 'https://api.pinata.cloud'
    endpoint = '/pinning/pinFileToIPFS'
    filepath = f"{os.getcwd()}\metadata\img\\{index}.png"
    file_name = convert_card_name(card_name)+ '.jpg'
    headers = {
        "pinata_api_key": os.getenv('PINIATA_PUBLIC_KEY'),
        "pinata_secret_api_key": os.getenv('PINIATA_PRIVATE_KEY')
    }
    img_binary = open(filepath, 'rb').read()
    response = requests.post(
        pinata_base_url + endpoint,
        files={'file': (file_name, img_binary)},
        headers=headers
    )
    return pinata_img_path.format(response.json()['IpfsHash'])


def upload_json_to_pinata(token_uri):
    pinata_deployed_url = 'ipfs://{}'
    pinata_base_url = 'https://api.pinata.cloud'
    pinata_endpoint = '/pinning/pinFileToIPFS'
    headers = {
        "pinata_api_key": os.getenv('PINIATA_PUBLIC_KEY'),
        "pinata_secret_api_key": os.getenv('PINIATA_PRIVATE_KEY')
    }
    response = requests.post(
        pinata_base_url + pinata_endpoint,
        headers=headers,
        files={'file': (convert_card_name(token_uri['name'])+'.json', json.dumps(token_uri, indent=2).encode('utf-8'))}
    )
    print(pinata_deployed_url.format(response.json()['IpfsHash']))
    return pinata_deployed_url.format(response.json()['IpfsHash'])