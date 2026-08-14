import requests
import synapseutils
import synapseclient


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
    email = "geetikasahasra@gmail.com"
    authToken = "eyJ0eXAiOiJKV1QiLCJraWQiOiJXN05OOldMSlQ6SjVSSzpMN1RMOlQ3TDc6M1ZYNjpKRU9VOjY0NFI6VTNJWDo1S1oyOjdaQ0s6RlBUSCIsImFsZyI6IlJTMjU2In0.eyJhY2Nlc3MiOnsic2NvcGUiOlsidmlldyIsImRvd25sb2FkIl0sIm9pZGNfY2xhaW1zIjp7fX0sInRva2VuX3R5cGUiOiJQRVJTT05BTF9BQ0NFU1NfVE9LRU4iLCJpc3MiOiJodHRwczovL3JlcG8tcHJvZC5wcm9kLnNhZ2ViYXNlLm9yZy9hdXRoL3YxIiwiYXVkIjoiMCIsIm5iZiI6MTc4NDE0MzUxOSwiaWF0IjoxNzg0MTQzNTE5LCJqdGkiOiI0MjI2NCIsInN1YiI6IjM2MDMwODQifQ.IRN4XLFfjZc4s4DgcEKLeMGa5sdSzFRxi-6nEBPArKHtol4_LLzCGBK4B_eriVWKE40-zino4ZZ5FRDT2v_bTWrrclHfgATocjf1i4qWgCXzBDaBNVjoR6VkSK6mGeeLD_dEUtOEeggM10HVXeCnTI4kQotitLJ3uejbluvyLui6odq04MgbJryraDfmdsXYZ3krt4fM6PMi-PNJlm9U6YngEWUj-kgAcobS6n9uJUjNZ_iPbuX9dAnej3LzSBiUcndcfVekm-dxpM00Stwg-hHTgSw22xLGD4st1NVdK0IlQncNNb_-gjwKR6FAkippKH3in1uyPeLfRgFefhQ_Ew"
    accesskey = "NTIJTFK.4194711"
    local_folder = r"data\CholecTrack20"

    main()