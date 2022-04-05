import base64
from typing import List, Tuple

from algosdk import account
from algosdk.future import transaction
from algosdk.kmd import KMDClient
from algosdk.v2client import algod, indexer


class SandboxAccount:
    def __init__(self) -> None:
        self.kmd_client = self.get_kmd_client()
        self.priv_keys = self.get_keys_from_wallet(self.kmd_client)

    def get_kmd_client(
        self, address="http://localhost:4002", token="a" * 64
    ) -> KMDClient:
        return KMDClient(token, address)

    def get_keys_from_wallet(
        self,
        kmd_client: KMDClient,
        wallet_name="unencrypted-default-wallet",
        wallet_password="",
    ):
        wallets = kmd_client.list_wallets()

        handle = None
        for wallet in wallets:
            if wallet["name"] == wallet_name:
                handle = kmd_client.init_wallet_handle(wallet["id"], wallet_password)
                break

        if handle is None:
            raise Exception("Could not find wallet")

        private_keys = None
        try:
            addresses = kmd_client.list_keys(handle)
            private_keys = [
                kmd_client.export_key(handle, wallet_password, address)
                for address in addresses
            ]
        finally:
            kmd_client.release_wallet_handle(handle)

        return private_keys

    def get_funded_account(self) -> Tuple[str, str]:
        priv_key = self.priv_keys[0]
        addr = account.address_from_private_key(priv_key)
        return (priv_key, addr)

    def get_funded_transient(self, client: algod.AlgodClient) -> Tuple[str, str]:
        funded_sk, funded_pk = self.get_funded_account()
        sk, pk = account.generate_account()

        txn = transaction.PaymentTxn(
            funded_pk,
            client.suggested_params(),
            pk,
            5 * (10**6),  # Fund with 5 Algos
        )
        stxn = txn.sign(funded_sk)
        tx_id = client.send_transaction((stxn))
        transaction.wait_for_confirmation(client, tx_id, 5)
        return (sk, pk)


def create_algod_client():
    return algod.AlgodClient(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "http://localhost:4001",
    )


def compile_program(client: algod.AlgodClient, source_code: str):
    try:
        # source_code = source_code.decode("utf-8")
        compile_response = client.compile(source_code)
        return base64.b64decode(compile_response["result"])
    except Exception as e:
        return str(e)


# Compile the program with algod
# source_code = ""
# with open("simple.teal", mode="rb") as file:
#     source_code = file.read()

# client = create_algod_client()
# source_program = compile_program(client, source_code.decode("utf-8"))
# print(source_program)

# acc = SandboxAccount()
# print(acc.get_funded_account())
# print(acc.get_funded_transient(client))
