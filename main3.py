import os
import json
from fastapi import FastAPI, Request, Response, Query
import httpx
from openai import AsyncOpenAI
import openai # For the synchronous background scheduler
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import asyncpg

load_dotenv()

app = FastAPI()
from fastapi.responses import HTMLResponse

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
                background-color: #060913; 
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
                background: linear-gradient(145deg, #0b1120, #070c17);
                border: 1px solid #1e293b;
                border-radius: 16px;
                padding: 40px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            }
            .logo-text {
                font-size: 28px;
                font-weight: 800;
                letter-spacing: 4px;
                background: linear-gradient(to right, #00ffcc, #00bcff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 8px;
            }
            .tagline {
                color: #94a3b8;
                font-size: 16px;
                letter-spacing: 1px;
                margin-bottom: 30px;
                text-transform: uppercase;
            }
            .divider {
                height: 1px;
                background: linear-gradient(to right, transparent, #1e293b, transparent);
                margin: 20px 0;
            }
            .section {
                text-align: left;
                margin-bottom: 25px;
            }
            .section h3 {
                color: #00ffcc;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 10px;
            }
            .section p {
                color: #cbd5e1;
                font-size: 15px;
                line-height: 1.6;
            }
            .footer-info {
                margin-top: 35px;
                font-size: 13px;
                color: #64748b;
                background: #090f1d;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #111827;
            }
            .footer-info a {
                color: #00bcff;
                text-decoration: none;
            }
            .policy-link {
                margin-top: 15px;
                font-size: 12px;
                display: block;
            }
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
                <p style="margin-bottom: 6px;"><strong>Legal Entity:</strong> Govt. of India MSME (Udyam) Registered</p>
                <p style="margin-bottom: 6px;"><strong>Corporate Correspondence:</strong> <a href="mailto:dsecure.ai@gmail.com">dsecure.ai@gmail.com</a></p>
                <a href="/privacy" class="policy-link">Privacy Policy & Data Security Compliance</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/privacy", response_class=HTMLResponse)
async def privacy_policy():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Privacy Policy | Dalynx Automations</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #060913; color: #cbd5e1; line-height: 1.7; padding: 40px 20px;
            }
            .wrapper { max-width: 750px; margin: 0 auto; background: #0b1120; padding: 40px; border-radius: 12px; border: 1px solid #1e293b; }
            h1 { color: #00ffcc; font-size: 26px; margin-bottom: 10px; }
            h2 { color: #00bcff; font-size: 18px; margin-top: 30px; margin-bottom: 10px; border-bottom: 1px solid #1e293b; padding-bottom: 5px; }
            p, li { font-size: 15px; color: #94a3b8; }
            ul { padding-left: 20px; margin-top: 10px; }
            .date { font-style: italic; color: #64748b; margin-bottom: 30px; }
        </style>
    </head>
    <body>
        <div class="wrapper">
            <h1>Privacy Policy</h1>
            <div class="date">Last Updated: June 18, 2026</div>
            
            <p>Dalynx Automations ("we," "our," or "us") operates enterprise-grade automated workflow pipelines and AI conversational utilities. This Privacy Policy details our operational data architecture and strict practices regarding information security handling for our conversational communication application integrations through Meta's WhatsApp Business Platform API.</p>

            <h2>1. Information We Process</h2>
            <p>To deliver real-time infrastructure automation, our systems temporarily ingest user interactions sent via webhooks. This includes:</p>
            <ul>
                <li><strong>Communication Metadata:</strong> Phone number information of incoming communication strings to establish chat session pathways.</li>
                <li><strong>Message Content:</strong> Text strings sent to our system instances to dynamically construct and stream intelligent context-aware replies via large language models.</li>
            </ul>

            <h2>2. Data Retention Policy</h2>
            <p>To preserve interaction memory seamlessly across client communication milestones without unnecessary exposure, transactional session transcripts are isolated within security-tight database nodes. Data logs can be cleared programmatically using explicit programmatic instructions ("RESET" signals) at any time.</p>

            <h2>3. Third-Party Protocols & Security</h2>
            <p>We do not aggregate, sell, or farm identity indices. System interaction points process context solely alongside secure endpoint infrastructure providers, specifically Meta platforms and secure AI compute backends (OpenAI API profiles), which maintain robust compliance models.</p>

            <h2>4. Corporate Contact Details</h2>
            <p>For questions or formal data inquiries concerning Dalynx Automations compliance policies, connect directly with our legal point of contact at: <a href="mailto:dsecure.ai@gmail.com" style="color: #00bcff; text-decoration: none;">dsecure.ai@gmail.com</a>.</p>
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
    """Silently reads the chat history to figure out what issue the patient has."""
    try:
        extraction_prompt = [
            {"role": "system", "content": "Analyze this chat history. What is the patient's primary dental complaint? Answer in 1 to 4 words only (e.g., 'Severe toothache', 'Bleeding gums', 'Root canal'). If unknown, reply 'General dental checkup'."},
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
        today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

# --- THE TIME-TRAVELER (AI SALES GENERATOR) ---
def check_and_send_followups():
    print("\n--- SCHEDULER WOKE UP: Checking for Day 3 and Day 5 follow-ups ---")
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        sheet_client = gspread.authorize(creds)
        sheet = sheet_client.open("Sales_Tracker").sheet1
        records = sheet.get_all_records()
        
        now = datetime.now()
        
        for i, row in enumerate(records):
            phone = str(row.get('Phone', ''))
            start_date_str = str(row.get('Demo Start Date', '')).strip()
            status = str(row.get('Followup Status', '')).strip()
            clinic_id = row.get('Clinic Tested', '')
            
            if not start_date_str or status == "Completed":
                continue
                
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            days_passed = (now - start_date).days
            row_num = i + 2
            
            # --- DAY 3 AI FOLLOW-UP GENERATION ---
            if days_passed == 3 and status == "Started":
                print(f"-> GENERATING CUSTOM DAY 3 FOLLOW-UP FOR: {phone}")
                
                # Connect to DB synchronously to get the patient's specific context
                import psycopg2
                from psycopg2.extras import RealDictCursor
                
                sync_client = openai.OpenAI(api_key=OPENAI_API_KEY)
                conn = psycopg2.connect(DATABASE_URL)
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                # Fetch clinic owner name and extracted context
                cursor.execute("SELECT owner_name FROM clinics WHERE clinic_id = %s", (clinic_id,))
                res_clinic = cursor.fetchone()
                owner_name = res_clinic['owner_name'] if res_clinic else "Doctor"
                
                cursor.execute("SELECT patient_context FROM user_sessions WHERE phone = %s", (phone,))
                res_session = cursor.fetchone()
                patient_context = res_session['patient_context'] if (res_session and res_session['patient_context']) else "a general dental inquiry"
                conn.close()

                # Generate the custom message using OpenAI
                ai_prompt = f"You are the AI receptionist for {owner_name}. Write a friendly, empathetic 2-sentence WhatsApp follow-up to a patient who complained about '{patient_context}' 3 days ago but never booked. Ask if they are still experiencing it and offer to get them slotted in today."
                
                res = sync_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": ai_prompt}],
                    temperature=0.3
                )
                generated_followup = res.choices[0].message.content.strip()

                # Wrap it in your Sales Pitch
                sales_pitch = (
                    f"⏳ *Automated Day 3 Demo Follow-Up*\n\n"
                    f"Hi {owner_name}! Your AI receptionist remembers exactly what this patient wanted. "
                    f"If I were talking to them right now, I would automatically send this message to bring them back:\n\n"
                    f"💬 _\"{generated_followup}\"_\n\n"
                    f"Imagine this personal touch running automatically for every single missed lead. Ready to set this up for real?"
                )
                
                send_whatsapp_message(phone, sales_pitch)
                sheet.update_cell(row_num, 6, "Day 3 Sent")
                
            # --- DAY 5 TRIGGER ---
            elif days_passed == 5 and status == "Day 3 Sent":
                import psycopg2
                conn = psycopg2.connect(DATABASE_URL)
                cursor = conn.cursor()
                cursor.execute("SELECT owner_name FROM clinics WHERE clinic_id = %s", (clinic_id,))
                res = cursor.fetchone()
                owner_name = res[0] if res else "Doctor"
                conn.close()

                msg = f"🚀 *Final Demo Check-In*\n\nHi {owner_name}! Your test bot successfully nurtured this lead for 5 days without you lifting a finger. Let's get this connected to your clinic's actual WhatsApp and start saving you time."
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
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_followups, 'cron', hour=13, minute=23) # Adjust time as needed
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

                # --- SECRET RESET COMMAND ---
                if clean_text == "RESET":
                    await delete_user_session(sender_phone)
                    reset_reply = "System Memory Cleared from Database! Fresh test started. Scan a QR code or type a DEMO keyword to begin again."
                    send_whatsapp_message(sender_phone, reset_reply)
                    return {"status": "reset_success"}
                
                # --- PHASE 1: SEAMLESS QR CODE INITIATION ---
                detected_clinic = None
                if "DEMO_MATHURAJMER" in clean_text:
                    detected_clinic = "MATHUR_AJMER"
                elif "DEMO_SHARMADELHI" in clean_text:
                    detected_clinic = "SHARMA_DELHI"
                
                if detected_clinic:
                    clinic_data = await get_clinic_data(detected_clinic)
                    if not clinic_data:
                        send_whatsapp_message(sender_phone, "Error: Clinic not found in database.")
                        return {"status": "clinic_not_found"}

                    # Load prompt and pretend the user just said "Hi"
                    new_history = [
                        {"role": "system", "content": clinic_data['system_instruction']},
                        {"role": "user", "content": "Hi"}
                    ]
                    
                    # Log the start of the demo
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, update_sales_tracker, sender_phone, detected_clinic)
                    
                    # Generate the authentic first greeting immediately
                    try:
                        response = await client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=new_history,
                            temperature=0.2 
                        )
                        ai_reply = response.choices[0].message.content
                        print(f"[AI FIRST GREETING]: {ai_reply}")
                        
                        new_history.append({"role": "assistant", "content": ai_reply})
                        await save_user_session(sender_phone, detected_clinic, new_history)
                        send_whatsapp_message(sender_phone, ai_reply)
                        
                    except Exception as e:
                        print(f"OpenAI Error on First Contact: {e}")
                        
                    return {"status": "demo_initialized"}
                
                # --- PHASE 2: MULTI-TENANT MEMORY ---
                active_clinic, current_history, _ = await get_user_session(sender_phone)
                
                if not active_clinic or not current_history:
                    send_whatsapp_message(sender_phone, "Welcome! Please scan your clinic's custom QR code to begin the AI demo.")
                    return {"status": "unauthorized"}
                
                # Append user message
                current_history.append({"role": "user", "content": user_text})
                
                # Truncate history
                if len(current_history) > (MAX_HISTORY * 2 + 1):
                    current_history = [current_history[0]] + current_history[-(MAX_HISTORY * 2):]
                
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, update_sales_tracker, sender_phone, active_clinic)
                
                # --- CALL OPENAI API ---
                try:
                    response = await client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=current_history,
                        temperature=0.2 
                    )
                    ai_reply = response.choices[0].message.content
                    print(f"[AI REPLY]: {ai_reply}")
                    
                    current_history.append({"role": "assistant", "content": ai_reply})
                    await save_user_session(sender_phone, active_clinic, current_history)
                    send_whatsapp_message(sender_phone, ai_reply)
                    
                    # --- TRIGGER BACKGROUND EXTRACTION ---
                    asyncio.create_task(extract_and_save_context(sender_phone, current_history))
                    
                except Exception as e:
                    print(f"OpenAI Error: {e}")
                
    except KeyError:
        pass
        
    return {"status": "success"}