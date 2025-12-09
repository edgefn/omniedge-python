<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from omniedge.omniedge_core import OmniEdge


with OmniEdge(
    api_key="<YOUR_BEARER_TOKEN_HERE>",
) as omni_edge:

    res = omni_edge.chat.create(model="openai/gpt-4o", messages=[], route="fallback", temperature=1, top_p=1, n=1, presence_penalty=0, frequency_penalty=0, repetition_penalty=1, stream=False)

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from omniedge.omniedge_core import OmniEdge

async def main():

    async with OmniEdge(
        api_key="<YOUR_BEARER_TOKEN_HERE>",
    ) as omni_edge:

        res = await omni_edge.chat.create_async(model="openai/gpt-4o", messages=[], route="fallback", temperature=1, top_p=1, n=1, presence_penalty=0, frequency_penalty=0, repetition_penalty=1, stream=False)

        async with res as event_stream:
            async for event in event_stream:
                # handle event
                print(event, flush=True)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->