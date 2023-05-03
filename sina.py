import re

from telethon import TelegramClient, events

import asyncio



api_id = '28320740'

api_hash = 'f5cedb36cb21c6dd390596075f1673fa'



source_channel_id = -1001945870907

destination_channel_id = -1001942970623



client = TelegramClient('anon1', api_id, api_hash)



@client.on(events.NewMessage(chats=source_channel_id))

async def forward_handler(event):

    original_text = event.message.text



    # Find the entry target and stop percentage

    entry_target_match = re.search(r"Entry Targets:\s*(\d+\.\d+)\s*", original_text)

    stop_percentage_match = re.search(r"❌STOP\s*\n*-(\d+)%", original_text, re.IGNORECASE)



    if entry_target_match and stop_percentage_match:

        entry_target = float(entry_target_match.group(1))

        stop_percentage = float(stop_percentage_match.group(1)) / 100



        # Calculate the new stop value

        stop_value = entry_target * (1 - stop_percentage)



        # Replace the stop value in the original text

        modified_text = re.sub(r"❌STOP\s*\n*-(\d+)%", f"❌STOP\n{stop_value:.5f}", original_text, flags=re.IGNORECASE)



        # Forward the modified message

        await client.send_message(destination_channel_id, modified_text)

    else:

        print(f"Entry target match: {entry_target_match}")

        print(f"Stop percentage match: {stop_percentage_match}")

        # If the regular expressions didn't match, forward the original message

        await client.forward_messages(destination_channel_id, event.message)



async def main():

    await client.start()

    await client.run_until_disconnected()



if __name__ == '__main__':

    asyncio.run(main())

