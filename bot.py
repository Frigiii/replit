import time
from webbrowser import get
from apikey import frigi_channel_id
import random
import asyncio
from typing import NoReturn
import messagehandler
import telegram


async def main() -> NoReturn:
    """Run the bot."""
    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    #async with request() as r:
    try:
        response = await telegram.request('getUpdates', {})
        if(response):
    #        print('Received {} new Updates'.format(len(response)))
            update_id = (await telegram.request('getUpdates', {}))[0]['update_id']
    #        print('Current update-id: {}'.format(update_id))
        else:
    #        print('Got no new Updates')
            update_id = None
    except BaseException as error:
        print('Error occured: {}'.format(error))
        update_id = None
        

    await telegram.request('sendMessage', {'chat_id' : frigi_channel_id, 'text' : 'I\'m alive!'})

    while True:
        try:
            update_id = await echo(update_id)
        except BaseException as error:
            # skips the current message
            text = "Oops! In Main Function \"" + format(error) + "\" occurred."
            print(text)
            await telegram.request('sendMessage', {'chat_id' : frigi_channel_id, 'text' : text})
            update_id += 1
            

async def echo(update_id: int) -> int:
    # Request updates after the last update_id
    #updates = await bot.get_updates(offset=update_id, timeout=10)
    updates = await telegram.request('getUpdates', {'offset' : update_id, 'timeout' : 10})
    if(updates):
        update_id = updates[0]['update_id']        
        for update in updates:
            next_update_id = update['update_id'] + 1
            # your bot can receive updates without messages
            # and not all messages contain text
    #        print('Next update-id: {}'.format(next_update_id))
            if update[list(update)[1]]['text']:
                # Reply to the message
                try:
                    await messagehandler.handler(update)
                except BaseException as error:
                    text = "Oops! In Echo-Function \"{}\" occurred.".format(error)
                    print(text)
                    await telegram.request('sendMessage', {'chat_id' : frigi_channel_id, 'text' : text})
            return next_update_id
    return update_id

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass