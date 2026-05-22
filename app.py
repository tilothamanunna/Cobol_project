from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.account_service import AccountService

app = FastAPI()
service = AccountService()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    accounts = service.get_all_accounts()
    history = service.get_transaction_history()
    total_balance = sum(acc['balance'] for acc in accounts)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_balance": f"{total_balance:,.2f}",
        "history": history[:5],
        "username": "tnunna"
    })

@app.get("/history", response_class=HTMLResponse)
async def view_history(request: Request):
    history = service.get_transaction_history()
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history,
        "user_account": "ACC-TNU-01"
    })

@app.get("/transfer", response_class=HTMLResponse)
async def view_transfer(request: Request):
    accounts = service.get_all_accounts()
    return templates.TemplateResponse("transfer.html", {"request": request, "accounts": accounts})

@app.get("/open-account", response_class=HTMLResponse)
async def view_open_account(request: Request):
    return templates.TemplateResponse("open_account.html", {"request": request})

@app.post("/accounts/create-form")
async def handle_create_account(name: str = Form(...), balance: float = Form(...), system: str = Form(...)):
    new_id = f"ACC-{name[:3].upper()}-01"
    service.create_new_account(new_id, name, balance, system)
    return RedirectResponse(url="/", status_code=303)

@app.post("/accounts/transfer-form")
async def handle_transfer_form(from_account: str = Form(...), to_account: str = Form(...), amount: float = Form(...)):
    service.transfer_funds(from_account, to_account, amount)
    return RedirectResponse(url="/history", status_code=303)