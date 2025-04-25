import { Transfer as TransferEvent } from "../generated/BoredApeYachtClub/BoredApeYachtClub"
import { Transfer } from "../generated/schema"

export function handleTransfer(event: TransferEvent): void {
  let entity = new Transfer(event.transaction.hash)  // 👈 transaction hash is already Bytes!

  entity.from = event.params.from
  entity.to = event.params.to
  entity.tokenId = event.params.tokenId
  entity.blockNumber = event.block.number
  entity.blockTimestamp = event.block.timestamp
  entity.transactionHash = event.transaction.hash

  entity.save()
}


