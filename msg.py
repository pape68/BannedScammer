START = """
👋🏻 Ciao {}!
{} è il <b>miglior bot</b> per la <b>sicurezza</b> del tuo <b>gruppo</b>.

🤖 <b>Aggiungimi</b> in un gruppo, rendimi <b>amministratore</b> e <b>configurami</b> a tuo piacimento tramite il comando /set.

✍🏻 <b>Lista comandi</b>
Esegui /comandi per vedere i <b>comandi</b> del bot e le <b>informazioni</b> relative ad essi.
"""

ADD_ADMIN = """ 
👮🏻‍♂️ Utente aggiunto admin
"""

ADMIN_UT = """ 
👮🏻‍♂️ Sei stato aggiunto admin
"""

RM_ADMIN = """ 
👮🏻‍♂️ Utente rimosso admin
"""

ADMIN_RM = """ 
👮🏻‍♂️ Sei stato rimosso admin
"""

ADD_VICE = """
👮🏻‍♂️ Utente aggiunto vice
"""

VICE_UT = """ 
👮🏻‍♂️ Sei stato aggiunto vice
"""

RM_VICE = """ 
👮🏻‍♂️ Utente rimosso vice
"""

VICE_RM = """ 
👮🏻‍♂️ Sei stato rimosso vice
"""

INFO = """
👮🏻‍♂️ **Staff:**

{}
 
• Si ringraziano tutti i gruppi che si affidano al nostro Bot per usufruire del nostro servizio. 
Ricordiamo che per ogni difficoltà lo staff è sempre a vostra disposizione
"""

CMD = """ 
✍🏻 **Lista comandi**

Visualizza i **comandi** disponibili per ogni ruolo utilizzando i sottostanti bottoni.

__📃 Alias disponibili [/]__
"""

CMD_FOUNDER = """
👑 Lista comandi Fondatore/vice bot
Comandi riservati per il Fondatore del bot.

• /admin ID/USERNAME » Aggiunge un admin

• /unadmin ID/USERNAME » Rimuove un admin

• /ban REPLY(dal bot) » Banna utente dal bot 

• /unban REPLY(dal bot) » Sbanna utente dal bot 

• /post mex » Post globale 
 
SOLO FOUNDER: 

• /vice ID/USERNAME » Aggiunge un vice-founder

• /unvice ID/USERNAME » Rimuove un vice-founder
"""

CMD_ADMIN = """
👮🏻‍♂️ Lista comandi Admin bot
Comandi riservati per gli admin e i founder del bot.

• /netban ID/USERNAME MOTIVO » Netban

• /netuban ID/USERNAME » NetUban
"""

CMD_UTENTI = """
👥 Lista comandi Utenti
Comandi disponibili per gli tutti.

• /info ID/USERNAME » Verifica la presenza di un utente in BlackList

• /set SOLO NEI GRUPPI » Impostazioni per settare il bot
"""

SUPPORTO = """ 
**✅ Sei in chat con un operatore !**

__Invia un messaggio__

⚠️ ```Non scrivere cose non consone o verrai bannato !``` 
"""

MSG_NETBAN = """
⚠️ Utente inserito in BlackList

🕵🏻‍♂ Informazioni sull'utente
├ Nome » {}
├ Username » @{}
└ ID » {}

⛑ Bannato da
├ Nome » {}
├ Username » @{}
└ ID » {}

🗞 Motivazione:
{}

🗂 Prove: <a href='https://t.me/BlackAntiscamArchivio'>Clicca qui</a>
🌐 Canale: <a href='https://t.me/BlackantiscamNews'>Clicca qui</a>
"""

MSG_UNBAN = """
✅ Utente rimosso dalla BlackList

🕵🏻‍♂ Informazioni sull'utente
├ Nome » {}
├ Username » @{}
└ ID » {}

💡 Lo staff si scusa per il disagio.
"""