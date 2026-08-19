import os
import json
from fastapi import FastAPI, Request, Response, Query
import httpx
from openai import AsyncOpenAI
import openai 
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo 
from apscheduler.schedulers.background import BackgroundScheduler
import asyncpg
from fastapi.responses import HTMLResponse

load_dotenv()

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dalynx Automations | Enterprise AI Infrastructure</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background-color: #040711; 
                color: #f7fafc; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 650px;
                width: 100%;
                background: linear-gradient(145deg, #090f20, #050914);
                border: 1px solid #1e293b;
                border-radius: 20px;
                padding: 50px 40px;
                text-align: center;
                box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
            }
            .logo-text {
                font-size: 32px;
                font-weight: 900;
                letter-spacing: 5px;
                background: linear-gradient(to right, #00ffcc, #00bcff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 12px;
            }
            .tagline {
                color: #64748b;
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 2px;
                margin-bottom: 35px;
                text-transform: uppercase;
            }
            .divider {
                height: 1px;
                background: linear-gradient(to right, transparent, #1e293b, transparent);
                margin: 25px 0;
            }
            .section {
                text-align: left;
                margin-bottom: 30px;
            }
            .section h3 {
                color: #00ffcc;
                font-size: 12px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                margin-bottom: 12px;
            }
            .section p {
                color: #94a3b8;
                font-size: 15px;
                line-height: 1.7;
            }
            .footer-info {
                margin-top: 40px;
                font-size: 13px;
                color: #475569;
                background: #060b18;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #111827;
                text-align: left;
            }
            .footer-info p { margin-bottom: 8px; }
            .footer-info p:last-child { margin-bottom: 0; }
            .footer-info a {
                color: #00bcff;
                text-decoration: none;
            }
            .privacy-link {
                display: inline-block;
                margin-top: 20px;
                font-size: 13px;
                color: #64748b;
                text-decoration: none;
                transition: color 0.2s;
            }
            .privacy-link:hover { color: #00ffcc; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-text">DALYNX AUTOMATIONS</div>
            <div class="tagline">Next-Gen AI & Workflow Infrastructure</div>
            
            <div class="divider"></div>
            
            <div class="section">
                <h3>Our Core Operations</h3>
                <p>We architect custom artificial intelligence pipelines, multi-tenant customer interaction systems, and automated operational infrastructure for healthcare providers, medical clinics, and enterprise clients globally.</p>
            </div>

            <div class="section">
                <h3>Corporate Statement</h3>
                <p>Dalynx Automations is dedicated to deploying seamless automated intelligence into high-touch market sectors, dramatically accelerating task efficiency and optimizing operational human lifecycles.</p>
            </div>

            <div class="divider"></div>

            <div class="footer-info">
                <p><strong>Legal Entity:</strong> Govt. of India MSME (Udyam) Registered</p>
                <p><strong>Corporate Correspondence:</strong> <a href="mailto:dsecure.ai@gmail.com">dsecure.ai@gmail.com</a></p>
            </div>

            <a href="/privacy" class="privacy-link">Privacy Policy & Data Protection</a>
        </div>
    </body>
    </html>
    """

@app.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Privacy Policy | Dalynx Automations</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                background-color: #040711; 
                color: #cbd5e1; 
                line-height: 1.7;
                padding: 40px 20px;
            }
            .privacy-container {
                max-width: 750px;
                margin: 0 auto;
                background: #090f20;
                border: 1px solid #1e293b;
                border-radius: 16px;
                padding: 40px;
            }
            h1 { color: #ffffff; font-size: 28px; margin-bottom: 10px; font-weight: 800; }
            h2 { color: #00ffcc; font-size: 18px; margin-top: 30px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }
            p, li { color: #94a3b8; font-size: 15px; margin-bottom: 15px; }
            ul { margin-left: 20px; margin-bottom: 20px; }
            .date { color: #64748b; font-size: 13px; margin-bottom: 30px; }
            a { color: #00bcff; text-decoration: none; }
            .back-btn { display: inline-block; margin-top: 30px; color: #64748b; text-decoration: none; font-size: 14px; }
            .back-btn:hover { color: #ffffff; }
        </style>
    </head>
    <body>
        <div class="privacy-container">
            <h1>Privacy Policy</h1>
            <div class="date">Last Updated: June 22, 2026</div>
            
            <p>Welcome to Dalynx Automations. We respect your privacy and are committed to protecting data processed through our custom AI architecture, webhook integrations, and client communications systems.</p>
            
            <h2>1. Information We Collect</h2>
            <p>In operating our automated enterprise services and custom communications tools (including our WhatsApp Business API integration setups), we temporarily ingest text-based interaction data strictly to facilitate intended workflows. This data is managed directly via encrypted databases and secure communication endpoints.</p>

            <h2>2. How We Use Data</h2>
            <p>Data handled by our systems is utilized exclusively to:</p>
            <ul>
                <li>Maintain multi-tenant operational memory during communication workflows.</li>
                <li>Process contextual information required to generate responsive AI output.</li>
                <li>Track basic performance matrix attributes as configured by our direct corporate clients.</li>
            </ul>

            <h2>3. Data Retentions and Security</h2>
            <p>We do not lease, trade, or distribute your information to unauthorized marketing aggregators. All communication history elements are secured within database structures with restricted accessibility profiles, matching our commitment to technical security and system architecture standards.</p>

            <h2>4. Third-Party Webhook Data Processing</h2>
            <p>Our automation engines hook safely into secure third-party communication layers (such as Meta API structures and cloud system instances). Any data handled over these channels is subject to the security guardrails outlined by their respective parent infrastructure organizations.</p>

            <h2>5. Contact Us</h2>
            <p>For official inquiries concerning individual system memory purges, data structural queries, or general security compliance, drop a message to our operations desk at: <a href="mailto:dsecure.ai@gmail.com">dsecure.ai@gmail.com</a></p>
            
            <a href="/" class="back-btn">&larr; Return to Home</a>
        </div>
    </body>
    </html>
    """

# --- CONFIGURATION ---
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "") 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
MAX_HISTORY = 10 

# --- DATABASE HELPER FUNCTIONS ---
async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

async def get_clinic_data(clinic_id: str):
    conn = await get_db_connection()
    row = await conn.fetchrow('SELECT owner_name, system_instruction FROM clinics WHERE clinic_id = $1', clinic_id)
    await conn.close()
    return dict(row) if row else None

async def get_user_session(phone: str):
    conn = await get_db_connection()
    row = await conn.fetchrow('SELECT clinic_id, history, patient_context FROM user_sessions WHERE phone = $1', phone)
    await conn.close()
    if row:
        return row['clinic_id'], json.loads(row['history']), row.get('patient_context', 'a general dental inquiry')
    return None, None, None

async def save_user_session(phone: str, clinic_id: str, history: list):
    conn = await get_db_connection()
    history_json = json.dumps(history)
    await conn.execute('''
        INSERT INTO user_sessions (phone, clinic_id, history, last_active)
        VALUES ($1, $2, $3, CURRENT_TIMESTAMP)
        ON CONFLICT (phone) DO UPDATE 
        SET clinic_id = EXCLUDED.clinic_id, history = EXCLUDED.history, last_active = CURRENT_TIMESTAMP
    ''', phone, clinic_id, history_json)
    await conn.close()

async def update_patient_context(phone: str, context: str):
    conn = await get_db_connection()
    await conn.execute('UPDATE user_sessions SET patient_context = $1 WHERE phone = $2', context, phone)
    await conn.close()

async def delete_user_session(phone: str):
    conn = await get_db_connection()
    await conn.execute('DELETE FROM user_sessions WHERE phone = $1', phone)
    await conn.close()

# --- BACKGROUND AI TASK: COMPLAINT EXTRACTION ---
async def extract_and_save_context(phone: str, history: list):
    try:
        extraction_prompt = [
            {"role": "system", "content": "Analyze this chat history. What is the patient's primary enquiry or complaint? Answer in 1 to 6 words only (e.g., 'botox', 'spa treatment', 'derma filler'). If unknown, reply 'General inquiry' .always attach the name of patient if mentioned in the chat history. If not, just give the issue."},
            {"role": "user", "content": str(history)}
        ]
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=extraction_prompt,
            temperature=0.0
        )
        context = response.choices[0].message.content.strip()
        print(f"[BACKGROUND EXTRACTION] Patient {phone} issue: {context}")
        await update_patient_context(phone, context)
    except Exception as e:
        print(f"Extraction Error: {e}")

# --- SALES TRACKING (GOOGLE SHEETS) ---
def update_sales_tracker(phone, clinic_id):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        sheet_client = gspread.authorize(creds)
        sheet = sheet_client.open("Sales_Tracker").sheet1
        
        records = sheet.get_all_records()
        today_str = datetime.now(ZoneInfo("Asia/Dubai")).strftime("%Y-%m-%d %H:%M:%S")
        clean_target_phone = str(phone).replace("+", "").replace(" ", "").strip()
        
        cell_found = False
        for i, row in enumerate(records):
            sheet_phone_raw = str(row.get('Phone', ''))
            clean_sheet_phone = sheet_phone_raw.split('.')[0].replace("+", "").replace(" ", "").strip()
            
            if clean_sheet_phone == clean_target_phone:
                cell_found = True
                row_num = i + 2  
                current_count_raw = row.get('Msg Count', 0)
                current_count = int(current_count_raw) if str(current_count_raw).isdigit() else 0
                
                sheet.update_cell(row_num, 3, current_count + 1)
                sheet.update_cell(row_num, 5, today_str)
                break
                
        if not cell_found:
            sheet.append_row([clean_target_phone, clinic_id, 1, today_str, today_str, "Started"])
            print(f"New prospect {clean_target_phone} added to Sales Tracker!")

    except Exception as e:
        print(f"Sales Tracker Logging Error: {e}")

# --- THE TIME-TRAVELER (AI SALES GENERATOR - FAST FORWARD EDITION) ---
def check_and_send_followups():
    print("\n--- SCHEDULER WOKE UP: Checking for 3-Hour and 5-Hour follow-ups ---")
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        sheet_client = gspread.authorize(creds)
        sheet = sheet_client.open("Sales_Tracker").sheet1
        records = sheet.get_all_records()
        
        now = datetime.now(ZoneInfo("Asia/Dubai"))
        
        for i, row in enumerate(records):
            phone = str(row.get('Phone', ''))
            start_date_str = str(row.get('Demo Start Date', '')).strip()
            status = str(row.get('Followup Status', '')).strip()
            clinic_id = row.get('Clinic Tested', '')
            
            if not start_date_str or status == "Completed":
                continue
                
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo("Asia/Dubai"))
            except ValueError:
                continue

            # NEW LOGIC: Calculate hours passed instead of days
            time_diff = now - start_date
            hours_passed = time_diff.total_seconds() / 3600
            row_num = i + 2
            
            # --- "DAY 3" FAST-FORWARD TRIGGER (Runs at 3 Hours) ---
            if hours_passed >= 1 and status == "Started":
                print(f"-> GENERATING CUSTOM 'DAY 3' FOLLOW-UP FOR: {phone}")
                
                import psycopg2
                from psycopg2.extras import RealDictCursor
                
                sync_client = openai.OpenAI(api_key=OPENAI_API_KEY)
                conn = psycopg2.connect(DATABASE_URL)
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                cursor.execute("SELECT owner_name FROM clinics WHERE clinic_id = %s", (clinic_id,))
                res_clinic = cursor.fetchone()
                owner_name = res_clinic['owner_name'] if res_clinic else "Doctor"
                
                # FIXED Key Error: Use variable directly
                clinic_name = clinic_id if clinic_id else "the clinic"
                
                cursor.execute("SELECT patient_context FROM user_sessions WHERE phone = %s", (phone,))
                res_session = cursor.fetchone()
                patient_context = res_session['patient_context'] if (res_session and res_session['patient_context']) else "a general inquiry"
                conn.close()

                # Adjust Prompt to fake the passage of time for the demo
                ai_prompt = f"You are the AI receptionist for {clinic_name}. Write a friendly, empathetic 2-sentence WhatsApp follow-up to a patient/client who inquired about '{patient_context}'. Pretend that 3 days have passed since they last messaged. Ask if they are still experiencing the issue and offer to get them slotted in today."
                
                res = sync_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": ai_prompt}],
                    temperature=0.3
                )
                generated_followup = res.choices[0].message.content.strip()

                # Sales Pitch Wrapper (Reminds them it's a fast-forwarded demo)
                sales_pitch = (
                    f"⏳ *Demo Fast-Forward: 'Day 3' Follow-Up*\n\n"
                    f"Hi {owner_name}! In a real deployment, your AI receptionist would send this exactly 3 days after a missed lead. "
                    f"To save you time today, we fast-forwarded the clock. Here is what the bot would automatically text the patient:\n\n"
                    f"💬 _\"{generated_followup}\"_\n\n"
                    f"Imagine this running perfectly in the background for every single missed lead."
                )
                
                send_whatsapp_message(phone, sales_pitch)
                sheet.update_cell(row_num, 6, "Day 3 Sent")
                
            # --- "DAY 5" FAST-FORWARD TRIGGER (Runs at 5 Hours) ---
            elif hours_passed >= 5 and status == "Day 3 Sent":
                import psycopg2
                conn = psycopg2.connect(DATABASE_URL)
                cursor = conn.cursor()
                cursor.execute("SELECT owner_name FROM clinics WHERE clinic_id = %s", (clinic_id,))
                res = cursor.fetchone()
                owner_name = res[0] if res else "Doctor"
                conn.close()

                msg = f"🚀 *Final Demo Check-In (Fast-Forwarded)*\n\nHi {owner_name}! Your test bot successfully nurtured this lead with multiple touchpoints without you lifting a finger. Let's get this connected to your clinic's actual WhatsApp and start saving you time."
                send_whatsapp_message(phone, msg)
                sheet.update_cell(row_num, 6, "Completed")

    except Exception as e:
        print(f"Follow-up Scheduler Error: {e}")

def send_whatsapp_message(to_phone, text_body):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {META_ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp", 
        "recipient_type": "individual", 
        "to": to_phone, 
        "type": "text", 
        "text": {"body": text_body}
    }
    import requests
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"[WHATSAPP API ERROR] Code: {response.status_code} | Details: {response.text}")

@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler(timezone=ZoneInfo("Asia/Dubai"))
    # NEW LOGIC: Runs every 15 minutes to constantly check for leads hitting the 3hr or 5hr mark
    scheduler.add_job(check_and_send_followups, 'interval', minutes=15) 
    scheduler.start()

# --- WEBHOOK ENDPOINTS ---
@app.get("/webhook")
async def verify_webhook(mode: str = Query(None, alias="hub.mode"), token: str = Query(None, alias="hub.verify_token"), challenge: str = Query(None, alias="hub.challenge")):
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    return Response(content="Verification failed", status_code=403)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": str(datetime.now())}

# --- THE BACKGROUND PROCESSOR ---
async def run_bot_flow(sender_phone, user_text, clean_text):
    try:
        # --- SECRET RESET COMMAND ---
        if clean_text == "RESET":
            delete_user_session(sender_phone)
            reset_reply = "System Memory Cleared from Database! Fresh test started. Scan a QR code or type a DEMO keyword to begin again."
            send_whatsapp_message(sender_phone, reset_reply)
            return 
        
        # --- SECRET GOD MODE TRIGGER ---
        if clean_text == "TEST":
            print("\n[GOD MODE] Forcing scheduler script to run RIGHT NOW...")
            try:
                check_and_send_followups() 
                send_whatsapp_message(sender_phone, "⚙️ Trigger fired! Check Render logs.")
            except Exception as e:
                send_whatsapp_message(sender_phone, f"Error: {e}")
            return 
        
        # --- PHASE 1: SEAMLESS QR CODE INITIATION ---
        detected_clinic = None
        if "DEMO_MATHURAJMER" in clean_text:
            detected_clinic = "MATHUR_AJMER"
        elif "DEMO_SHARMADELHI" in clean_text:
            detected_clinic = "SHARMA_DELHI"
        elif "BOOK A CONSULTATION AT SKIN111" in clean_text:
            detected_clinic = "skin111"
        
        if detected_clinic:
            clinic_data = get_clinic_data(detected_clinic)
            if not clinic_data:
                send_whatsapp_message(sender_phone, "Error: Clinic not found in database.")
                return 

            new_history = [
                {"role": "system", "content": clinic_data['system_instruction']},
                {"role": "user", "content": "Hi"}
            ]
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, update_sales_tracker, sender_phone, detected_clinic)
            
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=new_history,
                temperature=0.2 
            )
            ai_reply = response.choices[0].message.content
            
            new_history.append({"role": "assistant", "content": ai_reply})
            save_user_session(sender_phone, detected_clinic, new_history)
            send_whatsapp_message(sender_phone, ai_reply)
            return 
        
        # --- PHASE 2: MULTI-TENANT MEMORY ---
        active_clinic, current_history, _ = get_user_session(sender_phone)
        
        if not active_clinic or not current_history:
            send_whatsapp_message(sender_phone, "Welcome! Please scan your clinic's custom QR code to begin the AI demo.")
            return 
        
        current_history.append({"role": "user", "content": user_text})
        
        if len(current_history) > (MAX_HISTORY * 2 + 1):
            current_history = [current_history[0]] + current_history[-(MAX_HISTORY * 2):]
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, update_sales_tracker, sender_phone, active_clinic)
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=current_history,
            temperature=0.2 
        )
        ai_reply = response.choices[0].message.content
        
        current_history.append({"role": "assistant", "content": ai_reply})
        save_user_session(sender_phone, active_clinic, current_history)
        send_whatsapp_message(sender_phone, ai_reply)
        
        asyncio.create_task(extract_and_save_context(sender_phone, current_history))
            
    except Exception as e:
        print(f"Flow Error: {e}")

# --- THE WEBHOOK RECEPTION DESK ---
@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        
        if "messages" in value:
            message = value["messages"][0]
            sender_phone = message["from"]
            
            if message["type"] == "text":
                user_text = message["text"]["body"]
                clean_text = user_text.strip().upper()
                print(f"\n[OWNER TESTING] {sender_phone}: {user_text}")

                # Pass the heavy lifting to the background so Meta doesn't timeout
                asyncio.create_task(run_bot_flow(sender_phone, user_text, clean_text))
                
    except KeyError:
        pass
        
    # Meta instantly receives its 200 OK, preventing all spam loops
    return {"status": "success"}
