import random
import discord


def random_insult():
    slova = ["čurák", "zmrd", "kokot", "teplouš",
             "buzna", "cucák", "hovno", "prd", "sráč",
             "prďola", "vůl", "čuně", "osel", "prasopes",
             "kozel", "opičák", "svině", "pazneht",
             "negr", "turek", "bulhar", "maďar", "tatar", "křovák",
             "žabožrout", "všivák", "mizera", "židák", "hovado",
             "křivák", "křupan", "mrzák", "idiot", "debil", "kretén", "pablb",
             "cvok", "blázen", "šílenec", "blbec", "pitomec", "bulík",
             "buřtík", "špekoun", "plešoun", "držgrešle", "přetrhdílo",
             "fintílek", "hrubián", "nezdvořák", "podržtaška", "flink",
             "hnusák", "smraďoch", "vlezdobruselista", "trouba", "tydýt",
             "moula", "mamlas", "hejhula", "vrták", "truhlík", "trulant",
             "hňup", "nádiva", "debílek", "vysačka", "penis",
             "vlezdoprdelka", "jebka",
             "kokůtek", "stejně mrtvej", "špatnej warrior",
             "fakt kokot", "Jů a Hele", "hanebný parchant",
             "zbytečně bohatej zmrd"]
    return random.choice(slova)


def random_online_user(ctx):
    people_online = []
    for user in ctx.guild.members:
        if user.status is discord.Status.online:
            roles = [role.name for role in user.roles]
            if roles.count("BOT") == 0:
                people_online.append(user)
    return str(random.choice(people_online).mention)
