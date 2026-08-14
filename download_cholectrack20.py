import requests
import synapseutils
import synapseclient
from synapse_config import email, authToken, accesskey


def main():
    print("Authenticating user ...")
    syn = synapseclient.login(email=email, authToken=authToken)

    print("Authenticating access key permission to download dataset ...")
    API_URL = "https://synapse-response.onrender.com/validate_access"
    USER_ID = syn.getUserProfile()['ownerId']
    response = requests.post(API_URL, json={"access_key": accesskey, "synapse_id": USER_ID})
    if response.status_code == 200:
        entity_id = response.json()['entity_id']
    else:
        print("Failed to request access:", response.text)
        exit(1)

    print("Downloading dataset...")
    _ = synapseutils.syncFromSynapse(syn, entity=entity_id, path=local_folder)
    print("success!")


if __name__ == "__main__":
    local_folder = r"data\CholecTrack20"
    main()