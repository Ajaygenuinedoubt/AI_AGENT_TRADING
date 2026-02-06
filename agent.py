from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os

# ==============================
# PROMPT TEMPLATE (UPDATED)
# ==============================

prompt = PromptTemplate(
    input_variables=["stock", "price", "rsi", "sma20", "sma50"],
    template="""
You are a professional stock trading assistant.

Analyze the stock using ONLY the metrics below and generate a clear trading signal.

-----------------------------------
📊 STOCK METRICS
-----------------------------------
Stock Name     : {stock}
Current Price : ₹{price}
RSI (14)      : {rsi}
20-Day SMA    : {sma20}
50-Day SMA    : {sma50}

-----------------------------------
📈 DECISION RULES
-----------------------------------
BUY when:
- RSI < 35
- Price > SMA20
- SMA20 > SMA50

SELL when:
- RSI > 65
- Price < SMA20
- SMA20 < SMA50

Otherwise → HOLD

-----------------------------------
📊 CONFIDENCE SCORING (MANDATORY)
-----------------------------------
Assign confidence based on rule alignment:

HIGH:
- At least 3 conditions strongly align with the signal

MEDIUM:
- Exactly 2 conditions align

LOW:
- Only 1 or conflicting conditions

-----------------------------------
📌 OUTPUT FORMAT (STRICT)
-----------------------------------
Signal     : BUY / SELL / HOLD
Confidence : High / Medium / Low
Reason     :
- Maximum 5 important bullet points
- Each point must reference RSI, SMA20, SMA50, or Price

-----------------------------------
⚠️ CONSTRAINTS
-----------------------------------
- No candle patterns
- No assumptions
- No external data
- No financial advice
- Keep response concise and email-friendly

-----------------------------------
✍️ SIGNATURE (MANDATORY)
-----------------------------------
End the message EXACTLY with:

Best Regards,
Ajay Kumar Jha
Stock Trading Assistant
"""
)

# ==============================
# LLM CONFIG
# ==============================

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b",
    temperature=0.2  # LOW temperature = consistent decisions
)

# ==============================
# AI DECISION FUNCTION
# ==============================

def ai_decision(data, stock):
    latest = data.iloc[-1]

    formatted_prompt = prompt.format(
        stock=stock,
        price=round(latest["Close"], 2),
        rsi=round(latest["RSI"], 2),
        sma20=round(latest["SMA20"], 2),
        sma50=round(latest["SMA50"], 2),
    )

    response = llm.invoke(formatted_prompt)

    return response.content.strip()
