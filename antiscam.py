import os
import json
import asyncio
import datetime
import random
import traceback
import sqlite3
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, User
from pyrogram.errors import *
from pyrogram.session import Session
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from helpers import *
from msg import *

if not os.path.exists("bot_session"):
    os.mkdir("bot_session")

try:
    conn = sqlite3.connect("database.db")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS netban (userid INT, motivo TEXT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS admin (userid INT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS supporter (userid INT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS vice (userid INT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS gruppi (chat_id INT, categorie TEXT)")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS user (chat_id INT, ban BOOL)")
    conn.commit()
except:
    traceback.print_exc()
    exit(code="Errore nel database.")

api_id = 7007099
api_hash = "600a6e74d74ea09b8ddaf9a5499211cb"
bot_token = "5682688188:AAFQxm0leA75aZlKr7j5MIOBfLMBilSXyVk"

client = Client("bot_session/bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
Session.notice_displayed = True
client.start()
me = client.get_me()

status_chat = []
segnala_ut = []
dsupporter = []

developer = [5604301411, 2052072805]
owner = [5746038022]
channel_arch = -1001739927424
staff_group = -1001649021436
richiesta_supporto = []
print("Bot status [ON]")


@client.on_message(filters.new_chat_members)
async def me_join(_, message):
    for user in message.new_chat_members:
        if user.is_self:
            addGroup(message.chat.id)
            await message.reply_text("""**Ciao a tutti, grazie per avermi aggiunto al tuo gruppo !**

• Non dimenticare di farmi Admin del Gruppo (sennò non potrò rimuovere gli utenti pericolosi, almeno permesso di rimuovere membri)

__Lo staff ti ringrazia per il supporto__
""")
        else:
            if isNetBanned(message.from_user.id):
                try:
                    await client.ban_chat_member(message.chat.id, message.from_user.id)
                    await message.reply_text(
                        f"❌ {message.from_user.mention} è stato bannato perchè è presente nella blacklist !")
                except:
                    pass


@client.on_message(filters.private & filters.command("start"))
async def starter(_, message):
    isUserandAdd(message.from_user.id)
    await message.reply(START.format(message.from_user.mention, me.mention), reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Aggiugimi ad un gruppo ➕", url=f"https://t.me/{me.username}?startgroup=start")],
        [InlineKeyboardButton("🌐 Canale", url="https://t.me/CsArchivio"),
         InlineKeyboardButton("Archivio 🗂", url="https://t.me/CsArchvio")],
        [InlineKeyboardButton("🔧 Supporto", "supporto"), InlineKeyboardButton("Info ℹ️", "info")]
    ]), disable_web_page_preview=True)


@client.on_message(filters.command("admin"))
async def addadmin(_, message):
    if message.from_user.id in owner or isVice(message.from_user.id) or message.from_user.id in developer:
        try:
            split = message.text.split(" ")
            if len(split) > 1:
                try:
                    ut = await client.get_users(split[1])
                    if isAdmin(ut.id):
                        await message.reply_text("❌ | Questo utente è gia admin")
                    else:
                        conn.cursor().execute("INSERT INTO admin (userid) VALUES (?)", [ut.id])
                        conn.commit()
                        await message.reply_text("sei stato aggiunto admin")
                        try:
                            await client.send_message(ut.id, "sei stato aggiunto admin")
                        except:
                            pass
                except:
                    traceback.print_exc()
                    await message.reply_text("❌ | Utente non trovato")
            else:
                await message.reply_text("❌ | Usa <code>/admin @/ID</code>")
        except:
            pass


@client.on_message(filters.command("unadmin"))
async def remadmin(_, message):
    if message.from_user.id in owner or isVice(message.from_user.id) or message.from_user.id in developer:
        try:
            split = message.text.split(" ")
            if len(split) > 1:
                try:
                    ut = await client.get_users(split[1])
                    if isAdmin(ut.id):
                        conn.cursor().execute("DELETE FROM admin WHERE userid = ?", [ut.id])
                        conn.commit()
                        await message.reply_text("admin rimosso")
                        try:
                            await client.send_message(ut.id, "sei stato rimosso admin")
                        except:
                            pass
                    else:
                        await message.reply_text("❌ | Questo utente non è admin")
                except:
                    traceback.print_exc()
                    await message.reply_text("❌ | Utente non trovato")
            else:
                await message.reply_text("❌ | Usa <code>/unadmin @/ID</code>")
        except:
            pass


@client.on_message(filters.command("supporter"))
async def addsup(_, message):
    if message.from_user.id in owner or isVice(message.from_user.id) or message.from_user.id in developer:
        try:
            split = message.text.split(" ")
            if len(split) > 1:
                try:
                    ut = await client.get_users(split[1])
                    if isSupporter(ut.id):
                        await message.reply_text("❌ | Questo utente è gia supporter")
                    else:
                        conn.cursor().execute("INSERT INTO supporter (userid) VALUES (?)", [ut.id])
                        conn.commit()
                        await message.reply_text("🕵️ Utente aggiunto Supporter")
                        try:
                            await client.send_message(ut.id, "🕵️ Sei stato aggiunto supporter")
                        except:
                            pass
                except:
                    traceback.print_exc()
                    await message.reply_text("❌ | Utente non trovato")
            else:
                await message.reply_text("❌ | Usa <code>/supporter @/ID</code>")
        except:
            pass


@client.on_message(filters.command("unsupporter"))
async def remsup(_, message):
    if message.from_user.id in owner or isVice(message.from_user.id) or message.from_user.id in developer:
        try:
            split = message.text.split(" ")
            if len(split) > 1:
                try:
                    ut = await client.get_users(split[1])
                    if isSupporter(ut.id):
                        conn.cursor().execute("DELETE FROM supporter WHERE userid = ?", [ut.id])
                        conn.commit()
                        await message.reply_text("🕵️ Utente rimosso supporter")
                        try:
                            await client.send_message(ut.id, "🕵️ Sei stato rimosso supporter")
                        except:
                            pass
                    else:
                        await message.reply_text("❌ | Questo utente non è un supporter")
                except:
                    traceback.print_exc()
                    await message.reply_text("❌ | Utente non trovato")
            else:
                await message.reply_text("❌ | Usa <code>/unsupporter @/ID</code>")
        except:
            pass


@client.on_message(filters.command("vice"))
async def addvice(_, message):
    if message.from_user.id in owner or message.from_user.id in developer:
        try:
            split = message.text.split(" ")
            if len(split) > 1:
                try:
                    ut = await client.get_users(split[1])
                    if isVice(ut.id):
                        await message.reply_text("❌ | Questo utente è gia vice")
                    else:
                        conn.cursor().execute("INSERT INTO vice (userid) VALUES (?)", [ut.id])
                        conn.commit()
                        await message.reply_text(ADD_VICE)
                        try:
                            await client.send_message(ut.id, VICE_UT)
                        except:
                            pass
                except:
                    await message.reply_text("❌ | Utente non trovato")
            else:
                await message.reply_text("❌ | Usa <code>/vice @/ID</code>")
        except:
            pass


@client.on_message(filters.command("unvice"))
async def remvice(_, message):
    if message.from_user.id in owner or message.from_user.id in developer:
        try:
            split = message.text.split(" ")
            if len(split) > 1:
                try:
                    ut = await client.get_users(split[1])
                    if isSupporter(ut.id):
                        conn.cursor().execute("DELETE FROM vice WHERE userid = ?", [ut.id])
                        conn.commit()
                        await message.reply_text(RM_VICE)
                        try:
                            await client.send_message(ut.id, VICE_RM)
                        except:
                            pass
                    else:
                        await message.reply_text("❌ | Questo utente non è vice")
                except:
                    traceback.print_exc()
                    await message.reply_text("❌ | Utente non trovato")
            else:
                await message.reply_text("❌ | Usa <code>/unvice @/ID</code>")
        except:
            pass


@client.on_message(filters.command("info"))
async def infos(_, message):
    try:
        ut = await client.get_users(message.command[1])
        username = ""
        if ut.id in owner:
            if ut.username:
                username += f"\n🌐 @{ut.username}"
            else:
                username += ""
            await message.reply(
                f"🕵🏻‍♂️ <b>Informazioni sull'utente</b>\n\n👤 {ut.mention}{username}\n🆔 <code>{ut.id}</code>\n\n🔎 Situazione: 👑 Founder"
            )
        if isAdmin(ut.id):
            if ut.username:
                username += f"\n🌐 @{ut.username}"
            else:
                username += ""
            await message.reply(
                f"🕵🏻‍♂️ <b>Informazioni sull'utente</b>\n\n👤 {ut.mention}{username}\n🆔 <code>{ut.id}</code>\n\n🔎 Situazione: 👮🏻‍♂️ Admin"
            )
        if isSupporter(ut.id):
            await message.reply(
                f"🕵🏻‍♂️ <b>Informazioni sull'utente</b>\n\n👤 {ut.mention}{username}\n🆔 <code>{ut.id}</code>\n\n🔎 Situazione: 🕵🏻‍♂ Supporter")
        if isNetBanned(ut.id):
            if ut.username:
                username += f"\n🌐 @{ut.username}"
            else:
                username += ""
            await message.reply(
                f"🕵🏻‍♂️ <b>Informazioni sull'utente</b>\n\n👤 {ut.mention}{username}\n🆔 <code>{ut.id}</code>\n\n🔎 Situazione: ⚠️ **NetBannato**\n🗞 Motivazione: {get_info_netban(ut.id)}"
            )
        if ut.id in developer:
            if ut.username:
                username += f"\n🌐 @{ut.username}"
            else:
                username += ""
            await message.reply(
                f"🕵🏻‍♂️ <b>Informazioni sull'utente</b>\n\n👤 {ut.mention}{username}\n🆔 <code>{ut.id}</code>\n\n🔎 Situazione: 🧑‍💻 Developer")
        if not isAdmin(ut.id) and not isNetBanned(
                ut.id) and not ut.id in developer and not ut.id in owner and not isSupporter(ut.id):
            if ut.username:
                username += f"\n🌐 @{ut.username}"
            else:
                username += ""
            await message.reply(
                f"🕵🏻‍♂️ <b>Informazioni sull'utente</b>\n\n👤 {ut.mention}{username}\n🆔 <code>{ut.id}</code>\n\n🔎 Situazione: 👤 Utente"
            )
    except:
        await message.reply("Utente non trovato !")


link_var = {"link": "https://t.me/CsArchivio"}


@client.on_message(filters.command("netban"))
async def netbanneee(_, message):
    global link_var
    if message.from_user.id in owner or isVice(message.from_user.id) or message.from_user.id in developer or isAdmin(
            message.from_user.id) or isSupporter(message.from_user.id):
        split = message.text.split(" ")
        if len(split) >= 2:
            try:
                ll = split[1]
                ut = await client.get_users(ll)
                if ut.id in owner or ut.id in developer or isVice(ut.id) or isAdmin(ut.id) or isSupporter(ut.id):
                    await message.reply_text("❌ | Non puoi netbannare uno staffer")
                else:
                    if isNetBanned(ut.id):
                        await message.reply_text("❌ | Questo utente è gia netbannato")
                    else:
                        motivo = message.text.replace(f"/netban {ll}", "")
                        await message.reply_text(" | Netban eseguito con successo!")
                        try:
                            await client.send_message(channel_arch, MSG_NETBAN.format(ut.first_name, ut.username, ut.id,
                                                                                      message.from_user.first_name,
                                                                                      message.from_user.username,
                                                                                      message.from_user.id, motivo))
                        except:
                            pass
                        conn.cursor().execute("INSERT INTO netban (userid, motivo) VALUES (?,?)", [ut.id, motivo])
                        conn.commit()
                        for a, in conn.cursor().execute("SELECT chat_id FROM gruppi").fetchall():
                            await client.ban_chat_member(a, ut.id)
                            await client.send_message(a, MSG_NETBAN.format(ut.first_name, ut.username, ut.id,
                                                                           message.from_user.first_name,
                                                                           message.from_user.username,
                                                                           message.from_user.id, motivo))
            except:
                traceback.print_exc()
                await message.reply_text("❌ | Utente non trovato")
        else:
            await message.reply("Devi fare:\n\n/netban ID/USERNAME MOTIVO")


@client.on_message(filters.command("netunban"))
async def netUnbannee(_, message):
    if message.from_user.id in owner or isVice(message.from_user.id) or message.from_user.id in developer or isAdmin(
            message.from_user.id) or isSupporter(message.from_user.id):
        split = message.text.split(" ")
        if len(split) > 1:
            try:
                ut = await client.get_users(split[1])
                if isNetBanned(ut.id):
                    await message.reply_text("Sbannato con successo!")
                    try:
                        await client.send_message(channel_arch, MSG_UNBAN.format(ut.mention, ut.username, ut.id))
                    except:
                        pass
                    conn.cursor().execute("DELETE FROM netban WHERE userid = ?", [ut.id])
                    conn.commit()
                    for a, in conn.cursor().execute("SELECT chat_id FROM gruppi").fetchall():
                        await client.unban_chat_member(a, ut.id)
                        await client.send_message(a, MSG_UNBAN.format(ut.mention, ut.username, ut.id))
                else:
                    await message.reply_text("❌ | Non è netbannato")
            except:
                traceback.print_exc()
                await message.reply_text("❌ | Utente non trovato")
        else:
            await message.reply_text("❌ | Usa: <code>/netunban @/ID</code>")


@client.on_message(filters.command("comandi"))
async def listacomandidiocane(_, message):
    await message.reply("""✍🏻 <b>Lista comandi</b>

Visualizza i <b>comandi</b> disponibili per ogni ruolo utilizzando i sottostanti bottoni.

📃 <i>Alias disponibili [/]</i>
""", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Fondatore", "lista_founder"), InlineKeyboardButton("Admin 👮🏻‍♂", "lista_admin")],
        [InlineKeyboardButton("👥 Utenti", "lista_utenti"), InlineKeyboardButton("In Privato 👤", "lista_privato")]
    ]), disable_web_page_preview=True)


@client.on_message(filters.group & filters.command("assistenza"))
async def supp(_, message):
    global richiesta_supporto
    creator = await client.get_chat_member(message.chat.id, message.from_user.id)
    if creator.status.ADMINISTRATOR or creator.status.OWNER:
        if len(message.command) > 1:
            reason = message.text.replace("/assistenza", "")
            gruppo = await client.get_chat(message.chat.id)
            richiesta_supporto.append(message.chat.id)
            try:
                link = (await client.get_chat(message.chat.id)).invite_link
            except:
                link = "https://t.me/" + (await client.get_chat(message.chat.id)).username
            await message.reply_text("supporto inviato (ora non puoi usare più finchè non lo permetterà un admin)")
            await client.send_message(staff_group, f"""
🚨 Nuovo supporto di gruppo richiesto

ℹ️ Informazioni gruppo:

🙍‍♂️ Nome: {gruppo.title}
📧 Membri: {gruppo.members_count}
🆔 {gruppo.id}

📠 Motivazione
 ➥ {reason}

👤 Richiesta fatta da: {message.from_user.mention}
""", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Entra per dare supporto ✅", url=link)]
            ]))
        else:
            await message.reply("Devi fare: /assistenza motivo per cui la richiedi")


@client.on_message(filters.group & filters.command("finish"))
async def finishe(_, message):
    global richiesta_supporto
    if message.from_user.id in owner or isVice(message.from_user.id) or message.from_user.id in developer or isAdmin(
            message.from_user.id) or isSupporter(message.from_user.id):
        await message.reply_text(
            f"<b>✅ Supporto finito</b>\n\n<i>{message.from_user.mention} ha finito il suo supporto fra 5 secondi verrà rimosso dal bot automaticamente</i>")
        await client.send_message(staff_group, f"<b>✅ Supporto fatto da {message.from_user.mention}</b>")
        richiesta_supporto.remove(message.chat.id)
        await asyncio.sleep(5.0)
        try:
            await client.ban_chat_member(message.chat.id, message.from_user.id)
            await client.unban_chat_member(message.chat.id, message.from_user.id)
        except:
            pass


@client.on_message(filters.group & filters.command("stats"))
async def stastststs(_, message):
    if message.from_user.id in owner or isVice(message.from_user.id) or message.from_user.id in developer or isAdmin(
            message.from_user.id):
        gr = conn.cursor().execute("SELECT COUNT(chat_id )FROM gruppi").fetchone()[0]
        netban = conn.cursor().execute("SELECT COUNT(userid) FROM netban").fetchone()[0]
        ut = conn.cursor().execute("SELECT COUNT(chat_id) FROM user").fetchone()[0]
        await message.reply_text(
            f"⚙️ Statistiche {me.mention}\n👥 Gruppi » {gr}\n🚫 NetBan » {netban}\n📋 Utenti » {ut}"
        )


@client.on_message(filters.command("post"))
async def postglobal(_, message):
    if message.from_user.id in owner:
        text = message.text.replace("/post", "")
        for a, in conn.cursor().execute("SELECT chat_id FROM user").fetchall():
            try:
                await client.send_message(a, "**⚠️ Messaggio globale:**\n\n" + text)
            except:
                pass
        await message.reply("Messaggio globale inviato !")


@client.on_message(filters.command("checkstaff"))
async def checkthestaffer(_, message):
    try:
        split = message.text.split(" ")
        if len(split) > 1:
            try:
                ut = await client.get_users(split[1])
                if message.from_user.id in owner or isAdmin(ut.id) or isVice(ut.id) or isSupporter(
                        ut.id) or ut.id in developer:
                    await message.reply_text(MSG_CHECKSTAFF.format(ut.mention, me.mention))
                else:
                    await message.reply_text("❌ | Questo utente non è staff")
            except:
                traceback.print_exc()
                await message.reply_text("❌ | Utente non trovato")
        else:
            await message.reply_text("❌ | Usa: <code>/checkstaff @/ID</code>")
    except:
        pass


@client.on_message(filters.command("server"))
async def server(_, message):
    await message.reply_text(
        f"<b>🛠 Server del bot</b>\n\n♻️ Bot riavviato\n✅ Bot <b>ONLINE</b>")


@client.on_message(filters.private & filters.command("mex"))
async def sendmex(_, message):
    if message.from_user.id in owner or isVice(message.from_user.id) or message.from_user.id in developer or isAdmin(
            message.from_user.id) or isSupporter(message.from_user.id):
        split = message.text.split(" ")
        if len(split) > 1:
            try:
                ut = split[1]
                utente = await client.get_users(ut)
                mex = message.text.replace(f"/mex {ut}", "")
                await client.send_message(utente.id, f"{mex}")
                await message.reply_text("**✅ Messaggio inviato correttamente**")
            except:
                traceback.print_exc()
                await message.reply_text("Utente non trovato...")
        else:
            await message.reply_text("Usa /mex @/ID mex")


@client.on_callback_query()
async def button(_, query):
    global status_chat, link_var, segnala_ut, dsupporter
    if query.data == "home":
        if query.from_user.id in status_chat:
            status_chat.remove(query.from_user.id)
        await query.message.edit(START.format(query.from_user.mention, me.mention), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Aggiugimi ad un gruppo ➕", url=f"https://t.me/{me.username}?startgroup=start")],
            [InlineKeyboardButton("🌐 Canale", url="https://t.me/CsArchivio"),
             InlineKeyboardButton("Archivio 🗂", url="https://t.me/CsArchivio")],
            [InlineKeyboardButton("🔧 Supporto", "supporto"), InlineKeyboardButton("Info ℹ️", "info")]
        ]), disable_web_page_preview=True)
    elif query.data == "close":
        await query.message.delete()
    elif query.data == "info":
        await query.message.edit("""<a href='http://t.me/CaptureScammersBot'>CP 🔐</a> è un bot per la <b>protezione dei gruppi</b> online dal 2 Ottobre 2022 ed in <b>continuo aggiornamento</b> per garantirvi la <b>massima sicurezza</b>.

♻️ Versione del Bot: 1.4

<b>Staff del progetto </b>
• @EzIsFree, Proprietario
• @KillatoDev and @ChillatoDev, Sviluppatore del bot e di tutte le sue funzioni. 

• Si ringraziano <b>tutti i gruppi</b> che si affidano al nostro Bot per usufruire del <b>nostro servizio</b>. Ricordiamo che per ogni difficoltà lo staff è sempre a <b>vostra disposizione</b>.
""", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✍🏻 Lista comandi", "cmd")],
            [InlineKeyboardButton("🔙​", "home")]
        ]), disable_web_page_preview=True)
    elif query.data == "cmd":
        await query.message.edit("""✍🏻 <b>Lista comandi</b>

Visualizza i <b>comandi</b> disponibili per ogni ruolo utilizzando i sottostanti bottoni.

📃 <i>Alias disponibili [/]</i>
""", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 Fondatore", "lista_founder"), InlineKeyboardButton("Admin 👮🏻‍♂", "lista_admin")],
            [InlineKeyboardButton("👥 Utenti", "lista_utenti"), InlineKeyboardButton("In Privato 👤", "lista_privato")],
            [InlineKeyboardButton("🔙​", "info")]
        ]), disable_web_page_preview=True)
    elif query.data.startswith("lista"):
        text = query.data.split("_")
        if text[1] == "founder":
            await query.message.edit(CMD_FOUNDER, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙​", "cmd")]
            ]), disable_web_page_preview=True)
        elif text[1] == "admin":
            await query.message.edit(CMD_ADMIN, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙​", "cmd")]
            ]), disable_web_page_preview=True)
        elif text[1] == "utenti":
            await query.message.edit(CMD_UTENTI, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙​", "cmd")]
            ]), disable_web_page_preview=True)
        elif text[1] == "privato":
            await query.message.edit(CMD_PRIVATO, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙​", "cmd")]
            ]), disable_web_page_preview=True)
    elif query.data == "supporto":
        if isAdmin(query.from_user.id):
            return await query.answer("❌ Sei admin ! ❌", show_alert=True)
        elif isBan(query.from_user.id):
            return await query.answer("❌ Sei bannato ! ❌", show_alert=True)
        await query.message.edit("Ecco!", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("RICHIEDI SUPPORTO!", "dsupporter")],
            [InlineKeyboardButton("CONTATTA STAFF", "richiedi")],
            [InlineKeyboardButton("SEGNALA UTENTE", "segnalautente")]
        ]))
    elif query.data == "segnalautente":
        if not query.from_user.id in segnala_ut:
            segnala_ut.append(query.from_user.id)
        else:
            return await query.answer("❌ Sei già in chat ! ❌", show_alert=True)
        await query.message.edit("Invia foto con @/id del utente nella descrizione")
    elif query.data == "richiedi":
        if not query.from_user.id in status_chat:
            status_chat.append(query.from_user.id)
        else:
            return await query.answer("❌ Sei già in chat ! ❌", show_alert=True)
        await query.message.edit("Invia mex")
    elif query.data == "dsupporter":
        if not query.from_user.id in dsupporter:
            dsupporter.append(query.from_user.id)
        else:
            return await query.answer("❌ Sei già in chat ! ❌", show_alert=True)
        await query.message.edit("Invia id/@ gruppo")


@client.on_message(filters.private)
async def ass(_, message):
    global status_chat, segnala_ut, dsupporter
    user = message.from_user
    first_name = None

    if user.id in segnala_ut:
        if message.photo:
            for a in owner:
                try:
                    await message.forward(a)
                except:
                    traceback.print_exc()
                    pass
            for a, in conn.cursor().execute("SELECT userid FROM admin").fetchall():
                try:
                    await message.forward(a)
                except:
                    pass
            for a, in conn.cursor().execute("SELECT userid FROM vice").fetchall():
                try:
                    await message.forward(a)
                except:
                    pass
            for a, in conn.cursor().execute("SELECT userid FROM supporter").fetchall():
                try:
                    await message.forward(a)
                except:
                    pass
            for a in developer:
                try:
                    await message.forward(a)
                except:
                    traceback.print_exc()
                    pass
            for a in owner:
                try:
                    await message.forward(a)
                except:
                    traceback.print_exc()
                    pass
            segnala_ut.remove(user.id)
    elif user.id in dsupporter:
        gruppo = message.text
        gr = await client.get_chat(gruppo)
        try:
            for a in l.get_chat_members(gr.id, filter=ChatMembersFilter.BOTS):
                if a.user.is_bot == 5682688188:
                    print("errore")
                    pass
                else:
                    print(f"Ecco a te! " + (l.create_chat_invite_link(-1001702085392)).invite_link)
        except:
            await message.reply_text("""
⚠️ Attenzione! Non faccio ancora parte di questo gruppo, prima di inviare la candidatura aggiungimi.                
""", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Riprova", "dsupporter")]
            ]))
        dsupporter.remove(user.id)
    if isNetBanned(user.id):
        pass
    else:
        if not user.id in owner and not isVice(user.id) and not isSupporter(user.id) and not isAdmin(
                user.id) and not message.from_user.id in developer and user.id in status_chat:
            first_name = user.first_name
            try:
                mex = f"{user.username} : {message.text}"
            except:
                if message.text is None:
                    mex = f"{user.username} : Non ha allegato un testo"
            if message.media:
                for a in owner:
                    try:
                        await message.forward(a)
                        await client.send_message(a, mex)
                    except:
                        traceback.print_exc()
                        pass
                for a, in conn.cursor().execute("SELECT userid FROM admin").fetchall():
                    try:
                        await message.forward(a)
                        await client.send_message(a, mex)
                    except:
                        pass
                for a, in conn.cursor().execute("SELECT userid FROM vice").fetchall():
                    try:
                        await message.forward(a)
                        await client.send_message(a, mex)
                    except:
                        pass
                for a, in conn.cursor().execute("SELECT userid FROM supporter").fetchall():
                    try:
                        await message.forward(a)
                        await client.send_message(a, mex)
                    except:
                        pass
                for a in developer:
                    try:
                        await message.forward(a)
                        await client.send_message(a, mex)
                    except:
                        traceback.print_exc()
                        pass
                for a in owner:
                    try:
                        await message.forward(a)
                        await client.send_message(a, mex)
                    except:
                        traceback.print_exc()
                        pass
            else:
                for a in owner:
                    try:
                        await client.send_message(a, mex)
                    except:
                        traceback.print_exc()
                        pass
                for a, in conn.cursor().execute("SELECT userid FROM admin").fetchall():
                    try:
                        await cient.send_message(a, mex)
                    except:
                        pass
                for a, in conn.cursor().execute("SELECT userid FROM vice").fetchall():
                    try:
                        await client.send_message(a, mex)
                    except:
                        pass
                for a, in conn.cursor().execute("SELECT userid FROM supporter").fetchall():
                    try:
                        await client.send_message(a, mex)
                    except:
                        pass
                for a in developer:
                    try:
                        await client.send_message(a, mex)
                    except:
                        pass
            await message.reply("**✅ Messaggio inviato correttamente**")
        else:
            if message.reply_to_message:
                try:
                    user_reply_id = int(message.reply_to_message.text.split(" ")[0])
                except:
                    traceback.print_exc()
                    return await message.reply("Rispondi a un mex giusto !")
                try:
                    for a, in conn.cursor().execute("SELECT userid FROM admin").fetchall():
                        await client.send_message(a, f"{message.from_user.id} ha risposta al utente!")
                    for a, in conn.cursor().execute("SELECT userid FROM supporter").fetchall():
                        await client.send_message(a, f"{message.from_user.id} ha risposta al utente!")
                    for a, in conn.cursor().execute("SELECT userid FROM vice").fetchall():
                        await client.send_message(a, f"{message.from_user.id} ha risposta al utente!")
                    for a in owner:
                        await client.send_message(a, f"{message.from_user.id} ha risposta al utente!")
                    mex = f"👮🏻‍♂️: {message.text}"
                except:
                    mex = f"👮🏻‍♂️: Non ha allegato un testo"
                if message.media:
                    try:
                        await message.forward(user_reply_id)
                        await client.send_message(user_reply_id, mex)
                    except:
                        traceback.print_exc()
                        pass
                else:
                    try:
                        await client.send_message(user_reply_id, mex)
                    except:
                        traceback.print_exc()
                        pass
                await message.reply("**✅ Messaggio inviato correttamente**")


idle()