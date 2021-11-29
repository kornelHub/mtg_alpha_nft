from brownie import network
import requests
import json
import os



def upload_to_local_ipfs(card_name):
    ipfs_url = 'http://127.0.0.1:5001'
    endpoint = '/api/v0/add'
    card_img_path = f"{os.getcwd()}\metadata\img\\{card_name}.png"
    img_binary = open(card_img_path, 'rb')
    response = requests.post(ipfs_url + endpoint, files={"file": img_binary})
    ipfs_hash = response.json()['Hash']
    # compatible_card_name = card_name.replace(' ', '-').lower()
    image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={card_name}.png"
    return image_uri


def upload_to_piniata(card_name):
    pinata_img_path = 'https://gateway.pinata.cloud/ipfs/{}'
    pinata_base_url = 'https://api.pinata.cloud'
    endpoint = '/pinning/pinFileToIPFS'
    filepath = f"{os.getcwd()}\metadata\img\\{card_name}.png"
    file_name = str(card_name)+ '.jpg'
    print(file_name)
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


def main():
    generate_uri()