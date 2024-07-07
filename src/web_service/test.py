from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
)

@app.get('/oauth')
async def oauth_resolve(code: str):
    print(code)
    return RedirectResponse('https://t.me/test_work_upco_bot')

