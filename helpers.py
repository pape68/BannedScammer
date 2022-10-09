import sqlite3
import traceback
from msg import *

try:
    conn = sqlite3.connect("database.db")
except:
    traceback.print_exc()

def isUserandAdd(user_id: int):
    result = conn.cursor().execute("SELECT * FROM user WHERE chat_id = ?", [user_id])
    if len(result.fetchall()) > 0:
        pass
    else:
        conn.cursor().execute("INSERT INTO user (chat_id, ban) VALUES (?, ?)", [user_id, False])
        conn.commit()

def isAdmin(user_id: int) -> None:
    if len(conn.cursor().execute("SELECT * FROM admin WHERE chat_id = ?", [user_id]).fetchall()) > 0:
        return True
    else:
        return False

def isAdminAndAdd(user_id: int) -> None:
    if len(conn.cursor().execute("SELECT * FROM admin WHERE chat_id = ?", [user_id]).fetchall()) > 0:
        pass
    else:
        conn.cursor().execute("INSERT INTO admin (chat_id, ruolo) VALUES (?, ?)", [user_id, "admin"])
        conn.commit()

def isViceAndAdd(user_id: int) -> None:
    if len(conn.cursor().execute("SELECT * FROM admin WHERE chat_id = ?", [user_id]).fetchall()) > 0:
        pass
    else:
        conn.cursor().execute("INSERT INTO admin (chat_id, ruolo) VALUES (?, ?)", [user_id, "vice_founder"])
        conn.commit()

def removeAdmin(user_id: int) -> None:
    if len(conn.cursor().execute("SELECT * FROM admin WHERE chat_id = ?", [user_id]).fetchall()) > 0:
        conn.cursor().execute("DELETE FROM admin WHERE chat_id = ?", [user_id])
        conn.commit()


def rem_admin(user_id: int) -> None:
    if len(conn.cursor().execute("SELECT * FROM admin WHERE chat_id = ?", [user_id]).fetchall()) > 0:
        conn.cursor().execute("DELETE FROM admin WHERE chat_id = ?", [user_id])
        conn.commit()
    else:
        pass

def countAdmin() -> int:
    return conn.cursor().execute("SELECT COUNT(*) FROM admin").fetchone()[0]

def checker(user_id):
    result = conn.cursor().execute("SELECT userid FROM netban WHERE userid = ?", [user_id])
    if len(result.fetchall()) > 0:
        return True
    else:
        return False

def getRuolo(user_id):
    return conn.cursor().execute("SELECT ruolo FROM admin WHERE chat_id = ?", [user_id]).fetchone()[0]

async def getStaff(client):
    text = "• Founder "+(await client.get_users(conn.cursor().execute("SELECT chat_id FROM admin WHERE ruolo = ?", ["founder"]).fetchone()[0])).mention
    text += "\n\n• <a href='https://t.me/'>Lista admin e Staff al completo</a>"
    text += "\n\n• Developer " + (await client.get_users("pedalarti")).mention
    return text

def isBan(user_id: int) -> None:
    if conn.cursor().execute("SELECT ban FROM user WHERE chat_id = ?", [user_id]).fetchone()[0]:
        return True
    else:
        return False

def ban(user_id: int) -> None:
    if conn.cursor().execute("SELECT ban FROM user WHERE chat_id = ?", [user_id]).fetchone()[0]:
        return False
    else:
        conn.cursor().execute("UPDATE user SET ban = ? WHERE chat_id = ?", [True, user_id])
        conn.commit()
        return True

def unban(user_id: int) -> None:
    if conn.cursor().execute("SELECT ban FROM user WHERE chat_id = ?", [user_id]).fetchone()[0]:
        conn.cursor().execute("UPDATE user SET ban = ? WHERE chat_id = ?", [False, user_id])
        conn.commit()
    else:
        return False

def isNetBanned(user_id: int):
    if len(conn.cursor().execute("SELECT * FROM netban WHERE userid = ?", [user_id]).fetchall()) > 0:
        return True
    else:
        return False

def get_info_netban(user_id):
    return conn.cursor().execute("SELECT motivo FROM netban WHERE userid = ?", [user_id]).fetchone()[0]

def netban(user_id, link_prove, motivazione, categorie):
    conn.cursor().execute("INSERT INTO netban (userid, motivo, linkprove, categoria) VALUES (?, ?, ?, ?)", [user_id, motivazione, link_prove, categorie])
    conn.commit()

def netunban(user_id):
    conn.cursor().execute("DELETE FROM netban WHERE userid = ?", [user_id])
    conn.commit()

def insert_cat(chat_id, categoria):
    try:
        categorie = conn.cursor().execute("SELECT categorie FROM gruppi WHERE chat_id = ?", [chat_id]).fetchone()[0]
    except:
        traceback.print_exc()
        categorie = "None"
    if categorie != "None":
        if categorie == "all":
            if categoria == "all":
                conn.cursor().execute("UPDATE gruppi SET categorie = ? WHERE chat_id = ?", [categoria, chat_id])
                conn.commit()
            else:
                conn.cursor().execute("UPDATE gruppi SET categorie = ? WHERE chat_id = ?", [categoria, chat_id])
                conn.commit()
    else:
        conn.cursor().execute("UPDATE gruppi SET categorie = ? WHERE chat_id = ?", [categoria, chat_id])
        conn.commit()

def addGroup(ids):
    result = conn.cursor().execute("SELECT chat_id FROM gruppi WHERE chat_id = ?", [ids])
    if len(result.fetchall()) > 0:
        pass
    else:
        conn.cursor().execute("INSERT INTO gruppi (chat_id, categorie) VALUES (?, ?)", [ids, "None"])
        conn.commit()