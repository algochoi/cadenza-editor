from algosdk.future import transaction
from algosdk.v2client import algod


def deploy_app(
    client: algod.AlgodClient,
    source_program: bytes,
    clear_program: bytes,
    sk: str,
    pk: str,
):
    params = client.suggested_params()
    global_schema = transaction.StateSchema(5, 5)
    local_schema = transaction.StateSchema(5, 5)
    on_complete = transaction.OnComplete.NoOpOC

    # Note: Currently accounts have a 10 app limit, so create a transient
    # account if you wish to run this script many times.
    private_key, sender = sk, pk

    # clear_program = b"\x06\x81\x01C"

    # Create an unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        on_complete,
        source_program,
        clear_program,
        global_schema,
        local_schema,
    )

    # Sign transaction with funded private key
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    transaction_response = transaction.wait_for_confirmation(client, tx_id, 5)
    return transaction_response
    # print(transaction_response)
    # app_id = transaction_response["application-index"]
    # algod_response = client.application_info(app_id)
    # print(algod_response)
