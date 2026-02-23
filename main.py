from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import akshare as ak
from datetime import datetime

app = FastAPI(title="個股股市資料API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Monica會呼叫
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_stock_history")
async def get_stock_history(
    symbol: str = Query(..., description="股票代碼，例如 600519 或 sh.000300"),
    start_date: str = Query("20100101", description="開始日期 YYYYMMDD"),
    end_date: str = Query(None, description="結束日期 YYYYMMDD，留空=今天"),
    adjust: str = Query("qfq", description="復權: qfq前復權 / hfq後復權 / none不復權")
):
    try:
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            start_date=start_date,
            end_date=end_date or datetime.now().strftime("%Y%m%d"),
            adjust=adjust
        )
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
