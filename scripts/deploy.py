from brownie import LimitedEditionAlpha
from scripts.helpers import get_account
from scripts.create_uri import upload_to_local_ipfs, upload_to_piniata
from metadata.card_metadata import creature_template, nocreature_template, land_template
import pandas as pd
from brownie import network
from metadata.alpha_desc import description

def deploy_limited_edition_alpha():
    owner_acc = get_account()
    alpha_contract = LimitedEditionAlpha.deploy({'from': owner_acc})
    return alpha_contract

def mint_alpha_set(alpha_contract):
    owner_acc = get_account()
    cards_details_df = pd.read_csv(
        'D:/python_projects/mtg_nft/metadata/alpha_card_desc.csv',
        sep=';',
        header=None,
        index_col=0,
    )
    cards_details_df.sort_index(inplace=True)
    for index, row in cards_details_df.iterrows():
        if 'Summon' in row[2] or 'Artifact Creature' == row[2]:
            creature_template_temp = creature_template
            creature_template_temp['name'] = row[1]
            creature_template_temp['description'] = description
            creature_template_temp['attributes'][1]['value'] = row[3] # mana cost
            creature_template_temp['attributes'][2]['value'] = row[4] # card text
            creature_template_temp['attributes'][3]['value'] = row[5] # p/t
            creature_template_temp['attributes'][4]['value'] = row[6] # flavor text
            creature_template_temp['attributes'][5]['value'] = row[8] # expansion
            creature_template_temp['attributes'][6]['value'] = row[7] # rarity
            creature_template_temp['attributes'][7]['value'] = row[9] # artist
            creature_template_temp['attributes'][0]['value'] = row[2]  # types
            if network.show_active() == 'development':
                creature_template_temp['image'] = upload_to_local_ipfs(index)
            else:
                creature_template_temp['image'] = upload_to_piniata(index)
            alpha_contract.createCollectibleCard(creature_template_temp, {'from': owner_acc}).wait(1)
        elif 'Land' == row[2]:
            land_template_temp = land_template
            land_template_temp['name'] = row[1]
            land_template_temp['description'] = description
            land_template_temp['attributes'][1]['value'] = row[3]  # card text
            land_template_temp['attributes'][2]['value'] = row[4]  # flavor text
            land_template_temp['attributes'][3]['value'] = row[6]  # expansion
            land_template_temp['attributes'][4]['value'] = row[5]  # rarity
            land_template_temp['attributes'][5]['value'] = row[7]  # artist
            land_template_temp['attributes'][0]['value'] = row[2]  # types
            if network.show_active() == 'development':
                land_template_temp['image'] = upload_to_local_ipfs(index)
            else:
                land_template_temp['image'] = upload_to_piniata(index)
            alpha_contract.createCollectibleCard(land_template_temp, {'from': owner_acc}).wait(1)
        else:
            nocreature_template_temp = nocreature_template
            nocreature_template_temp['name'] = row[1]
            nocreature_template_temp['description'] = description
            nocreature_template_temp['attributes'][1]['value'] = row[3] # mana cost
            nocreature_template_temp['attributes'][2]['value'] = row[4] # card text
            nocreature_template_temp['attributes'][3]['value'] = row[5] # flavor text
            nocreature_template_temp['attributes'][4]['value'] = row[7] # expansion
            nocreature_template_temp['attributes'][5]['value'] = row[6] # rarity
            nocreature_template_temp['attributes'][6]['value'] = row[8] # artist
            nocreature_template_temp['attributes'][0]['value'] = row[2]  # types
            if network.show_active() == 'development':
                nocreature_template_temp['image'] = upload_to_local_ipfs(index)
            else:
                nocreature_template_temp['image'] = upload_to_piniata(index)
            alpha_contract.createCollectibleCard(nocreature_template_temp, {'from': owner_acc}).wait(1)


def get_uri():
    alpha_contract = LimitedEditionAlpha[-1]
    print(alpha_contract.tokenURI(293))


def verify_contract():
    LimitedEditionAlpha.publish_source(LimitedEditionAlpha[-1])


def main():
    alpha_contract = deploy_limited_edition_alpha()
    mint_alpha_set(alpha_contract)