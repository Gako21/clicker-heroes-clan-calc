import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import clancalc

def fetch_guild(guild_name):
    try:
        JSON = urllib.request.urlopen(
            "http://clickerheroes-savedgames3-747864888.us-east-1.elb.amazonaws.com/clans/findGuild.php?uid=0&passwordHash=0&highestZoneReached=0&guildName=" + guild_name
        )
        text = JSON.read()
        guilddict = clancalc.json.loads(text)["result"]
        users = []
        for user in guilddict["guildMembers"].values():
            member = clancalc.Member(user["nickname"], user["classLevel"], user["chosenClass"])
            users.append(member)
        return users
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []

def show_members(members, tree):
    for i in tree.get_children():
        tree.delete(i)
    for member in members:
        tree.insert("", "end", values=(member.name, member.level, member.role))

def on_search():
    guild_name = entry.get()
    members = fetch_guild(guild_name)
    show_members(members, tree)

root = tk.Tk()
root.title("Clan Members")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Guild Name:").grid(row=0, column=0)
entry = tk.Entry(frame)
entry.grid(row=0, column=1)
search_btn = tk.Button(frame, text="Search", command=on_search)
search_btn.grid(row=0, column=2)

columns = ("Name", "Level", "Role")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()